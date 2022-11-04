from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.http import JsonResponse

def create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        profile = Profile()
        if form.is_valid():
            user = form.save()
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect("reviews:index")

    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/create.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        form = AuthenticationForm()
    context = {
      "form": form,
    }
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("reviews:index")


# @login_required
# def follow(request, pk):
#     user = get_object_or_404(get_user_model(), pk=pk)
#     if request.user == user:
#         messages.warning(request, "자추금지!!!")
#         return redirect("accounts:detail", pk)
#     if request.user in user.followers.all():
#         user.followers.remove(request.user)
#     else:
#         user.followers.add(request.user)
#     return redirect("accounts:detail", pk)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    profile = user.profile_set.all()[0]
    user_point = (user.review_set.count() * 5) + ((user.comment_set.count() * 1))
    context = {
        "user": user,
        "profile": profile,
        "user_point": user_point,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "accounts/update.html", context)


@login_required
def profile(request, pk):  # 프로필
    user = get_user_model().objects.get(pk=pk)
    reviews = user.review_set.all()
    comments = user.comment_set.all()
    profile = user.profile_set.all()[0]
    context = {
        "reviews": reviews,
        "comments": comments,
        "profile": profile,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_update(request):  # 프로필 업데이트
    user = get_user_model().objects.get(pk=request.user.pk)
    current_user = user.profile_set.all()[0]
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect("reviews:index")
    else:
        form = ProfileForm(instance=current_user)
    context = {
        "profile_form": form,
    }
    return render(request, "accounts/profile_update.html", context)

def follow(request, pk):
  if request.user.is_authenticated:
    User = get_user_model()
    me = request.user
    you = User.objects.get(pk=pk)
    if me != you:
      if you.followers.filter(pk=me.pk).exists():
        you.followers.remove(me)
        is_followed = False
      else:
        you.followers.add(me)
        is_followed = True
      context = {
        'is_followed': is_followed,
        'followers_count': you.followers.count(),
        'followings_count': you.followings.count(),
      }
      return JsonResponse(context)
    return redirect('accounts:detail', you.username)
  return redirect('accounts:login')
