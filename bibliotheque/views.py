from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import Livre, Emprunt, Membre, Categorie
from .forms import LivreForm, EmpruntForm, InscriptionForm

# ---- PAGE D'ACCUEIL ----
def accueil(request):
    nb_livres = Livre.objects.count()
    nb_disponibles = Livre.objects.filter(disponible=True).count()
    nb_membres = Membre.objects.count()
    nb_emprunts = Emprunt.objects.filter(rendu=False).count()
    livres_recents = Livre.objects.order_by('-date_ajout')[:6]
    context = {
        'nb_livres': nb_livres,
        'nb_disponibles': nb_disponibles,
        'nb_membres': nb_membres,
        'nb_emprunts': nb_emprunts,
        'livres_recents': livres_recents,
    }
    return render(request, 'bibliotheque/accueil.html', context)

# ---- CATALOGUE ----
def liste_livres(request):
    livres = Livre.objects.all()
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie', '')

    if query:
        livres = livres.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(isbn__icontains=query)
        )
    if categorie_id:
        livres = livres.filter(categorie_id=categorie_id)

    categories = Categorie.objects.all()
    return render(request, 'bibliotheque/livres.html', {
        'livres': livres,
        'categories': categories,
        'query': query,
        'categorie_id': categorie_id,
    })

def detail_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    return render(request, 'bibliotheque/detail_livre.html', {'livre': livre})

# ---- AJOUTER UN LIVRE (admin) ----
@login_required
def ajouter_livre(request):
    if not request.user.is_staff:
        return redirect('accueil')
    form = LivreForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Livre ajouté avec succès !")
        return redirect('liste_livres')
    return render(request, 'bibliotheque/formulaire_livre.html', {'form': form, 'titre': 'Ajouter un livre'})

# ---- MODIFIER UN LIVRE (admin) ----
@login_required
def modifier_livre(request, pk):
    if not request.user.is_staff:
        return redirect('accueil')
    livre = get_object_or_404(Livre, pk=pk)
    form = LivreForm(request.POST or None, instance=livre)
    if form.is_valid():
        form.save()
        messages.success(request, "Livre modifié !")
        return redirect('detail_livre', pk=pk)
    return render(request, 'bibliotheque/formulaire_livre.html', {'form': form, 'titre': 'Modifier le livre'})

# ---- SUPPRIMER UN LIVRE ----
@login_required
def supprimer_livre(request, pk):
    if not request.user.is_staff:
        return redirect('accueil')
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        livre.delete()
        messages.success(request, "Livre supprimé.")
        return redirect('liste_livres')
    return render(request, 'bibliotheque/confirmer_suppression.html', {'livre': livre})

# ---- EMPRUNTER UN LIVRE ----
@login_required
def emprunter_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    try:
        membre = request.user.membre
    except Membre.DoesNotExist:
        messages.error(request, "Vous devez être membre pour emprunter.")
        return redirect('detail_livre', pk=pk)

    if not livre.disponible:
        messages.error(request, "Ce livre n'est pas disponible.")
        return redirect('detail_livre', pk=pk)

    form = EmpruntForm(request.POST or None)
    if form.is_valid():
        emprunt = form.save(commit=False)
        emprunt.livre = livre
        emprunt.membre = membre
        emprunt.save()
        livre.disponible = False
        livre.save()
        messages.success(request, f"Vous avez emprunté « {livre.titre} » !")
        return redirect('mes_emprunts')
    return render(request, 'bibliotheque/emprunter.html', {'form': form, 'livre': livre})

# ---- MES EMPRUNTS ----
@login_required
def mes_emprunts(request):
    try:
        membre = request.user.membre
        emprunts = Emprunt.objects.filter(membre=membre).order_by('-date_sortie')
    except Membre.DoesNotExist:
        emprunts = []
    return render(request, 'bibliotheque/mes_emprunts.html', {'emprunts': emprunts})

# ---- RETOURNER UN LIVRE ----
@login_required
def retourner_livre(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    if request.method == 'POST':
        from django.utils import timezone
        emprunt.rendu = True
        emprunt.date_retour_reel = timezone.now().date()
        emprunt.save()
        emprunt.livre.disponible = True
        emprunt.livre.save()
        messages.success(request, "Livre retourné avec succès !")
        return redirect('mes_emprunts')
    return render(request, 'bibliotheque/retourner.html', {'emprunt': emprunt})

# ---- INSCRIPTION ----
def inscription(request):
    form = InscriptionForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Membre.objects.create(user=user)
        login(request, user)
        messages.success(request, "Bienvenue ! Votre compte a été créé.")
        return redirect('accueil')
    return render(request, 'bibliotheque/inscription.html', {'form': form})

# ---- CONNEXION / DÉCONNEXION ----
def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
        messages.error(request, "Identifiants incorrects.")
    return render(request, 'bibliotheque/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('accueil')