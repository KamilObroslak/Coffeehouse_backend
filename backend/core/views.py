from django.contrib import auth
from django.contrib.auth.models import Group, User

from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider
from client.models import Client
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
        context = {}
        if request.method == "POST":
            try:
                user = User.objects.get(username=request.data["username"], email=request.data["email"])
                context["error"] = "Login or email already exist!"
                return Response(context)
            except User.DoesNotExist:
                if request.data["password"] != request.data["password2"]:
                    context["error"] = "Two different passwords!"
                    return Response(context)
                else:
                    user = User.objects.create_user(username=request.data["username"],
                                                    email=request.data["email"],
                                                    password=request.data["password"],
                                                    is_staff=True)
                    token = UserToken(owner=user)
                    token.save()
                    auth.login(request, user)
                    type = request.data["type"]
                    if type == "1":
                        kind = request.data["business_kind"]
                        provider = Provider.objects.create(name=request.data["business_name"],
                                                           city=request.data["business_city"],
                                                           postcode=request.data["business_postcode"],
                                                           street=request.data["business_street"],
                                                           kind=kind,
                                                           owner=user,
                                                           description=request.data["business_description"],
                                                           facebook_link=request.data["business_facebook_link"],
                                                           instagram_link=request.data["business_instagram_link"])
                        provider.save()
                        # send_email_instance = SendEmail()
                        # send_email_instance.send_email(recipient=user.email, token=token)
                        return Response({"message": "Business created successfully"}, status=status.HTTP_201_CREATED)
                    if type == "2":
                        client = Client.objects.create(phone=request.data["client_phone"],
                                                       city=request.data["client_city"],
                                                       postcode=request.data["client_postcode"],
                                                       street=request.data["client_street"],
                                                       owner=user)
                        client.save()
                        # send_email_instance = SendEmail()
                        # send_email_instance.send_email(recipient=user.email, token=token)
                        return Response({"message": "Client created successfully"}, status=status.HTTP_201_CREATED)
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


class Userdelete(APIView):
    def delete(self, request):
        token = request.data["token"]
        try:
            score = UserToken.objects.get(token=token)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(username=score.owner)
        user.delete()
        score.delete()

        return Response({"message": "User has been destroyed"}, status=status.HTTP_200_OK)
