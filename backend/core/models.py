import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# class Coffee(models.Model):
#     name = models.CharField(max_length=256, verbose_name="Coffee")
#     price = models.FloatField()
#     description = models.CharField(max_length=1024, default="", verbose_name="Description")
#     gluten = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Coffee"
#         verbose_name_plural = "Coffees"
#
#     def __str__(self):
#         return self.name
#
#
# class Cake(models.Model):
#     name = models.CharField(max_length=256, verbose_name="Cake")
#     price = models.FloatField()
#     description = models.CharField(max_length=1024, default="", verbose_name="Description")
#     gluten = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Cake"
#         verbose_name_plural = "Cakes"
#
#     def __str__(self):
#         return self.name
#
#
# class Snacks(models.Model):
#     name = models.CharField(max_length=256, verbose_name="Snacks")
#     price = models.FloatField()
#     description = models.CharField(max_length=1024, default="", verbose_name="Description")
#     gluten = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Snack"
#         verbose_name_plural = "Snacks"
#
#     def __str__(self):
#         return self.name
#
#
# class Place(models.Model):
#     spot_amount = models.IntegerField()
#     name = models.CharField(max_length=256, default="Table", verbose_name="Table")
#     availability = models.BooleanField(default=True)
#
#     class Meta:
#         verbose_name = "Table"
#         verbose_name_plural = "Tables"
#
#     def __str__(self):
#         return self.name
#
#
# class OrderStatus(models.IntegerChoices):
#     SENT = 1, _("Sent")
#     COMPLETE = 2, _("Complete")
#     NO_SHOW = 3, _("No show")
#
#
# class Order(models.Model):
#     spot = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="spot")
#     total_price = models.FloatField(verbose_name="total price")
#     coffees = models.ManyToManyField(Coffee, through='OrderCoffee', verbose_name="coffees")
#     cakes = models.ManyToManyField(Cake, through='OrderCake', verbose_name="cakes")
#     snacks = models.ManyToManyField(Snacks, through='OrderSnacks', verbose_name="snacks")
#     takeaway_order = models.BooleanField(default=False)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="client")
#     status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), null=True)
#     order_datatime = models.DateTimeField(verbose_name="order datatime", default=timezone.now)
#
#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#
#     def __str__(self):
#         return f"Order #{self.id}"
#
#
# class OrderCoffee(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="order")
#     coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name = "Coffee order"
#         verbose_name_plural = "Coffees order"
#
#     def __str__(self):
#         return str(self.order.id)
#
#
# class OrderCake(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name = "Cake order"
#         verbose_name_plural = "Cakes order"
#
#     def __str__(self):
#         return str(self.order.id)
#
#
# class OrderSnacks(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         verbose_name = "Snack order"
#         verbose_name_plural = "Snacks order"
#
#     def __str__(self):
#         return str(self.order.id)
#

class UserToken(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_query_name="user")
    token = models.CharField(default=uuid.uuid4(), unique=True, max_length=1024)

    class Meta:
        verbose_name = "User token"
        verbose_name_plural = "Users token"


# class OrderHistory(models.Model):
#     order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
#     time_of_change = models.DateTimeField(null=True, blank=True)
#     status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), null=True)
#
#     class Meta:
#         verbose_name = "Order history"
#         verbose_name_plural = "Orders history"
#
#     def __str__(self):
#         return str(self.order_id)
