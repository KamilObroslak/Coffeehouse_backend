from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from biz.models import Provider
from biz.serializers import ProviderSerializer, ProviderForClientSerializer
from client.models import Client
from client.serializers import ClientSerializer


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


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProvidersForMe(APIView):
    def get(self, request, id):
        print(request.data)
        print("test")
        providers = Provider.objects.all()
        serializer = ProviderForClientSerializer(providers, many=True)
        return Response(serializer.data)
