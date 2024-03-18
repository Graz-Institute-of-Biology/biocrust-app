from django.shortcuts import render
import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from PIL import Image
import sys
import requests
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
import json
import os
from collections import defaultdict
from biocrust_app.datasets.models import Image_Model, Dataset_Model, Model_Model, Mask_Model, Analysis_Model
from biocrust_app.datasets.serializers import Image_ModelSerializer, Dataset_ModelSerializer, Model_ModelSerializer, Mask_ModelSerializer, Analysis_ModelSerializer

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
    
    def generate_class_dist(self, parent_image_url):
        response = requests.get(parent_image_url)
        img = Image.open(BytesIO(response.content))
        class_counts = defaultdict(int)
        class_colors = {}

        pixels = img.load()

        with open('./biocrust_app/datasets/ontology.json', 'r') as file:
            color_config = json.load(file)

        pixel_to_label = {tuple(value['color']): value['name'] for value in color_config.values()}

        for class_label in color_config:
            class_counts[color_config[class_label]['name']] = 0

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel_value = pixels[i, j]
                class_label = pixel_to_label.get(pixel_value)
                if class_label:
                    class_counts[class_label] += 1

        total_pixels = sum(class_counts.values())
        class_distribution = {key: round(value / total_pixels, 3) for key, value in class_counts.items()}
        
        class_colors = {value['name']: str(value['color']) for value in color_config.values()}
        
        return json.dumps({"class_distributions": class_distribution, "class_colors": class_colors})
    
    def perform_create(self, serializer):
        if serializer.validated_data.get('source_manual'):        
            try:
                instance = serializer.save()
                if not instance.class_distributions:
                    parent_image_url = serializer.validated_data.get('parent_image_url')
                    parent_image_url = parent_image_url.replace("images", "masks")
                    parent_image_url = os.path.join(parent_image_url.rsplit("/", 1)[0], str(serializer.validated_data.get('mask')))
                    class_distribution = self.generate_class_dist(parent_image_url)
                    instance.class_distributions = class_distribution
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
        token = serializer.validated_data.get('token')
        dataset_id = serializer.validated_data.get('dataset').id

        instance = serializer.save() # call save to store analysis entry in db

        print("Sending request...", file=sys.stderr)
        analysis_id = instance.id
        print("ID: ", analysis_id, file=sys.stderr)
        print("New Build")
        print(ml_model_id, file=sys.stderr)
        self.send_analysis_request(parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id, dataset_id, token)

    def send_analysis_request(self, parent_image_url, model_url, analysis_id, parent_img_id, ml_model_id, dataset_id, token):
        # Send the request to the analysis API
        # parent_image_url = parent_image_url.replace("127.0.0.1", "django")
        # model_url = model_url.replace("127.0.0.1", "django")
        payload = {
            'file_path': parent_image_url,
            'ml_model_path': model_url,
            'analysis_id': analysis_id,
            'parent_img_id': parent_img_id,
            'ml_model_id': ml_model_id,
            'token': token,
            'dataset_id': dataset_id,
            'debug': True
        }
        headers = {}


        # "Fire and forget" request hack: send request with very short timeout
        #  catch the timeout exception, ignore it and continue
        #  only needed for sqlite3 db while testing
        
        # ml_url = 'https://ml.cc-explorer.com/api/v1/predict' # production
        # ml_url = 'http://ml-api:8082/api/v1/predict' # staging
        ml_url = 'http://localhost:8082/api/v1/predict' # local
        
        try:
            requests.post(
            url=ml_url, headers=headers, json=payload, timeout=0.0000000001) # localhost or ml-api (docker service name)
            print("Request sent...")
        except requests.exceptions.ReadTimeout: 
            pass

