from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website import views


app_name = 'website'

urlpatterns = [
    path('',views.index.as_view(),name='index'),
    
    path('register/<str:slug>',views.register.as_view(),name='register'),
    path('successpage',views.successpage.as_view(),name='successpage'),
    
    path('loginuser',views.loginuser.as_view(),name='loginuser'),
    path('dashboard',views.dashboard.as_view(),name='dashboard'),
    
]