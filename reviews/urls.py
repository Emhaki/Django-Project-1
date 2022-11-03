from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.index, name="index"),
    path("store/", views.store, name="store"),
    path("<int:store_pk>/", views.store_detail, name="store_detail"),
    path("<int:store_pk>/delete", views.store_delete, name="store_delete"),
    path("<int:store_pk>/update", views.store_update, name="store_update"),
    path("<int:store_pk>/review_create/", views.review_create, name="review_create"),
    path(
        "<int:store_pk>/<int:review_pk>/review_detail/",
        views.review_detail,
        name="review_detail",
    ),
    path(
        "<int:store_pk>/<int:review_pk>/review_delete/",
        views.review_delete,
        name="review_delete",
    ),
    path(
        "<int:store_pk>/<int:review_pk>/review_detail/review_update/",
        views.review_update,
        name="review_update",
    ),
    path("search/", views.search, name="search"),
    path(
        "<int:store_pk>/<int:review_pk>/review_detail/comment/",
        views.comment_create,
        name="comment_create",
    ),
    path(
        "<int:store_pk>/<int:review_pk>/review_detail/comment/<int:comment_pk>/comment_delete",
        views.comment_delete,
        name="comment_delete",
    ),
]
