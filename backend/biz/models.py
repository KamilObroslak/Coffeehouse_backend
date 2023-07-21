from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class KindProvider(models.IntegerChoices):
    COFFEEHOUSE = 1, _("Coffee house")


class Provider(models.Model):
    name = models.CharField(max_length=256, verbose_name=_("name"))
    city = models.CharField(max_length=256, verbose_name=_("city"))
    postcode = models.CharField(max_length=256, verbose_name=_("postcode"))
    street = models.CharField(max_length=256, verbose_name=_("street"))
    kind = models.IntegerField(choices=KindProvider.choices, verbose_name=_("kind"), default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="owner")
    description = models.CharField(max_length=2048, verbose_name="description", default="")
    facebook_link = models.CharField(max_length=512, verbose_name="facebook link", default="")
    instagram_link = models.CharField(max_length=512, verbose_name="instagram link", default="")

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name


class OpenDayProvider(models.Model):
    owner = models.ForeignKey(Provider, on_delete=models.CASCADE)

    monday = models.BooleanField(default=True)
    monday_from = models.TimeField(default=None)
    monday_to = models.TimeField(default=None)

    tuesday = models.BooleanField(default=True)
    tuesday_from = models.TimeField(default=None)
    tuesday_to = models.TimeField(default=None)

    wednesday = models.BooleanField(default=True)
    wednesday_from = models.TimeField(default=None)
    wednesday_to = models.TimeField(default=None)

    thursday = models.BooleanField(default=True)
    thursday_from = models.TimeField(default=None)
    thursday_to = models.TimeField(default=None)

    friday = models.BooleanField(default=True)
    friday_from = models.TimeField(default=None)
    friday_to = models.TimeField(default=None)

    saturday = models.BooleanField(default=True)
    saturday_from = models.TimeField(default=None)
    saturday_to = models.TimeField(default=None)

    sunday = models.BooleanField(default=True)
    sunday_from = models.TimeField(default=None)
    sunday_to = models.TimeField(default=None)


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name="Coffee")
    price = models.FloatField()
    description = models.CharField(max_length=1024, default="", verbose_name="Description")
    gluten = models.BooleanField(default=False)
    owner = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="owner")
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


class Place(models.Model):
    spot_amount = models.IntegerField()
    name = models.CharField(max_length=256, default="Table", verbose_name="Table")
    availability = models.BooleanField(default=True)

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
    spot = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name="spot")
    total_price = models.FloatField(verbose_name="total price")
    coffees = models.ManyToManyField(Coffee, through='OrderCoffee', verbose_name="coffees")
    cakes = models.ManyToManyField(Cake, through='OrderCake', verbose_name="cakes")
    snacks = models.ManyToManyField(Snacks, through='OrderSnacks', verbose_name="snacks")
    takeaway_order = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="client")
    status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), null=True)
    order_datatime = models.DateTimeField(verbose_name="order datatime", default=timezone.now)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id}"


class OrderCoffee(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="order")
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Coffee order"
        verbose_name_plural = "Coffees order"

    def __str__(self):
        return str(self.order.id)


class OrderCake(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Cake order"
        verbose_name_plural = "Cakes order"

    def __str__(self):
        return str(self.order.id)


class OrderSnacks(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    snacks = models.ForeignKey(Snacks, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Snack order"
        verbose_name_plural = "Snacks order"

    def __str__(self):
        return str(self.order.id)


class OrderHistory(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    time_of_change = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=OrderStatus.choices, verbose_name=_("status"), null=True)

    class Meta:
        verbose_name = "Order history"
        verbose_name_plural = "Orders history"

    def __str__(self):
        return str(self.order_id)
