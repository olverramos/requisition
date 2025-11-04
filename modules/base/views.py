from .models import Applicant, Taker, DocumentType
from django.contrib.auth.decorators import login_required
from .forms import CreateApplicantForm, ApplicantFilterForm, CreateTakerForm, \
    TakerFilterForm, EditApplicantForm, EditTakerForm
from modules.authentication.models import Account
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from core.utils import getPaginator
from django.contrib import messages
import datetime


@login_required(login_url="/auth/login/")
def applicants_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    applicant_list = Applicant.objects.all()
    
    data['page'] = page
    create_form = CreateApplicantForm()
    filter_form = ApplicantFilterForm()
    if request.method == 'POST':
        filter_form = ApplicantFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            if search is not None and search != '':
                applicant_list = applicant_list.filter(
                    name__icontains=search
                )

    paginator = getPaginator(applicant_list, page)

    context = {
        'table_title': 'Solicitantes',
        'table_description': 'Administrador de Solicitantes',
        'form': create_form,
        'filter_form': filter_form,
        'paginator': paginator,
        'segment': 'base'
    }

    return render(request, 'applicants/index.html', context)

@login_required(login_url="/auth/login/")
def create_applicant_view(request):
    current_account:Account | None = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateApplicantForm(request.POST)
        if form.is_valid():
            identification = form.cleaned_data['identification']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            if error is None:
                applicant:Applicant = Applicant()
                applicant.identification = identification
                applicant.name = name
                applicant.email = email
                applicant.phone_number = phone_number
                applicant.created_at = datetime.datetime.now()
                applicant.created_by = current_account.username
                applicant.save()

                messages.success (request, f'Solicitante {applicant} creado satisfactoriamente!')
        else:
            error = "¡Error en el registro del Solicitante!"
        if error is not None:
            messages.error (request, error)

    return redirect(reverse_lazy("base_applicants"))

@login_required(login_url="/auth/login/")
def edit_applicant_view(request, applicant_id):
    current_account:Account | None = Account.getAccount(request.user)
    error = None
    try:
        applicant:Applicant = Applicant.objects.get(pk=applicant_id)
    except Applicant.DoesNotExist:
        error = 'No existe una applicant con el id'
        applicant = None

    if error is None and request.method == 'POST':
        form = EditApplicantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if error is None:   
                applicant.name = name
                applicant.email = email
                applicant.updated_at = datetime.datetime.now()
                applicant.updated_by = current_account.username
                applicant.save()
                messages.success (request, f'Solicitante {applicant} actualizado satisfactoriamente!')
        else:
            error = "¡Error en la actualización del Solicitante!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("base_applicants"))

@login_required(login_url="/auth/login/")
def delete_applicant_view(request, applicant_id):
    error = None
    try:
        applicant = Applicant.objects.get(pk=applicant_id)
    except Applicant.DoesNotExist:
        error = 'No existe una applicant con el id'
        applicant = None

    if error is None:
        if request.method == 'POST':
            applicant.delete()
            messages.success (request, f'Solicitante {applicant} eliminado satisfactoriamente!')
    else:
        messages.error (request, error)

    return redirect(reverse_lazy("base_applicants"))

@login_required(login_url="/auth/login/")
def get_applicant_view(request, applicant_id):
    applicant = None
    applicant_data = {}
    try:
        applicant:Applicant = Applicant.objects.get(pk=applicant_id)
        applicant_data['id'] = str(applicant.id)
        applicant_data['identification'] = applicant.identification
        applicant_data['name'] = applicant.name
        applicant_data['email'] = applicant.email
        applicant_data['phone_number'] = applicant.phone_number
        if applicant.state is not None:
            applicant_data['state'] = str(applicant.state.id)
        if applicant.city is not None:
            applicant_data['city'] = str(applicant.city.id)
    except Applicant.DoesNotExist:
        pass

    return JsonResponse(data=applicant_data, safe=False)

@login_required(login_url="/auth/login/")
def takers_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    taker_list = Taker.objects.all()
    
    data['page'] = page
    create_form = CreateTakerForm()
    filter_form = TakerFilterForm()
    if request.method == 'POST':
        filter_form = TakerFilterForm(request.POST)
        if filter_form.is_valid():
            search = filter_form.cleaned_data['search']
            if search is not None and search != '':
                taker_list = taker_list.filter(
                    name__icontains=search
                )

    paginator = getPaginator(taker_list, page)

    context = {
        'table_title': 'Tomadores',
        'table_description': 'Administrador de Tomadores',
        'form': create_form,
        'filter_form': filter_form,
        'paginator': paginator,
        'segment': 'base'
    }

    return render(request, 'takers/index.html', context)

@login_required(login_url="/auth/login/")
def create_taker_view(request):
    current_account:Account | None = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateTakerForm(request.POST)
        if form.is_valid():
            person_type = form.cleaned_data['person_type']
            document_type = form.cleaned_data['document_type']
            identification = form.cleaned_data['identification']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            contact_name = form.cleaned_data['contact_name']

            if error is None:
                taker:Taker = Taker()
                taker.person_type = person_type
                taker.document_type = document_type
                taker.identification = identification
                taker.name = name
                taker.email = email
                taker.phone_number = phone_number
                taker.contact_name = contact_name
                taker.created_at = datetime.datetime.now()
                taker.created_by = current_account.username
                taker.save()

                messages.success (request, f'Solicitante {taker} creado satisfactoriamente!')
        else:
            error = "¡Error en el registro del Solicitante!"
        if error is not None:
            messages.error (request, error)

    return redirect(reverse_lazy("base_takers"))

@login_required(login_url="/auth/login/")
def edit_taker_view(request, taker_id):
    current_account:Account | None = Account.getAccount(request.user)
    error = None
    try:
        taker:Taker = Taker.objects.get(pk=taker_id)
    except Taker.DoesNotExist:
        error = 'No existe una taker con el id'
        taker = None

    if error is None and request.method == 'POST':
        form = EditTakerForm(request.POST)
        if form.is_valid():
            person_type = form.cleaned_data['person_type']
            document_type = form.cleaned_data['document_type']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            contact_name = form.cleaned_data['contact_name']

            if error is None:   
                taker.person_type = person_type
                taker.document_type = document_type
                taker.name = name
                taker.email = email
                taker.phone_number = phone_number
                taker.contact_name = contact_name
                taker.updated_at = datetime.datetime.now()
                taker.updated_by = current_account.username
                taker.save()
                messages.success (request, f'Solicitante {taker} actualizado satisfactoriamente!')
        else:
            error = "¡Error en la actualización del Solicitante!"
        if error is not None:
            messages.error (request, error)
    return redirect(reverse_lazy("base_takers"))

@login_required(login_url="/auth/login/")
def delete_taker_view(request, taker_id):
    error = None
    try:
        taker = Taker.objects.get(pk=taker_id)
    except Taker.DoesNotExist:
        error = 'No existe una taker con el id'
        taker = None

    if error is None:
        if request.method == 'POST':
            taker.delete()
            messages.success (request, f'Solicitante {taker} eliminado satisfactoriamente!')
    else:
        messages.error (request, error)

    return redirect(reverse_lazy("base_takers"))

@login_required(login_url="/auth/login/")
def get_taker_view(request, taker_id):
    taker = None
    taker_data = {}
    try:
        taker:Taker = Taker.objects.get(pk=taker_id)
        taker_data['id'] = str(taker.id)
        taker_data['person_type'] = taker.person_type.id
        taker_data['document_type'] = taker.document_type.id
        taker_data['identification'] = taker.identification
        taker_data['name'] = taker.name
        taker_data['email'] = taker.email
        taker_data['phone_number'] = taker.phone_number
        taker_data['contact_name'] = taker.contact_name
    except Taker.DoesNotExist:
        pass

    return JsonResponse(data=taker_data, safe=False)

def ajax_search_applicant(request):
    applicant_data = {}

    phone_number = None
    if 'phone_number' in request.GET.keys() and request.GET['phone_number']:
        phone_number = request.GET['phone_number']

    email = None
    if 'email' in request.GET.keys() and request.GET['email']:
        email = request.GET['email']
    
    applicant:Applicant = None
    try:
        if phone_number is not None:
            applicant:Applicant = Applicant.objects.get(phone_number=phone_number)
        elif email is not None:
            applicant:Applicant = Applicant.objects.get(email=email)
    except Applicant.DoesNotExist:
        pass
    
    if applicant is not None:
        applicant_data['id'] = str(applicant.id)
        applicant_data['identification'] = applicant.identification
        applicant_data['name'] = applicant.name
        applicant_data['email'] = applicant.email
        applicant_data['phone_number'] = applicant.phone_number

    return JsonResponse(data=applicant_data, safe=False)

def ajax_documenttypes(request, person_type_id):
    taker = None
    data_list = []

    document_type_list = DocumentType.objects.filter(person_type=person_type_id)
    for document_type in document_type_list:
        data = {
            'id': str(document_type.id),
            'name': str(document_type)
        }
        data_list.append(data)

    return JsonResponse(data=data_list, safe=False)


def ajax_search_taker(request):
    taker_data = {}

    identification = None
    if 'identification' in request.GET.keys() and request.GET['identification']:
        identification = request.GET['identification']
    try:
        taker:Taker = Taker.objects.get(identification=identification)
        taker_data['id'] = str(taker.id)
        taker_data['person_type'] = taker.person_type.id
        taker_data['document_type'] = taker.document_type.id
        taker_data['identification'] = taker.identification
        taker_data['name'] = taker.name
        taker_data['email'] = taker.email
        taker_data['phone_number'] = taker.phone_number
        taker_data['contact_name'] = taker.contact_name
    except Taker.DoesNotExist:
        pass

    return JsonResponse(data=taker_data, safe=False)
