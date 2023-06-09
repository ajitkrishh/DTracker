# Generated by Django 4.1.7 on 2023-03-28 09:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_remove_stock_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='close',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='current_price',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='high',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='low',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='open',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='previous_close',
        ),
        migrations.AddField(
            model_name='stock',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
