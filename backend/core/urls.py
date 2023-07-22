from django.urls import path, include
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView, OrderView, \
    OrderUpdateView
from client.views import ClientRegisterView
from .views import UserRegisterView, UserLoginView, \
    UserLogoutView, UserDeleteView

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # path("register_staff/", StaffRegisterView.as_view()),
    path("user_register/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("userdelete/", UserDeleteView.as_view()),

    path("user_register/<id>/client/", ClientRegisterView.as_view()),

    path("user_register/biz/", BusinessRegisterView.as_view()),
    path("user_register/<id>/biz/", BusinessRegisterView.as_view()),
    path("biz/updatehours/<id>", UpdateHours.as_view()),
    path("biz/addcoffee/<id>", AddCoffeeView.as_view()),
    path("biz/addcake/<id>", AddCakeView.as_view()),
    path("biz/addsnack/<id>", AddSnackView.as_view()),
    path("biz/order/", OrderView.as_view()),
    path("order/<int:id>", OrderUpdateView.as_view())
]
