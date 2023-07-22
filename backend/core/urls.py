from django.urls import path, include
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView, NewOrderView, \
    OrderUpdateView
from client.views import ClientRegisterView
from .views import UserRegisterView, UserLoginView, \
    UserLogoutView, UserDeleteView

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # path("user_register/staff/", StaffRegisterView.as_view()),
    path("user_register", UserRegisterView.as_view()), # OK
    path("login/", UserLoginView.as_view()), # OK
    path("logout/", UserLogoutView.as_view()), # OK
    path("<id>/userdelete/", UserDeleteView.as_view()), #OK

    path("user_register/<id>/client/", ClientRegisterView.as_view()), #OK
    path("client/<id>/neworder", NewOrderView.as_view()), #OK
    path("client/<id>/updateorder/<order>", OrderUpdateView.as_view()), #OK


    path("user_register/biz/", BusinessRegisterView.as_view()),
    path("user_register/<id>/biz/", BusinessRegisterView.as_view()),
    path("biz/<id>/updatehours", UpdateHours.as_view()),
    path("biz/<id>/addcoffee", AddCoffeeView.as_view()),
    path("biz/<id>/addcake", AddCakeView.as_view()),
    path("biz/<id>/addsnack", AddSnackView.as_view()),
    # path("biz/order/", OrderView.as_view()),
    # path("order/<int:id>", OrderUpdateView.as_view())
]
