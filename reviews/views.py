from django.shortcuts import render, redirect
from reviews.forms import ReviewForm
from django.shortcuts import redirect, render
from .models import Store, Review
from .forms import StoreForm
from django.contrib import messages

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        "stores": stores,
    }
    return render(request, "reviews/index.html", context)


def store(request):
    if request.method == "POST":
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

    return render(request, "reviews/store.html", context)


def store_detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    context = {
        "store": store,
        "reviews":store.review_set.all()

    }
    return render(request, "reviews/store_detail.html", context)


def review_create(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.store = store
            review.user = request.user
            review.save()
            return redirect("reviews:store_detail", store.pk)
    else:
        review_form = ReviewForm()
    context = {
        "review_form": review_form,
    }
    return render(request, "reviews/review_form.html", context)


def review_detail(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    store = Store.objects.get(pk=store_pk)
    context = {
        "review": review,
        "store": store,
    }
    return render(request, "reviews/review_detail.html", context)


def review_delete(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:store_detail", store_pk)
    return redirect("reviews:store_detail", store_pk)


def review_update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("reviews:review_detail", review_pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            "review_form": review_form,
        }
        print("여기 옴")
        return render(request, "reviews/review_form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("articles:detail", review.pk)
