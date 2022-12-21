from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Uloge(models.Model):
    ROLES = (('admin', 'administrator'), ('prof', 'profesor'), ('stu', 'student'))
    role = models.CharField(max_length=50, choices=ROLES)
    
    def __str__(self):
        return '%s' % (self.role)

class Korisnik(AbstractUser):
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length=50, choices=STATUS)
    role = models.ForeignKey(Uloge, on_delete=models.CASCADE, null=True)
    

class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.IZBORNI, self.name, self.kod, self.program, self.ects, self.sem_red, self.sem_izv, self.izborni, self.nositelj)
    

class Upisi(models.Model):
    statusi = (('Upisan', 'upisan'), ('Položio', 'položio') , ('Izgubio pravo', 'izgubio pravo'))
    student_id = models.ForeignKey(Korisnik, null=True, on_delete=models.CASCADE)
    predmet_id = models.ForeignKey(Predmeti, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=statusi)

    def __str__(self):
        return '%s %s %s' % (self.student_id, self.predmet_id, self.status)

