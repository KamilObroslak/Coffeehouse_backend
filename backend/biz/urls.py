from django.urls import path, include
from rest_framework import routers

from biz.views import CoffeeViewSet, CakeViewSet, PlaceViewSet, OrderViewSet, BusinessRegisterView, \
    UpdateHours, UserLoginView, UserLogoutView, UserDeleteView, OrderView, OrderUpdateView, AddCoffeeView
from client.views import ClientRegisterView
from core.views import UserRegisterView

router = routers.DefaultRouter()
router.register(r"coffee", CoffeeViewSet)
router.register(r"cake", CakeViewSet)
router.register(r"place", PlaceViewSet)
router.register(r"order", OrderViewSet)

urlpatterns = [
    # path("api/", include(router.urls)),
    # path("api-auth/", include("rest_framework.urls")),
    # # path("register_staff/", StaffRegisterView.as_view()),
    # path("user_register/", UserRegisterView.as_view()),
    # path("user_register/client/register_client/", ClientRegisterView.as_view()),
    # path("order/", OrderView.as_view()),
    # path("order/<int:id>", OrderUpdateView.as_view()),
    # path("user_register/<id>/biz/register_business/", BusinessRegisterView.as_view()),
    # path("login/", UserLoginView.as_view()),
    # path("logout/", UserLogoutView.as_view()),
    # path("userdelete/", UserDeleteView.as_view()),
    # path("biz/updatehours/<id>", UpdateHours.as_view()),
]
