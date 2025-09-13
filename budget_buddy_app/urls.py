from django.urls import path
from .views import *
urlpatterns = [
    path('', home,name="home"),
    path("register",register,name="register"),
    path("login",login,name="login"),
    path("get_user/<int:pk>",get_user,name="get_user"),
    path("forget_password/<str:email>", forget_password, name="forget password"),
    path("reset_password", reset_password, name="reset password"),
    path("add_expense", add_expense, name="add expense"),
    path('get_category', get_category, name="get categorys"),
    path("get_recentUse_byId", get_recentUse_byId, name="get recent use by id"),
]
