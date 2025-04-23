from urllib.parse import urljoin

from rest_framework import generics, status, permissions
# Create your views here.
from bs4 import BeautifulSoup
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
import requests

from .models import *
from .serializers import MainListSerializer, MainPostSerializer, MainDetailSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

from services import parse_website as parser

class MainDetailDelete(generics.RetrieveDestroyAPIView):
    serializer_class = MainDetailSerializer
    queryset = Bookmark.objects.all()

    #Определил, что удаляют только админы
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [AllowAny()]


class MainList(generics.ListCreateAPIView):

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['url', 'name']
    ordering_fields = ['created_at', 'name', 'url']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MainPostSerializer
        return MainListSerializer

    def get_queryset(self):
        queryset = Bookmark.objects.all()
        time = self.request.query_params.get('created_at')
        if time is not None:
            queryset = queryset.filter(created_at=time)
        return queryset

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')

        existing_url = Bookmark.objects.filter(url=url).first()
        #Тут проверка на дурака, повторяется ли URlка
        if existing_url:
            serializer = self.get_serializer(existing_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        #Тут проходит работа по парсингу с bs4
        parsed_data = self.parser(url)

        if 'error' in parsed_data:
            return Response({'error': parsed_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новую запись
        url_instance = Bookmark(
            url=url,
            name=parsed_data.get('name'),
            favicon=parsed_data.get('favicon'),
            description=parsed_data.get('description'),
        )
        url_instance.save()

        serializer = self.get_serializer(url_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


