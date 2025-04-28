from django.contrib import admin
from .models import Customer, Material, Order, OrderItem



admin.site.register(Customer)
admin.site.register(Material)
admin.site.register(Order)
admin.site.register(OrderItem)
