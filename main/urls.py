
from rest_framework.routers import DefaultRouter
from main.views import BookmarkViewSet, TestBookmarkViewSet

router = DefaultRouter()
router.register(r'site', BookmarkViewSet, basename='bookmark')
router.register(r'test', TestBookmarkViewSet, basename='test')

urlpatterns = router.urls