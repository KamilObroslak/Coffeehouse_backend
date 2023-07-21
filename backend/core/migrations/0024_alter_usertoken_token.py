# Generated by Django 4.2.1 on 2023-07-20 09:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('2342025c-86dc-4798-a8f1-d1538fefbf3c'), max_length=1024, unique=True),
        ),
    ]