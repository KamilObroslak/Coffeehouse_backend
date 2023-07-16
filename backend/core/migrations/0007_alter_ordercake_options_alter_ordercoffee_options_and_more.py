# Generated by Django 4.1.4 on 2023-07-15 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_remove_order_cafe_order_remove_order_cake_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordercake',
            options={'verbose_name': 'Zamówione ciastko', 'verbose_name_plural': 'Zamówione ciasteczka'},
        ),
        migrations.AlterModelOptions(
            name='ordercoffee',
            options={'verbose_name': 'Zamówiona kawa', 'verbose_name_plural': 'Zamówione kawy'},
        ),
        migrations.AlterModelOptions(
            name='ordersnacks',
            options={'verbose_name': 'Zamówiona przekąska', 'verbose_name_plural': 'Zamówione przekąski'},
        ),
        migrations.AddField(
            model_name='cake',
            name='description',
            field=models.CharField(default='', max_length=1024, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='coffee',
            name='description',
            field=models.CharField(default='', max_length=1024, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='takeaway_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='place',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='snacks',
            name='description',
            field=models.CharField(default='', max_length=1024, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Cake'),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Coffee'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('bf486d7c-f56f-4852-8f26-08450392454d'), max_length=1024, unique=True),
        ),
    ]
