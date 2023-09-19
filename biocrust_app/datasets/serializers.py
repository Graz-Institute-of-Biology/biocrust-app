from rest_framework import serializers
from .models import Dataset_Model, Image_Model

class Image_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Model
        fields = ('id',
                  'name',
                  'slug',
                  'description',
                  'img',
                  'thumbnail',
                  'date_added',
                  'dataset'
                  )
        
class Dataset_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset_Model
        fields = ('id',
                  'dataset_name',
                  'slug',
                  'coordinates',
                  'dataset_created',
                  'description',
                  'dataset_type'
                  )