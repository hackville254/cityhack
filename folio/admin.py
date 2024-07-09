# admin.py
from django.contrib import admin
from .models import *

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom_document', 'type_document', 'client')
    search_fields = ('nom_document', 'type_document')
    list_filter = ('type_document', 'client')
    autocomplete_fields = ['client']

@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date', 'client')
    search_fields = ('nom', 'description')
    list_filter = ('date', 'client')
    autocomplete_fields = ['client']

@admin.register(PieceJointeRealisation)
class PieceJointeRealisationAdmin(admin.ModelAdmin):
    list_display = ('realisation', 'fichier', 'lien')
    search_fields = ('realisation__nom',)
    list_filter = ('realisation',)
    autocomplete_fields = ['realisation']
