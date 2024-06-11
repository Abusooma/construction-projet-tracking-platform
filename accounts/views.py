from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserProfileForm, PhotoProfileForm
from .models import CustomUser


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Utilisateur connecté avec succès')
            return redirect('home')
        else:
            messages.error(request, 'Erreur de connexion Veuillez reessayez s\'il vous plaît ..!')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Utilisateur déconnecté avec succès ...!')
    return redirect('login')


def profile_update(request):
    form = UserProfileForm(instance=request.user)
    photo_form = PhotoProfileForm(instance=request.user)

    if request.method == 'POST':
        if request.FILES:
            photo_form = PhotoProfileForm(request.POST, request.FILES, instance=request.user)
            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, 'Votre photo de profil a été mise à jour avec succès.')
                return redirect('profile')
            else:
                messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
                return redirect('profile')
        else:
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('profile')
            else:
                messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
                return redirect('profile')

    return render(request, 'accounts/user_profile.html', {'form': form, 'photo_form': photo_form})

