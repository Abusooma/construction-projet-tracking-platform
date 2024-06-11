from django.db import models
from django.utils.text import slugify

from architecture import settings

from django.utils.translation import gettext_lazy as _


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    email = models.EmailField(_('email address'))
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom}"


class Employe(models.Model):
    DOMAINE = [
        ('', ' Selectionner un domaine '),
        ('1', 'Informatique'),
        ('2', 'Architecte'),
        ('3', 'Bijoutier'),
        ('4', 'Stagiaire'),
    ]
    email = models.EmailField(_('email address'))
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    domaine = models.CharField(max_length=15, choices=DOMAINE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def get_domaine(self):
        return dict(self.DOMAINE).get(self.domaine, 'N/A')


class Projet(models.Model):
    TYPE = [
        ('', 'Sélectionner un type de projet'),
        ('1', 'A'),
        ('2', 'B'),
        ('3', 'C'),
        ('4', 'D'),
    ]

    nom = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='projets')
    constructors = models.ManyToManyField(Employe)
    description = models.TextField()
    type_projet = models.CharField(max_length=20, choices=TYPE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    @property
    def get_type_projet(self):
        return dict(self.TYPE).get(self.type_projet, 'N/A')

    def get_first_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            # Maintenant que l'ID est disponible, créer le slug et sauvegarder à nouveau
            self.slug = slugify(f"{self.nom}-{self.pk}")
            kwargs['force_insert'] = False  # Pour éviter une erreur d'insertion en double
        super().save(*args, **kwargs)


class ProjetImage(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projet_images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.projet.nom}"


class Tache(models.Model):
    STATUT_TACHE = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches')
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_TACHE, default='en_attente')

    def __str__(self):
        return self.description

    def get_statut_display(self):
        return dict(self.STATUT_TACHE).get(self.statut, 'N/A')


class Commentaire(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='commentaires')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commentaires',
                              null=True)
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Commentaire')
        verbose_name_plural = _('Commentaires')

    def __str__(self):
        return f"Commentaire de {self.owner} sur {self.projet}"
