from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path("create/", groupCreateViewAPI.as_view()),
    path("", groupListViewAPI.as_view()),
    path("pk=<int:pk>/", groupDetailViewAPI.as_view()),
    path("ready/", userReadyViewAPI.as_view()),
    path("invite/", groupInviteViewAPI.as_view()),
    path("accept/", groupInviteAcceptViewAPI.as_view()),
    path("leave/", groupLeaveViewAPI.as_view())
]