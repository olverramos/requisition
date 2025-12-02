from django.utils.translation import gettext_lazy as _
from .models import RamoField, DocumentClass
from django import forms


class CreateRamoForm(forms.Form):
    id = forms.CharField(
        label=_("ID *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'ID'
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
    fields = forms.ModelMultipleChoiceField(
        queryset=RamoField.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Campos',
                'id': 'fields_id'
            }
        ),
        required=False,
        label="Campos"
    )
    document_classes = forms.ModelMultipleChoiceField(
        queryset=DocumentClass.objects.filter(document_type="CUSTOM"),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Documentos',
                'id': 'document_classes_id'
            }
        ),
        required=False,
        label="Documentos"
    )
    class Media:
        js = (
            'js/ramos/index.js', 
            'js/ramos/form.js', 
        )


class RamoFilterForm(forms.Form):
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
        js = ('js/ramos/index.js',  )


class DocumentClassFilterForm(forms.Form):
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
        js = ('js/documentclass/index.js',  )


class CreateDocumentClassForm(forms.Form):
    id = forms.CharField(
        label=_("ID *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'ID'
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

    class Media:
        js = (
            'js/documentclass/index.js', 
            'js/documentclass/form.js', 
        )

class EditDocumentClassForm(forms.Form):
    id = forms.CharField(
        label=_("ID *"),
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'ID',
                'readonly': True,
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

    class Media:
        js = (
            'js/documentclass/index.js', 
            'js/documentclass/form.js', 
        )
