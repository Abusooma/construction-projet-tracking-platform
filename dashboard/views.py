from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from architecture import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientProfileForm, EmployeForm, ProjetForm, ProjetImageForm, CommentaireForm
from .models import ClientProfile, Employe, Projet, ProjetImage, Tache, Commentaire
from .utils import generate_random_password, liste_taches

# Créer le formset pour ProjetImage
ProjetImageFormSet = inlineformset_factory(
    Projet,
    ProjetImage,
    form=ProjetImageForm,
    fields=('image',),  # Inclure les champs 'id' et 'DELETE'
    extra=3,
    can_delete=True
)


@login_required
def home(request):
    return render(request, 'dashboard/index.html')


def all_clients(request):
    clients = ClientProfile.objects.all()
    return render(request, 'dashboard/liste_clients.html', context={'clients': clients})


@login_required
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

            client.user = user
            client.save()

            html_message = render_to_string('email/invitation_client.html',
                                            {'user': user, 'password': password_generate})
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


@login_required
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


@login_required
def deleteClient(request, pk):
    client = get_object_or_404(ClientProfile, pk=pk)
    user = client.user
    client.delete()
    user.delete()
    messages.success(request, 'Client supprimé avec success ..!')
    return redirect('list-client')


@login_required
def allEmploye(request):
    all_employs = Employe.objects.all()
    return render(request, 'dashboard/list_employ.html', context={'employes': all_employs})


@login_required
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


@login_required
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


@login_required
def deleteEmploy(request, pk):
    employ = get_object_or_404(Employe, pk=pk)
    employ.delete()
    messages.success(request, 'Employé supprimé avec success ..!')
    return redirect('list-employ')


@login_required
def allProjets(request):
    if request.user.is_superuser:
        all_projets = Projet.objects.all()
    else:
        # Filtre les projets par le client associé à l'utilisateur actuel
        all_projets = Projet.objects.filter(client=request.user.client_profile)

    return render(request, 'dashboard/projetlist.html', context={'projets': all_projets})


@login_required
def addProjet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST, request.FILES)
        formset = ProjetImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            projet = form.save()
            formset.instance = projet
            formset.save()
            for tache in liste_taches:
                Tache.objects.create(projet=projet, description=tache)

            messages.success(request, 'Projet ajouté avec succès ...!')
            return redirect('projets')
        else:

            messages.error(request, 'Quelque chose s\'est mal passé')
            return redirect('add-projet')
    else:
        form = ProjetForm()
        formset = ProjetImageFormSet()

    number_of_task = 0

    context = {
        'form': form, 'formset': formset,
        'number_of_task': number_of_task
    }

    return render(request, 'dashboard/addprojet.html', context=context)


@login_required
def detailProjet(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    taches = Tache.objects.filter(projet=projet)
    number_of_task = taches.count()
    projet_images = projet.images.all()
    commentaires = Commentaire.objects.filter(owner=request.user, projet=projet)

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.projet = projet
            commentaire.owner = request.user
            commentaire.save()
            messages.success(request, "Votre commentaire a été soumis avec succès. Merci pour votre retour !")
            return redirect('detail-projet', slug=slug)
        else:
            messages.error(request, 'Quelque chose s\'est mal passé ..!')
    else:
        form = CommentaireForm()

    context = {
        'projet': projet,
        'projet_images': projet_images,
        'taches': taches,
        'form': form,
        'commentaires': commentaires,
        'number_of_task': number_of_task
    }
    return render(request, 'dashboard/projet_detail.html', context=context)


@login_required
def updateProjet(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    taches = Tache.objects.filter(projet=projet)
    number_of_task = taches.count()
    ProjetImageFormSet = inlineformset_factory(
        Projet,
        ProjetImage,
        form=ProjetImageForm,
        fields=('image',),
        extra=0,  # No additional blank forms initially
        can_delete=True
    )

    if request.method == 'POST':
        form = ProjetForm(request.POST, instance=projet)
        formset = ProjetImageFormSet(request.POST, request.FILES, instance=projet)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Projet mis à jour avec succès ...!')
            return redirect('projets')
        else:
            messages.error(request, 'Quelque chose s\'est mal passé')
    else:
        form = ProjetForm(instance=projet)
        formset = ProjetImageFormSet(instance=projet)

    context = {
        'form': form, 'formset': formset,
        'number_of_task': number_of_task
    }

    return render(request, 'dashboard/updateprojet.html', context=context)


@login_required
def deleteProjet(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    projet.delete()
    messages.success(request, 'Projet supprimé avec success')
    return redirect('projets')


@require_POST  # Assure que la vue n'accepte que les requêtes POST
def change_tache_status(request):
    tache_id = request.POST.get('tache_id')
    new_status = request.POST.get('statut')

    tache = get_object_or_404(Tache, id=tache_id)
    tache.statut = new_status
    tache.save()

    return JsonResponse({'success': True, 'new_status': new_status})
