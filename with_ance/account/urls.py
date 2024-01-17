from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path("user/<char:userID>", userDetailViewAPI.as_view()),
    path("user/userSearch", userSearchViewAPI.as_view()),
    path("user/follow/<char:userID>", userFollowAPI.as_view()),
    path("user/follower/<char:userID>", userFollowersViewAPI.as_view()),
    path("user/following/<char:userID>", userFollowingViewAPI.as_view())
]