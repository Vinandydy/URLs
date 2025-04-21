from urllib.parse import urljoin

from rest_framework import generics, status
# Create your views here.
from bs4 import BeautifulSoup
from rest_framework.response import Response
import requests

from .models import *
from .serializers import MainSerializer, MainPostSerializer


class MainDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MainSerializer
    queryset = Url.objects.all()


class MainList(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MainPostSerializer
        return MainSerializer

    def get_queryset(self):
        queryset = Url.objects.all()
        time = self.request.query_params.get('created_at')
        if time is not None:
            queryset = queryset.filter(created_at=time)
        return queryset

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')

        existing_url = Url.objects.filter(url=url).first()
        #Тут проверка на дурака, повторяется ли URlка
        if existing_url:
            serializer = self.get_serializer(existing_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        #Тут проходит работа по парсингу с bs4
        parsed_data = self.parse_website(url)

        if 'error' in parsed_data:
            return Response({'error': parsed_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новую запись
        url_instance = Url(
            url=url,
            name=parsed_data.get('name'),
            favicon=parsed_data.get('favicon'),
            description=parsed_data.get('description'),
        )
        url_instance.save()

        serializer = self.get_serializer(url_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def parse_website(self, url):
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.title.string

        favicon = None
        icon_link = soup.find("link", rel=lambda x: x and x.lower() in ["icon", "shortcut icon"])
        if icon_link:
            favicon = urljoin(url, icon_link['href'])

        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")


        return {
            "url": url,
            "name": name,
            "favicon": favicon,
            "description": description,
        }
