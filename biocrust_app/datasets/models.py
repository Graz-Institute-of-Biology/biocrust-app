from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from datetime import datetime

def dataset_image_path(instance, filename):
        return str(str(instance.dataset.id) + '/images/' + filename)

def dataset_mask_path(instance, filename):
        return str(str(instance.dataset.id) + '/masks/' + filename)

def dataset_model_path(instance, filename):
        return str(str(instance.dataset.id) + '/models/' + filename)

class Dataset_Model(models.Model):
    dataset_name = models.CharField(max_length=255, blank=True, unique=True)
    owner = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    coordinates = models.CharField(max_length=255, blank=True)
    dataset_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    dataset_type = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ('-dataset_created',)

    def __str__(self):
        return self.dataset_name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
class Model_Model(models.Model):
    dataset = models.ForeignKey(Dataset_Model, related_name='models', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(blank=True)
    coordinates = models.CharField(max_length=255, blank=True)
    model_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    model_type = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=dataset_model_path, blank=True)

    
    class Meta:
        ordering = ('-model_created',)

    def __str__(self):
        return self.model_name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Image_Model(models.Model):
    dataset = models.ForeignKey(Dataset_Model, related_name='images', on_delete=models.CASCADE)
    owner = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to=dataset_image_path, unique=True)
    thumbnail = models.ImageField(upload_to=dataset_image_path, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return f'/{self.dataset.slug}/{self.slug}/'
    

    def get_image(self):
        if self.img:
            return 'http://127.0.0.1:8000' + self.img.url
        else:
            return ''
        
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.img:
                self.thumbnail = self.make_thumbnail(self.img)
                self.save()
                
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    


class Mask_Model(models.Model):
    dataset = models.ForeignKey(Dataset_Model, related_name='masks', on_delete=models.CASCADE)
    parent_image = models.ForeignKey(Image_Model, related_name='masks', on_delete=models.CASCADE)
    parent_image_url = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    owner = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    mask = models.ImageField(upload_to=dataset_mask_path, blank=True, null=True)
    source_labelbox = models.CharField(max_length=255, blank=True, null=True) # labelbox api key / project id (????)
    source_model = models.ForeignKey(Model_Model, blank=True, null=True, related_name='masks', on_delete=models.CASCADE)
    source_model_url = models.CharField(max_length=255, blank=True, null=True)
    source_manual = models.BooleanField(max_length=255, blank=True, default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_categorical = models.BooleanField(default=True)
    class_distributions = models.TextField(blank=True, null=True, default="")


    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.dataset.slug}/{self.slug}/'
    

class Analysis_Model(models.Model):
    dataset = models.ForeignKey(Dataset_Model, related_name='analysis', on_delete=models.CASCADE)
    parent_img_id = models.ForeignKey(Image_Model, related_name='analysis', on_delete=models.CASCADE)
    ml_model_id = models.ForeignKey(Model_Model, related_name='analysis', on_delete=models.CASCADE)
    source_image_url = models.CharField(max_length=255, default='')
    ml_model_url = models.CharField(max_length=255, default='')
    owner = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    status = models.CharField(max_length=255, blank=True, default="Sent to FastAPI")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    errors = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-start_time',)
    
    def get_absolute_url(self):
        return f'/{self.dataset.slug}/{self.slug}/'

    def start_analysis(self):
        self.start_time = datetime.now()
        print("Analysis started at: " + str(self.start_time))
        self.save()