# Generated by Django 5.0 on 2024-01-30 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0012_alter_advertisements_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisements',
            name='condition',
            field=models.CharField(default='b/w'),
        ),
    ]
