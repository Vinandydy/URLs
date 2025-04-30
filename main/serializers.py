from rest_framework import serializers

from main.models import Bookmark


class MainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'description', 'url', 'time_created']


class MainPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ['url']


class MainListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ['url', 'name', 'favicon', 'created_at']