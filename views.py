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
from .models import productcustomer
from .models import pickup
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
            'ajcejobportal@gmail.com',
            [email],
            fail_silently=False,
        )


        return redirect('/login/?command=verification&email=' + email)
    return render(request,'Registration.html')
# #     if request.method == 'POST':
# #         name=request.POST['name']
# #         lname=request.POST['lname']
# #         email=request.POST['email']
# #         password=request.POST['password']
# #         cpassword=request.POST['cpassword']
# #         phone=request.POST['phone']
# #         # address=request.POST['address']
# #         Role=request.POST["Role"]
# #     #     if (password == cpassword):

# #     #         user=User.objects.create_user(name=name,lname=lname,email=email,password=password,cpassword=cpassword,phone=phone,Role=Role)
# #     #         user.save()
# #     #         print('user created')
# #     #         return redirect('login')

# #     #     else:
# #     #         print('not matching')
# #     #         return redirect('reg')
# #     # else:
# #     #     return redirect('reg')

# #         # if len(name)<3:
# #         #     return redirect('reg')
# #         # if len(phone)>10 or len(phone)<10:
# #         #     return redirect('reg')
# #         # else:
# #         #     if phone[0]=='7' or phone[0]=='8' or phone[0]=='9' or phone[0]=='6':
# #         #         try:
# #         #             phone=int(phone)
# #         #             return redirect('login')
# #         #         except:
# #         #             return redirect('reg')
# #         #     else:
# #         #         return redirect('reg')
# #         # if len(email)>10 and len(email)<30:
# #         #     validate_email(email)
# #         #     return redirect('login')
# #         # else:
# #         #     return redirect('reg')
# #         # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


# #         if (password == cpassword):
# #             if tbl_reg.objects.filter(email=email).exists():
# #                 print("email already exists")
# #                 pyautogui.alert('Just a notification', "Title")
# #                 return redirect('reg')
# #             else:
# #                 tbl_reg(name=name,lname=lname,email=email,password=password,cpassword=cpassword,phone=phone,Role=Role).save()
# #                 tbl_login(email=email,password=password).save()
# #                 print("registered")
# #                 return redirect('login')
# #             # return redirect('reg')
# #         else:
# #             print("not match")
# #             return redirect('reg')
# #         #return redirect('Login.html')
# #     return render(request,'Registration.html')


# # # def isValid(email):
# # #     if re.fullmatch(regex, email):
# # #         print("Valid email")
# # #     else:
# # #         print("Invalid email")
# # #         # return redirect('reg')   
        
        

    
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
# #     # request.session['email'] = 'null'
# #     # request.session['password'] = 'null'
# #     # if 'email' in request.session:
# #     #     return redirect('user/')
# #     if request.method == 'POST':
# #         email=request.POST['email']
# #         print('email')
# #         password=request.POST['password']
# #         print('password')
       
# #         if tbl_login.objects.filter(email=email,password=password).exists():
# #             # request.session['email']=email
# #             # request.session['password']=password
# #             user_detailes=tbl_login.objects.get(email=email,password=password)
# #             email=user_detailes.email
# #             request.session['email']=email
# #             return redirect('user')
# #         else:
# #             print("invalid")
# #             # return redirect('login')
# #     return render(request,"Login.html") 

         
    
def customer(request):
#     if request.session['email'] == 'null':
#         return redirect('login')
#     elif 'email' in request.session:
#         email=request.session['email']
    # if 'email' in request.session:
    #     email=request.session['email']
        obj = productcustomer.objects.all()
        return render(request,'customer.html',{'result':obj})
        # return redirect('user/')
        # ,'id':id,'email':email} 
        # return redirect('login')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        
    return redirect ('/')

# def cart(request):
#     user=auth.authenticate(email=email,password=password)
#     print(user)
#     if user is not None:
#         # order, created = Order.objects.get_or_create(email=email, complete=False)
#         items = order.orderitem_Set.all()
#     else:
#         items = []
#     context={'items':items}
#     return render(request, 'cart.html',context) 
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    #print(product_id)
    product = productcustomer.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/show_cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).order_by('id')

        amount = 0
        shipping_amount = 70.0
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                subtotal = (p.quantity * p.product.product_price)
                amount += int(subtotal)
                total_amount = amount + shipping_amount
            return render(request, 'addtocart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
        else:
            return render(request, 'emptycart.html')
def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 150.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            subtotal = (p.quantity * p.product.selling_price)
            amount += subtotal

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)

def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 50.0
            total_amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            subtotal = (p.quantity * p.product.selling_price)
            amount += subtotal
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)
def checkout(request):
    context={}
    return render(request, 'checkout.html',context)

def pickup(request):
    pickupprofile=Account.objects.get(id=request.user.id)
    context = {'pickupprofile':pickupprofile}
    if request.method=='POST':
        wimage=request.FILES['wimg']
        pickup(wimage=wimg).save()
        # image.save()
    else:
        messages.error(request, 'Image not entered')
        # return redirect('pickup')
   
    return render(request,'pickup.html', context)
    # )
def base(request):
    context={}
    return render(request, 'base.html')


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



#     if request.method == 'POST':
#         fname = request.POST.get("name")
#         lname = request.POST.get("lname")
#         phone_number = request.POST.get("phone")

#         userprofile.name=name
#         userprofile.lname=lname
#         userprofile.phone=phone
#         userprofile.save()
#         return redirect('updateProfile')
#     context = {
#         # 'orders_count': order_count,
#         'userprofile':userprofile,
#     }
#     return render(request, 'updateProfile.html', context)