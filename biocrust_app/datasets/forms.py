from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Document, DLModel, DSetDocument
from django import forms

class UploadForm(forms.ModelForm):
    class Meta:
        model = DSetDocument
        fields = ('document', 'name')

class ModelUploadForm(forms.ModelForm):
    class Meta:
        model = DLModel
        fields = ('document',)
