from django.utils.translation import gettext_lazy as _
from modules.localization.models import State, City
from .models import PersonType, DocumentType
from django import forms


class CreateApplicantForm(forms.Form):
    identification = forms.CharField(
        label=_("Identificación *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Identificación'
            }
        ),
    )
    name = forms.CharField(
        label=_("Nombre *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre'
            }
        ),
    )
    email = forms.CharField(
        label=_("Email *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email'
            }
        ),
    )
    phone_number = forms.CharField(
        label=_("Teléfono"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
            }
        ),
    )
    state = forms.ModelChoiceField(
        label=_("Departamento"),
        required=False,
        queryset=State.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Departamento', 'id': 'state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Ciudad', 'id': 'city_id'}),
    )

    class Media:
        js = ('js/applicants/index.js', 'js/applicants/form.js', )


class EditApplicantForm(CreateApplicantForm):
    email = forms.CharField(
        label=_("Email *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email'
            }
        ),
    )

    class Media:
        js = ('js/applicants/index.js', 'js/applicants/form.js', )


class ApplicantFilterForm(forms.Form):
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

    class Media:
        js = ('js/applicants/index.js',  )


class CreateTakerForm(forms.Form):
    person_type = forms.ModelChoiceField(
        label=_("Tipo de Persona *"),
        required=True,
        queryset=PersonType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Tipo de Persona', 'id': 'person_type_id'}),
    )
    documento_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=True,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Tipo de Documento', 'id': 'documento_type_id'}),
    )
    identification = forms.CharField(
        label=_("Identificación *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Identificación'
            }
        ),
    )
    name = forms.CharField(
        label=_("Nombre *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre'
            }
        ),
    )
    email = forms.CharField(
        label=_("Email *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email'
            }
        ),
    )
    phone_number = forms.CharField(
        label=_("Teléfono"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
            }
        ),
    )
    contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre Contacto'
            }
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
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
        queryset=State.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Departamento', 'id': 'state_id'}),
    )
    city = forms.ModelChoiceField(
        label=_("Ciudad"),
        required=False,
        queryset=City.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Ciudad', 'id': 'city_id'}),
    )

    class Media:
        js = ('js/takers/index.js', 'js/takers/form.js', )


class TakerFilterForm(forms.Form):
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

    class Media:
        js = ('js/takers/index.js',  )

