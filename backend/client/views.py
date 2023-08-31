import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import jwt as jwt
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider, Product, Place, Order
from biz.serializers import ProvidersForClientSerializer, \
    ProductSerializer, PlaceSerializer, OrderSerializer
from client.models import Client
from client.serializers import ClientSerializer


class ClientLogin(APIView):

    @method_decorator(never_cache)
    def get(self, request):
        return render(request, 'client_login.html')

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
        client = Client.objects.get(owner=owner)

        request.session["id"] = {
            "user_id": user.id
        }

        return redirect(f"http://127.0.0.1:8000/core/client/{client.id}/", id=user.id)
        #return None


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientForMe(APIView):
    def get(self, request, id):
        client = get_object_or_404(Client, id=id)
        serializer = ClientSerializer(client)
        return Response(serializer.data)


class ProvidersForMe(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
            client_localization = client.city
            providers = Provider.objects.filter(city=client_localization)

            if not providers:
                providers = Provider.objects.all()

            serializer = ProvidersForClientSerializer(providers, many=True)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({"message": "Client not found"})


class ProviderForMe(APIView):
    def get(self, request, client, provider):
        product = Product.objects.filter(owner__id=provider)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class SpotsForMe(APIView):
    def get(self, request, client, provider):
        table = Place.objects.filter(owner__id=provider)
        serializer = PlaceSerializer(table, many=True)
        return Response(serializer.data)


class OrderHistoryClient(APIView):
    def get(self, request, client):
        history = Order.objects.filter(owner=client)
        serializer = OrderSerializer(history, many=True)
        return Response(serializer.data)
