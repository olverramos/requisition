from .models import OperativeRequest, RequestField, RequestDocument, \
    RequestStatus, RequestEvent, RequestFile
from .forms import CreateRequestForm, RequestFilterForm, SearchRequestForm, \
    TakerRequestForm, EditRequestForm, TakerRequestFilesForm, \
    EditRequestFilesForm, ApplicantSearchRequestForm, TakerSearchRequestForm, \
    QueryRequestForm, PaymentRegisterForm, AttachmentDocumentForm
from django.contrib.humanize.templatetags.humanize import intcomma
from modules.authentication.models import Account, RoleEnum
from django.contrib.auth.decorators import login_required
from django_mongoengine.mongo_auth.models import User
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
    current_account:Account = Account.getAccount(request.user)

    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    operative_request_list = OperativeRequest.objects.filter(
        status__ne='9'
    )
    can_load_documents = False
    can_assign = False
    can_valide = False
    can_edit = False
    can_delete = False
    can_add = False
    can_download_documents = False
    can_register_payment = False

    if current_account.role.id == RoleEnum.ADMIN:
        table_description = "Administrador de Solicitudes"
        can_load_documents = True
        can_assign = True
        can_valide = True
        can_edit = True
        can_delete = True
    if current_account.role.id == RoleEnum.ASSISTANT:
        table_description = "Administrador de Solicitudes"
        operative_request_list = operative_request_list.filter(assigned_to=current_account)
        can_load_documents = True
        can_valide = True
    if current_account.role.id == RoleEnum.APPLICANT:
        can_add = True
        can_download_documents = True
        can_register_payment = True
        table_description = "Solicitudes Creadas"

        try:
            applicant = Applicant.objects.get(account=current_account)
            operative_request_list = operative_request_list.filter(applicant=applicant)
        except Applicant.DoesNotExist:
            operative_request_list = OperativeRequest.objects.none()

    data['page'] = page
    filter_form = RequestFilterForm()
    form = EditRequestForm()
    files_form = EditRequestFilesForm()
    if request.method == 'POST':
        filter_form = RequestFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            applicant = filter_form.cleaned_data['applicant']
            ramo = filter_form.cleaned_data['ramo']
            date = filter_form.cleaned_data['date']

            if search is not None and search != '':
                operative_request_list = operative_request_list.filter(
                    values_fields__icontains=search
                )
            if applicant is not None:
                operative_request_list = operative_request_list.filter(
                    applicant=applicant
                )
            if ramo is not None:
                operative_request_list = operative_request_list.filter(
                    ramo=ramo
                )
            if date is not None:
                start_date_time = datetime.datetime.combine(date, datetime.time.min)
                end_date_time = datetime.datetime.combine(date, datetime.time.max)
                operative_request_list = operative_request_list.filter(
                    created_at__gte=start_date_time,
                    created_at__lte=end_date_time
                )

    paginator = getPaginator(operative_request_list, page, items_per_page=10)

    user_list = User.objects.filter(is_active=True)
    form.fields['assigned_to'].queryset = Account.objects.filter(
        user__in=user_list,
        role__in=('assitant', 'admin',)
    )

    context = {
        'table_title': 'Solicitudes',
        'table_description': table_description,
        'filter_form': filter_form,
        'form': form,
        'files_form': files_form,
        'disable_add': True,
        'can_assign': can_assign,
        'can_add': can_add,
        'can_load_documents': can_load_documents,
        'can_valide': can_valide,
        'can_edit': can_edit,
        'can_delete': can_delete,
        'can_download_documents': can_download_documents,
        'can_register_payment': can_register_payment,
        'paginator': paginator,
        'segment': 'operative'
    }
 
    return render(request, 'requests/index.html', context)

def requests_applicant_search_view(request):
    data = { }
    
    current_account = Account.getAccount(request.user)
    
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    operative_request_list = OperativeRequest.objects.filter(status__ne='9')
    applicant = None
    data['page'] = page
    filter_form = ApplicantSearchRequestForm()
    form = TakerRequestForm()
    files_form = TakerRequestFilesForm()
    if request.method == 'POST':
        filter_form = ApplicantSearchRequestForm(request.POST)
        if filter_form.is_valid():
            applicant_phone_number = filter_form.cleaned_data['applicant_phone_number']
            taker_phone_number = filter_form.cleaned_data['taker_phone_number']
            taker_identification = filter_form.cleaned_data['taker_identification']
            search = filter_form.cleaned_data['search']
            
            applicant = None
            taker = None

            if applicant_phone_number:
                try:
                    applicant = Applicant.objects.get(phone_number=applicant_phone_number)
                except Applicant.DoesNotExist:
                    applicant = None
            if taker_phone_number:
                try:
                    taker = Taker.objects.get(phone_number=taker_phone_number)
                except Taker.DoesNotExist:
                    taker = None

            if taker_identification:
                try:
                    taker = Taker.objects.get(identification=taker_identification)
                except Taker.DoesNotExist:
                    taker = None

            if applicant:
                operative_request_list = operative_request_list.filter(
                    applicant=applicant
                )
            if taker:
                operative_request_list = operative_request_list.filter(
                    taker=taker
                )
            if search:
                operative_request_list = operative_request_list.filter(
                    request_fields__value=search
                )
                
    if applicant is None:
        operative_request_list = OperativeRequest.objects.none()

    paginator = getPaginator(operative_request_list, page, items_per_page=10)

    if current_account is None:
        can_register_payment = True
    else:
        can_register_payment = False

    context = {
        'table_title': 'Solicitudes',
        'table_description': 'Búsqueda de Solicitudes por Solicitante',
        'filter_form': filter_form,
        'form': form,
        'files_form': files_form,
        'disable_add': True,
        'can_register_payment': can_register_payment,
        'paginator': paginator,
        'segment': 'operative', 
        'back_url': '/',
        'filter_name': 'Buscar',
    }

    return render(request, 'requests/search_index.html', context)

def requests_taker_search_view(request):
    data = { }
    
    current_account = Account.getAccount(request.user)
    
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    operative_request_list = OperativeRequest.objects.filter(status__ne='9')
    search_data = False
    data['page'] = page
    filter_form = TakerSearchRequestForm()
    form = TakerRequestForm()
    files_form = TakerRequestFilesForm()
    if request.method == 'POST':
        filter_form = TakerSearchRequestForm(request.POST)
        if filter_form.is_valid():
            taker_phone_number = filter_form.cleaned_data['taker_phone_number']
            taker_identification = filter_form.cleaned_data['taker_identification']
            search = filter_form.cleaned_data['search']
            
            taker = None

            if taker_phone_number:
                search_data = True
                try:
                    taker = Taker.objects.get(phone_number=taker_phone_number)
                except Taker.DoesNotExist:
                    taker = None

            if taker_identification:
                search_data = True
                try:
                    taker = Taker.objects.get(identification=taker_identification)
                except Taker.DoesNotExist:
                    taker = None

            if taker:
                operative_request_list = operative_request_list.filter(
                    taker=taker
                )
            if search:
                search_data = True
                operative_request_list = operative_request_list.filter(
                    request_fields__value=search
                )
                
    if not search_data:
        operative_request_list = OperativeRequest.objects.none()

    paginator = getPaginator(operative_request_list, page, items_per_page=10)

    if current_account is None:
        can_register_payment = True
    else:
        can_register_payment = False

    context = {
        'table_title': 'Solicitudes',
        'table_description': 'Búsqueda de Solicitudes para el Tomador',
        'filter_form': filter_form,
        'form': form,
        'files_form': files_form,
        'disable_add': True,
        'can_register_payment': can_register_payment,
        'paginator': paginator,
        'segment': 'operative', 
        'back_url': '/',
        'filter_name': 'Buscar',
    }

    return render(request, 'requests/search_index.html', context)


def create_request_view(request):
    error = None
    data = {
        'number': OperativeRequest.getNextNumber()
    }
    form = CreateRequestForm(initial=data)
    if request.method == 'POST':
        form = CreateRequestForm(request.POST, request.FILES)
        if form.is_valid():
            applicant_phone_number = form.cleaned_data['applicant_phone_number']
            applicant_id = form.cleaned_data['applicant_id']
            taker_person_type = form.cleaned_data['taker_person_type']
            taker_document_type = form.cleaned_data['taker_document_type']
            taker_identification = form.cleaned_data['taker_identification']
            taker_name = form.cleaned_data['taker_name']
            taker_phone_number = form.cleaned_data['taker_phone_number']
            taker_contact_name = form.cleaned_data['taker_contact_name']
            ramo = form.cleaned_data['ramo']
            value = form.cleaned_data['value'].replace(',', '').replace('$ ', '')
            try:
                value = float(value)
            except ValueError:
                error = 'El valor debe ser un número'
            observations = form.cleaned_data['observations']
            
            applicant = None
            if applicant_phone_number is not None and applicant_phone_number != '':
                try:
                    applicant = Applicant.objects.get(phone_number=applicant_phone_number)
                except Applicant.DoesNotExist:
                    error = 'No existe un solicitante con el teléfono'

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
                taker.phone_number = taker_phone_number
                taker.contact_name = taker_contact_name
                taker.updated_at = datetime.datetime.now()
                taker.updated_by = applicant.email
                taker.save()

            request_fields = []
            values_fields = ''
            for ramo_field in ramo.ramo_fields:
                ramo_field_value = None
                if ramo_field.name in request.POST.keys():
                    ramo_field_value = request.POST[ramo_field.name]

                if ramo_field is not None and ramo_field_value is not None:
                    request_field = RequestField()
                    request_field.field = ramo_field
                    request_field.value = ramo_field_value
                    request_fields.append(request_field)
                    values_fields += ramo_field_value
                    values_fields += ' '

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

            request_status_id = '1'
            assigned_to = None
            assigned_at = None
            assigned_by = None

            assistants = Account.objects.filter(role=RoleEnum.ASSISTANT)
            if assistants.count() == 1:
                assistant = assistants[0]
                assigned_to = assistant
                assigned_at = datetime.datetime.now()
                assigned_by = applicant.email
                request_status_id = '2'
            
            try:
                request_status = RequestStatus.objects.get(id=request_status_id)
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
                operative_request.request_fields = request_fields
                operative_request.request_documents = request_documents
                operative_request.observations = observations
                operative_request.created_at = datetime.datetime.now()
                operative_request.created_by = applicant.email
                operative_request.assigned_to = assigned_to
                operative_request.assigned_at = assigned_at
                operative_request.assigned_by = assigned_by
                operative_request.status = request_status

                operative_request.save()

                request_event = RequestEvent()
                request_event.operative_request = operative_request
                request_event.status = request_status
                request_event.observations = "Creación de la Solicitud"
                request_event.created_at = datetime.datetime.now()
                request_event.created_by = applicant.email
                request_event.save()

                messages.success (request, f'Solicitud {operative_request} creada satisfactoriamente!')
                return redirect(reverse_lazy("home"))
        else:
            error = "¡Error en el registro de la solicitud! "
            for field, message_list in form.errors.items():
                if field == 'value':
                    error += 'Valor: '
                else:
                    error += field + ': '
                error += ','.join(message_list)

        if error is not None:
            messages.error (request, error)

    context = {
        'table_title': 'Requests',
        'table_description': 'Crear Nueva Solicitud',
        'form': form,
        'segment': 'operative'
    }

    return render(request, 'requests/create.html', context)

def query_request_view(request, operative_request_id):
    error = None
    current_account:Account = Account.getAccount(request.user)

    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    can_view_police = False
    if current_account is not None:
        if current_account.role.id in ( RoleEnum.ASSISTANT, RoleEnum.ADMIN):
            can_view_police = True
        elif operative_request.status.id >= "4":
            can_view_police = True

    data = {}
    if error is None:
        data = operative_request.query()

    form = QueryRequestForm(initial=data)

    if 'back_url' in request.GET:
        back_url = reverse_lazy(request.GET['back_url'])
    else:
        back_url = reverse_lazy("operative_requests")

    if error is not None:
        messages.error (request, error)

    context = {
        'table_title': 'Requests',
        'table_description': 'Consultar Solicitud',
        'form': form,
        'request_data': data,
        'can_view_police': can_view_police,
        'operative_request': operative_request,
        'back_url': back_url,
        'segment': 'operative'
    }

    return render(request, 'requests/query.html', context)


@login_required(login_url="/auth/login/")
def edit_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    if error is None and request.method == 'POST':
        form = EditRequestForm(request.POST)
        files_form = EditRequestFilesForm(request.POST, request.FILES)
        
        if form.is_valid() and files_form.is_valid():
            taker_person_type = form.cleaned_data['taker_person_type']
            taker_document_type = form.cleaned_data['taker_document_type']
            taker_identification = form.cleaned_data['taker_identification']
            taker_name = form.cleaned_data['taker_name']
            taker_phone_number = form.cleaned_data['taker_phone_number']
            taker_contact_name = form.cleaned_data['taker_contact_name']
            ramo = form.cleaned_data['ramo']
            value = form.cleaned_data['value'].replace(',', '').replace('$ ', '')
            try:
                value = float(value)
            except ValueError:
                error = 'El valor debe ser un número'
            request_status = form.cleaned_data['status']
            observations = form.cleaned_data['observations']
            assigned_to = form.cleaned_data['assigned_to']
            request_receipt = None
            request_police = None
            request_rc_police = None
            payment_receipt = None

            if 'request_receipt' in request.FILES.keys():
                request_receipt_file = request.FILES['request_receipt']
                if request_receipt_file is not None:
                    request_receipt = RequestFile()

                    filename = request_receipt_file.name
                    file_type = request_receipt_file.content_type
                    content = base64.b64encode(request_receipt_file.read()).decode('utf-8')

                    request_receipt.filename = filename
                    request_receipt.file_type = file_type
                    request_receipt.content = content

            if 'request_police' in request.FILES.keys():
                request_police_file = request.FILES['request_police']
                if request_police_file is not None:
                    request_police = RequestFile()

                    filename = request_police_file.name
                    file_type = request_police_file.content_type
                    content = base64.b64encode(request_police_file.read()).decode('utf-8')

                    request_police.filename = filename
                    request_police.file_type = file_type
                    request_police.content = content
            
            if 'request_rc_police' in request.FILES.keys():
                request_rc_police_file = request.FILES['request_rc_police']
                if request_rc_police_file is not None:
                    request_rc_police = RequestFile()

                    filename = request_rc_police_file.name
                    file_type = request_rc_police_file.content_type
                    content = base64.b64encode(request_rc_police_file.read()).decode('utf-8')

                    request_rc_police.filename = filename
                    request_rc_police.file_type = file_type
                    request_rc_police.content = content
            
            if 'payment_receipt' in request.FILES.keys():
                payment_receipt_file = request.FILES['payment_receipt']
                if payment_receipt_file is not None:
                    payment_receipt = RequestFile()

                    filename = payment_receipt_file.name
                    file_type = payment_receipt_file.content_type
                    content = base64.b64encode(payment_receipt_file.read()).decode('utf-8')

                    payment_receipt.filename = filename
                    payment_receipt.file_type = file_type
                    payment_receipt.content = content
            
            request_fields = []
            values_fields = ''
            for ramo_field in ramo.ramo_fields:
                ramo_field_value = None
                if ramo_field.name in request.POST.keys():
                    ramo_field_value = request.POST[ramo_field.name]

                if ramo_field is not None and ramo_field_value is not None:
                    request_field = RequestField()
                    request_field.field = ramo_field
                    request_field.value = ramo_field_value
                    request_fields.append(request_field)
                    values_fields += ramo_field_value
                    values_fields += ' '

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
                    taker.created_by = current_account.username 
                taker.name = taker_name
                taker.phone_number = taker_phone_number
                taker.contact_name = taker_contact_name
                taker.updated_at = datetime.datetime.now()
                taker.updated_by = current_account.username 
                taker.save()

            if error is None:   
                operative_request.taker = taker
                operative_request.ramo = ramo
                operative_request.value = value
                operative_request.status = request_status
                operative_request.request_fields = request_fields
                operative_request.request_documents = request_documents
                operative_request.observations = observations
                if request_receipt is not None:
                    operative_request.request_receipt = request_receipt
                if request_police is not None:
                    operative_request.request_police = request_police
                if request_rc_police is not None:
                    operative_request.request_rc_police = request_rc_police
                if payment_receipt is not None:
                    operative_request.payment_receipt = payment_receipt
                operative_request.assigned_to = assigned_to
                operative_request.assigned_at = datetime.datetime.now()
                operative_request.assigned_by = current_account.username
                operative_request.updated_at = datetime.datetime.now()
                operative_request.updated_by = current_account.username 
                operative_request.save()

                request_event = RequestEvent()
                request_event.operative_request = operative_request
                request_event.status = request_status
                request_event.observations = "Edición de la Solicitud"
                request_event.created_at = datetime.datetime.now()
                request_event.created_by = current_account.username 
                request_event.save()
                
                messages.success (request, f'Solicitud {operative_request} actualizado satisfactoriamente!')
        else:
            error = "¡Error en la actualización del Request!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("operative_requests"))

@login_required(login_url="/auth/login/")
def assign_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    if error is None and request.method == 'POST':
        form = EditRequestForm(request.POST)
        if form.is_valid():
            assigned_to = form.cleaned_data['assigned_to']

            request_status = RequestStatus.objects.get(id='2') 
            operative_request.status = request_status
            operative_request.assigned_to = assigned_to
            operative_request.assigned_at = datetime.datetime.now()
            operative_request.assigned_by = current_account.username
            operative_request.updated_at = datetime.datetime.now()
            operative_request.updated_by = current_account.username
            operative_request.save()

            request_event = RequestEvent()
            request_event.operative_request = operative_request
            request_event.status = request_status
            request_event.observations = "Asignación de la Solicitud"
            request_event.created_at = datetime.datetime.now()
            request_event.created_by = current_account.username
            request_event.save()

            messages.success (request, f'Solicitud {operative_request} asignada satisfactoriamente!')
        else: 
            error = 'Error en el formulario'
    if error is not None:
        messages.error (request, error)

    return redirect(reverse_lazy("operative_requests"))


@login_required(login_url="/auth/login/")
def load_documents_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    if error is None and request.method == 'POST':
        form = EditRequestFilesForm(request.POST, request.FILES)
        if form.is_valid():
            request_receipt = None
            request_police = None
            request_rc_police = None

            if 'request_receipt' in request.FILES.keys():
                request_receipt_file = request.FILES['request_receipt']
                if request_receipt_file is not None:
                    request_receipt = RequestFile()

                    filename = request_receipt_file.name
                    file_type = request_receipt_file.content_type
                    content = base64.b64encode(request_receipt_file.read()).decode('utf-8')

                    request_receipt.filename = filename
                    request_receipt.file_type = file_type
                    request_receipt.content = content

            if 'request_police' in request.FILES.keys():
                request_police_file = request.FILES['request_police']
                if request_police_file is not None:
                    request_police = RequestFile()

                    filename = request_police_file.name
                    file_type = request_police_file.content_type
                    content = base64.b64encode(request_police_file.read()).decode('utf-8')

                    request_police.filename = filename
                    request_police.file_type = file_type
                    request_police.content = content

            if 'request_rc_police' in request.FILES.keys():
                request_rc_police_file = request.FILES['request_rc_police']
                if request_rc_police_file is not None:
                    request_rc_police = RequestFile()

                    filename = request_rc_police_file.name
                    file_type = request_rc_police_file.content_type
                    content = base64.b64encode(request_rc_police_file.read()).decode('utf-8')

                    request_rc_police.filename = filename
                    request_rc_police.file_type = file_type
                    request_rc_police.content = content

            if request_receipt is not None and request_police is not None and request_rc_police is not None:
                request_status = RequestStatus.objects.get(id='3') 
                operative_request.status = request_status
            operative_request.request_receipt = request_receipt
            operative_request.request_police = request_police
            operative_request.request_rc_police = request_rc_police
            operative_request.updated_at = datetime.datetime.now()
            operative_request.updated_by = current_account.username
            operative_request.save()

            request_event = RequestEvent()
            request_event.operative_request = operative_request
            request_event.status = request_status
            request_event.observations = "Cargue de Documentación a la Solicitud"
            if request_receipt is not None:
                request_event.observations += ' Recibo de Pago cargado.'
            if request_police is not None:
                request_event.observations += ' Póliza cargada.'
            if request_rc_police is not None:
                request_event.observations += ' Póliza RC cargada.'
            request_event.created_at = datetime.datetime.now()
            request_event.created_by = current_account.username
            request_event.save()

            messages.success (request, f'Solicitud {operative_request} documentada satisfactoriamente!')
        else: 
            error = 'Error en el formulario'
    if error is not None:
        messages.error (request, error)

    return redirect(reverse_lazy("operative_requests"))

def payment_register_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None
    
    if 'back_url' in request.GET:
        back_url = request.GET['back_url'] 
    else:
        back_url = "operative_requests"
    data = {} 

    if error is None:
        data = operative_request.query()
    
    form = PaymentRegisterForm(initial=data)
    if error is None and request.method == 'POST':
        form = PaymentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            payment_receipt = None

            if 'payment_receipt' in form.cleaned_data.keys():
                payment_receipt_file = form.cleaned_data['payment_receipt']
                if payment_receipt_file is not None:
                    payment_receipt = RequestFile()

                    filename = payment_receipt_file.name
                    file_type = payment_receipt_file.content_type
                    content = base64.b64encode(payment_receipt_file.read()).decode('utf-8')

                    payment_receipt.filename = filename
                    payment_receipt.file_type = file_type
                    payment_receipt.content = content

            if payment_receipt is not None:
                request_status = RequestStatus.objects.get(id='4') 
                operative_request.status = request_status
            operative_request.payment_receipt = payment_receipt
            operative_request.updated_at = datetime.datetime.now()
            # operative_request.updated_by = current_account.username
            operative_request.save()

            request_event = RequestEvent()
            request_event.operative_request = operative_request
            request_event.status = request_status
            request_event.observations = "Cargue de Comprobante de Pago de la solicitud"
            if payment_receipt is not None:
                request_event.observations += ' Comprobante de Pago cargado.'
            request_event.created_at = datetime.datetime.now()
            if current_account is not None:
                request_event.created_by = current_account.username
            request_event.save()

            messages.success (request, f'Registro de Comprobante de Pago {operative_request} realizado satisfactoriamente!')
            return reverse_lazy(back_url)
        else: 
            error = f''
            if 'payment_receipt' in form.errors:
                error += f' Comprobante de pago: {form.errors["payment_receipt"]}'
            if 'request_receipt' in form.errors:
                error += f' Recibo de pago: {form.errors["request_receipt"]}'   

    if error is not None:
        messages.error (request, error)


    context = {
        'table_title': 'Requests',
        'table_description': 'Registrar Pago de Solicitud',
        'form': form,
        'request_data': data,
        'operative_request': operative_request,
        'back_url': reverse_lazy(back_url),
        'segment': 'operative'
    }

    return render(request, 'requests/paymentregister.html', context)

def attachment_documents_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
        ramo = operative_request.ramo
        old_request_documents = operative_request.request_documents
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None
    
    if 'back_url' in request.GET:
        back_url = request.GET['back_url'] 
    else:
        back_url = "operative_requests"
    data = {} 

    if error is None:
        data = operative_request.query()
    
    form = AttachmentDocumentForm(initial=data)
    if error is None and request.method == 'POST':
        request_documents_dict = {}

        for old_request_document in old_request_documents:
            request_documents_dict[old_request_document.document_name] = old_request_document

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

                request_documents_dict[document_field.name] = request_document

        operative_request.request_documents = list(request_documents_dict.values())
        operative_request.updated_at = datetime.datetime.now()
        if current_account is not None:
            operative_request.updated_by = current_account.username
        operative_request.save()

        request_event = RequestEvent()
        request_event.operative_request = operative_request
        request_event.status = operative_request.status
        request_event.observations = "Cargue de Documentos de la solicitud"
        request_event.created_at = datetime.datetime.now()
        if current_account is not None:
            request_event.created_by = current_account.username
        request_event.save()
        
        messages.success (request, f'Registro de Documentos {operative_request} realizado satisfactoriamente!')
        return redirect(back_url)

    if error is not None:
        messages.error (request, error)
    
    available_documents = ramo.available_documents

    context = {
        'table_title': 'Requests',
        'table_description': 'Registro de Documentos de la Solicitud',
        'form': form,
        'request_data': data,
        'operative_request': operative_request,
        'available_documents': available_documents,
        'back_url': reverse_lazy(back_url),
        'segment': 'operative'
    }

    return render(request, 'requests/attachmentdocument.html', context)

@login_required(login_url="/auth/login/")
def validate_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
    except OperativeRequest.DoesNotExist:
        error = 'No existe una request con el id'
        operative_request = None

    if error is None and request.method == 'POST':
        form = EditRequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_status = RequestStatus.objects.get(id='5') 
            operative_request.status = request_status
            operative_request.validated_at = datetime.datetime.now()
            operative_request.validated_by = current_account.username
            operative_request.updated_at = datetime.datetime.now()
            operative_request.updated_by = current_account.username
            operative_request.save()

            request_event = RequestEvent()
            request_event.operative_request = operative_request
            request_event.status = request_status
            request_event.observations = "Validación de la Solicitud"
            request_event.created_at = datetime.datetime.now()
            request_event.created_by = current_account.username
            request_event.save()

            messages.success (request, f'Solicitud {operative_request} validada satisfactoriamente!')
        else: 
            error = 'Error en el formulario'
    if error is not None:
        messages.error (request, error)

    return redirect(reverse_lazy("operative_requests"))

@login_required(login_url="/auth/login/")
def delete_request_view(request, operative_request_id):
    error = None
    current_account = Account.getAccount(request.user)
    try:
        operative_request:OperativeRequest = OperativeRequest.objects.get(pk=operative_request_id)
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

    return redirect(reverse_lazy("operative_requests"))


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
        request_data['assigned_to'] = str(operative_request.assigned_to) if operative_request.assigned_to else ''
        request_data['assigned_to_id'] = str(operative_request.assigned_to.id) if operative_request.assigned_to else ''
        request_data['assigned_at'] = operative_request.assigned_at.strftime("%Y-%m-%d %H:%M") if operative_request.assigned_at else ''
        request_data['created_at'] = operative_request.created_at.strftime("%Y-%m-%d %H:%M") if operative_request.created_at else ''
        request_data['created_by'] = operative_request.created_by if operative_request.created_by else ''
        request_data['updated_at'] = operative_request.updated_at.strftime("%Y-%m-%d %H:%M") if operative_request.updated_at else ''
        request_data['updated_by'] = operative_request.updated_by if operative_request.updated_by else ''
        request_data['validated_at'] = operative_request.validated_at.strftime("%Y-%m-%d %H:%M") if operative_request.validated_at else ''
        request_data['validated_by'] = operative_request.validated_by if operative_request.validated_by else ''
        request_data['request_receipt'] = None
        if operative_request.request_receipt is not None:
            request_data['request_receipt'] = {
                'filename': operative_request.request_receipt.filename,
                'file_type': operative_request.request_receipt.file_type,
                'content': operative_request.request_receipt.content,
            }
        request_data['request_police'] = None
        if operative_request.request_police is not None:
            request_data['request_police'] = {
                'filename': operative_request.request_police.filename,
                'file_type': operative_request.request_police.file_type,
                'content': operative_request.request_police.content,
            }
        request_data['request_rc_police'] = None
        if operative_request.request_rc_police is not None:
            request_data['request_rc_police'] = {
                'filename': operative_request.request_rc_police.filename,
                'file_type': operative_request.request_rc_police.file_type,
                'content': operative_request.request_rc_police.content,
            }
        request_data['payment_receipt'] = None
        if operative_request.payment_receipt is not None:
            request_data['payment_receipt'] = {
                'filename': operative_request.payment_receipt.filename,
                'file_type': operative_request.payment_receipt.file_type,
                'content': operative_request.payment_receipt.content,
            }

        request_data['observations'] = operative_request.observations if operative_request.observations else ''

        request_data['fields'] = {}
        for request_field in operative_request.request_fields:
            request_data['fields'][str(request_field.field.name)] = request_field.value
        request_data['documents'] = {}
        
        for document_field in operative_request.request_documents:
            request_data['documents'][str(document_field.document_name)] = {
                'document_name': document_field.document_name,
                'document_title': document_field.document_title,
                'filename': document_field.filename,
                'file_type': document_field.file_type,
                'content': document_field.content,
            }

    except OperativeRequest.DoesNotExist:
        pass

    return JsonResponse(data=request_data)
