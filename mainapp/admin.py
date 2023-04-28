from django.contrib import admin

# Register your models here.
from .models import stock,selected_stock

admin.site.register(stock)
admin.site.register(selected_stock)