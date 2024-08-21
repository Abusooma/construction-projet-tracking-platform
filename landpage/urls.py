from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('entreprise/projets/', views.projets, name='landing-projets')
]
