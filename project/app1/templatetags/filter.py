from multiprocessing import context
from urllib import request
from django import template
from app1.models import Upisi
from errno import ESTALE
from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
#from app1.forms import EmployeeForm  
#from .models import Employee
from django.utils.decorators import method_decorator 
from django.views import View
from django.contrib.auth import login
from django.contrib.auth import logout
from django.forms import Form
from django.db.models import Count
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='upisIspis')
def upisIspis(user_id, predmet_id):
    upisi = Upisi.objects.all()
    for upis in upisi:
        if upis.predmet_id_id == predmet_id and upis.student_id_id == user_id and upis.status != 'upisan':
            return 2
        elif upis.predmet_id_id == predmet_id and upis.student_id_id == user_id:
            return 1
    return 0

@register.filter(name='upisIspis2')
def upisIspis(user_id, predmet_id):
    upisi = Upisi.objects.all()
    for upis in upisi:
        if upis.predmet_id_id == predmet_id and upis.student_id_id == user_id:
            return upis.status
    return 'nije upisan'
