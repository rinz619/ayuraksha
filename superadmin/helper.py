# import firebase_admin
# from firebase_admin import credentials, messaging

# cred = credentials.Certificate("deutsh/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

from django.shortcuts import render
from django.shortcuts import HttpResponse
import datetime
def renderhelper(request,folder,htmlpage,context={}):
    return render(request,'superadmin/'+folder+'/'+htmlpage+'.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# def sendQAPushNotification(data, name):
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=data['title'],
#             body=data['body'],
#         ),
#         token=data['fcm'],
#     )

#     response = messaging.send(message)
#     return response
#     print('Successfully sent message:', response)

# import os
# from django.conf import settings
# from django.http import HttpResponse
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders
# from xhtml2pdf.files import pisaFileObject
# from django.core.handlers.wsgi import WSGIRequest

# def link_callback(uri, rel=None):
#     if isinstance(uri, WSGIRequest):
#         print(uri)
#         path = uri.get_full_path()
#     if uri.startswith(settings.STATIC_URL):
#         path = os.path.join(settings.STATIC_ROOT,uri.replace(settings.STATIC_URL, ""))
#     else:
#         path = uri
#     if not os.path.isfile(path):
#         raise Exception(f"Path does not exist: {path}")
#     pisaFileObject.getNamedFile = lambda self: path
#     print(path)
#     return path