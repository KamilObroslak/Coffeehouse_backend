import datetime

import jwt as jwt
from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider, Coffee, Product
from biz.serializers import ProviderSerializer, CoffeeSerializer
from .models import UserToken
from rest_framework import status


def create_limited_permissions_group():
    group, created = Group.objects.get_or_create(name="Basic User")

    admin_group = Group.objects.get(name="User")
    permissions = admin_group.permissions.all()

    group.permissions.set(permissions)

    return group


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
                                                    is_staff=False)
                    token = UserToken(owner=user)
                    token.save()
                    auth.login(request, user)
                    return Response({"message": "User created successfully"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        print(request.data)
        username = request.data.get("username")
        password = request.data.get("password")
        context = {}

        if username is None or password is None:
            context["error"] = "Proszę podać zarówno nazwę użytkownika, jak i hasło."
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        user = auth.authenticate(username=username, password=password)

        if not user:
            context["error"] = "Podane dane logowania są nieprawidłowe."
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        auth.login(request, user)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        provider = User.objects.get(id=user.id)

        try:
            business = Provider.objects.filter(owner=provider.id)
            for i in business:
                product = Product.objects.filter(owner=i)
        except Provider.DoesNotExist:
            business = None
            product = None

        response = Response({
            "user_id": user.id,
            "business": ProviderSerializer(business, context={'request': request},
                                           many=True).data if business else None,
            "coffees": CoffeeSerializer(product, context={'request': request}, many=True).data if product else None,
            "jwt": token
        })

        return response


class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response


class UserDeleteView(APIView):
    def delete(self, request, id, *args, **kwargs):
        email = request.data.get("email")
        token = request.data.get("token")
        instance = User.objects.filter(id=id, email=email)
        check = UserToken.objects.get(token=token)
        if check:
            if instance:
                instance.delete()
                return Response({"message": "Object destroyed successfully"})
            else:
                return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
