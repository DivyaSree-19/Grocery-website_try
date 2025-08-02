
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Grocery_app1 import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views

urlpatterns = [

    path('reset-admin/', reset_admin_password),
    
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Using default LoginView
    path('logout/', views.logout_v, name='logout'),
    #path('profile/', views.profile, name='profile'),
    #new dashboard app:
    path('profile/', dashboard_views.profile, name='profile'),
    
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('category/', views.category, name='category'),
    path('brands/', views.brands, name='brands'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('label/', views.label_top, name='label_top'),
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_favorite/<int:product_id>/', views.add_to_favorites, name='add_to_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search, name='search'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'), 
    
    path('register-shop/', views.register_shop, name='register_shop'),
    path('shop-registration-success/', views.shop_registration_success, name='success_page'),

    #admin
   # path('Admin_category/', dashboard_views.admin_category, name='admin_category'),
    path('Admin_product/', dashboard_views.admin_product, name='admin_product'),
    path('Admin_user/', dashboard_views.admin_user, name='admin_user'),
    path('Admin_order/', dashboard_views.admin_order, name='admin_order'),
    path('Admin_feedback/', dashboard_views.admin_feedback, name='admin_feedback'),
    path('Admin_password/', dashboard_views.admin_password, name='admin_password'),
    path('Admin_logout/', dashboard_views.admin_logout, name='admin_logout'),
    #path('Admin_shop/', dashboard_views.admin_shop, name='admin_shop'),
    path('Admin_myorder/', dashboard_views.admin_myorder,name='admin_myorder'),
    path('shops/add/', dashboard_views.add_shop, name='add_shop'),
    path('view/', dashboard_views.view_shops, name='view_shops'),
    path('edit/', dashboard_views.edit_shops, name='edit_shops'),  # Page listing all shops
    path('edit/<int:shop_id>/', dashboard_views.edit_shop_detail, name='edit_shop_detail'),  # Edit specific shop
    path('shops/delete/', dashboard_views.delete_shop_list, name='delete_shops'),
    path('shops/confirm_delete/<int:shop_id>/', dashboard_views.confirm_delete_shop, name='confirm_delete_shop'),
    path('categories/', dashboard_views.category_list, name='category_list'),
    path('categories/add/', dashboard_views.category_add, name='category_add'),
    path('categories/edit/', dashboard_views.admin_edit_categories, name='admin_edit_categories'),
    path('categories/edit/<int:id>/', dashboard_views.admin_edit_category, name='admin_edit_category'),
    path('categories/admin-delete/', dashboard_views.admin_delete_categories, name='admin_delete_categories'),
    path('categories/admin-delete/<int:id>/', dashboard_views.admin_delete_category, name='admin_delete_category'),
    path('products/admin/', dashboard_views.admin_view_products, name='admin_product'),
    path('products/admin/add/', dashboard_views.admin_add_product, name='admin_add_product'),  # Add a new product
    path('products/admin/edit/', dashboard_views.admin_edit_products_view, name='admin_edit_products_view'),  # Shows list
    path('products/admin/edit/<int:pk>/', dashboard_views.admin_edit_product, name='admin_edit_product'),  # Shows form
    path('dashboard/products/delete/', dashboard_views.admin_delete_products_view, name='admin_delete_products_view'),  # Show list
    path('dashboard/products/delete/<int:pk>/', dashboard_views.admin_delete_product, name='admin_delete_product'),  # Confirm delete
    path('dashboard/users/add/', dashboard_views.admin_add_user, name='admin_add_user'),
    path('dashboard/users/', dashboard_views.admin_manage_users, name='admin_manage_users'), 
     path('dashboard/users/edit/', dashboard_views.admin_users_list, name='admin_users_list'),  # View users
    path('dashboard/users/edit/<int:user_id>/', dashboard_views.admin_user_edit, name='admin_user_edit'),  # Edit user
    path('dashboard/users/delete/', dashboard_views.admin_delete_users_list, name='admin_delete_users_list'),
    path('dashboard/users/delete/<int:user_id>/', dashboard_views.admin_user_delete, name='admin_user_delete'),
    path('dashboard/orders/', dashboard_views.admin_orders_list, name='admin_orders_list'),
    path('dashboard/orders/view/<int:order_id>/', dashboard_views.admin_order_detail, name='admin_order_detail'),
    path('dashboard/orders/edit/<int:order_id>/', dashboard_views.admin_order_edit, name='admin_order_edit'),
    path('dashboard/orders/delete/<int:order_id>/', dashboard_views.admin_order_delete, name='admin_order_delete'),
path('dashboard/feedback/', dashboard_views.admin_feedback_list, name='admin_feedback_list'),
path('dashboard/feedback/view/<int:feedback_id>/', dashboard_views.admin_feedback_detail, name='admin_feedback_detail'),
path('dashboard/feedback/delete/<int:feedback_id>/', dashboard_views.admin_feedback_delete, name='admin_feedback_delete'),
path('dashboard/reviews/view/<int:review_id>/', dashboard_views.admin_review_detail, name='admin_review_detail'),
path('dashboard/admin/change-password/', dashboard_views.admin_change_password, name='admin_change_password'),
#path('customer/shops/', dashboard_views.customer_shops, name='customer_shops'),
path('customer/shops/', dashboard_views.customer_shops, name='customer_shops'),
path('order/<int:order_id>/', dashboard_views.order_detail, name='order_detail'),
path('feedback/', dashboard_views.customer_feedback, name='customer_feedback'),
path('update/', dashboard_views.update_user_details, name='update_user_details'),
path('change-password/', dashboard_views.customer_change_password, name='customer_change_password'),

path('shop-owner/shops/', dashboard_views.cus_shops, name='cus_shops'),
path('order/<int:order_id>/', dashboard_views.cus_order_detail, name='cus_order_detail'),
path('cus/feedback/', dashboard_views.cus_feedback, name='cus_feedback'),
path('cus/update/', dashboard_views.cus_update_user_details, name='cus_update_user_details'),
path('cus/change-password/', dashboard_views.cus_change_password, name='cus_change_password'),

#  path('categories/delete/<int:id>/', dashboard_views.category_delete, name='category_delete'),
    
    
     #shop
    path('Shop_category/', dashboard_views.shop_category, name='shop_category'),
    path('Shop_product/',  dashboard_views.shop_product,  name='shop_product'),
    path('Shop_user/',     dashboard_views.shop_user,     name='shop_user'),
    path('Shop_order/',    dashboard_views.shop_order,    name='shop_order'),
    path('Shop_feedback/', dashboard_views.shop_feedback, name='shop_feedback'),
    path('Shop_password/', dashboard_views.shop_password, name='shop_password'),
    path('Shop_logout/',   dashboard_views.shop_logout,   name='shop_logout'),
    path('Shop_shop/',     dashboard_views.shop_shop,     name='shop_shop'),
    path('Shop_myorder/',  dashboard_views.shop_myorder,  name='shop_myorder'),
    
    path('shop-owner-categories/', dashboard_views.shop_owner_categories, name='shop_owner_categories'),
    #path('categories/add/', dashboard_views.add_category, name='add_category'),
    path('add/', dashboard_views.add_category, name='add_category'),
    #path('view/', dashboard_views.view_categories, name='view_categories'), 
    #path('edit-categories/', dashboard_views.edit_categories_view, name='edit_categories_view'),
    #path('edit/<int:pk>/', dashboard_views.edit_category, name='edit_category'),
    
    path('edit-categories/', dashboard_views.edit_categories_view, name='edit_categories_view'),
    path('edit-category/<int:pk>/', dashboard_views.edit_category, name='edit_category'),

    
    path('delete-categories/', dashboard_views.delete_categories_view, name='delete_category'),
    path('delete/<int:pk>/', dashboard_views.delete_category, name='delete_category'),
    
    path('products/add/', dashboard_views.add_product, name='add_product'),
    path('products/', dashboard_views.view_products, name='view_products'),
    path('products/edit/', dashboard_views.edit_products_view, name='edit_products'),
    path('products/edit/<int:pk>/', dashboard_views.edit_product, name='edit_product'),
    path('products/delete/', dashboard_views.delete_products_view, name='delete_products'),
    path('products/delete/<int:pk>/', dashboard_views.delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
