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
from .forms import CreatePredmet, CreateStudentOrProfesor, CreateUpis

from app1.models import Korisnik, Predmeti, Upisi

# Create your views here.
def home(request):
    current_user = request.user
    predmeti = Predmeti.objects.all()
    if current_user.role_id == 3:
        return render(request, 'homeStudent.html', {'data': predmeti, 'status':current_user.status})
    elif current_user.role_id == 2:
        return render(request, 'homeProf.html', {'data': predmeti})
    elif current_user.role_id == 1:
        return render(request, 'homeAdmin.html', {'data': predmeti}) 
    
def predmetiNositelj(request):
    current_user = request.user
    predmeti = Predmeti.objects.all()
    return render(request, 'predmetiNositelj.html', {'id': current_user.id, 'data': predmeti}) 

def createPredmet(request):
  if request.method == "POST":
    form = CreatePredmet(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)
      instance.author = request.user
      instance.save()
      return HttpResponse("<h1>Predmet uspješno dodan!</h1>")
  else: 
    form = CreatePredmet()
  return render(request, 'createPredmet.html' ,{'form':form})

def createStudentOrProfesor(request):
    if request.method == "POST":
        form = CreateStudentOrProfesor(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(instance.password)
            instance.author = request.user
            if (instance.status != 'none' and instance.role_id != 3) or (instance.status == 'none' and instance.role_id == 3):
                return HttpResponse("<h1>Korisnik nije dodan zbog neispravnosti u formi</h1>")
            else:
                instance.save()
                return HttpResponse("<h1>Korinik uspješno dodan!</h1>")
    else: 
        form = CreateStudentOrProfesor()
    return render(request, 'createStudentOrProfesor.html' ,{'form':form})

def studenti(request):
    studenti = Korisnik.objects.all()
    return render(request, 'studenti.html', {'data': studenti}) 

def profesori(request):
    profesori = Korisnik.objects.all()
    return render(request, 'profesori.html', {'data': profesori}) 

def predmeti(request):
    predmeti = Predmeti.objects.all()
    upisi = Upisi.objects.all()
    return render(request, 'predmeti.html', {'data': predmeti, 'upisi': upisi}) 

def editProf(request, prof_id):
    context ={}
    obj = get_object_or_404(Korisnik, id=prof_id)
 
    form = CreateStudentOrProfesor(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect('profesori')
 
    context["form"] = form
 
    return render(request, "editProf.html", context)  

def editStudent(request, student_id):
    context ={}
    obj = get_object_or_404(Korisnik, id=student_id)
 
    form = CreateStudentOrProfesor(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect('studenti')
 
    context["form"] = form
 
    return render(request, "editStudent.html", context)  

def editPredmet(request, predmet_id):
    context ={}
    obj = get_object_or_404(Predmeti, id=predmet_id)
 
    form = CreatePredmet(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()

        if request.user.role_id == 1:
            return redirect('predmeti')
        else:
            return redirect('predmetiNositelj')
 
    context["form"] = form
 
    return render(request, "editPredmet.html", context)  

def studentiPoPredmetu(request, predmet_id):
    pregled = request.POST.get('pregled')
    predmet = Predmeti.objects.get(id=predmet_id)
    studenti = Korisnik.objects.filter(role_id=3)
    upisi = Upisi.objects.filter(predmet_id_id = predmet_id)
    count = Upisi.objects.filter(predmet_id_id = predmet_id).count()
    if pregled:
        if pregled=="1":
            upisi = Upisi.objects.filter(predmet_id_id = predmet_id)
        elif pregled=="2":
            upisi = Upisi.objects.filter(predmet_id_id = predmet_id, status='Položio')
        elif pregled=="3":
            upisi = Upisi.objects.filter(predmet_id_id = predmet_id, status='Izgubio pravo')
        return render(request, "studentiPoPredmetu.html", {'upisi': upisi, 'studenti': studenti, 'predmet': predmet, 'count': count, 'pregled': pregled}) 
    else:
        return render(request, "studentiPoPredmetu.html", {'upisi': upisi, 'studenti': studenti, 'predmet': predmet, 'count': count}) 

def promjenaUpisnogLista(request, student_id):
    predmeti = Predmeti.objects.all()
    student = Korisnik.objects.get(id=student_id)
    return render(request, "promjenaUpisnogLista.html", {'student': student, 'data': predmeti}) 
   
def upis(request, predmet_id, student_id):
    if not Upisi.objects.filter(predmet_id_id=predmet_id, student_id_id=student_id):
        predmet = Predmeti.objects.get(id=predmet_id)
        if (request.user.status == 'izv' and (predmet.sem_izv == 7 or predmet.sem_izv == 8)):
            predmeti = Predmeti.objects.filter(sem_izv=1)
            for key in predmeti:
                if Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'upisan') or Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'Izgubio pravo'):
                    return HttpResponse("Niste polozili prvu godinu!")
            predmeti = Predmeti.objects.filter(sem_izv=2)
            for key in predmeti:
                if Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'upisan') or Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'Izgubio pravo'):
                    return HttpResponse("Niste polozili prvu godinu!")
                
            upis = Upisi(predmet_id_id=predmet_id, student_id_id=student_id, status='upisan')    
            upis.save()
        elif (request.user.status == 'red' and (predmet.sem_red == 5 or predmet.sem_red == 6)):
            predmeti = Predmeti.objects.filter(sem_red=1)
            for key in predmeti:
                if Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'upisan') or Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'Izgubio pravo'):
                    return HttpResponse("Niste polozili prvu godinu!")
            predmeti = Predmeti.objects.filter(sem_red=2)
            for key in predmeti:
                if Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'upisan') or Upisi.objects.filter(student_id_id = student_id, predmet_id_id=key.id, status = 'Izgubio pravo'):
                    return HttpResponse("Niste polozili prvu godinu!")
        else:
            upis = Upisi(predmet_id_id=predmet_id, student_id_id=student_id, status='upisan')    
            upis.save()
        


    else:
        update = Upisi.objects.get(predmet_id_id=predmet_id, student_id_id=student_id)
        update.predmet_id_id=predmet_id
        update.student_id_id=student_id
        if update.status == 'upisan':
            update.delete()
    if request.user.role_id == 1:
        return redirect('promjenaUpisnogLista', student_id)
    else:
        return redirect('predmeti')

def promjenaStatusa(request, predmet_id, student_id):
    context ={}
    obj = get_object_or_404(Upisi, predmet_id_id=predmet_id, student_id_id=student_id)
 
    form = CreateUpis(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect('studentiPoPredmetu', predmet_id)
 
    context["form"] = form
 
    return render(request, "editUpis.html", context)

def provjera(id):
    student = Korisnik.objects.get(id=id)
    return student.status

#Ovaj radi polovicno, nije mi priznala
def projekt(request):
    upisi = Upisi.objects.all()
    lista = []
    for upis in upisi:
        if provjera(upis.student_id_id) == 'red':
            if upis.predmet_id_id == 5 or upis.predmet_id_id == 6:
                if Korisnik.objects.get(id=upis.student_id_id) not in lista:
                    lista.append(Korisnik.objects.get(id=upis.student_id_id))
        elif provjera(upis.student_id_id) == 'izv':
            if upis.predmet_id_id == 7 or upis.predmet_id_id == 8:
                if Korisnik.objects.get(id=upis.student_id_id) not in lista:
                    lista.append(Korisnik.objects.get(id=upis.student_id_id))
    return render(request, "projekt.html", {'data': lista}) 
    return render(request, "projekt.html") 


