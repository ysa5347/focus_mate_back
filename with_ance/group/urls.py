from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import groupDetailViewAPI, groupListViewAPI, groupCreateViewAPI

urlpatterns = [
    path("pk=<int:pk>", groupDetailViewAPI.as_view()),
    path("", groupListViewAPI.as_view()),
    path("create", groupCreateViewAPI.as_view())
]