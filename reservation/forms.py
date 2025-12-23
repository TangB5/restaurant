from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'nom_client', 'email', 'telephone',
            'date_reservation', 'heure_reservation',
            'nb_personnes', 'note_speciale'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Définition des styles communs Tailwind pour tous les inputs
        common_classes = 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 outline-none transition-all duration-200 bg-gray-50 hover:bg-white pl-10'

        # Application des styles à chaque champ
        self.fields['nom_client'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Ex: Jean Dupont'
        })
        self.fields['email'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'jean@exemple.com'
        })
        self.fields['telephone'].widget.attrs.update({
            'class': common_classes,
            'placeholder': '6XX XX XX XX'
        })
        self.fields['nb_personnes'].widget.attrs.update({
            'class': common_classes,
            'min': 1,
            'max': 20
        })

        # Styles spécifiques pour date et heure
        self.fields['date_reservation'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': common_classes
        })
        self.fields['heure_reservation'].widget = forms.TimeInput(attrs={
            'type': 'time',
            'class': common_classes
        })

        # Style spécifique pour le textarea (notes)
        self.fields['note_speciale'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 outline-none transition-all duration-200 bg-gray-50 hover:bg-white min-h-[120px] resize-none',
            'placeholder': 'Précisez ici vos allergies, régime spécial ou occasion particulière...'
        })