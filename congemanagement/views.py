from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import loginForm, AddLeaveForm, UpdateLeaveFormLive, UpdateLeaveForm, EditProfileForm, UserProfileForm, AddEmployeForm, EditEmployeForm, EditDisableDays, AddDisableDays, ResetAppForm
from . models import Conge, Employe, ApplicationConge,UserProfile, DisableDays
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm
#from django.contrib.auth.forms import EditProfileForm
import sweetify
from django.contrib import messages
from django.db.models import Q
from django.core import serializers
from django.core.mail import send_mail
import datetime 



##                 Fonctions en general


def show_success_save(request):
    return messages.success(request, ' les donnes sont bien enregistrees !')


def warning_exist_save(request):
    return messages.warning(request, 'Attention l\'identification de cet objet n\'existe pas dans la base de donnees !')


def show_warning_save(request):
    return messages.warning(request, 'Attention vous risquez de produire des erreur pour cet operation veuillez ressayez plus tard !')

def show_error_message(request):
    return messages.error(request, 'Erreur cet operation ne peut pas etre effectuee !') 


def clear_current_cin(current_cin):
    if current_cin is not str or current_cin.len()<4:
        return False

    return True

# Test users
def is_agent(user):
    user_prof=UserProfile.objects.get(user=user)
    if user_prof.user_type==1:
        return True
    else:
        return False

def is_superRH(user):
    user_prof=UserProfile.objects.get(user=user)
    if user_prof.user_type==2:
        return True
    else:
        return False

# -----------------------------------------------
# --------------- System authentication----------
# ------------------views------------------------

def loginpage(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                #if user.username.startswith('Yassine'):
                if is_superRH(user):
                    return redirect('index_superRH_historique_conges')
                elif is_agent(user):
                    return redirect('index_agent_historique')
                else:
                    return redirect('loginpage')
            else:
                messages.error(request, 'Erreur... le mot de passe ou le nom n\'est pas correct !')
                form = loginForm()
                context = {'form': form}

                return render(request, 'congemanagement/login.html', context)
    else:
        form = loginForm()
    return render(request, 'congemanagement/login.html', {'form': form})

def reset_password_profile(request):
    pass

    # Link send email debug server:python -m smtpd -n -c DebuggingServer localhost:1025


#@login_required
#def index_admin(request):
 #   if not request.user.username.startswith('Yassine'):
  #      return redirect('loginpage')
   # else:
    #    template2 = loader.get_template('congemanagement/index_admin.html')
     #   return HttpResponse(template2.render(request=request))

# ---------------------------- Index agent ---------------------

        
@login_required
@user_passes_test(is_agent)
def index_agent_historique(request):
    #if not request.user.username.startswith('Agent'):
    if not request.user.is_authenticated:
        return redirect('loginpage')
    else:
        apps_comgecin = ApplicationConge.app_manager.all()
        #employes=Employe.emp_manager.get(pk=apps_comgecin.employe_application_FK)
        if request.method=='POST':
            form=UpdateLeaveFormLive(request.POST)
            if form.is_valid():
                cin_edit=form.cleaned_data['cin_edit']
                date_demande_edit=form.cleaned_data['date_demande_edit']
                date_debut_edit=form.cleaned_data['date_debut_conge_edit']
                date_fin_edit=form.cleaned_data['date_fin_conge_edit']
                nbr_jours_edit=form.cleaned_data['nbr_jour_edit']
                mon_conge=Conge(date_demande=date_demande_edit, date_debut_conge=date_debut_edit, date_fin_conge=date_fin_edit, nbr_jour=nbr_jours_edit)
                if mon_conge.check_input_nbr_jour() and mon_conge.check_delai_conge():
                    if Employe.emp_manager.is_exist(cin_edit):
                        #messages.success(request,'You emp exist !')
                        if ApplicationConge.app_manager.is_exist(cin_edit):
                            emp=Employe(pk=cin_edit)
                            solde_from_db=Employe.emp_manager.get_solde_conge(cin_edit)
                            solde_from_clacul = emp.calculate_solde(date_fin_edit,date_debut_edit)
                            if emp.has_permission(solde_from_clacul,solde_from_db):
                                mon_conge_from_db=int(ApplicationConge.app_manager.get_conge_correspondant(cin_edit).id)
                                Conge.objects.filter(id=mon_conge_from_db).update(id=mon_conge_from_db,date_demande=date_demande_edit,date_debut_conge=date_debut_edit,date_fin_conge=date_fin_edit,nbr_jour=nbr_jours_edit)
                                messages.success(request,'La mis a jour applique avec succe !')
                                redirect('index_agent_historique')
                            else:
                                messages.error(request, 'Cet employe n\' a pas  le droit de passer un conge !')
                                messages.warning(request, 'Le solde correspondant a cet employe est: '+str(solde_from_db))
                            
                        else:
                            messages.error(request,'La mis a jour ne plus etre appliquee !')
                    else:
                        messages.error(request,'Aucunne enregistrement pour cet employe !')
                else:
                    messages.error(request, 'Erreur... les nombre de jours n\'est pas valide ou bien delai depassee !')





        else:
            form=UpdateLeaveFormLive()
        
        
        context={
            'apps_conge':apps_comgecin,
            'form':form
        }
        return render(request, 'congemanagement/index_agent_historique.html',context)


# --------------------------------------
#            Log out  
# -------------------------------------

@login_required
def logout(request):
    django_logout(request)
    return redirect('loginpage')


# ----------------------------------------------------------
#                    Add Leave bloc agent
# ----------------------------------------------------------

@login_required

def index_agent_add_leave(request):
    if request.method == 'POST':
        add_leave_form= AddLeaveForm(request.POST)
        if add_leave_form.is_valid():
                
            cin = add_leave_form.cleaned_data['cin']
            date_demande = add_leave_form.cleaned_data['date_demande']
            date_debut_conge = add_leave_form.cleaned_data['date_debut_conge']
            date_fin_conge = add_leave_form.cleaned_data['date_fin_conge']
            nbr_jour=add_leave_form.cleaned_data['nbr_jour']
            #date_sortie_conge = add_leave_form.cleaned_data['date_sortie_conge']
            mon_conge=Conge(date_demande=date_demande, date_debut_conge=date_debut_conge, date_fin_conge=date_fin_conge, nbr_jour=nbr_jour)
            if mon_conge.check_input_nbr_jour() and mon_conge.check_delai_conge():
                if Employe.emp_manager.is_exist(cin):
                    mon_conge=Conge(pk=mon_conge.pk,date_demande=date_demande, date_debut_conge=date_debut_conge, date_fin_conge=date_fin_conge, nbr_jour=nbr_jour)
                    emp=Employe(cin=cin)
                    mon_conge.save()
                    mon_app_conge=ApplicationConge(employe_application_FK=emp, conge_app_application_FK=mon_conge)
                    if ApplicationConge.app_manager.is_exist(cin):
                        mon_conge.delete()
                        messages.warning(request,'Attention cet employe a deja une affectation d\'un conge !')
                        redirect('index_agent_add_leave')
                    else:
                        solde_from_db = Employe.emp_manager.get_solde_conge(cin)
                        solde_from_clacul = emp.calculate_solde(date_fin_conge, date_debut_conge)
                        if emp.has_permission(solde_from_clacul, solde_from_db):
                            mon_app_conge.save()
                            show_success_save(request)
                            redirect('index_agent_historique')
                        else:
                            mon_conge.delete()
                            messages.warning(request, 'Attention cet employe n\'a pas le droit d\'affectation d\'un conge !')
                            messages.warning(request,'Le solde de conge est insuffisant il rest juste: '+str(solde_from_db))
                            redirect('index_agent_add_leave')
                else:
                    messages.error(request, 'Erreur... aucunne enregistrement pour cet identification !')
                    redirect('index_agent_add_leave')
            else:
                messages.error(request, 'Erreur... les nombre de jours n\'est pas valide ou bien delai depassee !')

        else:
            messages.error(request, 'Erreur... le formulaire n\'est pas valide !')
            redirect('index_agent_add_leave')
    else:
        add_leave_form=AddLeaveForm()
    return render(request, 'congemanagement/index_agent_add_leave.html', {'add_leave_form': add_leave_form})




def check_cin(request):
    cin=request.GET.get('cin')
    data = {
        'is_taken': Employe.emp_manager.is_exist(cin)
    }
    return JsonResponse(data)



# ----------------------------------------------------
#                   Edit Leave  bloc agent                    
# -------------------------------------------------------
@login_required

def index_agent_edit_leave(request):
    global cin_edit
    current_cin = request.GET.get('selected_cin_demande')
    if request.method == 'POST':
        edit_leave_form=UpdateLeaveForm(request.POST)
        if edit_leave_form.is_valid():
            cin_edit = current_cin
            date_demande_edit = edit_leave_form.cleaned_data['date_demande_edit']
            date_debut_conge_edit = edit_leave_form.cleaned_data['date_debut_conge_edit']
            date_fin_conge_edit = edit_leave_form.cleaned_data['date_fin_conge_edit']
            nbr_jour_edit=edit_leave_form.cleaned_data['nbr_jour_edit']
            mon_conge=Conge(date_demande=date_demande_edit, date_debut_conge=date_debut_conge_edit, date_fin_conge=date_fin_conge_edit, nbr_jour=nbr_jour_edit)
            if mon_conge.check_input_nbr_jour() and mon_conge.check_delai_conge():
                if Employe.emp_manager.is_exist(cin_edit):
                    if ApplicationConge.app_manager.is_exist(cin_edit):
                        # check solde d'employe
                        emp=Employe(pk=cin_edit)
                        solde_from_db=Employe.emp_manager.get_solde_conge(cin_edit)
                        solde_from_clacul = emp.calculate_solde(date_fin_conge_edit,date_debut_conge_edit)
                        
                        if emp.has_permission(solde_from_clacul,solde_from_db):
                            mon_conge_from_db=int(ApplicationConge.app_manager.get_conge_correspondant(cin_edit).id)
                            Conge.objects.filter(id=mon_conge_from_db).update(id=mon_conge_from_db,date_demande=date_demande_edit,date_debut_conge=date_debut_conge_edit,date_fin_conge=date_fin_conge_edit,nbr_jour=nbr_jour_edit)
                            messages.success(request,'La mis a jour applique avec succe !')
                            redirect('index_agent_historique')
                        else:
                            messages.error(request, 'Cet employe n\' a pas  le droit de passer un conge !')
                            messages.warning(request, 'Le solde correspondant a cet employe est: '+str(solde_from_db))
                            # mon_conge_from_db=int(ApplicationConge.app_manager.get_conge_correspondant(cin_edit).id)
                            # Conge.objects.filter(id=mon_conge_from_db).update(id=mon_conge_from_db,date_demande=date_demande_edit,date_sortie_conge=date_sortie_conge_edit,date_entre_conge=date_entre_conge_edit,nbr_jour=nbr_jour_edit,avis_admin='', etat_conge='', commentaire_conge='')
                            # messages.success(request,'La mis a jour applique avec succe !')
                            # messages.success(request, 'Votre solde est :!'+str(solde_from_db))
                    #  mon_conge=Conge(pk=mon_conge.pk,date_demande=date_demande_edit, date_sortie_conge=date_sortie_conge_edit, date_entre_conge=date_entre_conge_edit, nbr_jour=nbr_jour_edit, avis_admin='', etat_conge='', commentaire_conge='')
                    else:
                        messages.error(request,'Erreur la mise a jour ne peut pas effectue !')
                        redirect('index_agent_edit_leave')
                else:
                    messages.warning(request,'Attention cet employe n\'existe pas !')
                    redirect('index_agent_edit_leave')
            else:
                messages.error(request, 'Erreur... les nombre de jours n\'est pas valide ou bien delai depassee !')
        else:
            messages.error(request, 'Erreur... formulaire n\'est pas valide !')
    else:

        edit_leave_form=UpdateLeaveForm()
        # edit_leave_form.cin_edit=current_cin
    return render(request, 'congemanagement/index_agent_edit_leave.html', {'edit_leave_form': edit_leave_form,'current_cin':current_cin})





#============================================
#       Supp leave
def conge_exist(id_conge):
    mon_conge=Conge.objects.filter(id=id_conge)
    if mon_conge is not None:
        return True

    return False

@login_required
def delete_conge_demande(request):
    #current_cin=request.GET.get('cin')
    id_conge=int(request.GET.get('id_conge'))
    decision=request.GET.get('decision')
    #emp=Employe.emp_manager.get(cin=current_cin)
    #id_conge_correspondant=int(ApplicationConge.app_manager.get(employe_application_FK=emp).conge_app_application_FK.id)
    if decision=='Accepte':
        data={
            'warning_msg':'Attendez ! cet operation ne peut effectue que si la date de fin depassé !'
        }
    else:
        Conge.objects.get(id=id_conge).delete()
        data={
            'is_deleted':'Your data is deleted !'
        }
        #Conge.objects.filter(id__iexact=id_conge_correspondant).exists()
    return JsonResponse(data)


# Profile user

@login_required
def my_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        user_profile_form=UserProfileForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            #username=user_profile_form.cleaned_data['username']
            #last_name=user_profile_form.cleaned_data['last_name']
            #first_name=user_profile_form.cleaned_data['first_name']
            #email=user_profile_form.cleaned_data['email']
            #User.objects.filter(username=userprofile).update(id=userprofile.id, username=username, email=email, last_name=last_name, first_name=first_name)
            user_profile_form.save()
            messages.success(request,'La mis a jour est effectuee !')
            redirect('my_profile')
        else:
            messages.error(request, 'Erreur... Les entrees n\'est pas valide !')
    else:
        user_profile_form=UserProfileForm(instance=request.user)
    return render(request, 'congemanagement/index_agent_profile.html', {'user_profile_form':user_profile_form})






@login_required
def changer_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('my_profile')
        else:
            messages.error(request, 'Your password no match !')
            return redirect('changer_password')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request, 'congemanagement/index_agent_profile_changer_password.html', {'changer_password_form':form})





#--------------------------------------------------------------------
#                                   Work with calendar
# ------------------------------------------------------------------ 
# Calendre leave
def calendre_leave(request):
    # taken_conge=Conge.objects.get(Q(date_debut_conge__lte=date1) & Q(date_fin_conge__gte=date2))
    leaves=ApplicationConge.app_manager.all()
    return render(request,'congemanagement/calendre_leave.html',{'leaves':leaves})
# Convert date from timestomp
def convert_date(my_timestamp):

    return datetime.date.fromtimestamp(my_timestamp)

def select_range_date(date1,date2):
    try:
        take_conge=Conge.objects.get(date_fin_conge__in=[date1,date2]).order_by('id')
    except:
        take_conge={}
    return take_conge


#def calendre_range(request):
    #date1=convert_date(int(request.GET.get('date1')))
    #date2=convert_date(int(request.GET.get('date2')))
   # data = {
    #    'taken_app_conge': Conge.objects.get(date_fin_conge__in=[date1,date2])
    #}
    #if data['taken_app_conge']!={}:
    #    data['message']='Your data is avalaible !'
    #else:
     #   data['message']='Your data is not avalaible !'
    #data=serializers.serialize('json',data)
    #return JsonResponse(data)
    #return HttpResponse(data)


#-----------------------------------------------------
#                   Views of bloc Super RH
#-------------------------------------------------------

@login_required

def index_superRH_historique_conges(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')
    else:
        apps_comgecin = ApplicationConge.app_manager.all()
        #employes=Employe.emp_manager.get(pk=apps_comgecin.employe_application_FK)
        context={
            'apps_conge':apps_comgecin
        }
        return render(request, 'congemanagement/index_superRH_historique_conges.html', context)

@login_required
def search_conge(request):
    nom=request.GET.get('nom')
    emp=Employe.emp_manager.filter(nom__contains=nom).order_by('cin')
    app_conge=ApplicationConge.app_manager.filter(employe_application_FK__in=emp).all()
    #app_conge=ApplicationConge.app_manager.get(employe_application_FK=emp)
    conge=Conge.objects.filter(id=app_conge[0].conge_app_application_FK.id)
    #data=serializers.serialize('json',app_conge)
    #emp=serializers.serialize('json',emp)
    #app_conge=serializers.serialize('json',app_conge)
    #conge=serializers.serialize('json',conge)
    #data={
     #   'emp':emp,
      #  'app_conge':app_conge,
       # 'conge':conge
    #}
    data={
        'cin':emp[0].cin,
        'nom':emp[0].nom,
        'prenom':emp[0].prenom,
        'date_damande':conge[0].date_demande,
        'date_debut':conge[0].date_debut_conge,
        'date_fin':conge[0].date_fin_conge,
        'nbr_jour':conge[0].nbr_jour,
        'decision':conge[0].etat_conge
    }
    #list_data=[emp,app_conge]
    #data=serializers.serialize('json',data)
    return JsonResponse(data,safe=False)


#-----------------------
#   Calculate soustract days

def calculate_disable_day(start_date ,end_date, leave_days):
    k=0
    dates_range = [start_date + datetime.timedelta(n) for n in range(int((end_date - start_date).days))]
    for i in range(len(leave_days)):
        if leave_days[i] in dates_range:
            k=k+1

    return k




# Accepter conge

def info_day(my_date):
    now_date=datetime.date.today()
    if my_date>now_date:
        return True
    return False
@login_required

def accepte_conge(request):
    # Inf fron ajax

    id_conge=request.GET.get('id')
    current_cin=request.GET.get('cin')
    nbr_jour=int(request.GET.get('nbr_jour'))
    decision=request.GET.get('decision')
    # Inf from database

    emp_from_db=Employe.emp_manager.get(cin=current_cin)
    conge_from_db=Conge.objects.get(id=id_conge)
    etat_conge_from_db=conge_from_db.etat_conge
    solde_from_db=emp_from_db.solde_conge
    # Inf for disable day

    start_date=conge_from_db.date_debut_conge
    end_date=conge_from_db.date_fin_conge
    #leaves_days=DisableDays.objects.all()
    #soustract_days=calculate_disable_day(start_date,end_date,leaves_days.date_disable)
    count_disable_days=DisableDays.objects.exclude(date_disable__gt=end_date).filter(date_disable__gt=start_date).count()
    if etat_conge_from_db=='Accepte':
        data={
            'message_warning':'Ce conge deja accorde !'
        }
    else:
        solde_restant=solde_from_db-nbr_jour+count_disable_days
        Conge.objects.filter(id=id_conge).update(etat_conge='Accepte')
        Employe.emp_manager.filter(cin=current_cin).update(solde_conge=solde_restant)
        if info_day(end_date):
            Conge.objects.filter(id=id_conge).update(etat_conge='Depasse')
        #send_mail(
          #  'A propos de votre demande de conge',
           # 'Votre demande a etais accepte toutes l\'equipe de RH souhaitent vous ben conge pur plus de detaills contacter nous pour plus de details ! ',
           # email_emetteur,
           # [email_recepteur,],
           # fail_silently=False,
        #)
        data={
            'message_success':'Le conge est bien accorde !'
        }
    return JsonResponse(data)


# Refuser conge
@login_required

def refuse_conge(request):
    id_conge=request.GET.get('id')
    current_cin=request.GET.get('cin')
    nbr_jour=int(request.GET.get('nbr_jour'))
    decision=request.GET.get('decision')
    emp_from_db=Employe.emp_manager.get(cin=current_cin)
    conge_from_db=Conge.objects.get(id=id_conge)
    email_emetteur=User.objects.get(id=request.user.id).email
    email_recepteur=emp_from_db.email
    etat_conge_from_db=conge_from_db.etat_conge
    solde_from_db=emp_from_db.solde_conge
    if etat_conge_from_db=='Accepte':
        data={
            'message_warning':'Desole ! on ne peut pas refuser une demande deja acceptee !'
        }
    elif etat_conge_from_db=='Refuse':
        data={
            'message_warning':'Ce conge deja refuse !'
        }
    else:
        #send_mail(
         #   'A propos de votre demande de conge',
          #  'Desole, votre demande a etais refuse contacter nous pour plus de details ! ',
          #  email_emetteur,
          #  [email_recepteur,],
          #  fail_silently=False,
       # )
        Conge.objects.filter(id=id_conge).update(etat_conge='Refuse')
        #Employe.emp_manager.filter(cin=current_cin).update(solde_conge=solde_restant)
        data={
            'message_success':'Le conge est bien refuse !'
        }
    return JsonResponse(data)

#   send email
#   python -m smtpd -n -c DebuggingServer localhost:1025

@login_required

def profileRH(request):
    userprofile = UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        user_profile_form=UserProfileForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            #username=user_profile_form.cleaned_data['username']
            #last_name=user_profile_form.cleaned_data['last_name']
            #first_name=user_profile_form.cleaned_data['first_name']
            #email=user_profile_form.cleaned_data['email']
            #User.objects.filter(username=userprofile).update(id=userprofile.id, username=username, email=email, last_name=last_name, first_name=first_name)
            user_profile_form.save()
            messages.success(request,'La mis a jour est effectuee !')
            redirect('profileRH')
        else:
            messages.error(request, 'Erreur... Les entrees ne sont pas valides !')
    else:
        user_profile_form=UserProfileForm(instance=request.user)
    return render(request, 'congemanagement/index_superRH_profile.html', {'user_profile_form':user_profile_form})

@login_required
def changer_password_superRH(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profileRH')
        else:
            messages.error(request, 'Your password no match !')
            return redirect('changer_password_superRH')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request, 'congemanagement/index_superRH_profile_changer_password.html', {'changer_password_form':form})

#=========================
# Space employes
@login_required

def index_superRH_hist_employes(request):
    if request.method=='POST':
        edit_emp_form=EditEmployeForm(request.POST)
        if edit_emp_form.is_valid():

            cin_edit=edit_emp_form.cleaned_data['cin_edit']
            
            nom_edit=edit_emp_form.cleaned_data['nom_edit']
            prenom_edit=edit_emp_form.cleaned_data['prenom_edit']
            email_edit=edit_emp_form.cleaned_data['email_edit']
            tel_edit=edit_emp_form.cleaned_data['tel_edit']
            service_edit=edit_emp_form.cleaned_data['service_edit']
            emp=Employe(cin=cin_edit,nom=nom_edit,prenom=prenom_edit,email=email_edit,tel=tel_edit,service=service_edit)
            if Employe.emp_manager.is_exist(cin_edit):
                Employe.emp_manager.filter(cin=cin_edit).update(cin=cin_edit,nom=nom_edit,prenom=prenom_edit,email=email_edit,tel=tel_edit,service=service_edit)
                messages.success(request,'La mis a jour est effectuee !')
            else:
                messages.error(request, 'Erreur... cet employe n\'existe pas !')
        else:
             messages.error(request, 'Erreur... Les entrees ne sont pas valides !')
    else:
        edit_emp_form=EditEmployeForm()
    employes=Employe.emp_manager.all()
    
    context={
        'employes':employes,
        'form':edit_emp_form
    }
    return render(request,'congemanagement/index_superRH_hist_employes.html',context)

@login_required

def index_superRH_add_employes(request):
    if request.method=='POST':
        add_emp_form=AddEmployeForm(request.POST)
        if add_emp_form.is_valid():
            cin=add_emp_form.cleaned_data['cin']
            nom=add_emp_form.cleaned_data['nom']
            prenom=add_emp_form.cleaned_data['prenom']
            email=add_emp_form.cleaned_data['email']
            tel=add_emp_form.cleaned_data['tel']
            service=add_emp_form.cleaned_data['service']
            emp=Employe(cin=cin,nom=nom,prenom=prenom,email=email,tel=tel,service=service)
            if Employe.emp_manager.is_exist(cin):
                messages.warning(request,'Attention cet employe deja enregistre !')
                redirect('index_superRH_add_employes')
            else:
                emp.save()
                show_success_save(request)
                redirect('index_superRH_hist_employes')
        else:
            messages.error(request, 'Erreur... Les entrees ne sont pas valides !')
            redirect('index_superRH_add_employes')
    else:
        add_emp_form=AddEmployeForm()
    return render(request,'congemanagement/index_superRH_add_employes.html',{'add_emp_form':add_emp_form})





#=================================================
#   Delete employe
#================================================
@login_required

def delete_employe(request):
    cin=request.GET.get('cin')
    Employe.emp_manager.filter(cin=cin).delete()
    data = {
        'is_deleted': Employe.emp_manager.is_exist(cin)
    }
    return JsonResponse(data)
#===================================
#       Search employe
#==================================
@login_required
def search_employe(request):
    nom=request.GET.get('nom')
    emp=Employe.emp_manager.filter(nom__contains=nom).order_by('cin')
    data=serializers.serialize('json',emp)
    #data={
     #   'cin':emp_ser[0],
     #   'nom':emp_ser[1],
     #   'prenom':emp_ser[2],
     #   'tel':emp_ser[4],
     #   'service':emp_ser[5],
     #   'solde_conge':emp_ser[6]
    #}
    #data=serializers.serialize('json',data)
    return JsonResponse(data,safe=False)

#======================================================
#               App   Configurations
# =====================================================
@login_required

def configurate_conge(request):
    #dis_day_id=request.GET.get('id')
    #dis_day=DisableDays.objects.get(id=dis_day_id)
    disable_days_object=DisableDays.objects.all()
    if request.method=='POST':
        form_reset_app=ResetAppForm(request.POST, instance=request.user)
        form=EditDisableDays(request.POST)
        if form.is_valid():
            #form.save();
            nom=form.cleaned_data['nom']
            date_dis_day=form.cleaned_data['date_disable']
            DisableDays.objects.filter(nom=nom).update(date_disable=date_dis_day)
            messages.success(request,'La mis a jour est effectuee !')
            redirect('configurate_conge')
    else:
        form=EditDisableDays()
        form_reset_app=ResetAppForm(instance=request.user)
    return render(request,'congemanagement/index_superRH_configurations.html',{'disable_day':disable_days_object,'form':form, 'form_reset_app':form_reset_app}) 

@login_required
def restart_system(request):
    Employe.emp_manager.all().update(solde_conge=26)
    Conge.objects.all().update(etat_conge="En attente",avis_admin="En attente")
    data={
        'message':'Your application is restarted !'
    }
    return JsonResponse(data)


@login_required

def add_disable_day(request):
    if request.method=='POST':
        form=AddDisableDays(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'L\'operation effectuee avec succes !')
            redirect('configurate_conge')
        else:
            messages.error(request,'Les informations ns sont pas valides !')
            redirect('add_disable_day')
    else:
        form=AddDisableDays()
    return render(request,'congemanagement/index_superRH_configurations_add_disable_day.html',{'form':form}) 


@login_required

def supp_disable_day(request):

    nom=request.GET.get('nom')
    DisableDays.objects.filter(nom=nom).delete()
    data = {
        'is_deleted': DisableDays.objects.filter(nom__iexact=nom).exists()
    }
    return JsonResponse(data) 


#-------------------------------
#       Calendar view
@login_required

def index_superRH_calendar_leaves(request):
    leaves=ApplicationConge.app_manager.all()
    return render(request,'congemanagement/index_superRH_calendar_leaves.html',{'leaves':leaves})