from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:store_pk>", views.store_detail, name="store_detail"),
    path("store/", views.store, name="store"),
    path("<int:store_pk>/", views.store_detail, name="store_detail"),
    path("<int:store_pk>/review_create/", views.review_create, name="review_create"),
    path("<int:review_pk>/review/", views.review_detail, name="review_detail"),
]
