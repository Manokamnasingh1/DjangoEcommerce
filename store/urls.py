from django.urls import path
from django.contrib import admin
from .views import *
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('store/', views.store, name="store"),
    path('contact/', views.contact, name="contact"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	 path('login/' ,  views.login , name="login"),
    path('register/' ,  views.register  , name="register"),
     path('token/' ,  views.token  , name="token"),
	 path('error/' ,  views.error  , name="error"),
    path('success/' ,  views.success  , name="success"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('verify/<auth_token>/', views.verify, name='verify')
	

]