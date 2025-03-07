from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category ,SizeVariant,ColorVariant,QuantityVariant,Review,Cart,ProductVariant,Order, OrderItem,ShopRegistrationRequest

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(QuantityVariant)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShopRegistrationRequest)
# Register the User model with the admin site
admin.site.unregister(User)  # Unregister the default User admin (if previously registered)
admin.site.register(User, UserAdmin)  # Register the User model with the custom UserAdmin