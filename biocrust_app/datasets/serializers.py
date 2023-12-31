from rest_framework import serializers
from .models import Dataset_Model, Image_Model, Model_Model, Mask_Model

class Image_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Model
        fields = ('id',
                  'name',
                  'slug',
                  'owner',
                  'description',
                  'img',
                  'thumbnail',
                  'date_added',
                  'dataset'
                  )
class Mask_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mask_Model
        fields = ('id',
                  'name',
                  'owner',
                  'slug',
                  'description',
                  'mask',
                  'date_added',
                  'dataset',
                  'parent_image',
                  'source_labelbox',
                  'source_model',
                  'source_manual'
                  )
        
class Dataset_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset_Model
        fields = ('id',
                  'dataset_name',
                  'owner',
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