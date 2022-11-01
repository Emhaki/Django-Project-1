from django.shortcuts import render
from .models import Store

# Create your views here.
def index(request):
    stores = Store.objects.all()
    context = {
        "stores": stores,
    }
    return render(request, "reviews/index.html", context)


def store_detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    context = {
        "store": store,
    }
    return render(request, "reviews/store_detail.html", context)
