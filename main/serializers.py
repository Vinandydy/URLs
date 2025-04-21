from rest_framework import serializers

from main.models import Url


class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'

