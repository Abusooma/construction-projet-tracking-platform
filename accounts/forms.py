from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser


class PhotoProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo']


class UserProfileForm(UserChangeForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Entrez votre email',
        'class': 'form-control'
    }))
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrez votre nom'
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrez votre prenom'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrez votre numero de telephone'
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Entrez votre addresse',
    }))

    class Meta:
        model = CustomUser
        fields = ['nom', 'prenom', 'email', 'phone_number', 'address']
