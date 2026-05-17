from django.contrib import admin
from .models import Livre, Membre, Emprunt, Categorie

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'categorie', 'isbn', 'disponible']
    list_filter = ['disponible', 'categorie']
    search_fields = ['titre', 'auteur', 'isbn']
    list_editable = ['disponible']

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'date_adhesion']

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ['livre', 'membre', 'date_sortie', 'date_retour_prevue', 'rendu']
    list_filter = ['rendu']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom']