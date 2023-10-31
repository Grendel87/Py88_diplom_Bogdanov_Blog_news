from django.shortcuts import render
from django.shortcuts import redirect

from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout

from user.forms import SignUpForm, LoginForm
from blog.models import Article


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')

        return render(request, 'login.html')

    def post(self, request):
        errors = None
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                return redirect('profile')
            else:
                errors = 'User not found. Check login or password..'

        return render(request, 'login.html', {'errors': errors})


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        articles = Article.objects.filter(authors__in=[request.user]).values('id', 'title', 'content')
        return render(request, 'profile.html', context={'articles': articles})


class SignUpView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')

        return JsonResponse({})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')

        return render(request, 'signup.html')
