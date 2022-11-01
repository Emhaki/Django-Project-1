from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [

    path("signup/", views.create, name="create"),
    path("login/", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("<int:pk>/follow", views.follow, name="follow"),
    path('signup/', views.create, name="create"),
    path('<int:user_pk>/', views.detail, name="detail"),
] 


