from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
    path("signup", userCreateViewAPI.as_view()),
    path("login", loginAPI.as_view()),
    path("logout", logoutAPI.as_view()),
    path("config", userConfigViewAPI.as_view()),

]