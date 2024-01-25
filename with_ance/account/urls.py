from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path("<str:userID>", userDetailViewAPI.as_view()),
    path("userSearch", userSearchViewAPI.as_view()),
    path("follow/<str:userID>", userFollowAPI.as_view()),
    path("follower/<str:userID>", userFollowersViewAPI.as_view()),
    path("following/<str:userID>", userFolloweesViewAPI.as_view())
]