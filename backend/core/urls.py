from django.urls import path, include
from rest_framework import routers

from .views import CoffeeViewSet, \
    CakeViewSet, \
    PlaceViewSet, \
    OrderViewSet, \
    UserRegisterView, \
    UserLoginView, \
    UserLogoutView, UserDeleteView, OrderView

router = routers.DefaultRouter()
router.register(r"coffee", CoffeeViewSet)
router.register(r"cake", CakeViewSet)
router.register(r"place", PlaceViewSet)
router.register(r"order", OrderViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("register/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("userdelete/", UserDeleteView.as_view()),
    path("order/", OrderView.as_view())
]