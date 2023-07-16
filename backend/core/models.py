import uuid

from django.db import models
from django.contrib.auth.models import User


class Coffee(models.Model):
    name = models.CharField(max_length=256, verbose_name="Coffee")
    price = models.FloatField()
    description = models.CharField(max_length=1024, default="", verbose_name="Description")
    gluten = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Kawa"
        verbose_name_plural = "Kawy"

    def __str__(self):
        return self.name


class Cake(models.Model):
    name = models.CharField(max_length=256, verbose_name="Cake")
    price = models.FloatField()
    description = models.CharField(max_length=1024, default="", verbose_name="Description")
    gluten = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Ciasto"
        verbose_name_plural = "Ciasta"

    def __str__(self):
        return self.name


class Snacks(models.Model):
    name = models.CharField(max_length=256, verbose_name="Przekąski")
    price = models.FloatField()
    description = models.CharField(max_length=1024, default="", verbose_name="Description")
    gluten = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Przekąska"
        verbose_name_plural = "Przekąski"


class Place(models.Model):
    spot_amount = models.IntegerField()
    name = models.CharField(max_length=256, default="Stolik", verbose_name="Stolik")
    availability = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Stolik"
        verbose_name_plural = "Stoliki"

    def __str__(self):
        return self.name


class Order(models.Model):
    spot = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="spot")
    total_price = models.FloatField(verbose_name="total price")
    coffees = models.ManyToManyField(Coffee, through='OrderCoffee', verbose_name="coffees")
    cakes = models.ManyToManyField(Cake, through='OrderCake', verbose_name="cakes")
    snacks = models.ManyToManyField(Snacks, through='OrderSnacks', verbose_name="snacks")
    takeaway_order = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="client")
    # status
    # descripition

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

    def __float__(self):
        return self.total_price


class OrderCoffee(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Zamówiona kawa"
        verbose_name_plural = "Zamówione kawy"

    def __int__(self):
        return self.order


class OrderCake(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Zamówione ciastko"
        verbose_name_plural = "Zamówione ciasteczka"

    def __int__(self):
        return self.order


class OrderSnacks(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Zamówiona przekąska"
        verbose_name_plural = "Zamówione przekąski"

    def __int__(self):
        return self.order


class UserToken(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_query_name="użytkownik")
    token = models.CharField(default=uuid.uuid4(), unique=True, max_length=1024)

    class Meta:
        verbose_name = "Token użytkownika"
        verbose_name_plural = "Tokeny użytkowników"
