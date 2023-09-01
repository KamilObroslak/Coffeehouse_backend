from django.contrib import auth
from django.shortcuts import get_object_or_404
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

        return Response({"message" : "OK"}, status=status.HTTP_200_OK)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientForMe(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        client = get_object_or_404(Client, id=id)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class ProviderForMe(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, client, provider):
        product = Product.objects.filter(owner__id=provider)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpotsForMe(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, client, provider):
        table = Place.objects.filter(owner__id=provider)
        serializer = PlaceSerializer(table, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderHistoryClient(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, client):
        history = Order.objects.filter(owner=client)
        serializer = OrderSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
