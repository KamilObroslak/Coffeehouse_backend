import datetime

import jwt as jwt
from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider, Product
from biz.serializers import ProviderSerializer, CoffeeSerializer
from .messages import SendEmail
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
                    send_email_instance = SendEmail()
                    send_email_instance.send_email(recipient=user.email, token=token)
                    return Response({"message": "User created successfully"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProviderLoginView(APIView):

    @method_decorator(never_cache)
    def get(self, request):
        return render(request, 'login_and_register.html')

    def post(self, request):
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

        owner = User.objects.get(id=user.id)
        provider = Provider.objects.get(owner=owner)
        business = None
        product = None

        try:
            business = Provider.objects.filter(owner=owner.id)
            for i in business:
                product = Product.objects.filter(owner=i)
        except Provider.DoesNotExist:
            pass

        request.session["id"] = {
            "user_id": user.id,
            "business": ProviderSerializer(business, context={"request": request}, many=True).data if business else None,
            "coffees": CoffeeSerializer(product, context={"request": request}, many=True).data if product else None
        }

        return redirect(f"http://127.0.0.1:8000/core/biz/{provider.id}/", id=user.id)


class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        auth.logout(request)
        response.delete_cookie("jwt")
        response.data = {
            "message": "Logout success"
        }
        return response


def userdelete(request, token):
    try:
        score = UserToken.objects.get(token=token)
    except UserToken.DoesNotExist:
        return render(request, "user_not_found.html")

    user = User.objects.get(username=score.owner)
    print(user)
    user.delete()
    score.delete()

    return render(request, "user_deleted.html")


def index(request):
    return render(request, 'index.html')
