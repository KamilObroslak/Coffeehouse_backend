from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Coffee, Cake, Order, Place, Provider, OpenDayProvider, \
    Product, Snacks, OrderCoffee, OrderCake, OrderSnacks, OrderHistory, OrderStatus

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        fields = ["id", "name", "city", "postcode", "street",
                  "kind", "owner", "description", "facebook_link", "instagram_link"]

    def get_owner(self, obj):
        return obj.owner.username


class OpenDayProviderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = OpenDayProvider
        fields = ["id", "owner",
                  "monday", "monday_from", "monday_to",
                  "tuesday", "tuesday_from", "monday_to",
                  "wednesday", "wednesday_from", "wednesday_to",
                  "thursday", "thursday_from", "thursday_to",
                  "friday", "friday_from", "friday_to",
                  "saturday", "saturday_from", "saturday_to",
                  "sunday", "sunday_from", "sunday_to"]

    def get_owner(self, obj):
        return obj.owner.name


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "gluten",
                  "owner", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class CoffeeSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.StringRelatedField(source="owner.id")
    owner_name = serializers.StringRelatedField(source="owner.name")
    price = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Coffee
        fields = ["id", "name", "price", "description", "gluten", "owner_id", "owner_name", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class CakeSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.StringRelatedField(source="owner.id")
    owner_name = serializers.StringRelatedField(source="owner.name")
    price = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Cake
        fields = ["id", "name", "price", "description", "gluten", "owner_id", "owner_name", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class SnackSerializer(serializers.HyperlinkedModelSerializer):
    owner_id = serializers.StringRelatedField(source="owner.id")
    owner_name = serializers.StringRelatedField(source="owner.name")
    price = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Snacks
        fields = ["id", "name", "price", "description", "gluten", "owner_id", "owner_name", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class PlaceSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Place
        fields = ["id", "name", "spot_amount", "availability", "owner"]

    def get_owner(self, obj):
        return obj.owner.name


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    class Meta:
        model = Order
        fields = ["SENT", "COMPLETE", "NO_SHOW"]


class OrderSerializer(serializers.ModelSerializer):

    class OwnerSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        phone = serializers.CharField()
        owner = serializers.CharField()

    owner = OwnerSerializer(read_only=True)
    provider = serializers.CharField(source="provider.name")
    coffees = CoffeeSerializer(many=True, read_only=True)
    cakes = CakeSerializer(many=True, read_only=True)
    snacks = SnackSerializer(many=True, read_only=True)
    spot = PlaceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            "coffees": {'write_only': True},
            "cakes": {'write_only': True},
            "snacks": {'write_only': True}}

    def get_owner(self, obj):
        return obj.owner.name

    def get_provider(self, obj):
        return obj.provider.name

    def get_coffee(self, obj):
        return obj.coffee.price


class OrderCoffeeSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    coffee = CoffeeSerializer()

    class Meta:
        model = OrderCoffee
        fields = ["id", "order", "coffee", "quantity"]


class OrderCakeSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    cake = CakeSerializer()

    class Meta:
        model = OrderCake
        fields = ["id", "order", "cake", "quantity"]


class OrderSnackSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    snacks = SnackSerializer()

    class Meta:
        model = OrderSnacks
        fields = ["id", "order", "snacks", "quantity"]


class OrderHistorySerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()

    class Meta:
        model = OrderHistory
        fields = ["order_id", "time_of_change", "status"]


class ProvidersForClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name", "city", "postcode", "street",
                  "kind", "description", "facebook_link", "instagram_link"]


class ProviderForClientSerializer(serializers.ModelSerializer):
    coffees = CoffeeSerializer()
    cakes = CakeSerializer()
    snacks = SnackSerializer()

    class Meta:
        model = Provider
        fields = ["id", "name", "city", "postcode", "street", "kind",
                  "description", "facebook_link", "instagram_link",
                  "coffees", "cakes", "snacks"]
