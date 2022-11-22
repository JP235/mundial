from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View


class LandingView(LoginRequiredMixin, View):
    login_url = "/id"

    def get(self,request):
        print("landing")
        print(request.user)
        return render(request, 'main/main.html')