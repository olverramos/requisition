from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordResetForm, SetPasswordForm, PasswordChangeForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from modules.localization.models import State, City
from django.conf import settings
from .models import Genre, Role


class AccountLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg", 
                "placeholder": "Email"
            }
        )
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Contraseña"}),
    )


class AccountPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email'
    }))


class AccountSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Nueva Contraseña'
    }), label="Nueva Contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirme la Nueva Contraseña'
    }), label="Confirme la Nueva Contraseña")


class AccountPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Contraseña anterior'
    }), label="Nueva Contraseña")
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Nueva Contraseña'
    }), label="Nueva Contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirme la Nueva Contraseña'
    }), label="Confirme la Nueva Contraseña")


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label=_("Nombres"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombres'
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Apellidos"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Apellidos'
            }
        ),
    )
    username = forms.CharField(
        label=_("Usuario"),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
                'autocomplete': "off"
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label=_("Confirme la Contraseña"),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirme la Contraseña'}),
    )
    accept_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'required checkbox'}),   
    )

    class Media:
        js = ('js/registration.js',  )

    class Meta:
        fields = ('first_name', 'last_name','username', 'password1', 'password2', 'accept_conditions', )

class AccountFilterForm(forms.Form):
    search = forms.CharField(
        label=_("Buscar"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ingrese el texto para realizar la búsqueda'
            }
        ),
    )
    state = forms.ModelChoiceField(
        label=_("Departamento"),
        required=False,
        queryset=State.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select select2', 'placeholder': 'Departamento', 'id': 'filter_state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select select2', 'placeholder': 'Ciudad', 'id': 'filter_city_id'}),
    )
    role = forms.ModelChoiceField(
        label=_("Rol"),
        required=False,
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg form-select', 
                'placeholder': 'Rol', 
                'id': 'filter_role_id'
            }
        ),
    )
    is_active = forms.BooleanField(
        label=_("Es Activo"),
        required=False,
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control form-control-lg form-select', 
                'id': 'filter_is_active_id'
            }
        )
    )

    class Media:
        js = ('js/localization.js', 'js/account_index.js',  )

    class Meta:
        fields = ('state', 'city', )


class AdminSetPasswordForm(forms.Form):
    account = forms.CharField(widget=forms.HiddenInput(attrs={ "id": "account_id" }))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Nueva Contraseña'
    }), label="Nueva Contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirme la Nueva Contraseña'
    }), label="Confirme la Nueva Contraseña")


class CreateAccountForm(forms.Form):
    username = forms.CharField(
        label=_("Usuario *"),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
                'autocomplete': 'off'
            }
        ),
    )
    role = forms.ModelChoiceField(
        label=_("Rol"),
        required=False,
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Rol', 'id': 'role_id'}),
    )
    first_name = forms.CharField(
        label=_("Nombres *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombres'
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Apellidos *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Apellidos'
            }
        ),
    )
    genre = forms.ModelChoiceField(
        label=_("Género"),
        required=False,
        queryset=Genre.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Género', 'id': 'genre_id'}),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
            }
        ),
    )
    whatsapp = forms.CharField(
        label=_("Whatsapp"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Whatsapp'
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Dirección'
            }
        ),
    )
    state = forms.ModelChoiceField(
        label=_("Departamento"),
        required=False,
        queryset=State.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Departamento', 'id': 'state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ciudad', 'id': 'city_id'}),
    )


    class Media:
        js = ('js/localization.js', 'js/account_form.js', )


class EditAccountForm(forms.Form):
    username = forms.CharField(
        label=_("Usuario"),
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
                'autocomplete': "off"
            }
        ),
    )
    role = forms.ModelChoiceField(
        label=_("Rol *"),
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Rol', 'id': 'role_id'}),
    )
    first_name = forms.CharField(
        label=_("Nombres *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombres'
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Apellidos *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Apellidos'
            }
        ),
    )
    genre = forms.ModelChoiceField(
        label=_("Género"),
        required=False,
        queryset=Genre.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Género', 'id': 'genre_id'}),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
            }
        ),
    )
    whatsapp = forms.CharField(
        label=_("Whatsapp"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Whatsapp'
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Dirección'
            }
        ),
    )
    state = forms.ModelChoiceField(
        label=_("Departamento"),
        required=False,
        queryset=State.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Departamento', 'id': 'state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ciudad', 'id': 'city_id'}),
    )

    class Media:
        js = ('js/localization.js', 'js/account_form.js', )


class ProfileForm(forms.Form):
    username = forms.CharField(
        label=_("Usuario"),
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
                'readonly': 'readonly',
            }
        ),
    )
    role = forms.ModelChoiceField(
        label=_("Rol"),
        required=False,
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg form-select', 
                'placeholder': 'Rol', 
                'id': 'role_id',
                'disabled': 'disabled',
            }
        ),
    )
    first_name = forms.CharField(
        label=_("Nombres *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombres'
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Apellidos *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Apellidos'
            }
        ),
    )
    genre = forms.ModelChoiceField(
        label=_("Género"),
        required=False,
        queryset=Genre.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Género', 'id': 'genre_id'}),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
            }
        ),
    )
    whatsapp = forms.CharField(
        label=_("Whatsapp"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Whatsapp'
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Dirección'
            }
        ),
    )
    state = forms.ModelChoiceField(
        label=_("Departamento"),
        required=False,
        queryset=State.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select select2', 'placeholder': 'Departamento', 'id': 'state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.filter(country=settings.COUNTRY),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select select2', 'placeholder': 'Ciudad', 'id': 'city_id'}),
    )

    class Media:
        js = ('js/localization.js', 'js/profile_form.js', )
