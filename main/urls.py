
from django.urls import path

from main.views import MainList, MainDetail

urlpatterns = [
    path('site/', MainList.as_view()),
    path('site/<int:pk>/', MainDetail.as_view()),
]