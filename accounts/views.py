from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
# Create your views here.

def create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context={
        'form':form
    }
    return render(request, 'accounts/create.html', context)

def detail(request,user_pk):
    user= get_user_model().objects.get(pk=user_pk)
    context={
        'user':user
    }
    return render(request, 'accounts.detail.html', context)
