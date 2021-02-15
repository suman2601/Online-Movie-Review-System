from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("movie:home")
    else:
        if request.method == "POST":
            form = Register(request.POST or None)

            #check if it is valid
            if form.is_valid():
                user = form.save()

                #get raw password
                raw_password = form.cleaned_data.get('password1')

                #authenticate user

                user = authenticate(username = user.username, password = raw_password )

                #login user

                login(request, user)

                return redirect("movie:home")
            
        else:
            form = Register()
        return render(request, "user/register.html", {"form": form})


#Login

def login_user(request):
    if request.user.is_authenticated:
        return redirect("movie:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            #check the credentials

            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("movie:home")
                else:
                    return render(request, 'user/login.html', {"error": "Your account do not exist!"})
            else:
                return render(request, 'user/login.html', {"error": "Invalid credentials!"})
        return render(request, 'user/login.html')

#Logout

def user_logout(request):
    logout(request)
    return redirect("user:login")
    