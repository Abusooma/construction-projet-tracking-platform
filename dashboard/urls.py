from django.urls import path
from . import views

urlpatterns = [
    path('', views.allProjets, name='projets'),

    # URLS DE GESTION CLIENTS AJOUT/UPDATE/DELETE
    path('clients/', views.all_clients, name='list-client'),
    path('add_client/', views.addClient, name='add-client'),
    path('update_client/<int:pk>/', views.updateClient, name='update-client'),
    path('delete_client/<int:pk>/', views.deleteClient, name='delete-client'),

    # URLS DE GESTION DES EMPLOYES DE L'ENTREPRISE
    path('employees/', views.allEmploye, name='list-employ'),
    path('add_employ/', views.addEmploy, name='add-employ'),
    path('update_employ/<int:pk>', views.updateEmploye, name='update-employ'),
    path('delete_employ/<int:pk>', views.deleteEmploy, name='delete-employ'),

    # URLS DE GESTION DE PROJET DE L'ENTREPRISE

    path('add_projet/', views.addProjet, name='add-projet'),
    path('detail_projet/<str:slug>', views.detailProjet, name='detail-projet'),
    path('update/<str:slug>', views.updateProjet, name='update-projet'),
    path('delete_projet/<str:slug>', views.deleteProjet, name='delete-projet'),

    # Changement du statut de tache
    path('change_tache_status/', views.change_tache_status, name='change_tache_status'),

]
