# Generated by Django 4.1.4 on 2023-07-15 10:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_ordercake_options_alter_ordercoffee_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('09ccac94-90b1-4e79-89a0-e0507626c225'), max_length=1024, unique=True),
        ),
    ]
