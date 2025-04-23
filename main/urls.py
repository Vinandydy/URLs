
from django.urls import path

from main.views import MainList

urlpatterns = [
    path('site/', MainList.as_view()),
]