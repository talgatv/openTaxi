# Generated by Django 4.2.7 on 2024-01-06 02:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_driver_car_color_alter_driver_car_make_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "Passenger", "verbose_name_plural": "Passengers"},
        ),
        migrations.AlterModelOptions(
            name="driver",
            options={"verbose_name": "Driver", "verbose_name_plural": "Drivers"},
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="full_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
