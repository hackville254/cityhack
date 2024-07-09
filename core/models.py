from django.db import models
from django.contrib.auth.models import User

# Classe Client, liée à un utilisateur via une relation OneToOne
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

# Modèle pour les liens externes de l'utilisateur
class LienExterne(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='liens_externes')
    url = models.URLField(('URL'))
    def __str__(self):
        return self.url


# Classe Entreprise, liée à un utilisateur via une relation OneToOne
class Entreprise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pays = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    secteur_activite = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Entreprise"


# Classe Wallet, pour représenter le portefeuille de l'utilisateur
class Wallet(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    is_activate = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

# Classe Transcation
class Transcation(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,related_name="transcation")
    amount = models.FloatField()
    status = models.CharField(("status : pending , failled , succes"), max_length=50)
    order_id = models.CharField(max_length=30)
    type = models.CharField(("type : retrait , depot"), max_length=50)
    operateur = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = ("Transcation")
        verbose_name_plural = ("Transcations")

    def __str__(self):
        return self.amount

# Classe justification des competances
class JustificationCompetance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE , related_name="justification_competance")
    type = models.CharField(max_length=25)
    nom_document = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='justification/' , blank=True , null=True)
    lien = models.URLField(max_length=900 , blank=True , null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Justification Competance")
        verbose_name_plural = ("Justification Competances")

    def __str__(self):
        return self.nom_document
