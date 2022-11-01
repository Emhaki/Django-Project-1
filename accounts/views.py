from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

def create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('accounts:create')
    else:
        form = CustomUserCreationForm()
    context={
        'form':form
    }
    return render(request, 'accounts/create.html', context)