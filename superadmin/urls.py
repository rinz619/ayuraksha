from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from superadmin import views


app_name = 'superadmin'

urlpatterns = [
    path('',views.index.as_view(),name='login'),
    
    path('dashboard', views.dashboard.as_view(), name='dashboard'),
    
    path('courselist', views.courselist.as_view(), name='courselist'),
    path('coursecreate', views.coursecreate.as_view(), name='coursecreate'),
    path('courseedit/<int:id>', views.coursecreate.as_view(), name='courseedit'),
    
    path('registeredlist', views.registeredlist.as_view(), name='registeredlist'),
    
    path('userslist', views.userslist.as_view(), name='userslist'),
    path('userscreate', views.userscreate.as_view(), name='userscreate'),

     

    
]