from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider, Product, Place, Order
from biz.serializers import ProviderSerializer, ProviderForClientSerializer, ProvidersForClientSerializer, \
    ProductSerializer, PlaceSerializer, OrderSerializer
from client.models import Client
from client.serializers import ClientSerializer


class ClientRegisterView(APIView):
    def post(self, request, id):
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


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProvidersForMe(APIView):
    def get(self, request, id):
        providers = Provider.objects.all()
        serializer = ProvidersForClientSerializer(providers, many=True)
        return Response(serializer.data)


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
