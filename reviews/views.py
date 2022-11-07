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


# Create your views here.


@require_safe
def index(request):
    stores = Store.objects.order_by("-pk")
    paginator = Paginator(stores, 4)  # Show 25 contacts per page.
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
        reviews = store.review_set.filter(grade=5)
    elif request.POST.get("grade-4"):
        reviews = store.review_set.filter(grade=4)
    elif request.POST.get("grade-3"):
        reviews = store.review_set.filter(grade=3)
    elif request.POST.get("grade-2"):
        reviews = store.review_set.filter(grade=2)
    elif request.POST.get("grade-1"):
        reviews = store.review_set.filter(grade=1)
    elif request.POST.get("reset"):
        reviews = store.review_set.order_by("-pk")

    review_5 = store.review_set.filter(grade=5).count()
    review_4 = store.review_set.filter(grade=4).count()
    review_3 = store.review_set.filter(grade=3).count()
    review_2 = store.review_set.filter(grade=2).count()
    review_1 = store.review_set.filter(grade=1).count()

    review_ave = 0

    if review_ave == 0:
        review_ave = "평가 없음"

    if reviews_.count() > 0:
        ave = store.review_set.aggregate(Avg("grade"))

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
    store.hits += 1
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
        store_name = search.filter(store_name__icontains=q)
        address = search.filter(address__icontains=q)
        menu = search.filter(menu__icontains=q)
        price = search.filter(price__icontains=q)
        context = {
            "store_name": store_name,
            "address": address,
            "menu": menu,
            "price": price,
            "q": q,
        }
        return render(request, "reviews/search.html", context)
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


def mz_gangnam(request):
    stores = Store.objects.filter(address__icontains="강남구")
    paginator = Paginator(stores, 7)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
    }
    return render(request, "reviews/index_gangnam.html", context)


@require_safe
def local_list(request):
    return render(request, "reviews/local_list.html")


def local_detail_gn(request):
    stores = Store.objects.filter(address__icontains="강남구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "강남구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_sc(request):
    stores = Store.objects.filter(address__icontains="서초구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "서초구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_ys(request):
    stores = Store.objects.filter(address__icontains="용산구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "용산구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_sd(request):
    stores = Store.objects.filter(address__icontains="성동구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "성동구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_no(request):
    stores = Store.objects.filter(address__icontains="노원구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "노원구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_dj(request):
    stores = Store.objects.filter(address__icontains="동작구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "동작구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_sp(request):
    stores = Store.objects.filter(address__icontains="송파구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "송파구",
    }
    return render(request, "reviews/local_detail.html", context)


def local_detail_jn(request):
    stores = Store.objects.filter(address__icontains="중랑구")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "local": "중랑구",
    }
    return render(request, "reviews/local_detail.html", context)


@require_safe
def price_list(request):
    return render(request, "reviews/price_list.html")


def price_detail_1man(request):
    stores = Store.objects.filter(price__icontains="만원 미만")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "price": "만원 미만",
    }
    return render(request, "reviews/price_detail.html", context)


def price_detail_2man(request):
    stores = Store.objects.filter(price__icontains="만원-2만원")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "price": "만원-2만원",
    }
    return render(request, "reviews/price_detail.html", context)


def price_detail_3man(request):
    stores = Store.objects.filter(price__icontains="2만원-3만원")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "price": "2만원-3만원",
    }
    return render(request, "reviews/price_detail.html", context)


def price_detail_4man(request):
    stores = Store.objects.filter(price__icontains="3만원-4만원")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "price": "3만원-4만원",
    }
    return render(request, "reviews/price_detail.html", context)


def price_detail_4manup(request):
    stores = Store.objects.filter(price__icontains="4만원 이상")
    paginator = Paginator(stores, 5)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "stores": stores,
        "page_obj": page_obj,
        "price": "4만원 이상",
    }
    return render(request, "reviews/price_detail.html", context)
