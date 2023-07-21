from django.urls import path, include
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView
from client.views import ClientRegisterView
from .views import UserRegisterView, UserLoginView, \
    UserLogoutView, UserDeleteView

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("register_staff/", UserRegisterView.as_view()),
    path("client/register_client/", ClientRegisterView.as_view()),
    path("biz/register_business/", BusinessRegisterView.as_view()),
    path("biz/updatehours/<id>", UpdateHours.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("userdelete/", UserDeleteView.as_view()),
    # path("order/", OrderView.as_view()),
    # path("order/<int:id>", OrderUpdateView.as_view())
    path("biz/addcoffee/<id>", AddCoffeeView.as_view()),
    path("biz/addcake/<id>", AddCakeView.as_view()),
    path("biz/addsnack/<id>", AddSnackView.as_view())
]