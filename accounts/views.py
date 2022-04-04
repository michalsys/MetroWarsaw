from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.views import View
from accounts.forms import RegisterFormView, LoginFormView
# Create your views here.


class LoginView(View):
    def get(self, request):
        form = LoginFormView()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginFormView(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'form.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterFormView()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = RegisterFormView(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password_1']
            user = authenticate(username=username, password=password)
            if user is None:
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password_1'])
                new_user.save()
            return redirect('login')
        return render(request, 'form.html', {'form': form})


class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')
