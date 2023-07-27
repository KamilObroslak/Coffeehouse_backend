from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from client.models import Client


class KindProvider(models.IntegerChoices):
    COFFEEHOUSE = 1, _("Coffee house")


class Provider(models.Model):
    name = models.CharField(max_length=256, verbose_name=_("name"))
    city = models.CharField(max_length=256, verbose_name=_("city"))
    postcode = models.CharField(max_length=256, verbose_name=_("postcode"))
    street = models.CharField(max_length=256, verbose_name=_("street"))
    kind = models.IntegerField(choices=KindProvider.choices, verbose_name=_("kind"), default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="owner", blank=True)
    description = models.CharField(max_length=2048, verbose_name="description", blank=True)
    facebook_link = models.CharField(max_length=512, verbose_name="facebook link", blank=True)
    instagram_link = models.CharField(max_length=512, verbose_name="instagram link", blank=True)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name
    #
    # def reminder(self):
    #     # kod
    #     pass


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Product")
    price = models.FloatField()
    description = models.CharField(max_length=1024, default="", verbose_name="Description", blank=True)
    gluten = models.BooleanField(default=False)
    owner = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="owner", blank=True)
    active = models.BooleanField(default=True)


class Coffee(Product):
    class Meta:
        verbose_name = "Coffee"
        verbose_name_plural = "Coffees"

    def __str__(self):
        return self.name


class Cake(Product):
    class Meta:
        verbose_name = "Cake"
        verbose_name_plural = "Cakes"

    def __str__(self):
        return self.name


class Snacks(Product):
    class Meta:
        verbose_name = "Snack"
        verbose_name_plural = "Snacks"

    def __str__(self):
        return self.name


class OpenDayProvider(models.Model):
    owner = models.ForeignKey(Provider, on_delete=models.CASCADE, default="", blank=True)

    monday = models.BooleanField(default=True)
    monday_from = models.TimeField(default=None, blank=True, null=True)
    monday_to = models.TimeField(default=None, blank=True, null=True)

    tuesday = models.BooleanField(default=True)
    tuesday_from = models.TimeField(default=None, blank=True, null=True)
    tuesday_to = models.TimeField(default=None, blank=True, null=True)

    wednesday = models.BooleanField(default=True)
    wednesday_from = models.TimeField(default=None, blank=True, null=True)
    wednesday_to = models.TimeField(default=None, blank=True, null=True)

    thursday = models.BooleanField(default=True)
    thursday_from = models.TimeField(default=None, blank=True, null=True)
    thursday_to = models.TimeField(default=None, blank=True, null=True)

    friday = models.BooleanField(default=True)
    friday_from = models.TimeField(default=None, blank=True, null=True)
    friday_to = models.TimeField(default=None, blank=True, null=True)

    saturday = models.BooleanField(default=True)
    saturday_from = models.TimeField(default=None, blank=True, null=True)
    saturday_to = models.TimeField(default=None, blank=True, null=True)

    sunday = models.BooleanField(default=True)
    sunday_from = models.TimeField(default=None, blank=True, null=True)
    sunday_to = models.TimeField(default=None, blank=True, null=True)

    class Meta:
        verbose_name = "Opening day"
        verbose_name_plural = "Opening days"

    def __str__(self):
        return str(self.owner.name)


class Place(models.Model):
    spot_amount = models.IntegerField()
    name = models.CharField(max_length=256, default="Table", verbose_name="Table")
    availability = models.BooleanField(default=True)
    owner = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="owner", blank=True, default="")

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return self.name


class OrderStatus(models.IntegerChoices):
    SENT = 1, _("Sent")
    COMPLETE = 2, _("Complete")
    NO_SHOW = 3, _("No show")


class Order(models.Model):
    spot = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="spot", blank=True)
    total_price = models.FloatField(verbose_name="total price")
    coffees = models.ManyToManyField(Coffee, through='OrderCoffee', verbose_name="coffees")
    cakes = models.ManyToManyField(Cake, through='OrderCake', verbose_name="cakes")
    snacks = models.ManyToManyField(Snacks, through='OrderSnacks', verbose_name="snacks")
    takeaway_order = models.BooleanField(default=False)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="client", blank=True, default="")
    status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), blank=True, default=1)
    order_datatime = models.DateTimeField(verbose_name="order datatime", default=timezone.now)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, default="", null=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id}"


class OrderCoffee(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="order", blank=True)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Coffee order"
        verbose_name_plural = "Coffees order"

    def __str__(self):
        return str(self.order.id)


class OrderCake(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Cake order"
        verbose_name_plural = "Cakes order"

    def __str__(self):
        return str(self.order.id)


class OrderSnacks(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Snack order"
        verbose_name_plural = "Snacks order"

    def __str__(self):
        return str(self.order.id)


class OrderHistory(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    time_of_change = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), null=True, blank=True)

    class Meta:
        verbose_name = "Order history"
        verbose_name_plural = "Orders history"

    def __str__(self):
        return str(self.order_id)

#
# class Reminder(models.Model):
#     provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
#     reminder_date = models.DateTimeField(default=timezone.now())
#     sent = models.BooleanField(default=True)
#
#     class Meta:
#         verbose_name = "Reminder"
#         verbose_name_plural = "Reminders"
#
#     def __str__(self):
#         return str(self.provider)
