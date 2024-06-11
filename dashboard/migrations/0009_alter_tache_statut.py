# Generated by Django 5.0.6 on 2024-06-03 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_remove_projetimage_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tache',
            name='statut',
            field=models.CharField(choices=[('en_attente', 'En attente'), ('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], default='en_attente', max_length=20),
        ),
    ]
