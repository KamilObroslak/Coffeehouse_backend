from django.urls import path, include
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView, NewOrderView, \
    OrderUpdateView, EditCoffeeView, EditCakeView, EditSnackView, DeleteCoffeeView, DeleteCakeView, DeleteSnackView, \
    AddPlaceView, EditPlaceView, DeletePlaceView, BusinessViewSet, OpenDayProviderViewSet, ProductViewSet, \
    CoffeeViewSet, CakeViewSet, SnacksViewSet, PlaceViewSet, OrderViewSet, OrderCoffeeSet, OrderCakeSet, OrderSnackSet, \
    OrderHistorySet
from client.views import ClientRegisterView, ClientViewSet
from .views import UserRegisterView, UserLoginView, \
    UserLogoutView, UserDeleteView

router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"providers", BusinessViewSet)
router.register(r"opendayproviders", OpenDayProviderViewSet)
router.register(r"products", ProductViewSet)
router.register(r"coffees", CoffeeViewSet)
router.register(r"cakes", CakeViewSet)
router.register(r"snacks", SnacksViewSet)
router.register(r"places", PlaceViewSet)
# router.register(r"orderstatus", OrderStatusViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"coffeeorder", OrderCoffeeSet)
router.register(r"cakeorder", OrderCakeSet)
router.register(r"snackorder", OrderSnackSet)
router.register(r"order/history", OrderHistorySet)

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
