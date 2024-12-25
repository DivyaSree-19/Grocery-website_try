from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class QuantityVariant(models.Model):
    variant_name=models.CharField(max_length=100)
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


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    quantity_variant = models.ForeignKey(QuantityVariant, on_delete=models.CASCADE, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE, null=True, blank=True)

    trending = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        
        
        

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # e.g., 1 to 5
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
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} in {self.user.username}\'s cart'