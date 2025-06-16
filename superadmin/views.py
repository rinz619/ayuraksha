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
