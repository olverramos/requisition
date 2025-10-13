from .models import Ramo, FieldType, RamoField, AvailableDocument
from django.contrib.auth.decorators import login_required
from .forms import CreateRamoForm, RamoFilterForm
from modules.authentication.models import Account
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from core.utils import getPaginator
from django.contrib import messages
import datetime


@login_required(login_url="/auth/login/")
def ramos_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    ramo_list = Ramo.objects.all()
    
    data['page'] = page
    create_form = CreateRamoForm()
    filter_form = RamoFilterForm()
    if request.method == 'POST':
        filter_form = RamoFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            if search is not None and search != '':
                ramo_list = ramo_list.filter(
                    name__icontains=search
                )

    paginator = getPaginator(ramo_list, page)

    context = {
        'table_title': 'Ramos',
        'table_description': 'Administrador de Ramos',
        'form': create_form,
        'filter_form': filter_form,
        'paginator': paginator,
        'segment': 'bussiness'
    }

    return render(request, 'ramos/index.html', context)


@login_required(login_url="/auth/login/")
def create_ramo_view(request):
    current_account = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateRamoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            fields_data = []
            if 'fields' in request.POST.keys():
                fields_data = request.POST['fields']

            available_documents_data = []
            if 'available_documents' in request.POST.keys():
                available_documents_data = request.POST['available_documents']

            fields = []
            for field_data in fields_data:
                if 'field_type' in field_data.keys():
                    field_type_id = field_data["field_type"]
                    try:
                        field_type = FieldType.objects.get(pk=field_type_id)
                    except FieldType.DoesNotExist:
                        print (f"Tipo de Campo {field_type} no Existe")
                        field_type = None

                if field_type is not None and 'name' in field_data.keys():
                    name = field_data["name"]
                    mandatory = False
                    if 'mandatory' in field_data.keys():
                        mandatory = field_data["mandatory"]
                    
                    field = RamoField()
                    field.field_type = field_type
                    field.name = name
                    field.mandatory = mandatory
                    options = []
                    if 'options' in field_data.keys():
                        options = field_data["options"]
                    field.options = options

                    fields.append(field)

            available_documents = []
            for available_document_data in available_documents_data:
                if 'name' in available_document_data.keys():
                    name = available_document_data["name"]
                    mandatory = False
                    if 'mandatory' in available_document_data.keys():
                        mandatory = available_document_data["mandatory"]
                    
                    available_document = AvailableDocument()
                    available_document.name = name
                    available_document.mandatory = mandatory
                    available_documents.append(available_document)

            try:
                ramo = Ramo.objects.get(name=name)
                error = 'Hay una ramo registrado con el nombre'
            except Ramo.DoesNotExist:
                ramo = None

            if error is None:
                ramo:Ramo = Ramo()
                ramo.name = name
                ramo.ramo_fields = fields
                ramo.available_documents = available_documents
                ramo.created_at = datetime.datetime.now()
                ramo.created_by = current_account.username
                ramo.save()

                messages.success (request, f'Ramo {ramo} creada satisfactoriamente!')
        else:
            error = "¡Error en el registro de la ramo!"
        if error is not None:
            messages.error (request, error)

    return redirect(reverse_lazy("base_ramos"))

@login_required(login_url="/auth/login/")
def edit_ramo_view(request, ramo_id):
    current_account = Account.getAccount(request.user)
    error = None
    try:
        ramo:Ramo = Ramo.objects.get(pk=ramo_id)
    except Ramo.DoesNotExist:
        error = 'No existe una ramo con el id'
        ramo = None

    if error is None and request.method == 'POST':
        form = CreateRamoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            fields_data = []
            if 'fields' in request.POST.keys():
                fields_data = request.POST['fields']

            available_documents_data = []
            if 'available_documents' in request.POST.keys():
                available_documents_data = request.POST['available_documents']

            fields = []
            for field_data in fields_data:
                if 'field_type' in field_data.keys():
                    field_type_id = field_data["field_type"]
                    try:
                        field_type = FieldType.objects.get(pk=field_type_id)
                    except FieldType.DoesNotExist:
                        print (f"Tipo de Campo {field_type} no Existe")
                        field_type = None

                if field_type is not None and 'name' in field_data.keys():
                    name = field_data["name"]
                    mandatory = False
                    if 'mandatory' in field_data.keys():
                        mandatory = field_data["mandatory"]
                    
                    field = RamoField()
                    field.field_type = field_type
                    field.name = name
                    field.mandatory = mandatory
                    options = []
                    if 'options' in field_data.keys():
                        options = field_data["options"]
                    field.options = options

                    fields.append(field)

            available_documents = []
            for available_document_data in available_documents_data:
                if 'name' in available_document_data.keys():
                    name = available_document_data["name"]
                    mandatory = False
                    if 'mandatory' in available_document_data.keys():
                        mandatory = available_document_data["mandatory"]
                    
                    available_document = AvailableDocument()
                    available_document.name = name
                    available_document.mandatory = mandatory
                    available_documents.append(available_document)

            if error is None:   
                ramo.name = name
                ramo.ramo_fields = fields
                ramo.available_documents = available_documents
                ramo.updated_at = datetime.datetime.now()
                ramo.updated_by = current_account.username
                ramo.save()
                messages.success (request, f'Ramo {ramo} actualizado satisfactoriamente!')
        else:
            error = "¡Error en la actualización del Ramo!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("base_ramos"))


@login_required(login_url="/auth/login/")
def delete_ramo_view(request, ramo_id):
    error = None
    try:
        ramo = Ramo.objects.get(pk=ramo_id)
    except Ramo.DoesNotExist:
        error = 'No existe una ramo con el id'
        ramo = None

    if error is None:
        if request.method == 'POST':
            ramo.delete()
            messages.success (request, f'Ramo {ramo} eliminado satisfactoriamente!')
    else:
        messages.error (request, error)

    return redirect(reverse_lazy("base_ramos"))


@login_required(login_url="/auth/login/")
def get_ramo_view(request, ramo_id):
    ramo = None
    ramo_data = {}
    try:
        ramo:Ramo = Ramo.objects.get(pk=ramo_id)
        ramo_data['id'] = str(ramo.id)
        ramo_data['name'] = ramo.name
        ramo_data['fields'] = []
        for ramo_field in ramo.ramo_fields:
            ramo_field = {
                'field_type': ramo_field.field_type.id,
                'mandatory': ramo_field.mandatory,
                'name': ramo_field.name,
                'options': []
            }
            for ramo_field_option in ramo_field.options:
                ramo_option_data = {
                    'value': ramo_field_option.value
                }
                ramo_field['options'].append(ramo_option_data)
            ramo_data['fields'].append(ramo_field)
    except Ramo.DoesNotExist:
        return 

    return JsonResponse(data=ramo_data)
