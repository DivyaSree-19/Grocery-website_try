from django.shortcuts import render
from Grocery_app1.models import Order,Product,Category,Review,ShopRegistrationRequest
from django.db import models 
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Sum

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_shop(user):
    return user.groups.filter(name='Shop').exists()

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Grocery_app1.models import ShopRegistrationRequest, Order,OrderItem
from django.db.models import Count  # ✅ Add this import


@login_required
def customer_shops(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Get all ordered products along with their shop details
    ordered_products = OrderItem.objects.filter(order__user=request.user).select_related('product', 'order__shop')

    return render(request, 'dashboards/customer_shops.html', {
        'ordered_products': ordered_products,
    })


@login_required
def customer_feedback(request):
    # Fetch all reviews for the logged-in user
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboards/customer_feedback.html', {'reviews': reviews})

from Grocery_app1.forms import UserDetailUpdateForm
@login_required

@login_required
def update_user_details(request):
    user = request.user
    reviews = Review.objects.filter(user=user)

    if request.method == 'POST':
        form = UserDetailUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save updated details
            messages.success(request, 'Your details were successfully updated!')
            return redirect('profile')  # Redirect to the profile page or wherever you need
    else:
        form = UserDetailUpdateForm(instance=user)  # Prepopulate form with current details

    return render(request, 'dashboards/update_user_details.html', {'form': form, 'reviews': reviews})


@login_required
def customer_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps customer logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')  # Redirect to customer's profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dashboards/customer_change_password.html', {'form': form})




@login_required
def customer_shops(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Get all ordered products along with their shop details
    ordered_products = OrderItem.objects.filter(order__user=request.user).select_related('product', 'order__shop')

    return render(request, 'dashboards/customer_shops.html', {
        'ordered_products': ordered_products,
    })


@login_required
def customer_feedback(request):
    # Fetch all reviews for the logged-in user
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboards/customer_feedback.html', {'reviews': reviews})

from Grocery_app1.forms import UserDetailUpdateForm
@login_required

@login_required
def update_user_details(request):
    user = request.user
    reviews = Review.objects.filter(user=user)

    if request.method == 'POST':
        form = UserDetailUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save updated details
            messages.success(request, 'Your details were successfully updated!')
            return redirect('profile')  # Redirect to the profile page or wherever you need
    else:
        form = UserDetailUpdateForm(instance=user)  # Prepopulate form with current details

    return render(request, 'dashboards/update_user_details.html', {'form': form, 'reviews': reviews})


@login_required
def customer_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps customer logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')  # Redirect to customer's profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dashboards/customer_change_password.html', {'form': form})

###-----------------------------------


@login_required
def cus_shops(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Get all ordered products along with their shop details
    ordered_products = OrderItem.objects.filter(order__user=request.user).select_related('product', 'order__shop')

    return render(request, 'dashboards/cus_shops.html', {
        'ordered_products': ordered_products,
    })


@login_required
def cus_feedback(request):
    # Fetch all reviews for the logged-in user
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboards/cus_feedback.html', {'reviews': reviews})

from Grocery_app1.forms import UserDetailUpdateForm
@login_required

@login_required
def cus_update_user_details(request):
    user = request.user
    reviews = Review.objects.filter(user=user)

    if request.method == 'POST':
        form = UserDetailUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save updated details
            messages.success(request, 'Your details were successfully updated!')
            return redirect('profile')  # Redirect to the profile page or wherever you need
    else:
        form = UserDetailUpdateForm(instance=user)  # Prepopulate form with current details

    return render(request, 'dashboards/cus_update_user_details.html', {'form': form, 'reviews': reviews})


@login_required
def cus_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps customer logged in
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')  # Redirect to customer's profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dashboards/cus_change_password.html', {'form': form})

def cus_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)  # Fetch items

    return render(request, 'dashboards/order_detail.html', {
        'order': order,
        'order_items': order_items,  # Pass items to template
    })

@login_required
def profile(request):
    # Default context to prevent UnboundLocalError
    context = {
        'dashboard': None,
        'orders': None,
    }

    if is_admin(request.user):
        dashboard = 'admin'
        orders = Order.objects.filter(user=request.user)  # Admin's orders
        shop=ShopRegistrationRequest.objects.count()
        shops = ShopRegistrationRequest.objects.all() 
        context.update({
            'dashboard': dashboard,
            'total_users': User.objects.count(),
            'orders': orders,
            'shop':shop,
            'shops': shops,
            'total_products': Product.objects.count(),
            'total_categories': Category.objects.count(),
            #'new_orders': Order.objects.filter(status="New").count(),
            'total_orders': Order.objects.count(),
            'total_feedback': Review.objects.count(),
            'low_stock': Product.objects.filter(stock__lt=10).count(),
            'total_amount': Order.objects.aggregate(total=models.Sum('total_price'))['total'] or 0,
        })
        
        return render(request, 'dashboards/admin/admin_dashboard.html', context)

    elif is_manager(request.user):
        dashboard = 'manager'
        context.update({
            'dashboard': dashboard,
            # Add manager-specific context here
        })


#shops ----> shop
    elif is_shop(request.user):
        shop = getattr(request.user, 'shop', None)  # Get the shop linked to the user

        if shop and shop.is_approved:
            dashboard = 'shop'
            categories = Category.objects.all()
            orders = Order.objects.filter(shop=shop)
            products = Product.objects.filter(shop=shop)  # Filter products by shop

            context.update({
                'dashboard': dashboard,
                'categories': categories,
                'orders': orders,
                'products': products,
            })

            return render(request, 'dashboards/shop/staff_dashboard.html', context)

           # return render(request, 'dashboards/shop/staff_dashboard.html', context)
       
        else:          
        # Redirect non-approved or non-existent shops to the customer dashboard
            dashboard = 'customer'
            orders = Order.objects.filter(user=request.user)
            context.update({
                'dashboard': dashboard,
                'orders': orders,
            })
            return render(request, 'dashboards/customer_dashboard.html', context)



    else:  # Customer
        dashboard = 'customer'
        orders = Order.objects.filter(user=request.user)
        context.update({
            'dashboard': dashboard,
            'orders': orders,
        })

    return render(request, 'profile.html', context)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)  # Fetch items

    return render(request, 'dashboards/order_detail.html', {
        'order': order,
        'order_items': order_items,  # Pass items to template
    })


def admin_product(request):
    return render(request, 'dashboards/admin/admin_product.html')

def admin_user(request):
    return render(request, 'dashboards/admin/admin_user.html')

def admin_order(request):
    return render(request, 'dashboards/admin/admin_order.html')

def admin_feedback(request):
    return render(request, 'dashboards/admin/admin_feedback.html')

def admin_password(request):
    return render(request, 'dashboards/admin/admin_password.html')

def admin_logout(request):
    return render(request, 'dashboards/admin/admin_logout.html')

from Grocery_app1.models import ShopRegistrationRequest
from Grocery_app1.forms import ShopForm,OrderStatusForm,ProdForm
#Add a Shop (Admin Approval)
@login_required
def add_shop(request):
    # Check if the user already has a registered shop
    if hasattr(request.user, 'shop'):
        return render(request, 'already_registered.html')  # Redirect to the already registered page


    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user  # Assign user
            shop.is_approved = False
            shop.save()
            messages.success(request, "Shop registration request submitted!")
            #return redirect('view_shops')
    else:
        form = ShopForm()
    return render(request, 'dashboards/admin/add_shop.html', {'form': form})

    #return render(request, 'dashboards/admin/add_shop.html', {'form': form})

# ✅ View All Shops (Approved & Pending)
@login_required
def view_shops(request):
    shops = ShopRegistrationRequest.objects.all()
    return render(request, 'dashboards/admin/view_shop.html', {'shops': shops})



def edit_shops(request):
    shops = ShopRegistrationRequest.objects.all()  # Get all shops
    return render(request, 'dashboards/admin/edit_shop.html', {'shops': shops})
from django.contrib.auth.models import Group

def edit_shop_detail(request, shop_id):
    shop = get_object_or_404(ShopRegistrationRequest, id=shop_id)

    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            updated_shop = form.save()

            # Check if the shop is approved
            if updated_shop.is_approved:
                # Assuming `shop.user` is the user associated with the shop, 
                # and you want to assign them to the "shop" group
                shop.user.groups.add(Group.objects.get(name='Shop'))  # Assign to "shop" group
                shop.user.save()  # Save the user after assigning the group

            return redirect('edit_shops')  # Redirect back to the shop list
    else:
        form = ShopForm(instance=shop)

    return render(request, 'dashboards/admin/edit_shop_detail.html', {'form': form})


def delete_shop_list(request):
    shops = ShopRegistrationRequest.objects.all()
    return render(request, 'dashboards/admin/delete_shop.html', {'shops': shops})


def confirm_delete_shop(request, shop_id):
    shop = get_object_or_404(ShopRegistrationRequest, id=shop_id)

    if request.method == "POST":
        shop.delete()
        messages.success(request, f"Shop '{shop.shop_name}' has been deleted successfully!")
        return redirect('delete_shops')  # Redirect back to shop list

    return render(request, 'dashboards/admin/delete_shop_confirm.html', {'shop': shop})


# View Categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboards/admin/list.html', {'categories': categories})

# Add Category (Admin Only)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.is_default = True  # Set default category for admin-added
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboards/admin/add.html', {'form': form})


#edit category for admin
# 1️⃣ View all categories (for admin edit)
def admin_edit_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboards/admin/admin_edit_categories.html', {'categories': categories})

def admin_edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    # Allow editing only if the category is default OR belongs to an admin
    if request.user.is_superuser or not category.is_default:
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return redirect('admin_edit_categories')  # Redirect back to category list
        else:
            form = CategoryForm(instance=category)
    else:
        return HttpResponseForbidden("You cannot edit this category.")

    return render(request, 'dashboards/admin/admin_edit_category.html', {'form': form, 'category': category})


#  View all categories for deletion
def admin_delete_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboards/admin/admin_delete_categories.html', {'categories': categories})
from django.http import HttpResponseForbidden
                                                                         
#  Delete a specific category
def admin_delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_delete_categories')  # Redirect back to the category list after deletion
    return render(request, 'dashboards/admin/admin_delete_category.html', {'category': category})
#admin products
def admin_view_products(request):
    products = Product.objects.all()
    return render(request, 'dashboards/admin/admin_view_products.html', {'products': products})

@login_required

def admin_add_product(request):
    if request.method == 'POST':
        product_form = ProdForm(request.POST, request.FILES)
        formset = ProductVariantFormSet(request.POST)

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save()  # Save product

            formset.instance = product  # Attach variants to product
            formset.save()

            return redirect('admin_product')  # Redirect to admin product list

    else:
        product_form = ProdForm()
        formset = ProductVariantFormSet()

    return render(request, 'dashboards/admin/admin_add_product.html', {
        'product_form': product_form,
        'formset': formset,
    })

@login_required
def admin_edit_products_view(request):

    products = Product.objects.all()  # Get all products
    return render(request, 'dashboards/admin/admin_edit_products.html', {'products': products})

@login_required
def admin_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    formset = ProductVariantFormSet(request.POST or None, instance=product)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('admin_edit_products_view')  # Go back to list after editing

    return render(request, 'dashboards/admin/admin_edit_product_form.html', {
        'form': form,
        'formset': formset,
        'product': product
    })

@login_required
def admin_delete_products_view(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'dashboards/admin/admin_delete_products.html', {'products': products})

@login_required
def admin_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product_name = product.name
        product.delete()
        #messages.success(request, f"Product '{product_name}' deleted successfully.")
        return redirect('admin_delete_products_view')  # Go back to list after deleting

    return render(request, 'dashboards/admin/admin_confirm_delete_product.html', {'product': product})

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms

# Check if user is an admin
def is_admin(user):
    return user.is_staff

# Form for adding a new user
class AdminAddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Password field

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
            # Assign the user to the 'Customer' group by default
            customer_group, created = Group.objects.get_or_create(name='Customer')
            user.groups.add(customer_group)
        return user

# Admin view to add a new user
@login_required
@user_passes_test(is_admin)
def admin_add_user(request):
    if request.method == 'POST':
        form = AdminAddUserForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, "User added successfully!")
            return redirect('admin_add_user')  # Redirect to user list
    else:
        form = AdminAddUserForm()

    return render(request, 'dashboards/admin/admin_add_user.html', {'form': form})

# Admin view to see all users
@login_required
@user_passes_test(is_admin)
def admin_manage_users(request):
    users = User.objects.all()
    return render(request, 'dashboards/admin/admin_manage_users.html', {'users': users})

# View 1: Show user list with edit button
@login_required
@user_passes_test(is_admin)
def admin_users_list(request):
    users = User.objects.all()
    return render(request, 'dashboards/admin/admin_users_lists.html', {'users': users})

class AdminEditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']

# View 2: Edit user form
@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = AdminEditUserForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            #messages.success(request, "User details updated successfully!")
            return redirect('admin_users_list')  # Redirect back to user list

    return render(request, 'dashboards/admin/admin_user_edit.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def admin_delete_users_list(request):
    users = User.objects.exclude(is_superuser=True)  # Exclude superusers for safety
    return render(request, 'dashboards/admin/admin_delete_users_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        #messages.success(request, "User deleted successfully!")
        return redirect('admin_users_list')  # Redirect back to user list

    return render(request, 'dashboards/admin/admin_user_confirm_delete.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def admin_orders_list(request):
    orders = Order.objects.all().order_by('-created_at')  # Fetch all orders, latest first
    return render(request, 'dashboards/admin/admin_orders_list.html', {'orders': orders})

@login_required
@user_passes_test(is_admin)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'dashboards/admin/admin_order_detail.html', {'order': order})

@login_required
@user_passes_test(is_admin)
def admin_order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderStatusForm(request.POST or None, instance=order)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            #messages.success(request, "Order status updated successfully!")
            return redirect('admin_orders_list')

    return render(request, 'dashboards/admin/admin_order_edit.html', {'form': form, 'order': order})

@login_required
@user_passes_test(is_admin)
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.delete()
        #messages.success(request, "Order deleted successfully!")
        return redirect('admin_orders_list')

    return render(request, 'dashboards/admin/admin_order_confirm_delete.html', {'order': order})

@login_required
@user_passes_test(is_admin)
def admin_feedback_list(request):
    reviews = Review.objects.all().order_by('-created_at')  # Fetch latest reviews first
    return render(request, 'dashboards/admin/admin_feedback_list.html', {'reviews': reviews})

 
@login_required
@user_passes_test(is_admin)
def admin_feedback_detail(request, feedback_id):
    review = get_object_or_404(Review, id=feedback_id)
    return render(request, 'dashboards/admin/admin_feedback_detail.html', {'reviews': review})

@login_required
@user_passes_test(is_admin)
def admin_review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'dashboards/admin/admin_review_detail.html', {'review': review})


@login_required
@user_passes_test(is_admin)
def admin_feedback_delete(request, feedback_id):
    feedback = get_object_or_404(Review, id=feedback_id)

    if request.method == "POST":
        feedback.delete()
        #messages.success(request, "Feedback deleted successfully!")
        return redirect('admin_feedback_list')

    return render(request, 'dashboards/admin/admin_feedback_confirm_delete.html', {'feedback': feedback})


@login_required
@user_passes_test(is_admin)
def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps admin logged in
            #messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')  # Redirect to admin dashboard
        else:
            pass
            #messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dashboards/admin/admin_change_password.html', {'form': form})

"this is for shop"
@login_required
def admin_myorder(request):
    context = {
        'dashboard': 'admin',  # Mark this as admin dashboard
        'orders': Order.objects.filter(user=request.user),  # Fetch admin orders
    }

    return render(request, 'dashboards/admin/admin_myorder.html', context)


# shop


def shop_category(request):
    return render(request, 'dashboards/shop/shop_category.html')

def shop_product(request):
    return render(request, 'dashboards/shop/shop_product.html')


from Grocery_app1.models import Order, ShopRegistrationRequest

@login_required
def shop_order(request):
    shop = request.user.shop  # Get the logged-in user's shop
    orders = Order.objects.filter(shop=shop).prefetch_related('items__product')

    context = {
        'orders': orders
    }
    return render(request, 'dashboards/shop/shop_order.html', context)

@login_required
def shop_user(request):
    users_with_orders = Order.objects.values('user').distinct()
    user_orders = []

    for entry in users_with_orders:
        user_id = entry['user']
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user_id=user_id)
        
        shipping_address = orders.first().shipping_address if orders.exists() else "N/A"
        contact_no = orders.first().contact_no if orders.exists() else "N/A"  # ✅ Fetch contact number

        user_orders.append({
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'contact': contact_no,  # ✅ Include contact number
            'address': shipping_address,
            'orders': orders.values_list('id', flat=True)
        })

    context = {
        'user_orders': user_orders,
        'total_users': len(users_with_orders),
    }
    return render(request, 'dashboards/shop/shop_user.html', context)

def shop_feedback(request):
    shop = request.user.shop  # Assuming a Shop model linked to User
    reviews = Review.objects.filter(product__shop=shop).select_related("user", "product")

    context = {'reviews': reviews}
    return render(request, 'dashboards/shop/shop_feedback.html',context)

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def shop_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps user logged in
            #messages.success(request, "Your password has been changed successfully!")
            #return redirect('shop_dashboard')  # Redirect to the shop dashboard
        else:
            pass
            #messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboards/shop/shop_password.html', {'form': form})

def shop_logout(request):
    return render(request, 'dashboards/admin/shop_logout.html')


def shop_shop(request):
    # Query the shop details for the current user
    
    shop_detail = ShopRegistrationRequest.objects.get(user=request.user)
   
    # Pass the shop details to the template
    return render(request, 'dashboards/shop/shop_shop.html', {'shop_detail': shop_detail})


@login_required
def admin_myorder(request):
    context = {
        'dashboard': 'admin',  # Mark this as admin dashboard
        'orders': Order.objects.filter(user=request.user),  # Fetch admin orders
    }

    return render(request, 'dashboards/admin/admin_myorder.html', context)

@login_required
def shop_myorder(request):
    context = {
        'dashboard': 'admin',  # Mark this as admin dashboard
        'orders': Order.objects.filter(user=request.user),  # Fetch admin orders
    }

    return render(request, 'dashboards/shop/shop_myorder.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from Grocery_app1.models import Category,Product
from Grocery_app1.forms import CategoryForm

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user  # Assign the logged-in shop owner
            category.save()
            return redirect('shop_owner_categories')  # Redirect to shop_owner_categories view
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})



@login_required

@login_required
def shop_owner_categories(request):
    # Fetch categories based on whether they are default or owned by the shop owner
    default_categories = Category.objects.filter(is_default=True)  # Admin-added categories
    shop_owner_categories = Category.objects.filter(is_default=False, created_by=request.user)  # Shop owner's categories

    return render(request, 'shop_owner_categories.html', {   
        'default_categories': default_categories,
        'shop_owner_categories': shop_owner_categories,
    })

'''
@login_required
def view_categories(request):
    default_categories = Category.objects.filter(is_default=True)  # Admin-added categories
    shop_owner_categories = Category.objects.filter(is_default=False)  # All shop-owner categories

    return render(request, 'view_categories.html', {
        'default_categories': default_categories,
        'shop_owner_categories': shop_owner_categories,
    })
'''

'''
@login_required
def edit_categories_view(request):
    categories = Category.objects.filter(created_by=request.user)  # Only show their own categories
    return render(request, 'edit_category.html', {'categories': categories})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('edit_category')  # Redirect to the list page after editing
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category_form.html', {'form': form, 'category': category})

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category_name = category.name
        category.delete()
        #messages.success(request, f"Category '{category_name}' deleted successfully.")
        return redirect('delete_category')
    return render(request, 'confirm_delete_category.html', {'category': category})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Prevent editing if it's a default category or not owned by the logged-in shop owner
    if category.is_default or category.created_by != request.user:
        return redirect('shop_owner_categories')  # Redirect to shop_owner_categories if unauthorized

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('shop_owner_categories')  # Redirect after successful edit

    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category_form.html', {'form': form, 'category': category})

'''
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Grocery_app1.models import Category
from Grocery_app1.forms import CategoryForm

@login_required
def edit_categories_view(request):
    # Fetch only the categories created by the logged-in shop owner
    categories = Category.objects.filter(created_by=request.user)
    return render(request, 'edit_categories.html', {'categories': categories})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Ensure only the owner can edit their category
    if category.created_by != request.user:
        return redirect('edit_categories_view')

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('edit_categories_view')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category_form.html', {'form': form, 'category': category})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    # Ensure only the owner can delete their categories
    if category.created_by != request.user:
        return redirect('shop_owner_categories')  # Redirect to the shop owner categories view

    if request.method == "POST":
        category.delete()
        return redirect('shop_owner_categories')  # Redirect after successful deletion

    return render(request, 'confirm_delete_category.html', {'category': category})

@login_required
def delete_categories_view(request):
    # Only show the categories created by the logged-in shop owner
    categories = Category.objects.filter(created_by=request.user)
    return render(request, 'delete_category.html', {'categories': categories})



#product
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from Grocery_app1.models import Product, ProductVariant
from Grocery_app1.forms import ProductForm, ProductVariantForm
from django.contrib import messages

# Create an inline formset for Product and ProductVariant
ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant, form=ProductVariantForm, extra=1, can_delete=True
)


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        formset = ProductVariantFormSet(request.POST)

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)  # Do not save yet

            # Ensure only shop owners can add products
            if hasattr(request.user, 'shop'):
                product.shop = request.user.shop  # Assign the logged-in shop owner
                product.save()

                formset.instance = product  # Attach formset to product
                formset.save()

               # messages.success(request, "Product and variants added successfully!")
                return redirect('view_products')  # Redirect to shop's product view
            else:
                pass
                #messages.error(request, "You are not authorized to add products.")
        else:
            pass
           # messages.error(request, "Please correct the errors below.")
    else:
        product_form = ProductForm()
        formset = ProductVariantFormSet()

    return render(request, 'add_product.html', {
        'product_form': product_form,
        'formset': formset,
    })


'''
# View all products
def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})
'''
# View all products
@login_required
def view_products(request):
    if hasattr(request.user, 'shop'):  # Ensure user has a shop
        products = Product.objects.filter(shop=request.user.shop)  # Filter by shop
    else:
        products = []  # No products if user has no shop
    
    return render(request, 'view_products.html', {'products': products})

# Edit products view list

@login_required
def edit_products_view(request):
    products = Product.objects.filter(shop=request.user.shop)  # Filter by shop

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, shop=request.user.shop)  # Ensure it's owned by the user
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect('edit_products')  # Redirect back after editing

    return render(request, 'edit_product.html', {'products': products})

# Edit specific product form
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, shop=request.user.shop)  # Ensure only shop owner can edit
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    formset = ProductVariantFormSet(request.POST or None, instance=product)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('edit_products')

    return render(request, 'edit_product_form.html', {
        'form': form,
        'formset': formset,
        'product': product
    })

    
# Delete product
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, shop=request.user.shop)  # Ensure ownership
    if request.method == "POST":
        product_name = product.name
        product.delete()
        # messages.success(request, f"Product '{product_name}' deleted successfully.")
        return redirect('delete_products')
    return render(request, 'confirm_delete_product.html', {'product': product})



# Delete products view list
@login_required
def delete_products_view(request):
    products = Product.objects.filter(shop=request.user.shop)  # Filter by shop
    return render(request, 'delete_product.html', {'products': products})
