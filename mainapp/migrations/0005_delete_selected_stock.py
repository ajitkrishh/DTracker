# Generated by Django 4.1.7 on 2023-03-29 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_remove_stock_user_selected_stock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='selected_stock',
        ),
    ]