# Generated by Django 5.0 on 2024-02-12 16:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0012_user_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribers_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subscriptions_to', to=settings.AUTH_USER_MODEL),
        ),
    ]