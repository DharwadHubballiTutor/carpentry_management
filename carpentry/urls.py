from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/new/', views.create_order, name='create_order'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('order/edit/<int:order_id>/', views.order_edit, name='edit_order'),
]
