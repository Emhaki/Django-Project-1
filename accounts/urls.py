from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.create, name="create"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>/", views.detail, name="detail"),
    path("update/", views.update, name="update"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
]
