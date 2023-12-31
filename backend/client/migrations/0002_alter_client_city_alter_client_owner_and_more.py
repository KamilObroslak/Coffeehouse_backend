# Generated by Django 4.2.1 on 2023-08-29 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(blank=True, max_length=256, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='client',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='postcode',
            field=models.CharField(blank=True, max_length=256, verbose_name='postcode'),
        ),
        migrations.AlterField(
            model_name='client',
            name='street',
            field=models.CharField(blank=True, max_length=256, verbose_name='street'),
        ),
    ]
