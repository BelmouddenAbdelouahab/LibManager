from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('livres/', views.liste_livres, name='liste_livres'),
    path('livres/<int:pk>/', views.detail_livre, name='detail_livre'),
    path('livres/ajouter/', views.ajouter_livre, name='ajouter_livre'),
    path('livres/<int:pk>/modifier/', views.modifier_livre, name='modifier_livre'),
    path('livres/<int:pk>/supprimer/', views.supprimer_livre, name='supprimer_livre'),
    path('livres/<int:pk>/emprunter/', views.emprunter_livre, name='emprunter_livre'),
    path('livres/<int:pk>/retourner/', views.retourner_livre, name='retourner_livre'),
    path('mes-emprunts/', views.mes_emprunts, name='mes_emprunts'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]