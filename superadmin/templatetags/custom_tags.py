from django import template
from superadmin.models import *

register = template.Library()


@register.simple_tag()
def getcontents(id):
    lead = LessionContents.objects.filter(lesson=id).order_by('id')
    return lead
    


@register.simple_tag()
def lession_count(id):
    lead = Lessions.objects.filter(course=id,is_active=True).count()
    return lead
    
