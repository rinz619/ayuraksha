from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from superadmin import views


app_name = 'superadmin'

urlpatterns = [
    path('',views.index.as_view(),name='login'),
    
    path('Logout', views.Logout.as_view(), name='Logout'),
    path('profile', views.profile.as_view(), name='profile'),

    path('dashboard', views.dashboard.as_view(), name='dashboard'),
    
    path('trainerlist', views.trainerlist.as_view(), name='trainerlist'),
    path('trainercreate', views.trainercreate.as_view(), name='trainercreate'),
    path('traineredit/<int:id>', views.trainercreate.as_view(), name='traineredit'),    
    
    path('courselist', views.courselist.as_view(), name='courselist'),
    path('coursecreate', views.coursecreate.as_view(), name='coursecreate'),
    path('courseedit/<int:id>', views.coursecreate.as_view(), name='courseedit'),
    
    path('lessionlist/<int:id>', views.lessionlist.as_view(), name='lessionlist'),
    path('lessioncreate/<int:lessonid>', views.lessioncreate.as_view(), name='lessioncreate'),
    path('lessonedit/<int:lessonid>/<int:id>', views.lessioncreate.as_view(), name='lessonedit'),
    
    path('registeredlist', views.registeredlist.as_view(), name='registeredlist'),
    path('userslist', views.userslist.as_view(), name='userslist'),
    path('userscreate', views.userscreate.as_view(), name='userscreate'),
    path('usersedit/<int:id>', views.userscreate.as_view(), name='usersedit'),

     

    
]