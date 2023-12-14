from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from biocrust_app.datasets.models import Image_Model, Dataset_Model, Model_Model, Mask_Model
from biocrust_app.datasets.serializers import Image_ModelSerializer, Dataset_ModelSerializer, Model_ModelSerializer, Mask_ModelSerializer

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
    
    #def perform_create(self, serializer):
    #    serializer.save()

    def convert_to_grayscale(self, image):
        img = Image.open(image)
        # Convert the image to grayscale
        grayscale_img = img.convert("L")
        #grayscale_img.save("./gray.jpg")         # Save the grayscale image to BytesIO
        output = BytesIO()
        grayscale_img.save(output, format='PNG')

        return output
    
    def perform_create(self, serializer):
        original_mask = serializer.validated_data.get('mask')
        grayscale_mask = self.convert_to_grayscale(original_mask)

        grayscale_mask_data = {
            'dataset': serializer.validated_data.get('dataset').id,
            'parent_image': serializer.validated_data.get('parent_image').id,
            'name': serializer.validated_data.get('name'),
            'owner': serializer.validated_data.get('owner'),
            'slug': serializer.validated_data.get('slug'),
            'mask': ContentFile(grayscale_mask.getvalue(), name=f"{serializer.validated_data.get('name')}_mask.png"),
        }

        model_id = serializer.validated_data.get('source_model').id
        filename = serializer.validated_data.get('source_model').model_name
        path = serializer.validated_data.get('source_model').file

        model_instance = get_object_or_404(Model_Model, id=model_id)
        file_content = model_instance.file.read()
        model_name = model_instance.model_name

        with open('./log.txt', 'a+') as f:
            f.write('model_name: ')
            f.write(str(model_name))
            f.write('\n')
            f.write(str(filename))
            f.write('\n')
            f.write(str(path))

        grayscale_mask_serializer = Mask_ModelSerializer(data=grayscale_mask_data)
        if grayscale_mask_serializer.is_valid():
            grayscale_mask_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(grayscale_mask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Model_ModelViewSet(viewsets.ModelViewSet):
    queryset = Model_Model.objects.all()
    serializer_class = Model_ModelSerializer

    def get_queryset(self):
        # return self.queryset.filter(created_by=self.request.user)
        return self.queryset.all()
    
    def perform_create(self, serializer):
        serializer.save()
    
