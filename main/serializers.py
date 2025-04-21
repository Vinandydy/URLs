from rest_framework import serializers

from main.models import Url


class MainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['id','url','name','description','favicon','created_at']

class MainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['url']

class MainListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['url', 'name', 'favicon', 'created_at']