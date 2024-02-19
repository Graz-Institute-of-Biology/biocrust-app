from rest_framework import serializers
from .models import Dataset_Model, Image_Model, Model_Model, Mask_Model, Analysis_Model

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
                  'parent_image_url',
                  'source_labelbox',
                  'source_model',
                  'source_manual',
                  'source_model_url',
                  'class_distributions',
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
                  'dataset')
        
class Analysis_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis_Model
        fields = ('id',
                  'dataset',
                  'source_image_url',
                  'ml_model_url',
                  'parent_img_id',
                  'ml_model_id',
                  'owner',
                  'slug',
                  'status',
                  'start_time',
                  'end_time',
                  'completed',
                  'errors')
         
     
    
     
     
     
     
    