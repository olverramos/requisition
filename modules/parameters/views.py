from .forms import CreateRamoForm, RamoFilterForm, CreateDocumentClassForm, \
    DocumentClassFilterForm, EditDocumentClassForm
from .models import Ramo, FieldType, RamoField, DocumentClass, DocumentClassType
from django.contrib.auth.decorators import login_required
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
        'segment': 'parameters'
    }

    return render(request, 'ramos/index.html', context)


@login_required(login_url="/auth/login/")
def create_ramo_view(request):
    current_account = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateRamoForm(request.POST)
        if form.is_valid():
            ramo_id = form.cleaned_data['id']
            name = form.cleaned_data['name']
            fields = form.cleaned_data['fields']
            document_classes = form.cleaned_data['document_classes']

            try:
                ramo = Ramo.objects.get(name=name)
                error = 'Hay una ramo registrado con el nombre'
            except Ramo.DoesNotExist:
                ramo = None

            if error is None:
                ramo:Ramo = Ramo()
                ramo.id = ramo_id
                ramo.name = name
                ramo.ramo_fields = fields
                ramo.document_classes = document_classes
                ramo.created_at = datetime.datetime.now()
                ramo.created_by = current_account.username
                ramo.save()

                messages.success (request, f'Ramo {ramo} creada satisfactoriamente!')
        else:
            error = "¡Error en el registro de la ramo!"
        if error is not None:
            messages.error (request, error)

    return redirect(reverse_lazy("parameters_ramos"))

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
            fields = form.cleaned_data['fields']
            document_classes = form.cleaned_data['document_classes']
            if error is None:   
                ramo.name = name
                ramo.ramo_fields = fields
                ramo.document_classes = document_classes
                ramo.updated_at = datetime.datetime.now()
                ramo.updated_by = current_account.username
                ramo.save()
                messages.success (request, f'Ramo {ramo} actualizado satisfactoriamente!')
        else:
            error = "¡Error en la actualización del Ramo!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("parameters_ramos"))


@login_required(login_url="/auth/login/")
def delete_ramo_view(reques, ramo_id):
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

    return redirect(reverse_lazy("parameters_ramos"))

@login_required(login_url="/auth/login/")
def get_ramo_view(request, ramo_id) -> JsonResponse:
    ramo_data = {}
    try:
        ramo:Ramo = Ramo.objects.get(pk=ramo_id)
        ramo_data['id'] = str(ramo.id)
        ramo_data['name'] = ramo.name
        ramo_data['fields'] = []
        for ramo_field in ramo.ramo_fields:
            ramo_field = {
                'id': str(ramo_field.id),
                'field_type': ramo_field.field_type.id,
                'mandatory': ramo_field.mandatory,
                'name': ramo_field.name,
                'options': []
            }
            for ramo_field_option in ramo_field['options']:
                ramo_option_data = {
                    'value': ramo_field_option.value
                }
                ramo_field['options'].append(ramo_option_data)
            ramo_data['fields'].append(ramo_field)
        ramo_data['document_classes'] = []
        for document_class in ramo.document_classes:
            document_class = {
                'id': str(document_class.id),
                'name': document_class.name
            }
            ramo_data['document_classes'].append(document_class)
    except Ramo.DoesNotExist:
        pass

    return JsonResponse(data=ramo_data)

def ajax_getfields(request, ramo_id) -> JsonResponse:
    fields_data = []
    try:
        ramo:Ramo = Ramo.objects.get(pk=ramo_id)
        for ramo_field in ramo.ramo_fields:
            field_data = {
                'ramo': str(ramo.id),
                'field_type': str(ramo_field.field_type.id),
                'name': ramo_field.name,
                'title': ramo_field.title if ramo_field.title is not None else ramo_field.name.title(),
                'mandatory': ramo_field.mandatory,
                'options': []
            }
            
            for ramo_field_option in ramo_field.options:
                option_data = {
                    'value': ramo_field_option.value,
                    'title': ramo_field_option.title
                }
                field_data['options'].append(option_data)

            fields_data.append(field_data)
    except Ramo.DoesNotExist:
        pass 

    return JsonResponse(data=fields_data, safe=False)

def ajax_getdocuments(request, ramo_id) -> JsonResponse:
    fields_data = []
    try:
        ramo:Ramo = Ramo.objects.get(pk=ramo_id)
        for document in ramo.available_documents:
            field_data = {
                'ramo': str(ramo.id),
                'name': document.name,
                'title': document.title if document.title is not None else document.name.title(),
                'mandatory': document.mandatory,
            }
            
            fields_data.append(field_data)
    except Ramo.DoesNotExist:
        pass 

    return JsonResponse(data=fields_data, safe=False)


@login_required(login_url="/auth/login/")
def documentclass_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    documentclass_list = DocumentClass.objects.filter(document_type="CUSTOM")
    
    data['page'] = page
    create_form = CreateDocumentClassForm()
    filter_form = DocumentClassFilterForm()
    if request.method == 'POST':
        filter_form = DocumentClassFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            if search is not None and search != '':
                documentclass_list = documentclass_list.filter(
                    name__icontains=search
                )

    paginator = getPaginator(documentclass_list, page)

    context = {
        'table_title': 'Clases de Documentos',
        'table_description': 'Administrador de Clases de Documentos',
        'form': create_form,
        'filter_form': filter_form,
        'paginator': paginator,
        'segment': 'parameters'
    }

    return render(request, 'documentclass/index.html', context)

@login_required(login_url="/auth/login/")
def create_documentclass_view(request):
    current_account = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateDocumentClassForm(request.POST)
        if form.is_valid():
            document_class_id = form.cleaned_data['id']
            name = form.cleaned_data['name']

            try:
                document_class = DocumentClass.objects.get(id=document_class_id)
                error = 'Hay una Clase de Documento registrado con el nombre'
            except DocumentClass.DoesNotExist:
                document_class = None

            if error is None:
                document_class:DocumentClass = DocumentClass()
                document_class.id = document_class_id
                document_class.name = name
                document_class.document_type = DocumentClassType.objects.get(id="CUSTOM")
                document_class.created_at = datetime.datetime.now()
                document_class.created_by = current_account.username
                document_class.save()

                messages.success (request, f'Clase de Documento {document_class} creada satisfactoriamente!')
        else:
            error = "¡Error en el registro de la Clase de Documento!"
        if error is not None:
            messages.error (request, error)

    return redirect(reverse_lazy("parameters_documentclass"))

@login_required(login_url="/auth/login/")
def get_documentclass_view(request, document_class_id) -> JsonResponse:
    document_class_data = {}
    try:
        document_class:DocumentClass = DocumentClass.objects.get(pk=document_class_id)
        document_class_data['id'] = str(document_class.id)
        document_class_data['name'] = document_class.name
    except DocumentClass.DoesNotExist:
        pass

    return JsonResponse(data=document_class_data)

@login_required(login_url="/auth/login/")
def edit_documentclass_view(request, document_class_id):
    current_account = Account.getAccount(request.user)
    error = None
    try:
        document_class:DocumentClass = DocumentClass.objects.get(pk=document_class_id)
    except DocumentClass.DoesNotExist:
        error = 'No existe una Clase de Documento con el id'
        document_class = None

    if error is None and request.method == 'POST':
        form = EditDocumentClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if error is None:   
                document_class.name = name
                document_class.updated_at = datetime.datetime.now()
                document_class.updated_by = current_account.username
                document_class.save()
                messages.success (request, f'Clase de Documento {document_class} actualizada satisfactoriamente!')
        else:
            error = "¡Error en la actualización de la Clase de Documento!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("parameters_documentclass"))

@login_required(login_url="/auth/login/")
def delete_documentclass_view(request, document_class_id):
    error = None
    try:
        document_class = DocumentClass.objects.get(pk=document_class_id)
    except DocumentClass.DoesNotExist:
        error = 'No existe una Clase de Documento con el id'
        document_class = None

    if error is None:
        if request.method == 'POST':
            document_class.delete()
            messages.success (request, f'Clase de Documento {document_class} eliminada satisfactoriamente!')
    else:
        messages.error (request, error) 

    return redirect(reverse_lazy("parameters_documentclass"))
