from django.forms import ModelForm
from .models import Korisnik, Predmeti, Upisi
from django import forms  

class CreatePredmet(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = ['name','kod','program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj']
    
    def __init__(self,*args,**kwargs):
        super (CreatePredmet,self ).__init__(*args,**kwargs)
        self.fields['nositelj'].queryset = Korisnik.objects.filter(role_id=2)

class CreateStudentOrProfesor(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ['username', 'password','first_name', 'last_name', 'status', 'role']

class CreateUpis(forms.ModelForm):
    class Meta:
        model = Upisi
        fields = ['status']
