""" from django.db import models
from core.models import *

# Classe Chat, pour permettre la discussion entre le client et le travailleur
class Chat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    travailleur = models.ForeignKey(Travailleur, on_delete=models.CASCADE)
    message = models.TextField()
    fichier = models.FileField(upload_to='chats/', blank=True, null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat entre {self.client.user.username} et {self.travailleur.user.username}"

# Modèle pour les posts
class Post(models.Model):
    travailleur = models.ForeignKey(Travailleur, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post de {self.travailleur.user.username} - {self.date_creation}"

# Modèle pour les likes
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True) """