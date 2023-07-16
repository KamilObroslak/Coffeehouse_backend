from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Coffee, Cake, Order, Place

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ["id", "email", "password", "password2"]


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ["id", "name", "price"]


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = ["id", "name", "price"]


class PlaceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Place
       fields = ["id", "spot_amount", "name"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "spot", "total_price", "coffees", "cakes", "snacks", "takeaway_order", "owner"]
