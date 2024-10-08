from django import forms
from django.forms import HiddenInput
from .models import ClientProfile, Employe, Projet, ProjetImage, Commentaire
from django.forms import ClearableFileInput


class ClientProfileForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nom',
        'class': 'form-control'
    }))
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Prenom',
        'class': 'form-control'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Telephone',
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Adresse',
        'class': 'form-control'
    }))

    class Meta:
        model = ClientProfile
        fields = ['email', 'nom', 'prenom', 'phone_number', 'address']


class EmployeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))

    nom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nom',
        'class': 'form-control'
    }))

    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Prenom',
        'class': 'form-control'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Numero de Telephone',
        'class': 'form-control'
    }))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Adresse',
        'class': 'form-control'
    }))

    class Meta:
        model = Employe
        fields = ['email', 'nom', 'prenom', 'phone_number', 'domaine', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['domaine'] = forms.ChoiceField(
            choices=Employe.DOMAINE,
            widget=forms.Select(attrs={'class': 'form-control'})
        )


class ProjetForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom du projet',
            'class': 'form-control'
        })
    )
    client = forms.ModelChoiceField(
        queryset=ClientProfile.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    constructors = forms.ModelMultipleChoiceField(
        queryset=Employe.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Description du projet',
            'class': 'form-control',
            'rows': 5
        })
    )
    type_projet = forms.ChoiceField(
        choices=Projet.TYPE,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Projet
        fields = ['nom', 'client', 'constructors', 'description', 'type_projet']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].empty_label = "Sélectionner un client"


class ProjetImageForm(forms.ModelForm):
    class Meta:
        model = ProjetImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProjetImageForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].widget = forms.FileInput(attrs={'class': 'custom-file-input'})


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['commentaire']
        widgets = {
            'commentaire': forms.Textarea(
                attrs={'class': 'form-control comment-textarea', 'rows': 4, 'placeholder': 'Votre commentaire ici...'}),
        }
