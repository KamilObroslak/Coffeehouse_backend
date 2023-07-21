# Generated by Django 4.2.1 on 2023-07-20 09:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('ed7374aa-2e86-432f-8591-2c753e0e55e6'), max_length=1024, unique=True),
        ),
    ]
