# Generated by Django 5.0 on 2024-02-23 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0015_user_subscribers'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chats',
            field=models.ManyToManyField(blank=True, to='chat.chat'),
        ),
    ]