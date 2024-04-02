from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from socoldapp.models import Product,Cart,Order
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt 
from .models import Order,Cart
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
import random
import razorpay


def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['products']=p
    return render(request,"index.html",context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p                           
    return render(request,"index.html",context)

def pdetails(request,pid):
     context={}
     p=Product.objects.filter(id=pid)
     context["products"]=p
     return render(request,"pdetails.html",context)

def cart(request):
     return render(request,"cart.html")

def order(request):
     return render(request,'placeorder.html')

def index(request):
    return render(request,'index.html')

def about(request):
     return render(request,'about.html')

def contact(request):
     return render(request,'contacts.html')

def register(request):
     context={}
     if request.method=='POST':
       uname=request.POST['uname']
       upass=request.POST['upass']
       uemail=request.POST['uemail']
       uaddress=request.POST['uaddress']
       ucontact=request.POST['ucontact']
       upsc=request.POST['cpass']
       if uname==''or upass=='':
            context['errormsg']='Field should not be empty'
            return render(request,'register.html',context)
       elif upass !=upsc:
           context['errormsg']="Password didn't match"
           return render(request,'register.html',context)
           
       else:
          try:
               c=User.objects.create(username=uname,password=upass,email=uemail,first_name=uaddress,last_name=ucontact)
               c.set_password(upass)
               c.save()
               context['success']="user created succesfully please login"
               return render(request,'register.html',context)
          except Exception:
              context['errormsg']='Username Already Exists'
              return render(request,'register.html',context)
     else:
      
      if request.method=='GET':
        return render(request,'register.html')
 
def user_login(request):
    if request.method=="POST":
        context={}

        uname=request.POST["uname"]
        password=request.POST["upass"]

        if uname=="" or password=="":
            context['errormsg']="Field cannot be empty"
            return render(request,"register.html",context)
        
        else:
            u = authenticate(username=uname,password=password)
            print(u)
            if u is not None:
                login(request,u)

                return redirect("/home")
            
            else:
                context['errormsg']="Invalid username & password"
                return render(request,"login.html",context)
    else:
        return render(request,"login.html")
    
def user_logout(request):
    logout(request)
    return redirect("/loginn")

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
  
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    print(min)
    print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,"index.html",context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def viewcart(request):
    uid = request.user.id
    user_email = request.user.email  # Get the user's email
    user_details = User.objects.get(id=uid)  # Get the user's details
    c = Cart.objects.filter(uid=uid)
    s = 0
    context = {'products': c, 'total': s, 'user_email': user_email, 'user_details': user_details}  # Pass user's email and details to the context
    for x in c:
        s = s + x.pid.price * x.qty
    
    context['total'] = s                                                            
    return render(request, 'cart.html', context)


def placeorder(request):
    uid = request.user.id
    c = Cart.objects.filter(uid=uid)
    oid = random.randrange(1000, 9999)
    print('order id', oid)
    
    # Create an empty list to store user details
    user_details = []
    
    for x in c:
        # Fetch user details only if not fetched already
        if not user_details:
            user_details.append({
                'first_name': x.uid.first_name,
                'email': x.uid.email
            })
        
        o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()
        x.delete()

    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    np = len(c)
    for x in c:
        s = s + x.pid.price * x.qty

    context = {}
    context['n'] = np
    context['products'] = c
    context['total'] = s
    context['user_details'] = user_details  # Pass user details to the context

    return render(request, 'placeorder.html', context)


def updateqty(request,qv,cid):
    print(type(qv))
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")

def addtocart(request, pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id).first()  # Get the user
        p = Product.objects.filter(id=pid).first()  # Get the product

        if u is not None and p is not None:
            q1 = Q(uid=u)
            q2 = Q(pid=p)
            c = Cart.objects.filter(q1 & q2)

            if c.exists():
                messages.warning(request, "Product already exists in the cart.")
            else:
                cart_item = Cart.objects.create(uid=u, pid=p)
                cart_item.save()
                messages.success(request, "Product added successfully.")
        else:
            messages.error(request, "User or product does not exist.")

        return redirect('/home')
    else:
        return redirect('/loginn')

def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    s = 0

    for x in orders:
        s = s + x.pid.price * x.qty
        oid = x.order_id

    client = razorpay.Client(auth=("rzp_test_F9p0X4KwkKGNJb", "P3Br9sllGMi0zpjgfPmhFe14"))
    data = {"amount": s * 100, "currency": "INR", "receipt": oid}  
    payment = client.order.create(data=data)
    print(payment)

    context = {"data": payment}
    return render(request, "makepayment.html", context)


def search_view(request):
    query = request.GET.get('query', '')  
    results = Product.objects.filter(name__icontains=query)  

    context = {
        'products': results,
        'query': query,
    }

    return render(request, 'search_results.html', context)

def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a unique token for password reset
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Construct the password reset link
            reset_link = f"{settings.BASE_URL}/password-reset/{uidb64}/{token}/"

            # Send the password reset link to the user's email
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Display a success message
            messages.success(request, 'Password reset link sent to your email. Please check your inbox.')
    return render(request, 'password_reset.html')
                                                                                                                                

