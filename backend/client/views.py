from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import Client
from core.models import UserToken


class ClientRegisterView(APIView):
    def post(self, request, id):
        print(request.data)
        print("test")
        context = {}
        try:
            if request.method == "POST":
                user = User.objects.get(id=id)
                client = Client.objects.create(phone=request.data["client_phone"],
                                               city=request.data["client_city"],
                                               postcode=request.data["client_postcode"],
                                               street=request.data["client_street"],
                                               owner=user)
                client.save()
                return Response({"message": "User created successfully"})
        except:
            return Response({"message": "User already exists"})
