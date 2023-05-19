# serializers.py

from rest_framework import serializers
from .models import Image, Tier, UserProfile


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    tier = TierSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
