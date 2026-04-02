
from django.contrib import admin
from django.urls import path
from fines import views

urlpatterns = [
    path('fines', views.fines_handler),
    path('fines/<int:id>', views.get_fine),
    path('fines/user/<int:user_id>', views.get_user_fines),
    path('fines/<int:id>/pay', views.pay_fine),
]
