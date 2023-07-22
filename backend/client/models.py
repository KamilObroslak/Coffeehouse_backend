from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    phone = models.IntegerField(unique=True)
    city = models.CharField(max_length=256, verbose_name=_("city"),blank=True)
    postcode = models.CharField(max_length=256, verbose_name=_("postcode"), blank=True)
    street = models.CharField(max_length=256, verbose_name=_("street"), blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="owner")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.owner.username
