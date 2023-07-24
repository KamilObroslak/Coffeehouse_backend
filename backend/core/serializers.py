from django.contrib.auth import get_user_model
from rest_framework import serializers

from client.models import Client

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ["id", "email", "password", "password2"]


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "phone", "city", "postcode", "street", "owner"]

    def get_owner(self, obj):
        return obj.owner.username
