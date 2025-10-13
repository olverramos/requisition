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

    class Media:
        js = ('js/ramos/index.js', 'js/ramos/form.js', )


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

