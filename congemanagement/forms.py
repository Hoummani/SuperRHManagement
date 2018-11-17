from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from congemanagement.models import UserProfile,Employe, DisableDays


class loginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'username'}))
    # password = forms.CharField(widget=forms.PasswordInput, widget=forms.TextInput(attrs={'placeholder': 'password'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'password', 'type': 'password'}))

class AddLeaveForm(forms.Form):
    cin=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'CIN', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'cin'}))
    date_demande=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    date_debut_conge=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    date_fin_conge=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    nbr_jour=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Entrer le nombre de jours planifiees', 'type': 'number', 'class': 'form-control','id':'nbr-jour'}))

class UpdateLeaveForm(forms.Form):
    #cin_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'CIN', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4'}))
    date_demande_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    date_debut_conge_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    date_fin_conge_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd'}))
    nbr_jour_edit=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Entrer le nombre de jours planifiees', 'type': 'number', 'class': 'form-control','id':'nbr-jour'}))

class UpdateLeaveFormLive(forms.Form):
    cin_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'CIN', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'cin_edit'}))
    date_demande_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd','id':'date_demande_edit'}))
    date_debut_conge_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd','id':'date_debut_edit'}))
    date_fin_conge_edit=forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd','id':'date_fin_edit'}))
    nbr_jour_edit=forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Entrer le nombre de jours planifiees', 'type': 'number', 'class': 'form-control','id':'nbr-jour','id':'nbr_jours_edit'}))




class UserProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = {'username','last_name','first_name','email','password'}

class EditProfileForm(forms.Form):
    username=forms.CharField( max_length=250, required=True,widget=forms.TextInput(attrs={'placeholder': 'Username', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4'}))
    last_name=forms.CharField( max_length=250, required=True,widget=forms.TextInput(attrs={'placeholder': 'Nom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4'}))
    first_name=forms.CharField( max_length=250, required=True,widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4'}))
    email=forms.EmailField( max_length=250, required=True,widget=forms.EmailInput(attrs={'placeholder': 'Email', 'type': 'email', 'class': 'form-control','data-validation':'email'}))

    def get_object(self, queryset=None):
        '''This loads the profile of the currently logged in user'''

        return UserProfile.objects.get(user=self.request.user)

#=================================================================
#                   SuperRH Forms
#==================================================================
class AddEmployeForm(forms.Form):
    cin=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'CIN', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'cin'}))
    nom=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'nom'}))
    prenom=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'prenom'}))
    email=forms.EmailField( max_length=250, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'type': 'email', 'class': 'form-control','data-validation':'email','id':'email'}))
    tel=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Tel', 'type': 'tel', 'class': 'form-control','id':'tel'}))
    service=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Service', 'type': 'text', 'class': 'form-control','id':'service'}))
    
class EditEmployeForm(forms.Form):
    cin_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'CIN', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'cin_edit'}))
    nom_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'nom_edit'}))
    prenom_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prenom', 'type': 'text', 'class': 'form-control','data-validation':'length alphanumeric','data-validation-length':'min4','id':'prenom_dit'}))
    email_edit=forms.EmailField( max_length=250, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'type': 'email', 'class': 'form-control','data-validation':'email','id':'email_edit'}))
    tel_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Tel', 'type': 'tel', 'class': 'form-control','id':'tel_edit','data-validation':'length alphanumeric','data-validation-length':'min9'}))
    service_edit=forms.CharField( max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'Service', 'type': 'text', 'class': 'form-control','id':'service_edit'}))
    #class Meta:
    #    model=Employe
    #    fields=['cin','nom','prenom','email','tel','service']

class EditDisableDays(forms.ModelForm):

    class Meta:
        model=DisableDays
        fields=['nom','date_disable']
        widgets = {
            'nom':forms.TextInput(attrs={'placeholder': 'Nom', 'type': 'text', 'class': 'form-control','data-validation':'length','data-validation-length':'min4','id':'nom_disable_day'}),
            'date_disable':forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd','id':'date_dis_day'})
        }

class AddDisableDays(forms.ModelForm):

    class Meta:
        model=DisableDays
        fields=['nom','date_disable']
        widgets = {
            'nom':forms.TextInput(attrs={'placeholder': 'Nom', 'type': 'text', 'class': 'form-control','data-validation':'length','data-validation-length':'min4','id':'nom_disable_day'}),
            'date_disable':forms.DateInput(attrs={'placeholder': 'YY-MM-DD', 'class': 'form-control','data-validation':'date','data-validation-format':'yyyy-mm-dd','id':'date_dis_day'})
        }
class ResetAppForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['password']
        widgets = {
            'password':forms.TextInput(attrs={'type': 'password', 'class': 'form-control','data-validation':'length','data-validation-length':'min8','id':'reset_app_password'})
        }
