from django.shortcuts import render,redirect
from django.contrib.auth.models import auth , models
from django.http import HttpResponse
from . models import Account
from sample.models import Account
from django.contrib import messages
from django.contrib.auth.models import User,auth,models
from . models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import loader
# from . models import tbl_reg,tbl_login
from hashlib import sha256
from .models import Cart
from .models import product
from .models import dumb
from .models import productcustomer
from email_validator import validate_email
import re
from django.contrib.auth import authenticate
from django.contrib import messages
import pyautogui



# # Create your views here.
def demo(request):
#     request.session['email'] = 'null'
#     request.session['password']='null'
    obj=product.objects.all()
    return render(request,'index.html',{'result':obj})
    

def ewaste(request):
    return render(request,'EWasteManagement.html')
def reg(request):
    if request.method=='POST':
        name=request.POST['name']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        pincode=request.POST['pincode']
        password=request.POST['password']
        if Account.objects.filter(email=email).exists():
            messages.info(request,'Email already Exists')
            return redirect('reg')
        user=Account.objects.create_user(name=name,lname=lname,email=email,phone=phone,address=address,city=city,state=state,pincode=pincode,password=password)
        user.is_customer=True
        user.save()
        messages.success(request,'Thankyou for registering with us Please Login')
        # return redirect('reg')
        current_site = get_current_site(request)
        message = render_to_string('Account_verification.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(
            'Please activate your account',
            message,
            'ecodenmanage@gmail.com',
            [email],
            fail_silently=False,
        )


        return redirect('/login/?command=verification&email=' + email)
    return render(request,'Registration.html')

        
        

    
def login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user=auth.authenticate(email=email,password=password)
        # print(email)
        print(user)
        if user is not None:
            auth.login(request,user)
            # print('hurray')
            request.session['email']=email
            if user.is_admin:
                return redirect('/admin')
            else:
                return redirect('customer')
           
        else:
            messages.error(request,'Invalid Creddentials')
            return redirect('login')
    return render(request,'Login.html')


         
    
def customer(request):
    if 'email' in request.session:
        obj = productcustomer.objects.all()
        return render(request,'customer.html',{'result':obj})
    return redirect('login')
        
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        
    return redirect ('/')
def prof(request):
    return render(request,'prof.html')

def prof_update(request):
    if request.method == "POST":
        name = request.POST.get('name')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode = request.POST.get('pincode')
        # aadharno=request.POST.get('aadharno')




        user_id = request.user.id

        user = Account.objects.get(id=user_id)
        user.name = name
        user.lname = lname
        user.email = email
        user.phone = phone
        user.address = address
        user.city=city
        user.state=state
        user.pincode = pincode
        # user.aadharno=aadharno
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('prof')

def add_cart(request):
    if(request.method=='POST'):
        user = request.user
        product_id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity',1)
        if(product_id is None):
            messages.error(request,"Product id is not mentioned")
            # return
        p = productcustomer.objects.get(id=product_id)
        if(p.stock<quantity):
            messages.error(request,"Not suffcient Quantity")
            # return
        cart,created  = Cart.objects.get_or_create(user=user,product=product)
        if created:
            cart.quantity=quantity
        else:
            cart.quantity+=quantity            
        cart.save()
        messages.success(request,"Product Added Succesfully")
        return redirect('customer')

def cart(request):
    user=auth.authenticate(email=email,password=password)
    print(user)
    if user is not None:
        # order, created = Order.objects.get_or_create(email=email, complete=False)
        items = order.orderitem_Set.all()
    else:
        items = []
    context={'items':items}

    return render(request, 'cart.html',context) 

def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).order_by('-id')
        amount = 0.0
        shipping_amount = 150.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                subtotal = (p.quantity * p.product.product_price)
                amount += float(subtotal)
                total_amount = amount+shipping_amount 
            return render(request, 'addtocart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
        else:
            return render(request, 'emptycart.html')
    if user==request.user:
        item=productcustomer.objects.get(id=id)
        user=request.session['email'] 
        if item.stock>0:
            item.stock -=1
            if Cart.objects.filter( user=user,product_id=item).exists():
                c_item=Cart.objects.get( user =user,product_id=item)
                c_item.quantity = c_item.quantity + 1
                return redirect('/view_cart')
            else:
                quantity = 1
                price= item.price * quantity
                new_cart=Cart(user=user,product_id=item.id,quantity=quantity)
                new_cart.save()
                return redirect('/view_cart')
    #messages.success(request, 'Sign in..!!')
    return redirect('login')
def plusqty(request,id):
    cart=Cart.objects.filter(id=id) 
    for cart in cart:   
        if cart.product.stock > cart.quantity:
            cart.quantity +=1
            cart.price=cart.quantity * cart.productcustomer.product_price
            cart.save()
            return redirect('/view_cart')
        messages.info(request, 'Out of Stock')
        return redirect('/view_cart')
def minusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.quantity > 1 :
            cart.quantity -=1
            cart.price=cart.quantity * cart.price
            cart.save()
            return redirect('/view_cart')
        return redirect('/view_cart') 
def de_cart(request,id):
    Cart.objects.get(id=id).delete()
    return redirect(view_cart)       
def add_cart(request):
    user = request.user
    # quantity=request.get('quantity')
    product_id = request.GET.get('prod_id')
    #print(product_id)
    product = productcustomer.objects.get(id=product_id)
    if product.stock >0:
        Cart(user=user,product=product).save()
        return redirect('customer')
    else:
        quantity = 1
        total = productcustomer.product_price * quantity
        new_cart = Cart(user=user,product=product).save()
        return redirect('customer')
def productsummary(request):
    if request.user.is_authenticated:
        context={}
    return render(request, 'productsummary.html')
        # user = request.user
        # cart = Cart.objects.filter(user=user).order_by('-id')
        # amount = 0.0
        # shipping_amount = 150.0
        # total_amount = 0.0
        # cart_product = [p for p in Cart.objects.all() if p.user == user]
        # #print(cart_product)
        # if cart_product:
        #     for p in cart_product:
        #         subtotal = (p.quantity * p.product.product_price)
        #         amount += float(subtotal)
        #         total_amount = amount+shipping_amount 
        #     return render(request, 'productsummary.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
        # else:
        #     return render(request, 'customer.html')

def pickup1(request):
    pickupprofile=Account.objects.get(id=request.user.id)
    abc=dumb.objects.filter(fk=pickupprofile)
    context = {
        'pickupprofile':pickupprofile,
        'dumb':abc

    }
    if request.method=='POST':
        wimage=request.FILES['wimg']
        # date=request.date['date']
        date = request.POST.get('date')
        d = dumb(date=date,fk = request.user,wimage=wimage)
        d.save()
    # return render(request,'customer.html') 
        # pickup(wimage=wimg).save()
        # image.save()
    # else:
    #     messages.error(request, 'Image not entered')
        # return redirect('pickup')
   
    return render(request,'pickup.html', context)
    # )
# def base(request):
#     context={}
#     return render(request, 'base.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'ecodenmanage@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'changepassword.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('http://127.0.0.1:8000/login/')
    else:
        messages.error(request, 'In-valid activation link')
        return redirect('reg')
def updateProfile(request):
    userprofile=Account.objects.get(id=request.user.id)



