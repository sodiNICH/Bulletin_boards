# Generated by Django 5.0 on 2024-01-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_options_user_created_at_user_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(default='https://707.su/LpC'),
        ),
    ]
