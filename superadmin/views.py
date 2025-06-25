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
                
            elif type == '6':
                id = request.GET.get('id')
                rdata = RegisteredUsers.objects.get(id=id)
                rdata.status = 1
                rdata.save()
                
                udata = User()
                udata.name = rdata.name
                udata.phone = rdata.phone
                udata.email = rdata.email
                udata.image = rdata.image
                udata.profession = rdata.proffesion
                udata.user_type = 4
                udata.set_password(str(1234))
                udata.save()
                
                cdata = UserCourses()
                cdata.user = udata
                cdata.course = rdata.course
                cdata.save()
                messages.info(request, 'Successfully Granted')
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


class trainerlist(LoginRequiredMixin,View):
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
                cat = Trainers.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')
            elif type == '2':
                id = request.GET.get('id')
                Trainers.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')
            # if search:
            #     conditions &= Q(eng_title__icontains=search)
            if status:
                conditions &= Q(is_active=status)
            data_list = Trainers.objects.filter(conditions).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('superadmin/trainer/trainer-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        data = Trainers.objects.all().order_by('-id')
        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context['datas'] = page
        context['page'] = page_num

        return renderhelper(request, 'trainer', 'trainer-view',context)

class trainercreate(LoginRequiredMixin, View):
    def get(self, request, id=None):
        context = {}
        try:
            context['data'] = Trainers.objects.get(id=id)
        except:
            context['data'] = None
        return renderhelper(request, 'trainer', 'trainer-create', context)

    def post(self, request, id=None):
        try:
            data = Trainers.objects.get(id=id)
            messages.info(request, 'Successfully Updated')
        except:
            data = Trainers()
            messages.info(request, 'Successfully Added')

        course_thumbnail = request.FILES.get('imagefile')
        print('image=====',course_thumbnail)
        if course_thumbnail:
            data.image=course_thumbnail

       

        data.name=request.POST.get('name')
        data.designation=request.POST.get('designation')
        data.save()


        return redirect('superadmin:trainerlist')



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
        context['trainer'] = Trainers.objects.filter(is_active=True).order_by('name')
        return renderhelper(request, 'course', 'course-create', context)

    def post(self, request, id=None):
        try:
            data = Courses.objects.get(id=id)
            messages.info(request, 'Successfully Updated')
        except:
            data = Courses()
            messages.info(request, 'Successfully Added')

        course_thumbnail = request.FILES.get('imagefile')
        if course_thumbnail:
            data.image=course_thumbnail




       

        data.title=request.POST['title']
        data.validity=request.POST['validity']
        data.startdate=request.POST['start_date']
        data.enddate=request.POST['end_date']
        data.price=request.POST['price']
        data.trainer_id=request.POST['trainer']
        data.description=request.POST['description']
       

        data.save()


        return redirect('superadmin:courselist')






class lessionlist(LoginRequiredMixin,View):
    def get(self, request, id=None):
        context = {}
        context['lessonid'] =id
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
                cat = Lessions.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')
            elif type == '2':
                id = request.GET.get('id')
                Lessions.objects.filter(id=id).delete()
                messages.info(request, 'Successfully Deleted')
            # if search:
            #     conditions &= Q(eng_title__icontains=search)
            if status:
                conditions &= Q(is_active=status)
            data_list = Lessions.objects.filter(conditions).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('superadmin/course/lesson-table.html')
            html_content = template.render(context, request)
            return JsonResponse({'status': True, 'template': html_content})

        data = Lessions.objects.filter(course=id).order_by('-id')
        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context['datas'] = page
        context['page'] = page_num

        return renderhelper(request, 'course', 'lesson-view',context)


class lessioncreate(LoginRequiredMixin, View):
    def get(self, request,lessonid=None, id=None):
        context = {}
        try:
            context['data'] = Lessions.objects.get(id=id)
            context['content'] = dt = LessionContents.objects.filter(lesson=id)
            print(dt)
        except:
            context['data'] = None
            context['content'] = None
        context['lessonid'] =lessonid
        return renderhelper(request, 'course', 'lesson-create', context)

    def post(self, request,lessonid=None, id=None):
        try:
            data = Lessions.objects.get(id=id)
            messages.info(request, 'Successfully Updated')
        except:
            data = Lessions()
            messages.info(request, 'Successfully Added')


        data.course_id=lessonid
        data.title=request.POST['title']
        data.save()
        LessionContents.objects.filter(lesson=data.id).delete()
        ctitle = request.POST.getlist('video_title')
        curl = request.POST.getlist('video_url')
        for i in range(len(ctitle)):
            sub = LessionContents()
            sub.lesson = data
            sub.title = ctitle[i]
            sub.url = curl[i]
            sub.save()

        return redirect('superadmin:lessionlist',id=lessonid)




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

        data = User.objects.filter(user_type=4).order_by('-id')
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

