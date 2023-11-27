from rest_framework import serializers
from .models import Dataset_Model, Image_Model, Model_Model

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
        
class Model_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Model
        fields = ('id',
                  'model_name',
                  'slug',
                  'coordinates',
                  'model_created',
                  'file',
                  'description',
                  'model_type',
                  'belongs_to_dset'
                  )