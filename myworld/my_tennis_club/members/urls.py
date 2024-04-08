from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [

    path('members/', views.members, name='members'),
    path('members/details/<int:id>',views.details,name='details'),
    path('testing/',views.testing,name='testing'),
]