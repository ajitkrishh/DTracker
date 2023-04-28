from .models import stock,selected_stock
from django.db import transaction
from django.shortcuts import redirect, render
from .stocktickers import STOCKTICKERS
from .stocktickers import symbols
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User


query_url = settings.QUERY_URL
base_url = settings.BASE_URL

def login_(request):    
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if not request.user.is_authenticated and user is not None:
        login(request,user)
        return redirect("/")
    else:
        print(request.user)
        return redirect("/")
    
def logout_(req):
    logout(req)
    return redirect("/")

def signup_(req):
    username = req.POST.get('username')
    password = req.POST.get('password')
    cpassword = req.POST.get('cpassword')
    if password == cpassword and not User.objects.filter(username = username).first():
        newuser = User.objects.create(username = username)
        newuser.set_password(password)
        newuser.save()
        login(req,newuser)
        return redirect("/")
    else:
        print(req.user)
        return redirect("/")

def index(req):
    stockpicker = STOCKTICKERS
    symbols = symbols
    if req.method == "GET":
        if req.user.is_authenticated:
            # stocklist = req.GET.getlist("stocktickers")
            cryptolist = req.GET.getlist("cryptosymbols")
            if not cryptolist:
                cryptolist = []
            with transaction.atomic():
                for item in cryptolist:
                # check if item already exists in the database
                    stockk = selected_stock.objects.filter(user = req.user , ticker = stock.objects.get(ticker = item)).first()
                    if not stockk:
                        selected_stock.objects.create(user = req.user , ticker = stock.objects.get(ticker = item))
            print("updated")
        
    return render(req, "mainapp/index.html", {"stocktickers": symbols,  'room_name': 'track'})

