from django.contrib import admin

# Register your models here.

from .models import Product
from .models import  Cart, CartItem
from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)