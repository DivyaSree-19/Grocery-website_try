from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Product
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,ReviewForm
from .models import Product, Review ,Cart,Favorite,ProductVariant , Order, OrderItem
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import logout
 #path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name="Logout"),
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ShopRegistrationForm

from django.shortcuts import render, redirect
from .forms import ShopRegistrationForm
from .models import ShopRegistrationRequest

from django.contrib.auth.models import User
from django.http import HttpResponse

def reset_admin_password(request):
    try:
        user = User.objects.get(username='admin')  # Or use email if that's how you login
        user.set_password('admin123')  # Set your new password
        user.save()
        return HttpResponse("Password reset successfully.")
    except User.DoesNotExist:
        return HttpResponse("Admin user not found.")


def register_shop(request):
    if request.method == 'POST':
        # Check if user already has a shop request
        if ShopRegistrationRequest.objects.filter(user=request.user).exists():
            return render(request, 'already_registered.html')  # Show a warning page
        
        form = ShopRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            shop_request = form.save(commit=False)
            shop_request.user = request.user  # Associate the request with the logged-in user
            shop_request.save()
            return redirect('success_page')  # Redirect to a success page after submission
    else:
        form = ShopRegistrationForm()

    return render(request, 'register_shop.html', {'form': form})


def shop_registration_success(request):
    return render(request, 'registration_success.html')

'''
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

'''

def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Fetch variants for the products
    variants = ProductVariant.objects.filter(product__in=products)


    # Attach average rating to each product
    for product in products:
        product.avg_rating = product.average_rating()

    # Prepare the context with categories, products, and variants
    context = {
        'categories': categories,
        'variants': variants,
        'products': products
    }

    return render(request, "home.html", context)


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

#
@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    
    # Attach average rating to each product
    for product in products:
        product.avg_rating = product.average_rating()
        
     # Use __in to filter variants for all products in the category
    variants = ProductVariant.objects.filter(product__in=products)
    # Get all products that the user has favorited
    favorited_products = Favorite.objects.filter(user=request.user).values_list('product', flat=True)
    
    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
        'variants': variants,
        'favorited_products': favorited_products
    })


def about(request):
    return render(request,"about.html")


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    reviews = product.reviews.all()
    variants = ProductVariant.objects.filter(product=product)
  


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
        'variants': variants, 
        

        'reviews': reviews,
        'review_form': form,
        'is_favorited': is_favorited
    })




@login_required
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        email = request.POST.get("email")

        if not rating:
            return render(request, "product_detail.html", {"product": product, "error": "Please select a rating."})

        review, created = Review.objects.update_or_create(
            product=product, user=request.user,
            defaults={"rating": rating, "comment": comment, "email": email}
        )

        return redirect('product_detail', product_id=product.id)



#register func
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
    variant_name = request.POST.get('variant_name')  # Retrieve variant name from POST data
    price = float(request.POST.get('price', 0))  # Retrieve price from POST data
    
    # Find the variant
    variant = product.variants.filter(weight__variant_name=variant_name).first()
    if not variant:
        messages.error(request, 'Invalid variant selected.')
        return redirect('product_detail', product_id=product_id)

    # Check if enough stock is available for the product (not the variant)
    if product.stock < quantity:
        messages.error(request, f'Sorry, only {product.stock} unit(s) of {product.name} are available.')
        return redirect('product_detail', product_id=product_id)

    # Add product and variant to the cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, 
        product=product,
        variant=variant  # Associate cart item with the selected variant
    )

    if not created:
        # Check if the new quantity exceeds the product's stock
        if cart_item.quantity + quantity > product.stock:
            messages.error(
                request,
                f'Sorry, you can only add {product.stock - cart_item.quantity} more unit(s) of {product.name}.'
            )
            return redirect('product_detail', product_id=product_id)
        cart_item.quantity += quantity  # Add the specified quantity to the existing quantity
    else:
        cart_item.quantity = quantity  # Set the quantity for the new item

    cart_item.price = price  # Update the price of the cart item
    cart_item.save()

    # Update stock in the database for the product
    product.stock -= quantity
    product.save()

    messages.success(
        request, 
        f'Product {product.name} ({variant_name}) successfully added to cart with quantity {quantity}!'
    )

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
    total_price = 0
    qua_tot = []

    for item in cart_items:
        if item.variant:
            subtotal = item.variant.price * item.quantity
            total_price += subtotal
            item.subtotal = subtotal
            item.variant_weight = item.variant.weight  # Assign weight
        else:
            item.subtotal = 0
            item.variant_weight = 'Default'  # Assign default if no variant

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


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

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_by_shop = {}

    for item in cart_items:
        shop = item.product.shop
        if shop not in cart_items_by_shop:
            cart_items_by_shop[shop] = []
        cart_items_by_shop[shop].append(item)

    total_price = sum(item.variant.price * item.quantity for item in cart_items)

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address")
        contact_no = request.POST.get("contact_no")  # ✅ Capture contact number
        coupon_code = request.POST.get("coupon_code", "")

        order = None  # Initialize variable for order

        for shop, items in cart_items_by_shop.items():
            shop_total_price = sum(item.variant.price * item.quantity for item in items)

            # Create the order for each shop
            order = Order.objects.create(
                user=request.user,
                shop=shop,
                shipping_address=shipping_address,
                contact_no=contact_no,  # ✅ Save contact number
                coupon_code=coupon_code,
                total_price=shop_total_price,
                status='Pending'
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.variant.price,
                    subtotal=item.variant.price * item.quantity
                )

        # Clear the cart after placing the order
        cart_items.delete()

        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})


from django.shortcuts import render, redirect
from .models import Order, OrderItem, Cart, Product
from django.contrib.auth.decorators import login_required

@login_required
def place_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('cart')  # Redirect if cart is empty

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Get the shop from the first product (assuming all items in cart belong to one shop)
    shop = cart_items.first().product.shop  

    # Create the order
    order = Order.objects.create(
        user=user,
        shop=shop,  # Assign the shop here
        shipping_address=request.POST.get('address'),
        coupon_code=request.POST.get('coupon', None),
        total_price=total_price,
        status='Pending'
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            subtotal=item.product.price * item.quantity
        )

    # Clear the cart after order placement
    cart_items.delete()

    return redirect('order_success')  # Redirect to order success page
