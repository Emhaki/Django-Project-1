
from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('signup/', views.create, name="create"),
    path('<int:user_pk>/', views.detail, name="detail"),
] 


