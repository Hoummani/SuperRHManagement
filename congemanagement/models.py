from django.db import models
from django.db.models import Q
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import datetime

# from CustomFileField import CustomFileField

# Create your models here.
from django.urls import reverse

USER_TYPES = (
    (0, ''),
    (1, 'Agent standard'),
    (2, 'Responsable RH'),
    (4, 'President'),
)



# Model to represent different types of users
class UserProfile(models.Model):
    # user_manage_conge = models.ManyToManyField(Conge, through='ManageConge')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPES)
    #nom=models.CharField(null=true, max_length=50)
    #prenom=models.CharField(null=True, max_length=50)
    #email=models.EmailField(null=True, max_length=254)
    objects = UserManager()

    def __str__(self):
        return str(self.user)


class EmployeManager(models.Manager):

    # returner solde de l'employe
    def get_solde_conge(self, cin):
        new_solde = super().get(pk=cin).solde_conge
        return new_solde

    # Tester l'existence de l'employe
    def is_exist(self, cin):
        result = False
        try:
            emp = super().get(pk=cin)
            result = True
        except:
            result = False

        return result

    def get_absolute_url(self):
        pass


class Employe(models.Model):
    user_manage_employe = models.ForeignKey('UserProfile',null=True, on_delete=models.CASCADE)
    cin = models.CharField(max_length=50, unique=True, primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=50)
    service = models.CharField(max_length=250)

    solde_conge = models.IntegerField(default=26)
    # declarer le manager de la class Employe
    emp_manager = EmployeManager()

    def __str__(self):
        return self.nom + ' ' + self.prenom

    # calculer solde 
    def calculate_solde(self, date_fin, date_debut):
        return int((date_fin - date_debut).days)

    # tester si l'employe a le droit d'avoir un conge
    def has_permission(sel, solde_from_calcul, solde_from_db):
        solde_restant = solde_from_db - solde_from_calcul
        if solde_from_db < 1 or solde_restant <= 0:
            return False
        return True

    # get_url_object
    def get_absolute_url(self):
        return reverse('employe-detail', kwargs={'cin': self.cin})


class Conge(models.Model):
    user_manager = models.ManyToManyField(UserProfile, through='ManageConge')
    emp_has_conge = models.ManyToManyField(Employe, through='ApplicationConge')
    date_demande = models.DateField()
    date_debut_conge = models.DateField()
    date_fin_conge = models.DateField()
    nbr_jour = models.IntegerField(default=0)
    avis_admin = models.CharField(max_length=250, default='En attente')
    etat_conge = models.CharField(max_length=100, default='En attente')
    commentaire_conge = models.CharField(max_length=250, default='Pas encore')
    

    # Check all the input
    def check_input_nbr_jour(self):
        calcul_nbr_jour = int((self.date_fin_conge - self.date_debut_conge).days)
        if calcul_nbr_jour >= self.nbr_jour:
            return True
        return False

    # check delai conge
    def check_delai_conge(self):
        if self.date_demande > self.date_debut_conge:
            return False
        return True

    # get_url_object
    def get_absolute_url(self):
        return reverse('conge-detail', kwargs={'pk': self.pk})


class ApplicatonCongeManager(models.Manager):

    def is_exist(self, emp_fk):
        result = False
        try:
            mon_app_conge = super().get(employe_application_FK=emp_fk)
            result = True
        except:
            result = False
        return result

    def get_conge_correspondant(self, cin_edit):
        return super().get(employe_application_FK=cin_edit).conge_app_application_FK


class ApplicationConge(models.Model):
    employe_application_FK = models.ForeignKey('Employe', on_delete=models.CASCADE)
    conge_app_application_FK = models.ForeignKey('Conge', on_delete=models.CASCADE)

    app_manager = ApplicatonCongeManager()


class ManageConge(models.Model):
    manager_conge_FK = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    conge_manage_FK = models.ForeignKey('Conge', on_delete=models.CASCADE)


class DisableDays(models.Model):
    nom=models.CharField(max_length=250, null=True)
    date_disable=models.DateField()

    def __str__(self):
        return self.nom

class RangeDisableDays(models.Model):
    nom=models.CharField(max_length=250)
    date_begin=models.DateField()
    date_out=models.DateField()
    nbr_days=models.IntegerField(default=0)


#class ManageEmploye(models.Model):
    #user_profile_FK = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    #employe_FK = models.ForeignKey('Employe', on_delete=models.CASCADE)
