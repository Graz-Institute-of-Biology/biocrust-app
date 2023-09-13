from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model, decorators
from django.utils.translation import gettext_lazy as _

from biocrust_app.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import Dataset_Model, Image_Model

admin.site.register(Dataset_Model)
admin.site.register(Image_Model)
