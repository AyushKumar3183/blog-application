from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=user_name, password=password)  # Changed 'phone_number' to 'username'

        if user is None:
            messages.error(request, 'Invalid username or password')  # Updated message for clarity
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/mypost/')  # Redirect to homepage or dashboard after login

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=user_name).exists():  # Changed 'user_name' to 'username'
            messages.info(request, 'Username already exists')  # Updated message for clarity
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=user_name  # Changed 'user_name' to 'username'
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'You have created an account successfully')
        return redirect('/login/')  # Redirect to login after successful registration

    return render(request, 'register.html')

def mypost(request):
    posts=Post.objects.all()
    return render(request,'mypost.html',{'posts':posts})
def newpost (request):
    if request.method=="POST":
       title= request.POST.get("title")
       content= request.POST.get("content")
       post=Post.objects.create(
           title=title,
           content=content,
           author=request.user
       )
       
       return redirect('/mypost/')

    
    return render(request,'newpost.html')
def myPost(request):
    context = {
        'posts': Post.objects.filter(author= request.user)
    }
    return render(request, 'mypost.html', context)


def logout(request):
    return redirect(request,'/login/')

# payments/views.py





def payment_view(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=5000,  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )
            return redirect('success')  # Redirect to success page on success
        except stripe.error.StripeError:
            return redirect('error')  # Redirect to error page on failure
    else:
        return render(request, 'paymentform.html')  # Render the payment form for GET requests

def success_view(request):
    return render(request, 'sucess.html')  # Render a success page

def error_view(request):
    return render(request, 'error.html')  # Render an error page