from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TemoignageForm
from .models import Temoignage


def laisser_avis(request):
    if request.method == 'POST':
        # On inclut request.FILES pour gérer l'image uploadée
        form = TemoignageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            # Message de succès (Apparaîtra si vous avez le bloc messages dans votre base.html)
            messages.success(request, "Merci ! Votre avis a été envoyé et sera publié après validation.")

            # On redirige vers la même page pour vider le formulaire
            return redirect('laisser_avis')
        else:
            # En cas d'erreur, on affiche un message rouge
            messages.error(request, "Une erreur est survenue. Vérifiez les champs.")
    else:
        form = TemoignageForm()

    # Optionnel : Si vous voulez afficher d'autres éléments (ex: le chef) sur la page
    return render(request, 'experiance/avis.html', {
        'form': form
    })