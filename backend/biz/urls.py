from rest_framework import routers

from biz.views import CoffeeViewSet, CakeViewSet, PlaceViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r"coffee", CoffeeViewSet)
router.register(r"cake", CakeViewSet)
router.register(r"place", PlaceViewSet)
router.register(r"order", OrderViewSet)

urlpatterns = [
]
