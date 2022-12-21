"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView
from django.contrib import admin
from app1.views import *
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('predmetiNositelj/', predmetiNositelj, name='predmetiNositelj'),
    path('home/', home, name='home'),
    path('studenti/', studenti, name='studenti'),
    path('predmeti/', predmeti, name='predmeti'),
    path('profesori/', profesori, name='profesori'),
    path('createPredmet/', createPredmet, name="createPredmet"),
    path('createStudentOrProfesor/', createStudentOrProfesor, name="createStudentOrProfesor"),
    path('<int:prof_id>/editProf', editProf, name="editProf" ),
    path('<int:student_id>/editStudent', editStudent, name="editStudent" ),
    path('<int:predmet_id>/editPredmet', editPredmet, name="editPredmet" ),
    path('<int:predmet_id>/studentiPoPredmetu', studentiPoPredmetu, name="studentiPoPredmetu" ),
    path('<int:student_id>/promjenaUpisnogLista', promjenaUpisnogLista, name="promjenaUpisnogLista" ),
    path('<int:predmet_id>/<int:student_id>/upis', upis, name="upis" ),
    path('<int:predmet_id>/<int:student_id>/promjenaStatusa', promjenaStatusa, name="promjenaStatusa" ),
    path('<int:prikaz_id>/predmetiNositelj/', predmetiNositelj, name='predmetiNositelj'),
    path('projekt/', projekt, name='projekt'),

]
