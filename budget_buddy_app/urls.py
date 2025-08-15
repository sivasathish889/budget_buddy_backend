from django.urls import path
from .views import *
urlpatterns = [
    path('', home,name="home"),
    path("register",register,name="register"),
    path("login/",login,name="login"),
    path("get_user/<int:pk>",get_user,name="get_user"),
]
