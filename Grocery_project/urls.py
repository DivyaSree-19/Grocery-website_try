
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Grocery_app1 import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Using default LoginView
    path('logout/', views.logout_v, name='logout'),
    path('profile/', views.profile, name='profile'),
    
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
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
