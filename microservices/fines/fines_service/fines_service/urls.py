
from django.contrib import admin
from django.urls import path
from fines import views

urlpatterns = [
    path('fines/', views.create_fine, name='create_fine'),
    path('fines/user/<int:user_id>/', views.get_user_fines, name='get_user_fines'),
    path('fines/<int:id>/pay/', views.pay_fine, name='pay_fine'),
]
