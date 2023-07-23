from django.urls import path, include
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView, NewOrderView, \
    OrderUpdateView, EditCoffeeView, EditCakeView, EditSnackView, DeleteCoffeeView, DeleteCakeView, DeleteSnackView, \
    AddPlaceView, EditPlaceView, DeletePlaceView
from client.views import ClientRegisterView
from .views import UserRegisterView, UserLoginView, \
    UserLogoutView, UserDeleteView

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # path("user_register/staff/", StaffRegisterView.as_view()),

    # Core part
    path("user_register", UserRegisterView.as_view()), # OK
    path("login/", UserLoginView.as_view()), # OK
    path("logout/", UserLogoutView.as_view()), # OK
    path("<id>/userdelete/", UserDeleteView.as_view()), #OK

    # Client part
    path("user_register/<id>/client/", ClientRegisterView.as_view()), #OK ?
    path("client/<id>/neworder", NewOrderView.as_view()), #OK
    path("client/<id>/updateorder/<order>", OrderUpdateView.as_view()), #OK

    # Business part
    path("user_register/<id>/biz/", BusinessRegisterView.as_view()),  # OK

    path("biz/<id>/updatehours", UpdateHours.as_view()), #OK

    path("biz/<id>/addcoffee", AddCoffeeView.as_view()), #OK
    path("biz/<id>/editcoffee/<coffee>", EditCoffeeView.as_view()), #OK
    path("biz/<id>/deletecoffee/<coffee>", DeleteCoffeeView.as_view()), #OK !

    path("biz/<id>/addcake", AddCakeView.as_view()), #OK
    path("biz/<id>/editcake/<cake>", EditCakeView.as_view()), #OK
    path("biz/<id>/deletecake/<cake>", DeleteCakeView.as_view()), #OK !

    path("biz/<id>/addsnack", AddSnackView.as_view()), # OK
    path("biz/<id>/editsnack/<snack>", EditSnackView.as_view()), # OK
    path("biz/<id>/deletesnack/<snack>", DeleteSnackView.as_view()),  # OK !

    path("biz/<id>/addplace", AddPlaceView.as_view()),  # OK
    path("biz/<id>/editplace/<place>", EditPlaceView.as_view()),  # OK
    path("biz/<id>/deleteplace/<place>", DeletePlaceView.as_view()),  # OK !
]
