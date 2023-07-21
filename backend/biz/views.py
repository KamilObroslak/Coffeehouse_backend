from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from biz.models import Provider, OpenDayProvider
from core.models import UserToken

import jwt as jwt
from django.contrib import auth
from django.contrib.auth.models import Group, User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coffee, Cake, Place, Order, OrderCoffee, \
    OrderSnacks, Snacks, OrderCake, OrderHistory
from rest_framework import viewsets, status

from .serializers import CoffeeSerializer, CakeSerializer, PlaceSerializer, OrderSerializer


def create_limited_permissions_group():
    group, created = Group.objects.get_or_create(name="Basic User")

    admin_group = Group.objects.get(name="User")
    permissions = admin_group.permissions.all()

    group.permissions.set(permissions)

    return group


class BusinessRegisterView(APIView):
    def post(self, request):
        print(request.data)
        print("test")
        context = {}
        if request.method == "POST":
            try:
                user = User.objects.get(username=request.data["username"])
                context["error"] = "Podana email lub login już istnieje! Proszę użyć innego adresu!"
                return Response(context)
            except User.DoesNotExist:
                if request.data["password"] != request.data["password2"]:
                    context["error"] = "Podane hasła są takie same! Proszę wprowadzić takie same hasła!"
                    return Response(context)
                else:
                    user = User.objects.create_user(username=request.data["username"],
                                                    email=request.data["email"],
                                                    password=request.data["password"],
                                                    is_staff=False)
                    provider = Provider.objects.create(name=request.data["business_name"],
                                                       city=request.data["business_city"],
                                                       postcode=request.data["business_postcode"],
                                                       street=request.data["business_street"],
                                                       kind=request.data["business_kind"],
                                                       owner=user,
                                                       description=request.data["business_description"],
                                                       facebook_link=request.data["business_facebook_link"],
                                                       instagram_link=request.data["business_instagram_link"])
                    provider.save()
                    token = UserToken(owner=user)
                    token.save()
                    auth.login(request, user)
                    return Response({"message": "User created successfully"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateHours(APIView):
    def post(self, request, id):
        print(request.data)
        print("test")

        owner = Provider.objects.get(id=id)
        monday = request.data["monday"]
        monday_from = request.data["monday_from"]
        monday_to = request.data["monday_to"]

        tuesday = request.data["tuesday"]
        tuesday_from = request.data["tuesday_from"]
        tuesday_to = request.data["tuesday_to"]

        wednesday = request.data["wednesday"]
        wednesday_from = request.data["wednesday_from"]
        wednesday_to = request.data["wednesday_to"]

        thursday = request.data["thursday"]
        thursday_from = request.data["thursday_from"]
        thursday_to = request.data["thursday_to"]

        friday = request.data["friday"]
        friday_from = request.data["friday_from"]
        friday_to = request.data["friday_to"]

        saturday = request.data["saturday"]
        saturday_from = request.data["saturday_from"]
        saturday_to = request.data["saturday_to"]

        sunday = request.data["sunday"]
        sunday_from = request.data["sunday_from"]
        sunday_to = request.data["sunday_to"]

        days_hours = OpenDayProvider.objects.create(
            owner=owner,
            monday=monday,
            monday_from=monday_from,
            monday_to=monday_to,
            tuesday=tuesday,
            tuesday_from=tuesday_from,
            tuesday_to=tuesday_to,
            wednesday=wednesday,
            wednesday_from=wednesday_from,
            wednesday_to=wednesday_to,
            thursday=thursday,
            thursday_from=thursday_from,
            thursday_to=thursday_to,
            friday=friday,
            friday_from=friday_from,
            friday_to=friday_to,
            saturday=saturday,
            saturday_from=saturday_from,
            saturday_to=saturday_to,
            sunday=sunday,
            sunday_from=sunday_from,
            sunday_to=sunday_to
        )
        days_hours.save()

        return Response({"message": "The data has been saved"})


class CoffeeViewSet(viewsets.ModelViewSet):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserRegisterView(APIView):
    def post(self, request):
        print(request.data)
        print("test")
        context = {}
        if request.method == "POST":
            try:
                user = User.objects.get(username=request.data["username"])
                context["error"] = "Podana email lub login już istnieje! Proszę użyć innego adresu!"
                return Response(context)
            except User.DoesNotExist:
                if request.data["password"] != request.data["password2"]:
                    context["error"] = "Podane hasła są takie same! Proszę wprowadzić takie same hasła!"
                    return Response(context)
                else:
                    user = User.objects.create_user(username=request.data["username"],
                                                    email=request.data["email"],
                                                    password=request.data["password"],
                                                    is_staff=True)
                    token = UserToken(owner=user)
                    token.save()
                    auth.login(request, user)
                    return Response({"message": "User created successfully"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("Incorrect login details!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect login details!")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class UserLogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }


class UserDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        email = request.data.get("email")
        instance = User.objects.filter(email=email).first()

        if instance:
            instance.delete()
            return Response({"message": "Object destroyed successfully"})
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    def post(self, request):
        print(request.data)
        spot_number = request.data["spot"]
        customer_order = request.data["customer_order"]
        takeaway_order = request.data["takeaway_order"]
        owner_id = request.data["owner"]

        user = User.objects.get(id=owner_id)
        total_price = 0
        price_for_coffees = 0
        price_for_cakes = 0
        price_for_snacks = 0

        order = Order.objects.create(
            spot_id=spot_number,
            total_price=total_price,
            takeaway_order=(takeaway_order == "True"),
            owner=user
        )

        coffees = customer_order["coffees"]
        for coffee_data in coffees:
            coffee_name = coffee_data["name"]
            coffee_quantity = coffee_data["quantity"]
            coffee = Coffee.objects.get(name=coffee_name)
            price_for_coffees += coffee_quantity * coffee.price
            print(price_for_coffees)
            OrderCoffee.objects.create(
                order=order,
                coffee=coffee,
                quantity=coffee_quantity
            )

        cakes = customer_order["cakes"]
        for cake_data in cakes:
            cake_name = cake_data["name"]
            cake_quantity = cake_data["quantity"]
            cake = Cake.objects.get(name=cake_name)
            price_for_cakes += cake_quantity * cake.price
            print(price_for_cakes)
            OrderCake.objects.create(
                order=order,
                cake=cake,
                quantity=cake_quantity
            )

        snacks = customer_order["snacks"]
        for snack_data in snacks:
            snack_name = snack_data['name']
            snack_quantity = snack_data["quantity"]
            snack = Snacks.objects.get(name=snack_name)
            price_for_snacks += snack_quantity * snack.price
            print(price_for_snacks)
            OrderSnacks.objects.create(
                order=order,
                snacks=snack,
                quantity=snack_quantity
            )

        total_price_order = price_for_coffees + price_for_cakes + price_for_snacks
        order.total_price = total_price_order
        order.status = 1
        order.save()

        return Response({"message": "Order created successfully"})


class OrderUpdateView(APIView):
    def post(self, request, id):
        print(request.data)
        token = request.data["token"]
        new_status = request.data["new_status"]
        user = request.data["user"]
        user = User.objects.get(id=user)
        check = UserToken.objects.get(owner=user, token=token)
        if check:
            order = Order.objects.get(id=id)
            now = datetime.now()
            order.status = new_status
            order.save()
            order_history = OrderHistory.objects.create(order_id=order, time_of_change=now, status=new_status)
            order_history.save()
            return Response({"message": "Order has been changed"})
        else:
            return Response({"message": "Problem with authorization or data"})


class AddCoffeeView(APIView):
    def post(self, request, id):
        print(request.data)
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        gluten = request.data["gluten"]
        active = request.data["active"]
        owner = Provider.objects.get(id=id)

        coffee = Coffee.objects.create(name=name,
                                       price=price,
                                       description=description,
                                       gluten=gluten,
                                       owner=owner,
                                       active=active)
        coffee.save()
        return Response({"message": "Coffee has been saved"})


class AddCakeView(APIView):
    def post(self, request, id):
        print(request.data)
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        gluten = request.data["gluten"]
        active = request.data["active"]
        owner = Provider.objects.get(id=id)

        cake = Cake.objects.create(name=name,
                                   price=price,
                                   description=description,
                                   gluten=gluten,
                                   owner=owner,
                                   active=active)
        cake.save()
        return Response({"message": "Cake has been saved"})


class AddSnackView(APIView):
    def post(self, request, id):
        print(request.data)
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        gluten = request.data["gluten"]
        active = request.data["active"]
        owner = Provider.objects.get(id=id)

        snack = Snacks.objects.create(name=name,
                                      price=price,
                                      description=description,
                                      gluten=gluten,
                                      owner=owner,
                                      active=active)
        snack.save()
        return Response({"message": "Snack has been saved"})
