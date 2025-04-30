from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Bookmark
from .serializers import MainListSerializer, MainPostSerializer, MainDetailSerializer
from .services import parse_website as parser



class TestBookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = MainDetailSerializer


class BookmarkViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Bookmark.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]

    # Для DjangoFilterBackend
    filterset_fields = {
        'created_at': ['exact'],
        'name': ['exact', 'icontains'],
        'url': ['exact', 'icontains'],
    }

    # Для SearchFilter
    search_fields = ['name', 'url']

    # Для OrderingFilter
    ordering_fields = ['created_at', 'name', 'url']
    ordering = ['-created_at']  # Сортировка по умолчанию

    def get_serializer_class(self):
        if self.action == 'create':
            return MainPostSerializer
        elif self.action in ['retrieve', 'destroy']:
            return MainDetailSerializer
        return MainListSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        existing_url = Bookmark.objects.filter(url=url).first()

        if existing_url:
            serializer = self.get_serializer(existing_url)
            return Response(serializer.data, status=status.HTTP_200_OK)

        parsed_data = parser(url)

        if 'error' in parsed_data:
            return Response({'error': parsed_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        url_instance = Bookmark(
            url=url,
            name=parsed_data.get('name'),
            favicon=parsed_data.get('favicon'),
            description=parsed_data.get('description'),
        )
        url_instance.save()

        serializer = self.get_serializer(url_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)