# Generated by Django 5.0 on 2024-03-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0017_remove_advertisements_created_at_str'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisements',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
