from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from rest_framework.response import Response
from rest_framework.views import APIView

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

    # @method_decorator(never_cache)
    def get(self, request):
        return render(request, 'user_register.html')

    def post(self, request):
        print(request.data)
        print("test")
        context = {}
        if request.method == "POST":
            try:
                user = User.objects.get(username=request.data["username"], email=request.data["email"])
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