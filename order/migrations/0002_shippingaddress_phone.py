# Generated by Django 4.2.2 on 2023-06-11 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]