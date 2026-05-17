from django import forms
from .models import Livre, Emprunt, Membre
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'categorie', 'isbn', 'description']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['date_retour_prevue']
        widgets = {
            'date_retour_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')