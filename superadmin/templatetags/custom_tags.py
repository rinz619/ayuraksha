from django import template
from superadmin.models import *

register = template.Library()


@register.simple_tag()
def getcontents(id):
    lead = LessionContents.objects.filter(lesson=id).order_by('id')
    return lead
    
