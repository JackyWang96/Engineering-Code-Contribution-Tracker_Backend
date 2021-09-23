from rest_framework import serializers
from .models import GitCommit
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class CommitSerializer(serializers.ModelSerializer):
    """Serializer for a list of users"""
    class Meta:
        model = GitCommit
        fields = '__all__'
