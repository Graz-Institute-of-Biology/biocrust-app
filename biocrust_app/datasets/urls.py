from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from datasets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('datasets', views.Dataset_ModelViewSet)
router.register('images', views.Image_ModelViewSet)
router.register('masks', views.Mask_ModelViewSet)
router.register('models', views.Model_ModelViewSet)
router.register('analyses', views.Analysis_ModelViewSet)


app_name = "datasets"
urlpatterns = [
    path('', include(router.urls)),
    # path('datasets/', views.Dataset_ModelList.as_view()),
    # path('uploaddataset/', views.uploadDataset, name='dataset-upload'),
]
