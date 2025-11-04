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
    phone_number = forms.CharField(
        label=_("Teléfono *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
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

    class Media:
        js = ('js/applicants/index.js', 'js/applicants/form.js', )


class EditApplicantForm(CreateApplicantForm):
    phone_number = forms.CharField(
        label=_("Teléfono *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono'
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
    document_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=True,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Tipo de Documento', 'id': 'document_type_id'}),
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
    class Media:
        js = ('js/takers/index.js', 'js/takers/form.js', )


class EditTakerForm(CreateTakerForm):
    identification = forms.CharField(
        label=_("Identificación *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Identificación'
            }
        ),
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

