import datetime

import jwt as jwt
from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coffee, Cake, Place, Order, UserToken, OrderCoffee, OrderSnacks, Snacks, OrderCake
from rest_framework import viewsets, status, mixins

from .serializers import CoffeeSerializer, CakeSerializer, PlaceSerializer, OrderSerializer, UserSerializer


def create_limited_permissions_group():
    group, created = Group.objects.get_or_create(name="Basic User")

    admin_group = Group.objects.get(name="User")
    permissions = admin_group.permissions.all()

    group.permissions.set(permissions)

    return group


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
        # user_token = get_object_or_404(UserToken, owner=instance, token=hash_id)
        # print(email, instance, user_token)

        if instance:
            # if user_token.exits():
            instance.delete()
            return Response({"message": "Object destroyed successfully"})
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    def post(self, request):
        print(request.data)
        spot_number = request.data["spot"]
        total_price = request.data["total_price"]
        customer_order = request.data["customer_order"]
        takeaway_order = request.data["takeaway_order"]
        owner_id = request.data["owner"]

        user = User.objects.get(id=owner_id)

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
            OrderSnacks.objects.create(
                order=order,
                snacks=snack,
                quantity=snack_quantity
            )

        return Response({"message": "User created successfully"})

    # return Response({"message": "Invalid request method"}, status=400)

    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     group = create_limited_permissions_group()
    #     user.groups.add(group)
    #     user.is_staff = True
    #     user.save()
