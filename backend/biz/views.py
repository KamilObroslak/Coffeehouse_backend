import datetime
from datetime import datetime
import jwt as jwt

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User

from rest_framework import viewsets, status, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Coffee, Cake, Place, Order, OrderCoffee, \
    OrderSnacks, Snacks, OrderCake, OrderHistory
from biz.models import Provider, OpenDayProvider, Product
from client.models import Client
from core.models import UserToken


from .serializers import CoffeeSerializer, CakeSerializer, OpenDayProviderSerializer, \
    ProductSerializer, ProviderSerializer, SnackSerializer, PlaceSerializer, \
    OrderSerializer, OrderCoffeeSerializer, OrderCakeSerializer, \
    OrderSnackSerializer, OrderHistorySerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class UpdateHours(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            calendar = OpenDayProvider.objects.get(owner=id)
            serializer = OpenDayProviderSerializer(calendar)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            x = OpenDayProvider.objects.get(owner=id)

            monday = request.data["monday"]
            monday_from = request.data["monday_from"]
            monday_to = request.data["monday_to"]

            tuesday = request.data["tuesday"]
            tuesday_from = request.data["tuesday_from"]
            tuesday_to = request.data["tuesday_to"]

            wednesday = request.data["wednesday"]
            wednesday_from = request.data["wednesday_from"]
            wednesday_to = request.data["wednesday_to"]

            thursday = request.data["thursday"]
            thursday_from = request.data["thursday_from"]
            thursday_to = request.data["thursday_to"]

            friday = request.data["friday"]
            friday_from = request.data["friday_from"]
            friday_to = request.data["friday_to"]

            saturday = request.data["saturday"]
            saturday_from = request.data["saturday_from"]
            saturday_to = request.data["saturday_to"]

            sunday = request.data["sunday"]
            sunday_from = request.data["sunday_from"]
            sunday_to = request.data["sunday_to"]

            x.monday = monday
            x.monday_from = monday_from
            x.monday_to = monday_to
            x.tuesday = tuesday
            x.tuesday_from = tuesday_from
            x.tuesday_to = tuesday_to
            x.wednesday = wednesday
            x.wednesday_from = wednesday_from
            x.wednesday_to = wednesday_to
            x.thursday = thursday
            x.thursday_from = thursday_from
            x.thursday_to = thursday_to
            x.friday = friday
            x.friday_from = friday_from
            x.friday_to = friday_to
            x.saturday = saturday
            x.saturday_from = saturday_from
            x.saturday_to = saturday_to
            x.sunday = sunday
            x.sunday_from = sunday_from
            x.sunday_to = sunday_to
            x.save()

            return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)

        except OpenDayProvider.DoesNotExist:

            owner = Provider.objects.get(id=id)
            monday = request.data["monday"]
            monday_from = request.data["monday_from"]
            monday_to = request.data["monday_to"]

            tuesday = request.data["tuesday"]
            tuesday_from = request.data["tuesday_from"]
            tuesday_to = request.data["tuesday_to"]

            wednesday = request.data["wednesday"]
            wednesday_from = request.data["wednesday_from"]
            wednesday_to = request.data["wednesday_to"]

            thursday = request.data["thursday"]
            thursday_from = request.data["thursday_from"]
            thursday_to = request.data["thursday_to"]

            friday = request.data["friday"]
            friday_from = request.data["friday_from"]
            friday_to = request.data["friday_to"]

            saturday = request.data["saturday"]
            saturday_from = request.data["saturday_from"]
            saturday_to = request.data["saturday_to"]

            sunday = request.data["sunday"]
            sunday_from = request.data["sunday_from"]
            sunday_to = request.data["sunday_to"]

            days_hours = OpenDayProvider.objects.create(
                owner=owner,
                monday=monday,
                monday_from=monday_from,
                monday_to=monday_to,
                tuesday=tuesday,
                tuesday_from=tuesday_from,
                tuesday_to=tuesday_to,
                wednesday=wednesday,
                wednesday_from=wednesday_from,
                wednesday_to=wednesday_to,
                thursday=thursday,
                thursday_from=thursday_from,
                thursday_to=thursday_to,
                friday=friday,
                friday_from=friday_from,
                friday_to=friday_to,
                saturday=saturday,
                saturday_from=saturday_from,
                saturday_to=saturday_to,
                sunday=sunday,
                sunday_from=sunday_from,
                sunday_to=sunday_to
            )
            days_hours.save()

            return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)


class OpenDayProviderViewSet(viewsets.ModelViewSet):
    queryset = OpenDayProvider.objects.all()
    serializer_class = OpenDayProviderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CoffeeViewSet(viewsets.ModelViewSet):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer


class SnacksViewSet(viewsets.ModelViewSet):
    queryset = Snacks.objects.all()
    serializer_class = SnackSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCoffeeSet(viewsets.ModelViewSet):
    queryset = OrderCoffee.objects.all()
    serializer_class = OrderCoffeeSerializer


class OrderCakeSet(viewsets.ModelViewSet):
    queryset = OrderCake.objects.all()
    serializer_class = OrderCakeSerializer


class OrderSnackSet(viewsets.ModelViewSet):
    queryset = OrderSnacks.objects.all()
    serializer_class = OrderSnackSerializer


class OrderHistorySet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer


class UserRegisterView(APIView):
    def post(self, request):
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
                                                    is_staff=True)
                    token = UserToken(owner=user)
                    token.save()
                    auth.login(request, user)
                    return Response({"message": "User created successfully"})
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("Incorrect login details!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect login details!")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class UserLogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }


class UserDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        email = request.data.get("email")
        instance = User.objects.filter(email=email).first()

        if instance:
            instance.delete()
            return Response({"message": "Object destroyed successfully"})
        else:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class NewOrderView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, client, provider):
        customer_order = request.data["customer_order"]
        takeaway_order = request.data["takeaway_order"]
        owner_id = client
        provider_id = provider

        client = Client.objects.get(id=owner_id)
        provider = Provider.objects.get(id=provider_id)
        total_price = 0
        price_for_coffees = 0
        price_for_cakes = 0
        price_for_snacks = 0

        place = request.data["place"]
        spot = Place.objects.get(id=place)

        order = Order.objects.create(
            spot=spot,
            total_price=total_price,
            takeaway_order=(takeaway_order == "True"),
            owner=client,
            provider=provider
        )

        # Coffees
        coffees = customer_order["coffees"]
        for coffee_data in coffees:
            coffee_id = coffee_data["coffee_id"]
            coffee_quantity = coffee_data["quantity"]
            try:
                coffee = Coffee.objects.get(id=coffee_id, owner=provider)
                price_for_coffees += coffee_quantity * coffee.price
                OrderCoffee.objects.create(
                    order=order,
                    coffee=coffee,
                    quantity=coffee_quantity
                )
            except ObjectDoesNotExist:
                # Przedmiot nie istnieje, więc pomijamy go
                pass

        # Cakes
        cakes = customer_order["cakes"]
        for cake_data in cakes:
            cake_id = cake_data["cake_id"]
            cake_quantity = cake_data["quantity"]
            try:
                cake = Cake.objects.get(id=cake_id, owner=provider)
                price_for_cakes += cake_quantity * cake.price
                OrderCake.objects.create(
                    order=order,
                    cake=cake,
                    quantity=cake_quantity
                )
            except ObjectDoesNotExist:
                # Przedmiot nie istnieje, więc pomijamy go
                pass

        # Snacks
        snacks = customer_order["snacks"]
        for snack_data in snacks:
            snack_id = snack_data['snack_id']
            snack_quantity = snack_data["quantity"]
            try:
                snack = Snacks.objects.get(name=snack_id, owner=provider)
                price_for_snacks += snack_quantity * snack.price
                OrderSnacks.objects.create(
                    order=order,
                    snacks=snack,
                    quantity=snack_quantity
                )
            except ObjectDoesNotExist:
                # Przedmiot nie istnieje, więc pomijamy go
                pass

        total_price_order = price_for_coffees + price_for_cakes + price_for_snacks
        order.total_price = total_price_order
        order.status = 1
        order.save()
        # recipient = User.objects.get(username=provider.owner)
        # send_email_instance = SendOrderEmail()
        # send_email_instance.send_email(recipient=recipient.email)

        return Response({"message": "Order created successfully"}, status=status.HTTP_200_OK)


class OrderUpdateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id, order):
        new_status = request.data["new_status"]
        order_obj = Order.objects.get(id=order)
        now = datetime.now()
        order_obj.status = new_status
        order_obj.save()
        order_history = OrderHistory.objects.create(order_id=order_obj, time_of_change=now, status=new_status)
        order_history.save()
        return Response({"message": "Order has been changed"}, status=status.HTTP_200_OK)


class CoffeeView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CoffeeSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        coffees = Coffee.objects.filter(owner=id)
        return coffees


class AddCoffeeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        x = request.data.get("gluten")
        if x == True or "on":
            gluten = True
        else:
            gluten = False
        y = request.data.get("active")
        if y == True or "on":
            active = True
        else:
            active = False

        owner = Provider.objects.get(id=id)

        coffee = Coffee.objects.create(name=name,
                                       price=price,
                                       description=description,
                                       gluten=gluten,
                                       owner=owner,
                                       active=active)
        coffee.save()
        return Response({"message": "Coffee has been saved"}, status=status.HTTP_200_OK)


class EditCoffeeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, coffee):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        gluten = request.data["gluten"]
        active = request.data["active"]

        x = Coffee.objects.get(id=coffee)

        x.name = name
        x.price = price
        x.description = description
        x.gluten = gluten
        x.active = active
        x.save()

        return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)


class DeleteCoffeeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, coffee):
        try:
            x = Coffee.objects.get(id=coffee)
            x.delete()
            return Response({"message": "Object destroyed successfully"}, status=status.HTTP_200_OK)
        except Coffee.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class CakesView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CakeSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        cakes = Cake.objects.filter(owner=id)
        return cakes


class AddCakeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        x = request.data.get("gluten")
        if x == True or "on":
            gluten = True
        else:
            gluten = False
        y = request.data.get("active")
        if y == True or "on":
            active = True
        else:
            active = False
        owner = Provider.objects.get(id=id)

        cake = Cake.objects.create(name=name,
                                   price=price,
                                   description=description,
                                   gluten=gluten,
                                   owner=owner,
                                   active=active)
        cake.save()
        return Response({"message": "Cake has been saved"}, status=status.HTTP_200_OK)


class EditCakeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, cake):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        gluten = request.data["gluten"]
        active = request.data["active"]

        x = Cake.objects.get(id=cake)

        x.name = name
        x.price = price
        x.description = description
        x.gluten = gluten
        x.active = active
        x.save()

        return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)


class DeleteCakeView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, cake):
        try:
            x = Cake.objects.get(id=cake)
            x.delete()
            return Response({"message": "Object destroyed successfully"}, status=status.HTTP_200_OK)
        except Cake.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class SnacksView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SnackSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        snacks = Snacks.objects.filter(owner=id)
        return snacks


class AddSnackView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        x = request.data.get("gluten")
        if x == True or "on":
            gluten = True
        else:
            gluten = False
        y = request.data.get("active")
        if y == True or "on":
            active = True
        else:
            active = False
        owner = Provider.objects.get(id=id)

        snack = Snacks.objects.create(name=name,
                                      price=price,
                                      description=description,
                                      gluten=gluten,
                                      owner=owner,
                                      active=active)
        snack.save()
        return Response({"message": "Snack has been saved"}, status=status.HTTP_200_OK)


class EditSnackView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, snack):
        name = request.data["name"]
        price = request.data["price"]
        description = request.data["description"]
        x = request.data.get("gluten")
        if x == True or "on":
            gluten = True
        else:
            gluten = False
        y = request.data.get("active")
        if y == True or "on":
            active = True
        else:
            active = False

        x = Snacks.objects.get(id=snack)

        x.name = name
        x.price = price
        x.description = description
        x.gluten = gluten
        x.active = active
        x.save()

        return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)


class DeleteSnackView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, snack):
        try:
            x = Snacks.objects.get(id=snack)
            x.delete()
            return Response({"message": "Object destroyed successfully"}, status=status.HTTP_200_OK)
        except Snacks.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class PlacesView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        places = Place.objects.filter(owner=id)
        return places


class AddPlaceView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        spot_amount = request.data["spot_amount"]
        name = request.data["name"]
        availability = request.data["availability"]
        owner = Provider.objects.get(id=id)

        place = Place.objects.create(spot_amount=spot_amount,
                                     name=name,
                                     availability=availability,
                                     owner=owner)
        place.save()
        return Response({"message": "Place has been saved"}, status=status.HTTP_200_OK)


class EditPlaceView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id, place):
        spot_amount = request.data["spot_amount"]
        name = request.data["name"]
        availability = request.data["availability"]
        owner = Provider.objects.get(id=id)

        x = Place.objects.get(id=place)

        x.spot_amount = spot_amount
        x.name = name
        x.availability = availability
        x.owner = owner
        x.save()

        return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)


class DeletePlaceView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, place):
        try:
            x = Place.objects.get(id=place)
            x.delete()
            return Response({"message": "Object destroyed successfully"}, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class ProviderView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            provider = Provider.objects.get(id=id)
            serializer = ProviderSerializer(provider)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class EditBusinessView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
            business = Provider.objects.get(owner=user)

            name = request.data["name"]
            city = request.data["city"]
            postcode = request.data["postcode"]
            street = request.data["street"]
            kind = request.data["kind"]
            description = request.data["description"]
            facebook_link = request.data["facebook_link"]
            instagram_link = request.data["instagram_link"]

            business.name = name
            business.city = city
            business.postcode = postcode
            business.street = street
            business.kind = kind
            business.owner = user
            business.description = description
            business.facebook_link = facebook_link
            business.instagram_link = instagram_link
            business.save()

            return Response({"message": "The data has been saved"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Provider.DoesNotExist:
            return Response({"message": "Provider not found"}, status=status.HTTP_404_NOT_FOUND)


class ProviderOrders(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        provider = Provider.objects.get(id=id)
        orders = Order.objects.filter(provider=provider)
        return orders


class ProviderLoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

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

        return Response({"message": "OK"}, status=status.HTTP_200_OK)
