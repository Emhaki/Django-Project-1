from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import ReviewForm, CommentForm
from django.shortcuts import redirect, render
from .forms import StoreForm, CommentForm
from .models import Store, Review, Comment
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

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
    reviews = store.review_set.all()

    if request.POST.get("grade-5"):
        reviews = Review.objects.filter(grade=5)
    elif request.POST.get("grade-4"):
        reviews = Review.objects.filter(grade=4)
    elif request.POST.get("grade-3"):
        reviews = Review.objects.filter(grade=3)
    elif request.POST.get("grade-2"):
        reviews = Review.objects.filter(grade=2)
    elif request.POST.get("grade-1"):
        reviews = Review.objects.filter(grade=1)
    elif request.POST.get("reset"):
        reviews = Review.objects.order_by("-pk")

    review_5 = Review.objects.filter(grade=5).count()
    review_4 = Review.objects.filter(grade=4).count()
    review_3 = Review.objects.filter(grade=3).count()
    review_2 = Review.objects.filter(grade=2).count()
    review_1 = Review.objects.filter(grade=1).count()

    review_ave = 0

    if review_ave == 0:
        review_ave = "평가 없음"

    if reviews == True:
        ave = Review.objects.aggregate(Avg("grade"))

        # round(값, 표시하고 싶은 자리수)
        review_ave = round(ave["grade__avg"], 2)

    context = {
        "store": store,
        "reviews": reviews,
        "review_5": review_5,
        "review_4": review_4,
        "review_3": review_3,
        "review_2": review_2,
        "review_1": review_1,
        "review_ave": review_ave,
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
        "comment_form": CommentForm(),
        "comments": review.comment_set.all(),
    }
    return render(request, "reviews/review_detail.html", context)


def review_delete(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:store_detail", store_pk)
    return redirect("reviews:store_detail", store_pk)


def review_update(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                form = review_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect("reviews:review_detail", store_pk, review_pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            "review_form": review_form,
        }
        return render(request, "reviews/review_form.html", context)
    else:
        messages.warning(request, "작성자만 수정할 수 있습니다.")
        return redirect("articles:detail", review.pk)


def search(request):
    search = Store.objects.all().order_by("-pk")
    q = request.POST.get("q", "")
    if q:
        search = search.filter(store_name__icontains=q)
        return render(request, "reviews/search.html", {"search": search, "q": q})
    else:
        return render(request, "reviews/search.html")


def comment_create(request, store_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect("reviews:review_detail", store_pk, review_pk)
    return redirect("reviews:review_detail", store_pk, review_pk)


"""
 def comment_create(request, store_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.review = review
                comment.user = request.user
                comment.save()
                context = {
                    "content": comment.content,
                    "userName": comment.user.username,
                }
                return JsonResponse(context)
        else:
            return HttpResponse(status=403)
    else:
        return redirect("accounts:login")
"""


def comment_delete(request, store_pk, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
            return redirect("reviews:review_detail", store_pk, review_pk)
    return redirect("reviews:review_detail", store_pk, review_pk)
