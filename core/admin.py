from django.contrib import admin
from .models import Client, LienExterne, Entreprise, Wallet

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'pays', 'ville', 'categorie', 'date_creation', 'date_modification')
    search_fields = ('user__username', 'pays', 'ville', 'categorie')
    list_filter = ('pays', 'ville', 'categorie', 'date_creation', 'date_modification')
    readonly_fields = ('date_creation', 'date_modification')

@admin.register(LienExterne)
class LienExterneAdmin(admin.ModelAdmin):
    list_display = ('client', 'url')
    search_fields = ('client__user__username', 'url')
    list_filter = ('client',)

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('user', 'pays', 'ville', 'secteur_activite', 'date_creation', 'date_modification')
    search_fields = ('user__username', 'pays', 'ville', 'secteur_activite')
    list_filter = ('pays', 'ville', 'secteur_activite', 'date_creation', 'date_modification')
    readonly_fields = ('date_creation', 'date_modification')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('client', 'balance', 'is_activate', 'date_creation', 'date_modification')
    search_fields = ('client',)
    list_filter = ('is_activate', 'date_creation', 'date_modification')
    readonly_fields = ('date_creation', 'date_modification')
