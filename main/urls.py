
from django.urls import path

from main.views import MainList, MainDetailDelete

urlpatterns = [
    path('site/', MainList.as_view()),
    path('site/<int:pk>/', MainDetailDelete.as_view()),
]