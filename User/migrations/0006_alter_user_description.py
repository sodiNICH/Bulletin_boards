# Generated by Django 5.0 on 2024-01-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='', max_length=200),
        ),
    ]