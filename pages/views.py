from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from menu.models import Plat
from .models import HorairesOuverture, Temoignage
from .forms import UserLoginForm, UserRegisterForm


def home(request):
    """
    Vue de la page d'accueil.
    Charge les plats spéciaux, les horaires et les témoignages.
    """
    try:
        # On récupère les plats spéciaux, ou les 3 premiers si aucun n'est marqué spécial
        plats_speciaux = Plat.objects.filter(is_special=True, disponible=True)[:3]
        if not plats_speciaux:
            plats_speciaux = Plat.objects.filter(disponible=True)[:3]
    except Exception:
        plats_speciaux = []

    horaires = HorairesOuverture.objects.all().order_by('id')
    temoignages = Temoignage.objects.filter(visible=True).order_by('-date_ajout')[:2]

    context = {
        'plats_speciaux': plats_speciaux,
        'horaires': horaires,
        'temoignages': temoignages,
    }

    return render(request, 'index.html', context)


def login_user(request):
    """
    Gère la connexion des utilisateurs.
    """
    # Si l'utilisateur est déjà connecté, on le redirige vers l'accueil
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Message de succès (barre verte)
                messages.success(request, f"Ravi de vous revoir, {username} !")

                # Redirection : on vérifie s'il y a un paramètre 'next' (ex: après avoir cliqué sur 'réserver')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                # Sinon redirection par défaut (Mettez le nom de votre URL, ex: 'menu:commande')
                return redirect('home')
            else:
                # Message d'erreur (barre rouge) - Identifiants incorrects
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    else:
        login_form = UserLoginForm()

    context = {
        'login_form': login_form,
    }

    return render(request, 'login.html', context)


def register_user(request):
    """
    Gère l'inscription des nouveaux utilisateurs.
    """
    # Si l'utilisateur est déjà connecté, on le redirige
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            # Sauvegarde l'utilisateur dans la base de données
            register_form.save()

            username = register_form.cleaned_data.get('username')
            messages.success(request, f"Compte créé avec succès pour {username} ! Veuillez vous connecter.")

            # Redirige vers la page de connexion après inscription réussie
            return redirect('login')
        else:
            # Si le formulaire n'est pas valide (ex: mots de passe différents), Django génère les erreurs
            # mais on ajoute un message global pour l'UX
            messages.error(request, "Une erreur est survenue lors de l'inscription. Vérifiez les champs ci-dessous.")
    else:
        register_form = UserRegisterForm()

    context = {
        'register_form': register_form,
    }

    return render(request, 'register.html', context)


def logout_user(request):
    """
    Déconnecte l'utilisateur et redirige vers l'accueil.
    """
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')