from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_default = models.BooleanField(default=False)  # New field to track default categories
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Track who created the category


    def __str__(self):
        return self.name

class QuantityVariant(models.Model):
    variant_name=models.CharField(max_length=100)
    weight_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add weight value field


    def __str__(self):
        return self.variant_name
    

class ColorVariant(models.Model):
    color_name=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)
    
    def __str__(self):
        return self.color_name    
    
class SizeVariant(models.Model):
    size_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.size_name    


class ShopRegistrationRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='shop')
    shop_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    logo = models.ImageField(upload_to="shop_logos/", blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopRegistrationRequest, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField()
    
    
    stock = models.PositiveIntegerField()
    
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE, null=True, blank=True)

    trending = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def average_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0  # Default to 0 if no reviews

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    weight =  models.ForeignKey(QuantityVariant, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.weight} - ₹{self.price}"




class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        
        
        

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1) # e.g., 1 to 5
    comment = models.TextField(blank=True, null=True)
    email=models.EmailField(default='default@example.com')
    created_at = models.DateTimeField(default=timezone.now)
    

    class Meta:
        unique_together = ('product', 'user')  # A user can only leave one review per product

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)  # Track variants
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} in {self.user.username}\'s cart'
    

class Order(models.Model):
    shop = models.ForeignKey(ShopRegistrationRequest, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15, null=True, blank=True) 
    coupon_code = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
