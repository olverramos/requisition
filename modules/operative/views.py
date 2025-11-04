from .models import OperativeRequest, RequestField, RequestDocument, \
    RequestStatus, RequestEvent
from .forms import CreateRequestForm, RequestFilterForm, SearchRequestForm, \
    EditRequestForm
from modules.parameters.models import RamoField, AvailableDocument
from django.contrib.auth.decorators import login_required
from modules.authentication.models import Account
from modules.base.models import Applicant, Taker
from django.shortcuts import render, redirect
from core.templatetags.tools import currency
from django.http import JsonResponse
from django.urls import reverse_lazy
from core.utils import getPaginator
from django.contrib import messages
import datetime
import base64


@login_required(login_url="/auth/login/")
def requests_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    operative_request_list = OperativeRequest.objects.filter(
        status__ne='9')
    
    data['page'] = page
    filter_form = RequestFilterForm()
    if request.method == 'POST':
        filter_form = RequestFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            applicant = filter_form.cleaned_data['applicant']
            ramo = filter_form.cleaned_data['ramo']

            if search is not None and search != '':
                operative_request_list = operative_request_list.filter(
                    name__icontains=search
                )
            if applicant is not None:
                operative_request_list = operative_request_list.filter(
                    applicant=applicant
                )
            if ramo is not None:
                operative_request_list = operative_request_list.filter(
                    ramo=ramo
                )

    paginator = getPaginator(operative_request_list, page)

    context = {
        'table_title': 'Solicitudes',
        'table_description': 'Administrador de Solicitudes',
        'filter_form': filter_form,
        'disable_add': True,
        'paginator': paginator,
        'segment': 'operative'
    }
 
    return render(request, 'requests/index.html', context)


def requests_search_view(request):
    data = { }
    
    current_account = Account.getAccount(request.user)
    
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    operative_request_list = OperativeRequest.objects.filter(status__ne='9').order_by('-created')
    
    data['page'] = page
    filter_form = SearchRequestForm()
    form = EditRequestForm()
    if request.method == 'POST':
        filter_form = SearchRequestForm(request.POST)
        if filter_form.is_valid():
            applicant_phone_number = filter_form.cleaned_data['applicant_phone_number']
            applicant_list = Applicant.objects.filter(phone_number=applicant_phone_number)
            if applicant_phone_number is not None:
                operative_request_list = operative_request_list.filter(
                    applicant__in=applicant_list
                )
            else:
                operative_request_list = OperativeRequest.objects.none()

    paginator = getPaginator(operative_request_list, page)

    if current_account is None:
        disable_edit = True
        disable_delete = True
    else:
        disable_edit = False
        disable_delete = False

    context = {
        'table_title': 'Solicitudes',
        'table_description': 'Administrador de Solicitudes',
        'filter_form': filter_form,
        'form': form,
        'disable_add': True,
        'disable_edit': disable_edit,
        'disable_delete': disable_delete,
        'paginator': paginator,
        'segment': 'operative'
    }

    return render(request, 'requests/index.html', context)


def create_request_view(request):
    error = None
    data = {
        'number': OperativeRequest.getNextNumber()
    }
    form = CreateRequestForm(initial=data)
    if request.method == 'POST':
        form = CreateRequestForm(request.POST, request.FILES)
        if form.is_valid():
            applicant_email = form.cleaned_data['applicant_email']
            applicant_id = form.cleaned_data['applicant_id']
            taker_person_type = form.cleaned_data['taker_person_type']
            taker_document_type = form.cleaned_data['taker_document_type']
            taker_identification = form.cleaned_data['taker_identification']
            taker_name = form.cleaned_data['taker_name']
            taker_email = form.cleaned_data['taker_email']
            taker_phone_number = form.cleaned_data['taker_phone_number']
            taker_contact_name = form.cleaned_data['taker_contact_name']
            taker_address = form.cleaned_data['taker_address']
            taker_state = form.cleaned_data['taker_state']
            taker_city = form.cleaned_data['taker_city']
            ramo = form.cleaned_data['ramo']
            value = form.cleaned_data['value']
            observations = form.cleaned_data['observations']
            
            applicant = None
            if applicant_email is not None and applicant_email != '':
                try:
                    applicant = Applicant.objects.get(email=applicant_email)
                except Applicant.DoesNotExist:
                    error = 'No existe un solicitante con el email'

            taker = None
            if taker_identification is not None and taker_identification != '':
                try:
                    taker = Taker.objects.get(identification=taker_identification)
                except Taker.DoesNotExist:
                    taker = Taker()
                    taker.person_type = taker_person_type
                    taker.document_type = taker_document_type
                    taker.identification = taker_identification
                    taker.created_at = datetime.datetime.now()
                    taker.created_by = applicant.email 
                taker.name = taker_name
                taker.email = taker_email
                taker.phone_number = taker_phone_number
                taker.contact_name = taker_contact_name
                taker.address = taker_address
                taker.state = taker_state
                taker.city = taker_city
                taker.updated_at = datetime.datetime.now()
                taker.updated_by = applicant.email
                taker.save()

            request_fields = []

            for ramo_field in ramo.ramo_fields:
                ramo_field_value = None
                if ramo_field.name in request.POST.keys():
                    ramo_field_value = request.POST[ramo_field.name]

                if ramo_field is not None and ramo_field_value is not None:
                    request_field = RequestField()
                    request_field.field = ramo_field
                    request_field.value = ramo_field_value
                    request_fields.append(request_field)

            request_documents = []
            for document_field in ramo.available_documents:
                document_file = None
                document_field_name = 'document_' + document_field.name
                if document_field_name in request.FILES.keys():
                    document_file = request.FILES[document_field_name]

                if document_field is not None and document_file is not None:
                    request_document = RequestDocument()
                    request_document.document_name = document_field.name
                    request_document.document_title = document_field.title

                    filename = document_file.name
                    file_type = document_file.content_type
                    content = base64.b64encode(document_file.read()).decode('utf-8')

                    request_document.filename = filename
                    request_document.file_type = file_type
                    request_document.content = content

                    request_documents.append(request_document)

            try:
                request_status = RequestStatus.objects.get(id='1')
            except RequestStatus.DoesNotExist:
                error = 'Error de Parametrización: Estado de Solicitud Inicial no encontrado'
                request_status = None

            if error is None:
                number = OperativeRequest.getNextNumber()

                operative_request:OperativeRequest = OperativeRequest()
                operative_request.applicant = applicant
                operative_request.taker = taker
                operative_request.ramo = ramo
                operative_request.number = number
                operative_request.value = value
                operative_request.status = request_status
                operative_request.request_fields = request_fields
                operative_request.request_documents = request_documents
                operative_request.observations = observations
                operative_request.created_at = datetime.datetime.now()
                operative_request.created_by = applicant.email
                operative_request.save()

                request_event = RequestEvent()
                request_event.operative_request = operative_request
                request_event.status = request_status
                request_event.observations = "Creación de la Solicitud"
                request_event.created_at = datetime.datetime.now()
                request_event.created_by = applicant.email
                request_event.save()

                messages.success (request, f'Solicitud {operative_request} creada satisfactoriamente!')
                return redirect(reverse_lazy("operative_requests"))
        else:
            error = "¡Error en el registro de la solicitud!"
        if error is not None:
            messages.error (request, error)

    context = {
        'table_title': 'Requests',
        'table_description': 'Crear Nueva Solicitud',
        'form': form,
        'segment': 'operative'
    }

    return render(request, 'requests/create.html', context)


# @login_required(login_url="/auth/login/")
# def edit_request_view(request, request_id):
#     current_account = Account.getAccount(request.user)
#     error = None
#     try:
#         request:Request = Request.objects.get(pk=request_id)
#     except Request.DoesNotExist:
#         error = 'No existe una request con el id'
#         request = None

#     if error is None and request.method == 'POST':
#         form = CreateRequestForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']

#             fields_data = []
#             if 'fields' in request.POST.keys():
#                 fields_data = request.POST['fields']

#             available_documents_data = []
#             if 'available_documents' in request.POST.keys():
#                 available_documents_data = request.POST['available_documents']

#             fields = []
#             for field_data in fields_data:
#                 if 'field_type' in field_data.keys():
#                     field_type_id = field_data["field_type"]
#                     try:
#                         field_type = FieldType.objects.get(pk=field_type_id)
#                     except FieldType.DoesNotExist:
#                         print (f"Tipo de Campo {field_type} no Existe")
#                         field_type = None

#                 if field_type is not None and 'name' in field_data.keys():
#                     name = field_data["name"]
#                     mandatory = False
#                     if 'mandatory' in field_data.keys():
#                         mandatory = field_data["mandatory"]
                    
#                     field = RequestField()
#                     field.field_type = field_type
#                     field.name = name
#                     field.mandatory = mandatory
#                     options = []
#                     if 'options' in field_data.keys():
#                         options = field_data["options"]
#                     field.options = options

#                     fields.append(field)

#             available_documents = []
#             for available_document_data in available_documents_data:
#                 if 'name' in available_document_data.keys():
#                     name = available_document_data["name"]
#                     mandatory = False
#                     if 'mandatory' in available_document_data.keys():
#                         mandatory = available_document_data["mandatory"]
                    
#                     available_document = AvailableDocument()
#                     available_document.name = name
#                     available_document.mandatory = mandatory
#                     available_documents.append(available_document)

#             if error is None:   
#                 request.name = name
#                 request.request_fields = fields
#                 request.available_documents = available_documents
#                 request.updated_at = datetime.datetime.now()
#                 request.updated_by = current_account.username
#                 request.save()
#                 messages.success (request, f'Request {request} actualizado satisfactoriamente!')
#         else:
#             error = "¡Error en la actualización del Request!"
#         if error is not None:
#             messages.error (request, error)
#     return redirect(reverse_lazy("base_requests"))


@login_required(login_url="/auth/login/")
def delete_request_view(request, request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    if error is None:
        if request.method == 'POST':
            request_status =  RequestStatus.objects.get(id='9') 
            operative_request.status = request_status
            operative_request.updated_at = datetime.datetime.now()
            operative_request.updated_by = current_account.username
            operative_request.save()

            request_event = RequestEvent()
            request_event.operative_request = operative_request
            request_event.status = request_status
            request_event.observations = "Eliminación de la Solicitud"
            request_event.created_at = datetime.datetime.now()
            request_event.created_by = current_account.username
            request_event.save()

            messages.success (request, f'Solicitud {operative_request} eliminada satisfactoriamente!')
    else:
        messages.error (request, error)

    return redirect(reverse_lazy("base_requests"))


def get_request_view(request, operative_request_id):
    operative_request = None
    request_data = {}
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
        request_data['id'] = str(operative_request.id)
        request_data['number'] = operative_request.number

        request_data['applicant_phone_number'] = str(operative_request.applicant.phone_number)
        request_data['applicant_name'] = str(operative_request.applicant)

        request_data['taker_person_type_id'] = str(operative_request.taker.person_type.id)
        request_data['taker_person_type'] = str(operative_request.taker.person_type)
        request_data['taker_document_type_id'] = str(operative_request.taker.document_type.id)
        request_data['taker_document_type'] = str(operative_request.taker.document_type)
        request_data['taker_identification'] = str(operative_request.taker.identification)
        request_data['taker_name'] = str(operative_request.taker.name)
        request_data['taker_phone_number'] = str(operative_request.taker.phone_number)
        request_data['taker_contact_name'] = str(operative_request.taker.contact_name)
        
        request_data['ramo_id'] = str(operative_request.ramo.id)
        request_data['ramo'] = str(operative_request.ramo)
        
        request_data['status_id'] = str(operative_request.status.id)
        request_data['status'] = str(operative_request.status)
        request_data['value'] = currency(operative_request.value)
        request_data['assigned_to'] = operative_request.assigned_to if operative_request.assigned_to else ''
        request_data['assigned_at'] = operative_request.assigned_at.strftime("%Y-%m-%d %H:%M") if operative_request.assigned_at else ''
        request_data['observations'] = operative_request.observations if operative_request.observations else ''
        request_data['fields'] = {}
        for request_field in operative_request.request_fields:
            request_data['fields'][str(request_field.field.name)] = request_field.value
        request_data['documents'] = []
        # request_documents = fields.ListField(
        #     fields.EmbeddedDocumentField(RequestDocument), blank=True,
        # )

    except OperativeRequest.DoesNotExist:
        pass

    return JsonResponse(data=request_data)
