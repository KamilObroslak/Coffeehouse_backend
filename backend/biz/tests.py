from django.test import TestCase
from django.urls import reverse

from biz.models import OpenDayProvider
from core.models import *
# from faker import Faker
from django.contrib.auth.models import User


class UpdateHoursTestCase(TestCase):
    def setUp(self):
        self.model = OpenDayProvider.objects.create(owner=User.objects.get(id=1),
                                                    monday=True,
                                                    monday_from="05:00",
                                                    monday_to="15:00",
                                                    tuesday=True,
                                                    tuesday_from="06:00",
                                                    tuesday_to="15:00",
                                                    wednesday=True,
                                                    wednesday_from="07:00",
                                                    wednesday_to="16:00",
                                                    thursday=True,
                                                    thursday_from="08:00",
                                                    thursday_to="18:00",
                                                    friday=True,
                                                    friday_from="12:00",
                                                    friday_to="23:00",
                                                    saturday=True,
                                                    saturday_from="12:00",
                                                    saturday_to="23:00",
                                                    sunday=True,
                                                    sunday_from="08:00",
                                                    sunday_to="22:00")
        print("UpdateHoursTestCase setUp OK")

    def test_opendayprovider_add(self):
        self.assertTrue(OpenDayProvider.objects.all().exists())
        print("UpdateHoursTestCase test_opendayprovider_add OK")

    def test_opendayprovider_modify(self):
        new_days = OpenDayProvider(monday=True,
                                   monday_from="05:00",
                                   monday_to="15:00",
                                   tuesday=True,
                                   tuesday_from="06:00",
                                   tuesday_to="15:00",
                                   wednesday=True,
                                   wednesday_from="07:00",
                                   wednesday_to="16:00",
                                   thursday=True,
                                   thursday_from="08:00",
                                   thursday_to="18:00",
                                   friday=True,
                                   friday_from="12:00",
                                   friday_to="23:00",
                                   saturday=True,
                                   saturday_from="12:00",
                                   saturday_to="23:00",
                                   sunday=True,
                                   sunday_from="10:00",
                                   sunday_to="22:00")
        self.model = new_days
        self.model.save()
        print("OK..")
        return new_days

    def test_opendayprovider_delete(self):
        self.model.delete()
        self.assertFalse(OpenDayProvider.objects.filter(monday=True).exists())
