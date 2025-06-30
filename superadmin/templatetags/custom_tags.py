from django import template
from superadmin.models import *
from datetime import datetime, timedelta
register = template.Library()


@register.simple_tag()
def getcontents(id):
    lead = LessionContents.objects.filter(lesson=id).order_by('id')
    return lead
    


@register.simple_tag()
def lession_count(id):
    lead = Lessions.objects.filter(course=id,is_active=True).count()
    return lead
    

@register.simple_tag()
def mycoursecount(uid):
    lead = UserCourses.objects.filter(user=uid).count()
    return lead
    

@register.simple_tag()
def mycertificatecount(uid):
    lead = UserCourses.objects.filter(user=uid,course__enddate__lt=datetime.now().date()).count()
    return lead
    
