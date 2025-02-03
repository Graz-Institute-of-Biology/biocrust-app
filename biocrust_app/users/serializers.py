from djoser.serializers import UserSerializer as DjoserUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = list(DjoserUserSerializer.Meta.fields) + ["is_uploader", "daily_uploads", "total_uploads", "is_superuser"]
        read_only_fields = ["id", "is_uploader", "daily_uploads", "total_uploads", "is_superuser"]