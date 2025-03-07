from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Review
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserDetailUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']  # Exclude 'password'

    phone_number = forms.CharField(max_length=15, required=False)  # Add phone number field if needed

    # This method ensures that the password field is not included in the form
    def __init__(self, *args, **kwargs):
        super(UserDetailUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')  # Remove the password field
        
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

from django import forms
from .models import ShopRegistrationRequest

class ShopForm(forms.ModelForm):
    class Meta:
        model = ShopRegistrationRequest
        fields = ['shop_name', 'description', 'address', 'contact_number', 'logo', 'is_approved']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from Grocery_app1.models import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('Pending', 'Pending'),
                ('Shipped', 'Shipped'),
                ('Delivered', 'Delivered'),
                ('Cancelled', 'Cancelled'),
            ])
        }


class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'shop','stock', 'color_variant', 'size_variant', 'image2', 'available']
