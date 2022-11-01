from django.shortcuts import render, redirect
from reviews.forms import ReviewForm
from django.shortcuts import redirect, render
from .models import Store
from .forms import StoreForm

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        "stores": stores,
    }
    return render(request, "reviews/index.html", context)

def store(request):
  if request.method == 'POST':
    store_form = StoreForm(request.POST, request.FILES)
    if store_form.is_valid():
      store = store_form.save(commit=False)
      store.save()
      return redirect("reviews:index")
  else:
    store_form = StoreForm()
  
  context = {
    "store_form": store_form,
  }

  return render(request, 'reviews/store.html', context)

def store_detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    context = {
        "store": store,
    }
    return render(request, "reviews/store_detail.html", context)


def review_create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form(commit=False)
            review.store = store
            review.user = request.user
            review.save()
            return redirect("reviews:store_detail", store.pk)
    else:
        form = ReviewForm()
    context = {
        "form": form,
    }
    return render(request, "reviews/review_form.html", context)
