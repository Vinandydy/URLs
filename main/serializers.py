from rest_framework import serializers

from main.models import Bookmark


class MainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id','url','name','description','favicon','created_at']


class MainPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ['url']


class MainListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ['url', 'name', 'favicon', 'created_at']