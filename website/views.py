from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from website.helper import renderhelper, is_ajax
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from website.custom_permision import LoginRequiredMixin, AdminLoginRequiredMixin
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from superadmin.models import *
# from superadmin.serializer import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.db.models import Q

from django.http import JsonResponse
from django.template.loader import render_to_string, get_template

from itertools import chain
from django.core.files.base import ContentFile
from django.urls import reverse
from django.http import HttpResponseRedirect

# from superadmin.helper import renderhelper, is_ajax, sendQAPushNotification,link_callback
# from docx import Document
from datetime import datetime,timedelta
import random



class index(View):
    def get(self, request):
        context = {}
        context['course'] = Courses.objects.filter(is_active=True)
        return renderhelper(request, 'home', 'index', context)

class register(View):
    def get(self, request,slug=None):
        context = {}
        context['course'] = Courses.objects.get(slug=slug)
        return renderhelper(request, 'register', 'register', context)
    
    def post(self, request,slug=None):
        course = Courses.objects.get(slug=slug)
        data = RegisteredUsers()
        data.course = course
        data.name = request.POST.get('name')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.proffesion = request.POST.get('profession')
        image = request.FILES.get('imagefile')
        if image:
            data.image = image
        data.save()
        return redirect('website:successpage')
        
    
class successpage(View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'register', 'success-page', context)    
        
class loginuser(View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'register', 'login', context)    
    def post(self,request):
        context = {}
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        # return HttpResponse(user)

        if user:
            login(request, user)
            return redirect('website:dashboard')
        else:
            context['username'] = username
            context['password'] = password
            messages.info(request, 'Invalid Username or Password')
            return renderhelper(request, 'register', 'login', context)
        
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('website:index')   
    
class dashboard(View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'register', 'dashboard', context)    
    
class myprofile(View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'register', 'profile', context)   
         
class mycourse(View):
    def get(self, request):
        context = {}
        context['today'] = datetime.today()
        context['courses'] = UserCourses.objects.filter(user=request.user.id)
        return renderhelper(request, 'register', 'mycourse', context)   
              
class coursedetails(View):
    def get(self, request,id=None):
        context = {}
        context['course'] =course= Courses.objects.get(slug=id)
        lessons = Lessions.objects.filter(course=course.id,is_active=True).order_by('id')
        lsn = []
        for i in lessons:
            tmp = {
                'id': i.id,
                'title': i.title,
                'chapter':list(LessionContents.objects.filter(lesson=i.id,is_active=True).values('id','title','url'))
                
            }
            lsn.append(tmp)
        context['lessions'] = lsn
        context['lessionscount'] = lessons.count()
        return renderhelper(request, 'register', 'course-details', context)   
              
class coursecertificate(View):
    def get(self, request,id=None):
        context = {}
        context['course'] =course= Courses.objects.get(slug=id)
        
        return renderhelper(request, 'register', 'certificate', context)   
     
class settings(View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'register', 'settings', context)
    
    def post(self, request):
        context = {}
        request.user.name = request.POST.get('name')
        request.user.phone = request.POST.get('phone')
        request.user.profession = request.POST.get('proffession')
        image = request.FILES.get('image')
        if image:
            request.user.image = image
        request.user.save()
        return redirect('website:settings')
        