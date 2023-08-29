from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers

from biz.views import BusinessRegisterView, UpdateHours, AddCoffeeView, AddCakeView, AddSnackView, NewOrderView, \
    OrderUpdateView, EditCoffeeView, EditCakeView, EditSnackView, DeleteCoffeeView, DeleteCakeView, DeleteSnackView, \
    AddPlaceView, EditPlaceView, DeletePlaceView, BusinessViewSet, OpenDayProviderViewSet, ProductViewSet, \
    CoffeeViewSet, CakeViewSet, SnacksViewSet, PlaceViewSet, OrderViewSet, OrderCoffeeSet, OrderCakeSet, \
    OrderSnackSet, OrderHistorySet, ProviderView, ProviderOrders, ProviderLoginView
from client.views import ClientRegisterView, ProvidersForMe, ProviderForMe, SpotsForMe, \
    OrderHistoryClient, ClientLogin, ClientForMe, ClientViewSet
from .views import UserRegisterView, userdelete, index

router = routers.DefaultRouter()
router.register(r"clients", ClientViewSet)
router.register(r"providers", BusinessViewSet)
router.register(r"opendayproviders", OpenDayProviderViewSet)
router.register(r"products", ProductViewSet)
router.register(r"coffees", CoffeeViewSet)
router.register(r"cakes", CakeViewSet)
router.register(r"snacks", SnacksViewSet)
router.register(r"places", PlaceViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"coffeeorder", OrderCoffeeSet)
router.register(r"cakeorder", OrderCakeSet)
router.register(r"snackorder", OrderSnackSet)
router.register(r"order/history", OrderHistorySet)
urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),

    # Core part
    path("", index, name="start"),
    path("user_register", UserRegisterView.as_view()),  # OK @ OK
    path("logout/", auth_views.LogoutView.as_view(next_page="start"), name="logout"),  # OK
    path("userdelete/<token>", userdelete),  # OK @ OK

    # Client part
    path("user_register/<id>/client/", ClientRegisterView.as_view()),  # OK
    path("client/login/", ClientLogin.as_view()),  # OK
    path("client/<id>/", ClientForMe.as_view()),  # OK
    path("client/<id>/businesses/", ProvidersForMe.as_view()),  # OK
    path("client/<client>/businesses/<provider>/", ProviderForMe.as_view()),  # OK
    path("client/<client>/businesses/<provider>/spots/", SpotsForMe.as_view()),  # OK
    path("client/<client>/businesses/<provider>/spots/<spot>", NewOrderView.as_view()),  # OK @ OK
    path("client/<client>/history/", OrderHistoryClient.as_view()),  # OK

    # Business part
    path("user_register/<id>/biz/", BusinessRegisterView.as_view()),  # OK
    path("biz/login/", ProviderLoginView.as_view()),  # OK ?
    path("biz/<int:id>/", ProviderView.as_view(), name="provider_view"),  # OK ?
    path("biz/<id>/updatehours", UpdateHours.as_view()),  # OK
    path("biz/<id>/ordershistory/", ProviderOrders.as_view()),  # OK
    path("biz/<id>/updateorder/<order>", OrderUpdateView.as_view()),  # OK

    path('biz/<id>/addcoffee', AddCoffeeView.as_view()),  # OK
    path("biz/<id>/editcoffee/<coffee>", EditCoffeeView.as_view()),  # OK
    path("biz/<id>/deletecoffee/<coffee>", DeleteCoffeeView.as_view()),  # OK !

    path("biz/<id>/addcake", AddCakeView.as_view()),  # OK
    path("biz/<id>/editcake/<cake>", EditCakeView.as_view()),  # OK
    path("biz/<id>/deletecake/<cake>", DeleteCakeView.as_view()),  # OK !

    path("biz/<id>/addsnack", AddSnackView.as_view()),  # OK
    path("biz/<id>/editsnack/<snack>", EditSnackView.as_view()),  # OK
    path("biz/<id>/deletesnack/<snack>", DeleteSnackView.as_view()),  # OK !

    path("biz/<id>/addplace", AddPlaceView.as_view()),  # OK
    path("biz/<id>/editplace/<place>", EditPlaceView.as_view()),  # OK
    path("biz/<id>/deleteplace/<place>", DeletePlaceView.as_view()),  # OK !
]
