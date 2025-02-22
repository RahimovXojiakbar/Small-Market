from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.shop_view, name='shop'),
    path('product_detail/<int:uuid>/', views.product_detail_view, name='product_detail'),
    path('orders/', views.orders_view, name='orders'),
    path('order/<int:uuid>/', views.order_detail, name='order_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('buy-now/<int:uuid>/', views.buy_now_view, name='buy_now'),
    path('cancel-order/<int:uuid>/', views.cancel_order_view, name='cancel_order'),

    
]
