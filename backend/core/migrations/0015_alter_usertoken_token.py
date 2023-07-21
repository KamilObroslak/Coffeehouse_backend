# Generated by Django 4.2.1 on 2023-07-19 08:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('9036c761-9dd2-4d68-bbb4-bd52ecba4473'), max_length=1024, unique=True),
        ),
    ]
