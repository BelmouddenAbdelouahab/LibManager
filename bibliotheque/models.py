from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Livre"


class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    date_adhesion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Membre"


class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_sortie = models.DateField(auto_now_add=True)
    date_retour_prevue = models.DateField()
    date_retour_reel = models.DateField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.livre} → {self.membre}"

    class Meta:
        verbose_name = "Emprunt"