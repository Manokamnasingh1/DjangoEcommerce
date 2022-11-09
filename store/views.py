
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from store.models import Profile
from django.http import JsonResponse
import json
import datetime
from django.contrib import messages
from .models import * 
import uuid
from .utils import cookieCart, cartData, guestOrder
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from .models import Contact
def login(request):
    
    if request.method == "POST":
        # Get the post parameters
         
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"successfully logged In")
            return redirect('/store')
        else:
            messages.info(request,'successfully logged In')
            return redirect('/store')
        
    return render(request, "store/login.html")
        
         

def contact(request):
    if request.method =='POST':
       name = request.POST['name']
       email = request.POST['email']
       phone = request.POST['phone']
       content = request.POST['content']
       print(name, email, phone, content)

       if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
           messages.error(request, "Please fill the form of correctly")
       else:
           contact = Contact(name=name,email=email, phone=phone, content=content )
           contact.save()
           messages.success(request, "your message has been successfully sent")
    return render(request , 'store/contact.html')  

def register(request):
      
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
           
            profile_obj = Profile.objects.create(user = user_obj , auth_token =  auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)

            messages.success(request, 'We have sent an mail to you plese verify your email.')
            return redirect('/token')

        except Exception as e:
            print(e)



    return render(request , 'store/register.html')   
   
def success(request):
    return render(request , 'store/success.html')    

def token(request):
    return render(request , 'store/token.html')     


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')

            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request, 'Your account has been  verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error(request):
    return render(request , 'store/error.html')   


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )   


     
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)