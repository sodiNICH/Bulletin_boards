# Generated by Django 5.0 on 2024-01-25 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0006_alter_advertisements_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisements',
            name='condition',
            field=models.CharField(choices=[('b/w', 'Б/у'), ('new', 'Новый')], null=True),
        ),
    ]
