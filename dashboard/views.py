from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from architecture import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientProfileForm, EmployeForm, ProjetForm, ProjetImage
from .models import ClientProfile, Employe, Projet
from .utils import generate_random_password


def home(request):
    return render(request, 'dashboard/index.html')


def all_clients(request):
    clients = ClientProfile.objects.all()
    return render(request, 'dashboard/liste_clients.html', context={'clients': clients})


def addClient(request):
    if request.method == 'POST':
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            password_generate = generate_random_password()
            user = get_user_model().objects.create_user(
                email=client.email,
                nom=client.nom,
                prenom=client.prenom,
                phone_number=client.phone_number,
                address=client.address,
                password=password_generate
            )
            user.is_customer = True
            client.user = user
            client.save()

            html_message = render_to_string('email/invitation_client.html', {'user': user, 'password': password_generate})
            subject = 'Vos informations de connexion'
            send_mail(subject, None, settings.EMAIL_HOST_USER, [user.email], html_message=html_message,
                      fail_silently=True)

            messages.success(request, 'Client ajouté avec succès!')

            del password_generate
            return redirect('list-client')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé!')
            return redirect('add-client')
    else:
        form = ClientProfileForm()

    return render(request, 'dashboard/addclient.html', context={'form': form})


def updateClient(request, pk):
    client = get_object_or_404(ClientProfile, pk=pk)
    user = client.user
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            user.email = client.email
            user.nom = client.nom
            user.prenom = client.prenom
            user.phone_number = client.phone_number
            user.address = client.address
            user.save()
            client.save()
            messages.success(request, 'Client mis à jour avec succès!')
            return redirect('list-client')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé!')
    else:
        form = ClientProfileForm(instance=client)

    return render(request, 'dashboard/updateclient.html', context={'form': form, 'client': client})


def deleteClient(request, pk):
    client = get_object_or_404(ClientProfile, pk=pk)
    user = client.user
    client.delete()
    user.delete()
    messages.success(request, 'Client supprimé avec success ..!')
    return redirect('list-client')


def allEmploye(request):
    all_employs = Employe.objects.all()
    return render(request, 'dashboard/list_employ.html', context={'employes': all_employs})


def addEmploy(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employe ajouté avec success ..!')
            return redirect('list-employ')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé ..!')
            return redirect('add-employ')
    else:
        form = EmployeForm()

    return render(request, 'dashboard/addEmploye.html', context={'form': form})


def updateEmploye(request, pk):
    employ = get_object_or_404(Employe, pk=pk)
    form = EmployeForm(instance=employ)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employ)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employe mis a jour avec success ..!')
            return redirect('list-employ')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé')
            return redirect('update-employ')
    return render(request, 'dashboard/updateEmploye.html', context={'form': form})


def deleteEmploy(request, pk):
    employ = get_object_or_404(Employe, pk=pk)
    employ.delete()
    messages.success(request, 'Employé supprimé avec success ..!')
    return redirect('list-employ')


def allProjets(request):
    all_projets = Projet.objects.all()
    return render(request, 'dashboard/projetlist.html', context={'projets': all_projets})


def addProjet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES)

        if form.is_valid():
            projet = form.save()

            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')

            if image1:
                ProjetImage.objects.create(projet=projet, image=image1)
            if image2:
                ProjetImage.objects.create(projet=projet, image=image2)
            if image3:
                ProjetImage.objects.create(projet=projet, image=image3)

            projet.save()
            messages.success(request, 'Projet ajouter avec success ...!')

            return redirect('projets')
        else:
            messages.success(request, 'Quelque chose s\'est mal passé')
            return redirect('add-projet')
    else:
        form = ProjetForm()

    return render(request, 'dashboard/addprojet.html', {'form': form})


def detailProjet(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    projet_images = projet.images.all()
    return render(request, 'dashboard/projet_detail.html', context={'projet': projet, 'projet_images': projet_images})


def updateProjet(request, slug):
    projet = get_object_or_404(Projet, slug=slug)

    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES, instance=projet)

        if form.is_valid():
            projet = form.save()

            # Supprimez les images existantes pour ce projet
            ProjetImage.objects.filter(projet=projet).delete()

            # Enregistrez les nouvelles images
            for i in range(1, 4):
                image = request.FILES.get(f'image{i}')
                if image:
                    ProjetImage.objects.create(projet=projet, image=image)

            messages.success(request, 'Projet mis à jour avec succès ...!')
            return redirect('projets')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé')
    else:
        form = ProjetForm(instance=projet)

    return render(request, 'dashboard/updateprojet.html', {'form': form})
