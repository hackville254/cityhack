from django.db import models
from django.contrib.auth.models import User
from core.models import *
from django.utils.translation import gettext_lazy as _

# Modèle pour les compétences de l'utilisateur


class Competence(models.Model):
    TYPE_DOCUMENT_CHOICES = [
        ('diplome', 'Diplôme'),
        ('certification', 'Certification'),
        ('autre', 'Autre'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='competences')
    type_document = models.CharField(_('type de document'), max_length=50, choices=TYPE_DOCUMENT_CHOICES)
    nom_document = models.CharField(_('nom du document'), max_length=255)
    fichier_document = models.FileField(_('fichier du document'), upload_to='documents/', blank=True, null=True)
    lien_document = models.URLField(_('lien vers le document'), blank=True, null=True)

    def __str__(self):
        return self.nom_document

# Modèle pour les réalisations de l'utilisateur
class Realisation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='realisations')
    nom = models.CharField(_('nom de la réalisation'), max_length=255)
    description = models.TextField(_('description de la réalisation'))
    date = models.DateField(_('date'))

    def __str__(self):
        return self.nom

# Modèle pour les pièces jointes des réalisations
class PieceJointeRealisation(models.Model):
    realisation = models.ForeignKey(Realisation, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(_('fichier'), upload_to='realisations/', blank=True, null=True)
    lien = models.URLField(_('lien'), blank=True, null=True)

    def __str__(self):
        return f'Pièce jointe de {self.realisation.nom}'


class Categorie(models.Model):
    nom = models.CharField(max_length=50)
    image = models.ImageField(upload_to="categorie/")
    date_creation = models.DateTimeField(auto_now_add=True)