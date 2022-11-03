from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms import ReviewForm, CommentForm
from .forms import StoreForm, CommentForm
from .models import Store, Review, Comment
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
from datetime import date, datetime , timedelta

# Create your views here.
@require_safe
def index(request):
    stores = Store.objects.all()
    paginator = Paginator(stores, 1)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "stores": stores,
        "page_obj": page_obj,
    }
    return render(request, "reviews/index.html", context)


@login_required
def store(request):
    if request.method == "POST":
        store_form = StoreForm(request.POST, request.FILES)
        if store_form.is_valid():
            store = store_form.save(commit=False)
            store.user = request.user
            store.save()
            messages.success(request, "가게 정보 작성이 완료되었습니다.")
            return redirect("reviews:index")
    else:
        store_form = StoreForm()
    context = {
        "store_form": store_form,
    }
    return render(request, "reviews/store.html", context)


def store_detail(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    reviews = store.review_set.all()
    reviews_ = store.review_set.all()

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
        "reviews_": reviews_,
        "review_5": review_5,
        "review_4": review_4,
        "review_3": review_3,
        "review_2": review_2,
        "review_1": review_1,
        "review_ave": review_ave,
    }
    response = render(request, "reviews/store_detail.html", context)
    store.hits +=1
    store.save()

    return response


@login_required
def store_delete(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    if request.user == store.user:
        if request.method == "POST":
            store.delete()
            messages.success(request, "가게 정보 삭제가 완료되었습니다.")
            return redirect("reviews:index")
    messages.success(request, "작성자만 삭제가 가능합니다.")
    return redirect("reviews:index")


@login_required
def store_update(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    if request.user == store.user:
        if request.method == "POST":
            store_form = StoreForm(request.POST, request.FILES, instance=store)
            if store_form.is_valid():
                form = store_form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, "가게 정보 수정이 완료되었습니다.")
                return redirect("reviews:store_detail", store_pk)
        else:
            store_form = StoreForm(instance=store)
        context = {
            "store_form": store_form,
        }
        return render(request, "reviews/store.html", context)
    else:
        messages.success(request, "작성자만 수정이 가능합니다.")
        return redirect("reviews:store_detail", store_pk)


@login_required
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
    review = get_object_or_404(Review, pk=review_pk)
    store = Store.objects.get(pk=store_pk)
    context = {
        "review": review,
        "store": store,
        "comment_form": CommentForm(),
        "comments": review.comment_set.all(),
    }
    return render(request, "reviews/review_detail.html", context)


@login_required
def review_delete(request, store_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:store_detail", store_pk)
    return redirect("reviews:store_detail", store_pk)


@login_required
def review_update(request, store_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
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


@login_required
def comment_create(request, store_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect("reviews:review_detail", store_pk, review_pk)
    return redirect("reviews:review_detail", store_pk, review_pk)


@login_required
def comment_delete(request, store_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
            return redirect("reviews:review_detail", store_pk, review_pk)
    return redirect("reviews:review_detail", store_pk, review_pk)
