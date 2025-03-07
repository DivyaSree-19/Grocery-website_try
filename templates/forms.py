from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Review

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment','email']
        widgets = {
     
            'comment': forms.Textarea(attrs={'id': 'comment', 'class': 'form-control custom-comment','placeholder': 'Enter your comment'}),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'form-control custom-email',
                'placeholder': 'Enter your email'
            }),
        }

from django import forms
from .models import ShopRegistrationRequest

class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = ShopRegistrationRequest
        fields = ['shop_name', 'description', 'address', 'contact_number', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


from django import forms
from .models import Category,Product,ShopRegistrationRequest
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'image']
from django import forms
from .models import Product, ProductVariant,QuantityVariant

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'stock', 'color_variant', 'size_variant', 'image2', 'available']

class ProductVariantForm(forms.ModelForm):
   # weight = forms.ModelChoiceField(queryset=QuantityVariant.objects.all(), empty_label="Select Weight")
    
    class Meta:
        model = ProductVariant
        fields = ['weight', 'price']

