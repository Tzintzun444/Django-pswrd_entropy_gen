# Generated by Django 5.2.1 on 2025-06-23 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_registration_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='registration_date',
        ),
    ]
