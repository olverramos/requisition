from .models import RamoField, DocumentClass, FieldType
from django.utils.translation import gettext_lazy as _
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
        required=False,
        label="Campos",
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Campos',
                'id': 'fields_id'
            }
        ),
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


class RamoFieldFilterForm(forms.Form):
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
        js = ('js/ramofield/index.js',  )


class CreateRamoFieldForm(forms.Form):
    field_type = forms.ModelChoiceField(
        label=_("Tipo de Campo *"),
        queryset=FieldType.objects.all(), 
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Tipo de Campo'
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
    title = forms.CharField(
        label=_("Título *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Título'
            }
        ),
    )
    mandatory = forms.BooleanField(
        label=_("Es Obligatorio"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Media:
        js = (
            'js/ramofield/index.js', 
            'js/ramofield/form.js', 
        )



class FieldOptionFilterForm(forms.Form):
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
        js = ('js/fieldoption/index.js',  )


class CreateFieldOptionForm(forms.Form):
    value = forms.CharField(
        label=_("Valor *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Valor'
            }
        ),
    )
    title = forms.CharField(
        label=_("Título *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Título'
            }
        ),
    )
    
    class Media:
        js = (
            'js/fieldoption/index.js', 
            'js/fieldoption/form.js', 
        )        


class RamoFieldFilterForm(forms.Form):
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
        js = ('js/ramofield/index.js',  )


class CreateRamoFieldForm(forms.Form):
    field_type = forms.ModelChoiceField(
        label=_("Tipo de Campo *"),
        queryset=FieldType.objects.all(), 
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Tipo de Campo'
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
    title = forms.CharField(
        label=_("Título *"),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Título'
            }
        ),
    )
    mandatory = forms.BooleanField(
        label=_("Es Obligatorio"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Media:
        js = (
            'js/ramofield/index.js', 
            'js/ramofield/form.js', 
        )
