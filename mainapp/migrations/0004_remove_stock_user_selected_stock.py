# Generated by Django 4.1.7 on 2023-03-29 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_remove_stock_close_remove_stock_current_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='user',
        ),
        migrations.CreateModel(
            name='selected_stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
