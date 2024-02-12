# Generated by Django 5.0 on 2024-01-26 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0008_alter_advertisements_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisements',
            name='condition',
            field=models.CharField(choices=[('b/w', 'Б/у'), ('new', 'Новый')]),
        ),
        migrations.AlterField(
            model_name='advertisements',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'),
        ),
    ]