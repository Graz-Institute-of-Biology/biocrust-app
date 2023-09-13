from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from biocrust_app.datasets.models import Image_Model
from biocrust_app.datasets.serializers import Image_ModelSerializer

class Image_ModelList(APIView):
    def get(self, request, format=None):
        images = Image_Model.objects.all()
        data = Image_ModelSerializer(images, many=True).data
        return Response(data)
