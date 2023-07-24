from rest_framework import serializers


from client.models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ["id", "phone", "city", "postcode", "street", "owner"]

    def get_owner(self, obj):
        return obj.owner.username
