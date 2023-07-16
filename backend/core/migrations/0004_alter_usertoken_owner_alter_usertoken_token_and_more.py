# Generated by Django 4.1.4 on 2023-07-14 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_rename_user_customuser_alter_usertoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.CharField(default=uuid.UUID('166c5688-54a5-4c3c-8c53-c9fe25467c12'), max_length=1024, unique=True),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
