from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
import sys
import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from biocrust_app.datasets.models import Image_Model, Dataset_Model, Model_Model, Mask_Model, Analysis_Model
from biocrust_app.datasets.serializers import Image_ModelSerializer, Dataset_ModelSerializer, Model_ModelSerializer, Mask_ModelSerializer, Analysis_ModelSerializer
from biocrust_app.datasets.process_data import *

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

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
    def perform_create(self, serializer):
        serializer.save()


class Image_ModelViewSet(viewsets.ModelViewSet):
    queryset = Image_Model.objects.all()
    serializer_class = Image_ModelSerializer

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
    def perform_create(self, serializer):
        serializer.save()


class Mask_ModelViewSet(viewsets.ModelViewSet):
    queryset = Mask_Model.objects.all()
    serializer_class = Mask_ModelSerializer

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
    def perform_create(self, serializer):
        if serializer.validated_data.get('source_manual'):        
            try:
                instance = serializer.__class__(data=serializer.data)
                instance.is_valid(raise_exception=True)
                
                mask_image_data_serialized = serializer.validated_data.get('mask')
                mask_image = Image.open(mask_image_data_serialized)
                
                print("Mask Image Loaded")
                input_image, pixels = translate_categorical_to_color(mask_image)
                print(f'Colored Image Shape: {pixels.shape}')
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
                    class_distribution = generate_class_dist(mask_image)
                    instance.validated_data['class_distributions'] = class_distribution
                
                instance.save()
            except Exception as e: 
                print(e)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            serializer.save()

class Model_ModelViewSet(viewsets.ModelViewSet):
    queryset = Model_Model.objects.all()
    serializer_class = Model_ModelSerializer

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
    def perform_create(self, serializer):
        serializer.save()    
        file_name = serializer.validated_data.get('file')
        
        model_path = os.path.join('./biocrust_app/media', str(serializer.validated_data.get('dataset').id), 'models', str(file_name))
        print(model_path)


class Analysis_ModelViewSet(viewsets.ModelViewSet):
    queryset = Analysis_Model.objects.all()
    serializer_class = Analysis_ModelSerializer

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
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

        instance = serializer.save() # call save to store analysis entry in db

        print("Sending request...", file=sys.stderr)
        analysis_id = instance.id
        print("ID: ", analysis_id, file=sys.stderr)
        print("New Build")
        print(ml_model_id, file=sys.stderr)
        self.send_analysis_request(parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id)

    def send_analysis_request(self, parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id):
        # Send the request to the analysis API
        # parent_image_url = parent_image_url.replace("127.0.0.1", "django")
        # model_url = model_url.replace("127.0.0.1", "django")
        payload = {
            'file_path': parent_image_url,
            'ml_model_path': model_url,
            'analysis_id': analysis_id,
            'parent_img_id': parent_img_id,
            'ml_model_id': ml_model_id
        }
        headers = {}

        print("PAYLOAD:")
        print(payload)

        # "Fire and forget" request hack: send request with very short timeout
        #  catch the timeout exception, ignore it and continue
        #  only needed for sqlite3 db while testing
        try:
            requests.post(
            'http://ml-api:8082/api/v1/predict', headers=headers, json=payload, timeout=0.0000000001) # localhost or ml-api (docker service name)
            print("Request sent...")
        except requests.exceptions.ReadTimeout: 
            pass

