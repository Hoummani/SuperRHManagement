from django.contrib import admin
#from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)
from . import views

urlpatterns = [
    #path('index_admin', views.index_admin, name="index_admin"),
    
    path('index_agent_historique', views.index_agent_historique, name="index_agent_historique"),
    path('', views.loginpage, name="loginpage"),
    path('loginpage/reset_password_profile', password_reset, name="reset_password_profile"),
    path('loginpage/reset_password_profile/done', password_reset_done, name="password_reset_done"),
    path('loginpage/reset_password_profile/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name="password_reset_confirm"),
    path('loginpage/reset_password_profile/complete', password_reset_complete, name="password_reset_complete"),
    path('logout', views.logout, name="logout"),
    path('index_agent_historique/index_agent_add_leave',views.index_agent_add_leave, name="index_agent_add_leave"),
    path('check_employe',views.check_cin, name="check_cin"),
    path('index_agent_historique/index_agent_edit_leave', views.index_agent_edit_leave, name='index_agent_edit_leave'),
    path('index_agent_historique/index_agent_supp_leave', views.delete_conge_demande, name='delete_conge_demande'),
    path('index_agent_historique/index_agent_profile', views.my_profile, name="my_profile"),
    path('index_agent_historique/index_agent_profile/changer_password', views.changer_password, name="changer_password"),
    path('index_agent_historique/index_agent_calendre_leave', views.calendre_leave, name='calendre_leave'),
    #path('index_agent_historique/index_agent_calendre_range', views.calendre_range, name='calendre_range'),
    #path('index_admin/', views.index_admin, name="index_admin"),
    #--------------------------------------------------------------------
    #               Paths SuperRH
    #       profileRH   search_conge
    #---------------------------------------------------------------------
    path('index_superRH_historique_conges', views.index_superRH_historique_conges, name="index_superRH_historique_conges"),
    path('index_superRH_historique_conges/search_conge', views.search_conge, name="search_conge"),
    path('configuration_conge', views.configurate_conge, name="configurate_conge"),
    path('configuration_conge/restart_system', views.restart_system, name="restart_system"),
    path('index_superRH_historique_conges/accepte_conge', views.accepte_conge, name="accepte_conge"),
    path('configuration_conge/add_disable_day', views.add_disable_day, name="add_disable_day"),
    path('configuration_conge/sup_disable_dy', views.supp_disable_day, name="supp_disable_day"),
    path('index_superRH_historique_conges/refuse_conge', views.refuse_conge, name="refuse_conge"),
    path('index_superRH_profile', views.profileRH, name="profileRH"),
    path('index_superRH_profile/changer_password', views.changer_password_superRH, name="changer_password_superRH"),
    path('index_superRH_hist_employes', views.index_superRH_hist_employes, name="index_superRH_hist_employes"),
    path('index_superRH_hist_employes/index_superRH_add_employes', views.index_superRH_add_employes, name="index_superRH_add_employes"),
    path('index_superRH_hist_employes/delete_employe', views.delete_employe,name="delete_employe"),
    path('index_superRH_hist_employes/search_employe', views.search_employe,name="search_employe"),
    path('index_superRH_calendar_leaves', views.index_superRH_calendar_leaves,name="index_superRH_calendar_leaves")
]
