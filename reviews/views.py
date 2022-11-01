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
    
  }

  return render(request, 'reviews/store.html', context)

def store_detail(request, store_pk):
    store = Store.objects.get(pk=store_pk)
    context = {
        "store": store,
    }
    return render(request, "reviews/store_detail.html", context)
