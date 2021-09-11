from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    return render(request, "index.html")

def signUp(request):
    if request.method == "POST":        
        email = request.POST["email"]
        username = request.POST["name"]
        pass1 = request.POST["pass"]
        pass2 = request.POST["confirm_pass"]
        #config = request.user_agent.os
        # checks for error
        if pass1 == pass2:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, "Passwords don't match.")
            return render(request, "index.html")
    else:
        return HttpResponse("Not Found")

def logIn(request):
    if request.method == "POST":
        l_name = request.POST["login_name"]
        l_pass = request.POST["login_pass"]

        user = authenticate(username = l_name, password = l_pass)
        if user is not None and user.is_staff == True:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('admin/')
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('courses:home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    else:
        HttpResponse("Not Found")

def logOut(request):
    logout(request)
    return redirect('home')
