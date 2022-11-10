from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .forms import NewUserForm


def login_request(request):
    if request.user.is_authenticated:
        return redirect("bracket:open")
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Login successful.")
        return redirect("home:home")
    messages.error(request, "Unsuccessful registration. Invalid information.")  
    return render (request=request, template_name="identification/login-register.html", context={})

def register_request(request):
    if request.user.is_authenticated:
        return redirect("bracket:open")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home:home")
    messages.error(request, "Unsuccessful Login. Invalid information.")  
    form = NewUserForm()
    return render (request=request, template_name="identification/login-register", context={"register_form":form})
