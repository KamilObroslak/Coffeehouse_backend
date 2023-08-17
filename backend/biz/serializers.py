from django.contrib.auth import get_user_model
from rest_framework import serializers, request
from .models import Coffee, Cake, Order, Place, Provider, OpenDayProvider, \
    Product, Snacks, OrderCoffee, OrderCake, OrderSnacks, OrderHistory, OrderStatus

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ["id", "email", "password", "password2"]


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Provider
        # fields = ["id", "name", "owner"]
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
    owner = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Cake
        fields = ["id", "name", "price", "description", "gluten",
                  "owner", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class SnacksSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Snacks
        fields = ["id", "name", "price", "description", "gluten",
                  "owner", "active"]

    def get_owner(self, obj):
        return obj.owner.name


class PlaceSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Place
        fields = ["id", "spot_amount", "availability", "owner"]

    def get_owner(self, obj):
        return obj.owner.name


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    class Meta:
        model = Order
        fields = ["SENT", "COMPLETE", "NO_SHOW"]


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedModelSerializer
    provider = serializers.HyperlinkedModelSerializer

    class Meta:
        model = Order
        fields = ["id", "spot", "total_price", "coffees", "cakes", "snacks", "takeaway_order",
                  "owner", "status", "order_datatime", "provider"]

    def get_owner(self, obj):
        return obj.owner.name

    def get_provider(self, obj):
        return obj.provider.name

    def get_coffee(self, obj):
        return obj.coffee.price


# class OrderSerializer(serializers.ModelSerializer):
#     owner = serializers.HyperlinkedModelSerializer
#     provider = serializers.HyperlinkedModelSerializer
#
#     coffees = serializers.SerializerMethodField()
#     cakes = serializers.SerializerMethodField()
#     snacks = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Order
#         fields = ["id", "spot", "total_price", "coffees", "cakes", "snacks", "takeaway_order",
#                   "owner", "status", "order_datatime", "provider"]
#
#         def get_owner(self, obj):
#             return obj.owner.name
#
#         def get_provider(self, obj):
#             return obj.owner.name
#
#         def get_coffees(self, obj):
#             coffees_data = []
#             for coffee_order in obj.coffees.all():
#                 coffee_data = {
#                     "name": coffee_order.coffee.name,
#                     "quantity": coffee_order.quantity
#                 }
#                 coffees_data.append(coffee_data)
#             return coffees_data
#
#         def get_cakes(self, obj):
#             cakes_data = []
#             for cake_order in obj.cake.all():
#                 cake_data = {
#                     "name": cake_order.cake.name,
#                     "quantity": cake_order.quantity
#                 }
#                 cakes_data.append(cake_data)
#             return cakes_data
#
#         def get_snacks(self, obj):
#             snacks_data = []
#             for snack_order in obj.snacks.all():
#                 snack_data = {
#                     "name": snack_order.snacks.name,
#                     "quantity": snack_order.quantity
#                 }
#                 snacks_data.append(snack_data)
#             return snacks_data


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
    snacks = SnacksSerializer()

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
    snacks = SnacksSerializer()

    class Meta:
        model = Provider
        fields = ["id", "name", "city", "postcode", "street", "kind",
                  "description", "facebook_link", "instagram_link",
                  "coffees", "cakes", "snacks"]
