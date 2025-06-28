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
    
    path('myprofile',views.myprofile.as_view(),name='myprofile'),
    path('mycourse',views.mycourse.as_view(),name='mycourse'),
    path('coursedetails/<str:id>',views.coursedetails.as_view(),name='coursedetails'),
    path('coursecertificate/<str:id>',views.coursecertificate.as_view(),name='coursecertificate'),
    path('settings',views.settings.as_view(),name='settings'),
    path('Logout',views.Logout.as_view(),name='Logout'),
    
]