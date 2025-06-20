from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from superadmin.helper import renderhelper, is_ajax
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from superadmin.custom_permision import LoginRequiredMixin, AdminLoginRequiredMixin
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



# Create your views here.
class index(View):
    def get(self, request):
        context = {}
        if request.user.id:
            return redirect('superadmin:dashboard')
        else:
            return renderhelper(request, 'login', 'login', context)

    def post(self, request):
        context = {}
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
        # return HttpResponse(user)

        if user:
            login(request, user)
            return redirect('superadmin:dashboard')
        else:
            context['username'] = username
            context['password'] = password
            messages.info(request, 'Invalid Username or Password')
            return renderhelper(request, 'login', 'login', context)




class dashboard(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return renderhelper(request, 'home', 'index', context)



class registeredlist(LoginRequiredMixin,View):
    def get(self, request, id=None):
        context = {}
        conditions = Q()
        # context['previllage'] = check_previllage(request, 'Course')
        if is_ajax(request):
            page = request.GET.get('page', 1)
            context['page'] = page
            status = request.GET.get('status')
            # search = request.GET.get("search")
            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                cat = RegisteredUsers.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')
            elif type == '2':
                id = request.GET.get('id')
                RegisteredUsers.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')
            # if search:
            #     conditions &= Q(eng_title__icontains=search)
            if status:
                conditions &= Q(is_active=status)
            data_list = RegisteredUsers.objects.filter(conditions).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('superadmin/course/course-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        data = RegisteredUsers.objects.all().order_by('-id')
        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context['datas'] = page
        context['page'] = page_num

        return renderhelper(request, 'register', 'reguser-view',context)


class courselist(LoginRequiredMixin,View):
    def get(self, request, id=None):
        context = {}
        conditions = Q()
        # context['previllage'] = check_previllage(request, 'Course')
        if is_ajax(request):
            page = request.GET.get('page', 1)
            context['page'] = page
            status = request.GET.get('status')
            # search = request.GET.get("search")
            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                cat = Courses.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')
            elif type == '2':
                id = request.GET.get('id')
                Courses.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')
            # if search:
            #     conditions &= Q(eng_title__icontains=search)
            if status:
                conditions &= Q(is_active=status)
            data_list = Courses.objects.filter(conditions).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('superadmin/course/course-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        data = Courses.objects.all().order_by('-id')
        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context['datas'] = page
        context['page'] = page_num

        return renderhelper(request, 'course', 'course-view',context)

class coursecreate(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        try:
            context['data'] = Courses.objects.get(id=id)
        except:
            context['data'] = None
        context['mentors'] = User.objects.filter(user_type=2).order_by('name')
        return renderhelper(request, 'course', 'course-create', context)

    def post(self, request, id=None):
        try:
            data = Courses.objects.get(id=id)
            messages.info(request, 'Successfully Updated')
        except:
            data = Courses()
            messages.info(request, 'Successfully Added')

        course_thumbnail = request.FILES.get('course_thumbnail')
        if course_thumbnail:
            data.image=course_thumbnail

        course_chat_room_thumbnail = request.FILES.get('course_chat_room_thumbnail')
        if course_chat_room_thumbnail:
            data.chatroom=course_chat_room_thumbnail


       

        # data.type=request.POST['course_type']
        data.type=request.POST['type']
        data.title=request.POST['title']
        data.mentor_id=request.POST['mentor_id']
        data.duration=request.POST['duration']
        data.demourl=request.POST['demo_video_url']
        data.priceaed_android=request.POST['priceaed_android']
        data.pricedollar_android=request.POST['pricedollar_android']
        data.priceaed_ios=request.POST['priceaed_ios']
        data.pricedollar_ios=request.POST['pricedollar_ios']
        data.highlight1=request.POST['highlight_1']
        data.highlight2=request.POST['highlight_2']
        data.highlight3=request.POST['highlight_3']
        data.value1=request.POST['value_1']
        data.value2=request.POST['value_2']
        data.value3=request.POST['value_3']
        data.description=request.POST['course_description']

        data.offering_Identifier=request.POST['offering_Identifier']
        data.package_Identifier=request.POST['package_Identifier']
        data.entitlement_Identifier=request.POST['entitlement_Identifier']
        

        data.save()


        return redirect('superadmin:courselist')




class userslist(LoginRequiredMixin,View):
    def get(self, request, id=None):
        context = {}
        conditions = Q()
        # context['previllage'] = check_previllage(request, 'Course')
        if is_ajax(request):
            page = request.GET.get('page', 1)
            context['page'] = page
            status = request.GET.get('status')
            # search = request.GET.get("search")
            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                cat = Courses.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')
            elif type == '2':
                id = request.GET.get('id')
                Courses.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')
            # if search:
            #     conditions &= Q(eng_title__icontains=search)
            if status:
                conditions &= Q(is_active=status)
            data_list = Courses.objects.filter(conditions).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('superadmin/course/course-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        data = Courses.objects.all().order_by('-id')
        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context['datas'] = page
        context['page'] = page_num

        return renderhelper(request, 'users', 'users-view',context)


class userscreate(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        try:
            context['data'] = Courses.objects.get(id=id)
        except:
            context['data'] = None
        context['mentors'] = User.objects.filter(user_type=2).order_by('name')
        return renderhelper(request, 'users', 'users-create', context)

    def post(self, request, id=None):
        try:
            data = User.objects.get(id=id)
            messages.info(request, 'Successfully Updated')
        except:
            data = User()
            messages.info(request, 'Successfully Added')

        course_thumbnail = request.FILES.get('course_thumbnail')
        if course_thumbnail:
            data.image=course_thumbnail

        course_chat_room_thumbnail = request.FILES.get('course_chat_room_thumbnail')
        if course_chat_room_thumbnail:
            data.chatroom=course_chat_room_thumbnail


       

        # data.type=request.POST['course_type']
        data.type=request.POST['type']
        data.title=request.POST['title']
        data.mentor_id=request.POST['mentor_id']
        data.duration=request.POST['duration']
        data.demourl=request.POST['demo_video_url']
        data.priceaed_android=request.POST['priceaed_android']
        data.pricedollar_android=request.POST['pricedollar_android']
        data.priceaed_ios=request.POST['priceaed_ios']
        data.pricedollar_ios=request.POST['pricedollar_ios']
        data.highlight1=request.POST['highlight_1']
        data.highlight2=request.POST['highlight_2']
        data.highlight3=request.POST['highlight_3']
        data.value1=request.POST['value_1']
        data.value2=request.POST['value_2']
        data.value3=request.POST['value_3']
        data.description=request.POST['course_description']

        data.offering_Identifier=request.POST['offering_Identifier']
        data.package_Identifier=request.POST['package_Identifier']
        data.entitlement_Identifier=request.POST['entitlement_Identifier']
        

        data.save()


        return redirect('superadmin:userslist')

