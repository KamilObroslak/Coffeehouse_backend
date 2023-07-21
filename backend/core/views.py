from datetime import datetime

import jwt as jwt
from django.contrib import auth
from django.contrib.auth.models import Group, User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

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
