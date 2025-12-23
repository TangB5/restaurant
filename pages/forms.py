from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# --- FORMULAIRE DE CONNEXION ---
class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: jean.dupont',
            'autocomplete': 'username',
            # Les classes CSS sont gérées dans le template HTML via <style>
            # pour éviter d'avoir du code "spaghetti" ici.
        }),
        error_messages={'required': 'Veuillez entrer votre nom d\'utilisateur.'}
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'current-password'
        }),
        error_messages={'required': 'Veuillez entrer votre mot de passe.'}
    )


# --- FORMULAIRE D'INSCRIPTION ---
class UserRegisterForm(UserCreationForm):
    # On ajoute le champ email qui n'est pas présent par défaut dans UserCreationForm
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'jean.dupont@exemple.com',
            'autocomplete': 'email'
        }),
        label="Adresse Email",
        error_messages={'required': 'Une adresse email est nécessaire.'}
    )

    class Meta:
        model = User
        # L'ordre ici détermine l'ordre d'affichage si on utilisait {{ form.as_p }}
        # Mais comme on fait le rendu manuel dans le HTML, c'est surtout pour la validation.
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation des widgets pour correspondre à notre Design UI/UX

        # 1. Username
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choisissez un nom d\'utilisateur',
            'autocomplete': 'username'
        })

        # 2. Password 1 (Mot de passe principal)
        # Note: UserCreationForm nomme automatiquement ce champ 'password1'
        self.fields['password1'].widget.attrs.update({
            'placeholder': '8 caractères minimum',
            'autocomplete': 'new-password'
        })
        self.fields[
            'password1'].help_text = None  # On retire le texte d'aide par défaut de Django pour mettre le nôtre dans le HTML

        # 3. Password 2 (Confirmation)
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Répétez le mot de passe',
            'autocomplete': 'new-password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email