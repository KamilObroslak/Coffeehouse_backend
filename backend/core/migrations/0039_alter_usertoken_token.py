# Generated by Django 4.2.1 on 2023-07-27 06:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('8a51aec6-6b07-4043-ba50-66b8098355f6'), max_length=1024, unique=True),
        ),
    ]
