from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-plan/', views.create_plan, name='create_plan'),
    path('<str:name>-profile/', views.profile, name='profile'),
]
