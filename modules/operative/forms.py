from modules.base.models import Applicant, PersonType, DocumentType
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import gettext_lazy as _
from modules.operative.models import RequestStatus
from modules.authentication.models import Account
from modules.parameters.models import Ramo
from django import forms


class CreateRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
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
                'class': 'form-control form-select', 
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
                'class': 'form-control form-select', 
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
                'class': 'form-control',
                'placeholder': 'Identificación',
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre Contacto',
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo *"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control form-select', 'placeholder': 'Ramo', 'id': 'ramo_id'}),
    )
    value = forms.CharField(
        label=_("Valor *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor'
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': 4,
            }
        ),
    )

    class Media:
        js = (
            'js/requests/create.js', 
        )


class EditRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    status = forms.ModelChoiceField(
        label=_("Estado *"),
        required=False,
        queryset=RequestStatus.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'status_id',
                'readonly': True
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo *"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'ramo_id'
            }
        ),
    )
    taker_person_type = forms.ModelChoiceField(
        label=_("Tipo de Persona *"),
        required=False,
        queryset=PersonType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Persona', 
                'id': 'taker_person_type_id'
            }
        ),
    )
    taker_document_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=False,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Identificación',
                'readonly': True
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre Contacto',
            }
        ),
    )
    value = forms.CharField(
        label=_("Valor *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor'
            }
        ),
    )
    assigned_to = forms.ModelChoiceField(
        label=_("Asignado a:"),
        required=False,
        queryset=Account.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'assigned_to_id'
            }
        ),
    )
    created_at = forms.CharField(
        label=_("Fecha Creación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    validated_at = forms.CharField(
        label=_("Fecha Validación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    validated_by = forms.CharField(
        label=_("Validado por"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': 4,
            }
        ),
    )

    class Media:
        js = (
            'js/requests/form.js', 
            'js/requests/index.js', 
            'js/localization.js', 
        )


class EditRequestFilesForm(forms.Form):
    request_receipt = forms.FileField(
        label=_("Recibo de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Recibo de Pago',
                'autocomplete': 'off'
            }
        ),
    )
    request_police = forms.FileField(
        label=_("Póliza"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )
    request_rc_police = forms.FileField(
        label=_("Póliza RC"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )
    payment_receipt = forms.FileField(
        label=_("Comprobante de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )

    class Media:
        js = (
            'js/requests/form.js', 
            'js/requests/index.js', 
            'js/localization.js', 
        )


class QueryRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    status = forms.CharField(
        label=_("Estado *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'id': 'status_id',
                'readonly': True
            }
        ),
    )
    ramo = forms.CharField(
        label=_("Ramo"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly', 
                'id': 'ramo_id',
                'readonly': True
            }
        ),
    )
    taker_person_type = forms.CharField(
        label=_("Tipo de Persona"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Tipo de Persona', 
                'id': 'taker_person_type_id',
                'readonly': True
            }
        ),
    )
    taker_document_type = forms.CharField(
        label=_("Tipo de Documento"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id',
                'readonly': True
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Identificación',
                'readonly': True
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'readonly': True
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
                'readonly': True
            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre Contacto',   
                'readonly': True
            }
        ),
    )
    value = forms.CharField(
        label=_("Valor"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor',
                'readonly': True
            }
        ),
    )
    assigned_to = forms.ModelChoiceField(
        label=_("Asignado a:"),
        required=False,
        queryset=Account.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'assigned_to_id',
                'readonly': True
            }
        ),
    )
    created_at = forms.CharField(
        label=_("Fecha Creación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    validated_at = forms.CharField(
        label=_("Fecha Validación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    validated_by = forms.CharField(
        label=_("Validado por"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    request_receipt = forms.FileField(
        label=_("Recibo de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Recibo de Pago',
                'autocomplete': 'off'
            }
        ),
    )
    request_police = forms.FileField(
        label=_("Póliza"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )
    request_rc_police = forms.FileField(
        label=_("Póliza RC"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )
    payment_receipt = forms.FileField(
        label=_("Comprobante de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': 4,
                'readonly': True
            }
        ),
    )

    class Media:
        js = (
            'js/requests/query.js', 
        )


class AssignRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    status = forms.ModelChoiceField(
        label=_("Estado *"),
        required=False,
        queryset=RequestStatus.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'status_id',
                'readonly': True
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo *"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'ramo_id'
            }
        ),
    )
    taker_person_type = forms.ModelChoiceField(
        label=_("Tipo de Persona *"),
        required=False,
        queryset=PersonType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Persona', 
                'id': 'taker_person_type_id'
            }
        ),
    )
    taker_document_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=False,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Identificación',
                'readonly': True
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre Contacto',
            }
        ),
    )
    created_at = forms.CharField(
        label=_("Fecha Creación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    value = forms.CharField(
        label=_("Valor *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor'
            }
        ),
    )
    assigned_to = forms.ModelChoiceField(
        label=_("Asignado a:"),
        required=False,
        queryset=Account.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'assigned_to_id'
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': 4,
            }
        ),
    )

    class Media:
        js = (
            'js/requests/form.js', 
            'js/requests/index.js', 
        )


class TakerRequestForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    status = forms.ModelChoiceField(
        label=_("Estado *"),
        required=False,
        queryset=RequestStatus.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'status_id',
                'readonly': True,
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo *"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'id': 'ramo_id',
                'readonly': True,
            }
        ),
    )
    taker_person_type = forms.ModelChoiceField(
        label=_("Tipo de Persona *"),
        required=True,
        queryset=PersonType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Persona', 
                'id': 'taker_person_type_id',
                'readonly': True
            }
        ),
    )
    taker_document_type = forms.ModelChoiceField(
        label=_("Tipo de Documento *"),
        required=True,
        queryset=DocumentType.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id',
                'readonly': True
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Identificación',
                'readonly': True
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'readonly': True
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
                'readonly': True

            }
        ),
    )
    taker_contact_name = forms.CharField(
        label=_("Nombre Contacto"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre Contacto',
                'readonly': True
            }
        ),
    )
    value = forms.CharField(
        label=_("Valor *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor',
                'readonly': True
            }
        ),
    )
    observations = forms.CharField(
        label=_("Observaciones"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': 4,
                'readonly': True
            }
        ),
    )
    class Media:
        js = (
            'js/requests/search_form.js', 
            'js/requests/search.js', 
            'js/localization.js', 
        )


class TakerRequestFilesForm(forms.Form):
    request_receipt = forms.FileField(
        label=_("Recibo de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )    
    payment_receipt = forms.FileField(
        label=_("Comprobante de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )    
    class Media:
        js = (
            'js/requests/search_form.js', 
            'js/requests/search.js', 
            'js/localization.js', 
        )


class PaymentRegisterForm(forms.Form):
    number = forms.IntegerField(
        label=_("Número"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Número',
                'readonly': True
            }
        ),
    )
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'readonly': True
            }
        ),
    )
    applicant_name = forms.CharField(
        label=_("Nombre Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control readonly',
                'placeholder': 'Nombre Solicitante',
                'readonly': True
            }
        ),
    )
    status = forms.CharField(
        label=_("Estado *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'id': 'status_id',
                'readonly': True,
            }
        ),
    )
    ramo = forms.CharField(
        label=_("Ramo *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'id': 'ramo_id',
                'readonly': True,
            }
        ),
    )
    taker_document_type = forms.CharField(
        label=_("Tipo de Documento *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Tipo de Documento', 
                'id': 'taker_document_type_id',
                'readonly': True
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Identificación',
                'readonly': True
            }
        ),
    )
    taker_name = forms.CharField(
        label=_("Nombre *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'readonly': True
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono Tomador',
                'readonly': True

            }
        ),
    )
    value = forms.CharField(
        label=_("Valor *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Valor',
                'readonly': True
            }
        ),
    )
    payment_receipt = forms.FileField(
        label=_("Comprobante de Pago"),
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control ',
                'placeholder': 'Póliza',
                'autocomplete': 'off'
            }
        ),
    )    
    class Media:
        js = (
            'js/requests/paymentregister.js', 
            'js/requests/search.js', 
            'js/localization.js', 
        )

class RequestFilterForm(forms.Form):
    search = forms.CharField(
        label=_("Buscar"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el texto para realizar la búsqueda'
            }
        ),
    )
    applicant = forms.ModelChoiceField(
        label=_("Solicitante"),
        required=False,
        queryset=Applicant.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Solicitante', 
                'id': 'filter_applicant_id'
            }
        ),
    )
    ramo = forms.ModelChoiceField(
        label=_("Ramo"),
        required=False,
        queryset=Ramo.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select', 
                'placeholder': 'Ramo', 
                'id': 'filter_ramo_id'
            }
        ),
    )
    date = forms.DateField(
        label=_("Fecha Solicitud"),
        required=False,
        widget=DatePickerInput(
            attrs={
                'class': 'form-control text-end', 
                'name': "date", 
                'placeholder': 'AAAA-MM-DD'
            }
        ),
    )

    class Media:
        js = ('js/requests/index.js',  )


class ApplicantSearchRequestForm(forms.Form):
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante *"),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_applicant_phone_number_id'
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono Tomador"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_phone_number_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_identification_id'
            }
        ),
    )
    search = forms.CharField(
        label=_("Campo de Búsqueda"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_search_id'
            }
        ),
    )

    class Media:
        js = ('js/requests/index.js',  )


class TakerSearchRequestForm(forms.Form):
    taker_phone_number = forms.CharField(
        label=_("Teléfono Tomador"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_phone_number_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_identification_id'
            }
        ),
    )
    search = forms.CharField(
        label=_("Campo de Búsqueda"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_search_id'
            }
        ),
    )

    class Media:
        js = ('js/requests/index.js',  )



class SearchRequestForm(forms.Form):
    applicant_phone_number = forms.CharField(
        label=_("Teléfono Solicitante"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_applicant_phone_number_id'
            }
        ),
    )
    taker_phone_number = forms.CharField(
        label=_("Teléfono Tomador"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_phone_number_id'
            }
        ),
    )
    taker_identification = forms.CharField(
        label=_("Identificación"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_taker_identification_id'
            }
        ),
    )
    search = forms.CharField(
        label=_("Buscar"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-xs',
                'id': 'filter_search_id'
            }
        ),
    )

    class Media:
        js = ('js/requests/index.js',  )

