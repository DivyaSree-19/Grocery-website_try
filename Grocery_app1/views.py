from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,ReviewForm
from .models import Product, Review ,Cart,Favorite
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import logout
 #path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name="Logout"),
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_staff(user):
    return user.groups.filter(name='Staff').exists()

@login_required
def profile(request):
    if is_customer(request.user):
        dashboard = 'customer'
        orders = None  # Set orders to None since there's no Order model
    elif is_admin(request.user):
        dashboard = 'admin'
        orders = None
    elif is_manager(request.user):
        dashboard = 'manager'
        orders = None
    elif is_staff(request.user):
        dashboard = 'staff'
        orders = None
    else:
        dashboard = 'customer'
        
        orders = None
    
    return render(request, 'profile.html', {'dashboard': dashboard, 'orders': orders})



def logout_view(request):
    logout(request)
    return redirect('login')



# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    for product in products:
        print(product.id, product.name) 
    context = {
        'categories': categories,
        'products':products
    }
    return render(request,"home.html",context)

def category(request):
    return render(request,"category.html")

def brands(request):
    return render(request,"brands.html")

def blog(request):
    categories = Category.objects.all()
    for category in categories:
        print(category.id, category.name) 
    context = {
        'categories': categories,
    }
    return render(request, 'blog.html', context)


@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    # Get all products that the user has favorited
    favorited_products = Favorite.objects.filter(user=request.user).values_list('product', flat=True)

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
        'favorited_products': favorited_products
    })

def about(request):
    return render(request,"about.html")


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    is_favorited = Favorite.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False
      
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added.')
            return redirect('product_details', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'product_details.html', {
        'product': product,
        'reviews': reviews,
        'review_form': form,
        'is_favorited': is_favorited
    })



@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added.')
        else:
            messages.error(request, 'There was an error with your review.')
    return redirect('product_detail', product_id=product.id)

def register(request):
    if request.method=='POST':
        name=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:
            user=User.objects.create_user(username=name,email=email,password=password1)
            user.is_staff=False
            user.is_superuser=False
            user.save()
            
            # Add user to 'Customer' group
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)
            
            messages.success(request,'u account has been created..')
            return redirect('login')
        else:
            messages.warning(request,'password mismatching...!')
            return redirect('register')
    else:
       form=CreateUserForm()
       return render(request,"register.html",{'form':form})



def logout_v(request):
    logout(request) 
    return render(request,'logout.html')

def label_top(request,category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'navbar.html', context)
    
#****************************************************************************************    

#@login_required
#def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Retrieve quantity from POST data, defaulting to 1

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity  # Add the specified quantity to the existing quantity
    else:
        cart_item.quantity = quantity  # Set the quantity for the new item

    cart_item.save()
    messages.success(request, f'Product {product.name} successfully added to cart with quantity {quantity}!')

    return redirect('product_detail', product_id=product_id)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Retrieve quantity from POST data, defaulting to 1

    # Check if enough stock is available
    if product.stock < quantity:
        messages.error(request, f'Sorry, only {product.stock} unit(s) of {product.name} are available.')
        return redirect('product_detail', product_id=product_id)

    # Add product to the cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        # Check if the new quantity exceeds stock
        if cart_item.quantity + quantity > product.stock:
            messages.error(
                request,
                f'Sorry, you can only add {product.stock - cart_item.quantity} more unit(s) of {product.name}.'
            )
            return redirect('product_detail', product_id=product_id)
        cart_item.quantity += quantity  # Add the specified quantity to the existing quantity
    else:
        cart_item.quantity = quantity  # Set the quantity for the new item

    cart_item.save()

    # Update stock in the database
    product.stock -= quantity
    product.save()

    messages.success(request, f'Product {product.name} successfully added to cart with quantity {quantity}!')

    return redirect('product_detail', product_id=product_id)

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's favorites
    favorite_item, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If it's already in favorites, remove it
        favorite_item.delete()
        messages.success(request, f'{product.name} has been removed from your favorites!')
    else:
        # If it's a new favorite, add it
        messages.success(request, f'{product.name} has been added to your favorites!')

    return redirect('product_detail', product_id=product_id)



def search(request):
    query = request.GET.get('q', '')  # Get the search term from the query parameters
    results = Product.objects.filter(
        Q(name__icontains=query) |
      #  Q(description__icontains=query) |
        Q(price__icontains=query) |
        Q(category__name__icontains=query)  # Assuming a ForeignKey relationship with Category
    ) if query else []  # Perform a case-insensitive search
    return render(request, 'search_results.html', {'query': query, 'results': results})

   

@login_required
def favorites_list(request):
    # Retrieve all favorites for the logged-in user
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites_list.html', {'favorites': favorites})

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    qua_tot= (item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,'qua_tot':qua_tot})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    # Implement your checkout logic here
   # cart_items.delete()  # Clear the cart after checkout
    return render(request, 'checkout.html')