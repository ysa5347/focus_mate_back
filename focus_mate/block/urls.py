from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path('statistics/', blockCreateViewAPI.as_view()),
    path('statistics/', userTotalBlockViewAPI.as_view()),
]