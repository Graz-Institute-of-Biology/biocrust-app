from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from datasets import views


app_name = "datasets"
urlpatterns = [
    path('images/', views.Image_ModelList.as_view()),
]
