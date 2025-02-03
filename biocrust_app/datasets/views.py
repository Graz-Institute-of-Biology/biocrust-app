from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, SAFE_METHODS
import sys
import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from biocrust_app.datasets.models import Image_Model, Dataset_Model, Model_Model, Mask_Model, Analysis_Model
from biocrust_app.datasets.serializers import Image_ModelSerializer, Dataset_ModelSerializer, Model_ModelSerializer, Mask_ModelSerializer, Analysis_ModelSerializer
from biocrust_app.datasets.process_data import *
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny


class PublicDatasetFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(dataset__is_public=True)
    
class Image_ModelList(APIView):
    def get(self, request, format=None):
        images = Image_Model.objects.all()
        data = Image_ModelSerializer(images, many=True).data
        return Response(data)

class Dataset_ModelList(APIView):
    def get(self, request, format=None):
        datasets = Dataset_Model.objects.all()
        data = Dataset_ModelSerializer(datasets, many=True).data
        return Response(data)
    
class Model_ModelList(APIView):
    def get(self, request, format=None):
        datasets = Model_Model.objects.all()
        data = Model_ModelSerializer(datasets, many=True).data
        return Response(data)
    

class Dataset_ModelViewSet(viewsets.ModelViewSet):
    queryset = Dataset_Model.objects.all()
    serializer_class = Dataset_ModelSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Dataset_Model.objects.all()
        return Dataset_Model.objects.filter(is_public=True)
   
    def perform_create(self, serializer):
        user = self.request.user
        if not (user.is_uploader or user.is_superuser or user.is_staff):
            raise PermissionDenied("User not authorized to create datasets")
        serializer.save()


class Image_ModelViewSet(viewsets.ModelViewSet, PublicDatasetFilterMixin):
    queryset = Image_Model.objects.all()
    serializer_class = Image_ModelSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = self.request.user

        if not (user.is_uploader or user.is_superuser or user.is_staff):
            raise PermissionDenied("User not authorized to upload images")
        
        if user.daily_uploads > 10:  # Set your limit
            raise PermissionDenied("Daily upload limit reached")
        
        user.increment_uploads()
        serializer.save()


class Mask_ModelViewSet(viewsets.ModelViewSet, PublicDatasetFilterMixin):
    queryset = Mask_Model.objects.all()
    serializer_class = Mask_ModelSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = self.request.user
        if not (user.is_uploader or user.is_superuser or user.is_staff):
            raise PermissionDenied("User not authorized to upload masks")
        
        if serializer.validated_data.get('source_manual'):        
            try:            
                mask_image_data_serialized = serializer.validated_data.get('mask')
                mask_image = Image.open(mask_image_data_serialized)
                
                print("Mask Image Loaded")
                print("Mask Image Mode: ", mask_image.mode)
                if mask_image.mode == "L":
                    instance = serializer.__class__(data=serializer.data)
                    instance.is_valid(raise_exception=True)
                    dataset_type = instance.validated_data.get('dataset').dataset_type
                    _, pixels = translate_categorical_to_color(mask_image, dataset_type)
                    colored_image = Image.fromarray(pixels)

                    buffer = BytesIO()
                    colored_image.save(buffer, format='PNG')
                    mask_file = InMemoryUploadedFile(
                            buffer,  
                            None, 
                            instance.validated_data['name'] + '.png',  
                            'image/png', 
                            buffer.getbuffer().nbytes,  
                            None  
                        )
                    
                    instance.validated_data['mask'] = mask_file
                    if not instance.validated_data['class_distributions']:
                        print('Generating class distribution:')
                        class_distribution = generate_class_dist(mask_image, dataset_type)
                        instance.validated_data['class_distributions'] = class_distribution
                else:
                    instance = serializer.save()
                    if not instance.class_distributions:
                        print('Generating class distribution:')
                        dataset_type = instance.dataset.dataset_type
                        class_distribution = generate_class_dist(mask_image, dataset_type)
                        instance.class_distributions = class_distribution
                
                instance.save()
            except Exception as e: 
                print(e)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # instance = serializer.__class__(data=serializer.data)
            serializer.save()

class Model_ModelViewSet(viewsets.ModelViewSet, PublicDatasetFilterMixin):
    queryset = Model_Model.objects.all()
    serializer_class = Model_ModelSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()    
        file_name = serializer.validated_data.get('file')
        
        model_path = os.path.join('./biocrust_app/media', str(serializer.validated_data.get('dataset').id), 'models', str(file_name))
        print(model_path)


class Analysis_ModelViewSet(viewsets.ModelViewSet, PublicDatasetFilterMixin):
    queryset = Analysis_Model.objects.all()
    serializer_class = Analysis_ModelSerializer
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        model_object = self.get_object(pk)
        serializer = Analysis_ModelSerializer(model_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
    
    def perform_create(self, serializer):
        parent_image_url = serializer.validated_data.get('source_image_url')
        model_url = serializer.validated_data.get('ml_model_url')
        parent_img_id = serializer.validated_data.get('parent_img_id').id
        ml_model_id = serializer.validated_data.get('ml_model_id').id
        token = serializer.validated_data.get('token')
        dataset_id = serializer.validated_data.get('dataset').id
        dataset_type = serializer.validated_data.get('dataset').dataset_type
        ontology = get_ontology(dataset_type)
        num_classes = len(ontology.keys())

        instance = serializer.save() # call save to store analysis entry in db

        analysis_id = instance.id
        print("Saved: ", analysis_id)
        self.send_analysis_request(parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id, dataset_id, num_classes, token)

    def send_analysis_request(self, parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id, dataset_id, num_classes, token):
        # Send the request to the analysis API
        # parent_image_url = parent_image_url.replace("127.0.0.1", "django") # needed for docker
        # model_url = model_url.replace("127.0.0.1", "django") # needed for docker
        
        payload = {
            'file_path': parent_image_url.replace("http", "https"),
            'ml_model_path': model_url.replace("http", "https"),
            'analysis_id': analysis_id,
            'parent_img_id': parent_img_id,
            'ml_model_id': ml_model_id,
            'token': token,
            'dataset_id': dataset_id,
            'num_classes': num_classes
        }
        headers = {}
        # Production:
        ml_url = 'https://ml.cc-explorer.com/api/v1/predict'
        requests.post(url=ml_url, headers=headers, json=payload) # USE THIS FOR PRODUCTION WITH POSTGRES!


        # TESTING:
        # "Fire and forget" request hack: send request with very short timeout
        #  catch the timeout exception, ignore it and continue
        #  only needed for sqlite3 db while testing
        
        # ml_url = 'http://ml-api:8082/api/v1/predict' # staging
        # ml_url = 'http://localhost:8082/api/v1/predict' # local
        # print("Other post:")
        # requests.post(url=ml_url, headers=headers, json=payload) # USE THIS FOR PRODUCTION WITH POSTGRES!

        # ONLY WORKS WITH SQLITEDB:

        # try:
        #     requests.post(
        #     url=ml_url, headers=headers, json=payload, timeout=0.0000000001) # localhost or ml-api (docker service name)
        # except requests.exceptions.ReadTimeout: 
        #     pass

