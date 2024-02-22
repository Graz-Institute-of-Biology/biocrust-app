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
        class_counts = {
        'class 1': 0,
        'class 2': 0,
        'class 3': 0,
        'class 4': 0,
        'class 5': 0,
        'class 6': 0,
        'class 7': 0,
        'class 8': 0
        }
        
        # Define the mapping of pixel values to class labels
        class_labels = {
            (200, 0, 10): 'class 1',
            (187,207, 74): 'class 2',
            (0,108,132): 'class 3',
            (255,204,184): 'class 4',
            (0,0,0): 'class 5',
            (226,232,228): 'class 6',
            (174,214,220): 'class 7',
            (232,167,53): 'class 8'
        }

        # Iterate over each pixel and count occurrences of each class
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel_value = pixels[i, j]
                #print(pixel_value)
                class_label = class_labels.get(pixel_value, 'other')
                class_counts[class_label] += 1

        # Calculate class distribution
        total_pixels = sum(class_counts.values())
        class_distribution = {key: round(value / total_pixels, 3) for key, value in class_counts.items()}

        return json.dumps({"class_distributions": class_distribution})

    
    def perform_create(self, serializer):
        if serializer.validated_data.get('source_manual'):        
            try:
                instance = serializer.save()
                if not instance.class_distributions:
                    # If class_distributions parameter is not created, generate it
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
