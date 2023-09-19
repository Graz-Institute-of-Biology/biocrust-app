from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File


class Dataset_Model(models.Model):
    dataset_name = models.CharField(max_length=255, blank=True)
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


class Image_Model(models.Model):
    dataset = models.ForeignKey(Dataset_Model, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='images/', blank=True, null=True)
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