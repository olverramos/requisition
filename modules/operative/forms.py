from modules.base.models import Applicant, PersonType, DocumentType
from django.utils.translation import gettext_lazy as _
from modules.localization.models import State, City
from modules.parameters.models import Ramo
from django import forms


class CreateRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.EmailField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    applicant_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput( ),
    )
    taker_person_type = forms.ModelChoiceField(
        label=_("Tipo de Persona *"),
        required=True,
        queryset=PersonType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg form-select', 
                'placeholder': 'Tipo de Persona', 
                'id': 'taker_person_type_id'
            }
        ),
    )
    taker_document_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=True,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg form-select', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Identificación',
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre',
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Teléfono Tomador',
            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Nombre Contacto',
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo *"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Ramo', 'id': 'ramo_id'}),
    )
    value = forms.IntegerField(
        label=_("Valor *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Valor'
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Observaciones',
                'rows': 4,
            }
        ),
    )

    class Media:
        js = (
            'js/requests/index.js', 
            'js/requests/form.js', 
            'js/localization.js', 
        )


class RequestFilterForm(forms.Form):
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
    applicant = forms.ModelChoiceField(
        label=_("Solicitante"),
        required=False,
        queryset=Applicant.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Solicitante', 'id': 'filter_applicant_id'}),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-control-lg form-select', 'placeholder': 'Ramo', 'id': 'filter_ramo_id'}),
    )

    class Media:
        js = ('js/requests/index.js',  )


class SearchRequestForm(forms.Form):
    applicant_email = forms.CharField(
        label=_("Email Solicitante"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ingrese el email del solicitante'
            }
        ),
    )
    class Media:
        js = ('js/requests/index.js',  )

