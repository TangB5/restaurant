from django import forms
from .models import Temoignage


class TemoignageForm(forms.ModelForm):
    class Meta:
        model = Temoignage
        fields = ['auteur', 'titre_plat', 'note', 'texte', 'image']

        # On personnalise les widgets pour qu'ils soient jolis
        # Note : Le style CSS principal est géré dans le template HTML fourni précédemment,
        # mais ici on ajoute les placeholders.
        widgets = {
            'auteur': forms.TextInput(attrs={
                'placeholder': 'Ex: Jean Dupont',
                'class': '...'  # Les classes sont gérées dans le HTML via le CSS global
            }),
            'titre_plat': forms.TextInput(attrs={
                'placeholder': 'Ex: Poulet DG Royal'
            }),
            'texte': forms.Textarea(attrs={
                'placeholder': 'Racontez-nous votre expérience en quelques mots...',
                'rows': 4
            }),
            # Le champ note est géré par le JavaScript, on le laisse en hidden ou number
            'note': forms.NumberInput(attrs={'id': 'note_input', 'type': 'hidden'}),
        }