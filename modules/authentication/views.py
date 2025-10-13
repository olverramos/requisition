from .forms import AccountLoginForm, RegistrationForm, AccountPasswordResetForm, \
    AccountSetPasswordForm, AccountPasswordChangeForm, AccountFilterForm, \
    AdminSetPasswordForm, CreateAccountForm, EditAccountForm, ProfileForm
from django.contrib.auth.views import LoginView, PasswordResetDoneView
from django.contrib.auth.decorators import login_required
from .models import Account, Role, RoleEnum, Genre, Token
from modules.localization.models import State, City
from django_mongoengine.mongo_auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from mongoengine.queryset.visitor import Q
from django.contrib.auth import logout
from django.views.generic import View
from django.urls import reverse_lazy
from core.utils import getPaginator
from django.contrib import messages
from django.template import loader
import datetime


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AccountLoginForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    messages.success(request, 'Se ha cerrado la sesión corectamente.')
    return redirect(reverse_lazy("home"))


class AccountPasswordResetView(View):

    def get(self, request, *args, **kwargs):
        form = AccountPasswordResetForm()
        html_template = loader.get_template('accounts/passwordreset.html')

        context = {
           'form': form,
           'segment': 'authentication'
        }
        return HttpResponse(html_template.render(context, request))

    def post(self, request, *args, **kwargs):
        form = AccountPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.data['email']
            account = Account.getAccount(email)
            if account is not None:
                Account.resetpassword(email)
                return redirect(reverse_lazy("auth_passwordresetdone"))
            else:
                messages.error(request, 'El correo electrónico no pertenece a una cuenta.')
        else:
            messages.error(request, f"Error en el formulario: {form.errors['email']}.")
        return redirect(reverse_lazy("home"))
    

class AccountPasswordResetDoneView(View):

    def get(self, request, *args, **kwargs):
        html_template = loader.get_template('accounts/passwordresetdone.html')

        context = {
           'segment': 'authentication'
        }
        return HttpResponse(html_template.render(context, request))


def register_view(request):
    error = None
    data = { }
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.data['username']
            data['username'] = username

            password = form.data['password1']
            
            confirm_password = form.data['password2']
            
            first_name = form.data['first_name']
            data['first_name'] = first_name

            last_name = form.data['last_name']
            data['last_name'] = last_name

            accept_conditions = False
            if form.data['accept_conditions'] == 'on':
                accept_conditions = True
            else:
                error = "No se ha aceptado las condiciones de manejo de datos."

            try:
                user = User.objects.get(username=username)
                error = 'Hay un usuario registrado con el usuario'
            except User.DoesNotExist:
                user = None

            if error is None:
                if password != confirm_password:
                    error = 'Las contraseñas no coinciden'

            if error is None:
                user = User.create_user(username, password, username)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False
                user.save()
    
                account = Account()
                account.user = user
                account.role = Role.objects.get(pk=RoleEnum.MEMBER) 
                account.accept_conditions = accept_conditions
                account.created_at = datetime.datetime.now()
                account.created_by = username
                account.save()

                account.send_register_message()

                messages.success (request, f'Cuenta {account} creada satisfactoriamente!')
                return redirect(reverse_lazy("home"))
        else:
            error = "¡Error en el registro de la cuenta!"

    form = RegistrationForm(initial=data)
    if error is not None:
        messages.error(request, error)
    context = { 'form': form, 'error': error }
    return render(request, 'accounts/register.html', context)


class AccountPasswordChangeView(View):

    def get(self, request, *args, **kwargs):
        form = AccountPasswordChangeForm(request.user)
        html_template = loader.get_template('accounts/passwordchange.html')

        context = {
           'form': form,
           'segment': 'authentication'
        }
        return HttpResponse(html_template.render(context, request))

    def post(self, request, *args, **kwargs):
        account = Account.getAccount(request.user)
        form = AccountPasswordChangeForm(request.user, request.POST)
        error = None
        if form.is_valid():
            old_password = form.data['old_password']
            new_password1 = form.data['new_password1']
            new_password2 = form.data['new_password2']

            if not account.check_password(old_password):
                error = "Contraseña ingresada no es válida"
            if error is None and new_password1 != new_password2:
                error = "La nueva contraseña y la confirmación no son iguales"
            
            if error is None:
                account.set_password(new_password1)
                return redirect(reverse_lazy("auth_passwordchangedone"))
        else:
            error = 'Error en el formulario.'
        html_template = loader.get_template('accounts/passwordchange.html')
        form = AccountPasswordChangeForm(request.user)
        context = {
           'form': form,
           'segment': 'authentication',
           'error': error
        }
        if error is not None:
            messages.error(request, error)

        return HttpResponse(html_template.render(context, request))


class AccountPasswordChangeDoneView(PasswordResetDoneView):
    template_name = 'accounts/passwordchangedone.html'


class AccountSetPasswordView(View):

    def post(self, request, *args, **kwargs):
        current_account = Account.getAccount(request.user)
        form = AdminSetPasswordForm(request.POST)
        error = None
        if form.is_valid():
            account_id = form.data['account']
            try:
                account = Account.objects.get(pk=account_id)
            except Account.DoesNotExist:
                error = "No existe la cuenta de usuario"
            new_password1 = form.data['new_password1']
            new_password2 = form.data['new_password2']

            if error is None and new_password1 != new_password2:
                error = "La nueva contraseña y la confirmación no son iguales"
            
            if error is None:
                account.set_password(new_password1)
                account.update_at = datetime.datetime.now()
                account.update_by = current_account.username
                account.save()
    
                messages.success(request, 'La contraseña fue actualizada satisfactoreamente')

                return redirect(reverse_lazy("auth_accounts"))
        else:
            error = 'Error en el formulario'
        if error:
            messages.error(request, error)

        return redirect(reverse_lazy("auth_accounts"))

@login_required(login_url="/auth/login/")
def account_index_view(request):
    data = { }
    page = 1
    if 'page' in request.GET.keys() and request.GET['page']:
        page = int(request.GET['page'])
    if 'page' in request.POST.keys() and request.POST['page']:
        page = int(request.POST['page'])
    
    account_list = Account.objects.all()
    user_list = User.objects.all()

    filter_form = AccountFilterForm(initial=data)
    if request.method == 'POST':
        filter_form = AccountFilterForm(request.POST)
        if filter_form.is_valid():
            try:
                page = int(filter_form.data['page'])
            except:
                pass
            search_text = filter_form.cleaned_data['search']
            state = filter_form.cleaned_data['state']
            city = filter_form.cleaned_data['city']
            role = filter_form.cleaned_data['role']
            is_active = filter_form.cleaned_data['is_active']
            is_active_data = filter_form.data['is_active']
            if is_active_data != 'unknown':
                user_list = user_list.filter(is_active=is_active)

            if search_text is not None and search_text != '':
                user_list = user_list.filter(Q(username__icontains=search_text) |
                                             Q(first_name__icontains=search_text) |
                                             Q(last_name__icontains=search_text))
            
            account_list = account_list.filter(user__in=user_list)
            if state is not None and state != '':
                account_list = account_list.filter(state=state)
            if city is not None and city != '':
                account_list = account_list.filter(city=city)
            if role is not None and role != '':
                account_list = account_list.filter(role=role)


    if 'state' in data.keys() and data['state'] is not None and data['state'] != '':
        filter_form.fields['city'].queryset = City.objects.filter(
        state=data['state']
    )
    setpassword_form = AdminSetPasswordForm()
    create_form = CreateAccountForm()
    paginator = getPaginator(account_list, page)

    context = {
        'table_title': 'Usuarios',
        'table_description': 'Administrador de Usuarios',
        'filter_form': filter_form,
        'setpassword_form': setpassword_form,
        'form': create_form,
        'paginator': paginator,
        'segment': 'authentication'
    }

    return render(request, 'accounts/index.html', context)


@login_required(login_url="/auth/login/")
def profile_account_view(request):
    current_account = Account.getAccount(request.user)
    error = None
    
    data = {}
    data['username'] = current_account.username
    data['role'] = current_account.role.id
    data['first_name'] = current_account.user.first_name
    data['last_name'] = current_account.user.last_name
    if current_account.genre is not None:
        data['genre'] = current_account.genre.id
    data['phone'] = current_account.phone
    data['whatsapp'] = current_account.whatsapp
    data['address'] = current_account.address
    if current_account.state is not None:
        data['state'] = current_account.state
    if current_account.city is not None:
        data['city'] = current_account.city

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            
            genre_id = form.data['genre']
            try:
                genre = Genre.objects.get(pk=genre_id)
            except Genre.DoesNotExist:
                genre = None

            phone = form.data['phone']
            whatsapp = form.data['whatsapp']
            address = form.data['address']
            
            state_id = form.data['state']
            state = None
            if state_id is not None and state_id != '':
                try:
                    state = State.objects.get(pk=state_id)
                except State.DoesNotExist:
                    state = None

            city_id = form.data['city']
            city = None
            if city_id is not None and city_id != '':
                try:
                    city = City.objects.get(pk=city_id)
                except City.DoesNotExist:
                    city = None

            if error is None:
                current_account.user.first_name = first_name
                current_account.user.last_name = last_name
                current_account.user.save()
                current_account.genre = genre
                current_account.address = address
                current_account.phone = phone
                current_account.whatsapp = whatsapp
                current_account.state = state
                current_account.city = city
                current_account.updated_at = datetime.datetime.now()
                current_account.updated_by = current_account.username
                current_account.save()

                messages.success (request, f'Cuenta {current_account} actualizada satisfactoriamente!')
                return redirect(reverse_lazy("home"))
        else:
            error = "¡Error en el registro de la cuenta!"
    form = ProfileForm(initial=data)
    
    if 'state' in data.keys() and data['state'] is not None and data['state'] != '':
        form.fields['city'].queryset = City.objects.filter(
        state=data['state']
    )

    context = { 'form': form, 'error': error }
    if error is not None:
        messages.error(request, error)

    return render(request, 'accounts/profile.html', context)


@login_required(login_url="/auth/login/")
def create_account_view(request):
    current_account = Account.getAccount(request.user)
    error = None
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            username = form.data['username']
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            
            genre_id = form.data['genre']
            genre = None
            if genre_id is not None and genre_id != '':
                try:
                    genre = Genre.objects.get(pk=genre_id)
                except Genre.DoesNotExist:
                    genre = None

            phone = form.data['phone']
            whatsapp = form.data['whatsapp']
            address = form.data['address']
            
            state = None
            state_id = form.data['state']
            state = None
            if state_id is not None and state_id != '':
                try:
                    state = State.objects.get(pk=state_id)
                except State.DoesNotExist:
                    state = None

            city_id = form.data['city']
            city = None
            if city_id is not None and city_id != '':
                try:
                    city = City.objects.get(pk=city_id)
                except City.DoesNotExist:
                    city = None

            role_id = form.data['role']
            try:
                role = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                role = Role.objects.get(pk=RoleEnum.MEMBER)

            try:
                user = User.objects.get(username=username)
                error = 'Hay un usuario registrado con el usuario'
            except User.DoesNotExist:
                user = None

            if error is None:
                user = User.create_user(username, '', username)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False
                user.save()
    
                account = Account()
                account.user = user
                account.role = role
                account.genre = genre
                account.address = address
                account.phone = phone
                account.whatsapp = whatsapp
                account.state = state
                account.city = city
                account.created_at = datetime.datetime.now()
                account.created_by = current_account.username
                account.save()

                account.send_register_message()

                messages.success(request, f'Cuenta {account} creada satisfactoriamente!')
                return redirect(reverse_lazy("auth_accounts"))
        else:
            error = "¡Error en el registro de la cuenta!"

    if error is not None:
        messages.error(request, error)

    return redirect(reverse_lazy("auth_accounts"))

@login_required(login_url="/auth/login/")
def edit_account_view(request, account_id):
    current_account = Account.getAccount(request.user)
    error = None
    try:
        account = Account.objects.get(pk=account_id)
        user = account.user
    except Account.DoesNotExist:
        error = 'No existe una cuenta con el id'
        account = None

    if error is None and request.method == 'POST':
        form = EditAccountForm(request.POST)
        if form.is_valid():
            first_name = form.data['first_name']
            last_name = form.data['last_name']
            
            genre_id = form.data['genre']
            genre = None
            if genre_id is not None and genre_id != '':
                try:
                    genre = Genre.objects.get(pk=genre_id)
                except Genre.DoesNotExist:
                    genre = None

            phone = form.data['phone']
            whatsapp = form.data['whatsapp']
            address = form.data['address']

            state_id = form.data['state']            
            state = None
            if state_id is not None and state_id != '':
                try:
                    state = State.objects.get(pk=state_id)
                except State.DoesNotExist:
                    state = None

            city_id = form.data['city']
            city = None
            if city_id is not None and city_id != '':
                try:
                    city = City.objects.get(pk=city_id)
                except City.DoesNotExist:
                    city = None

            role_id = form.data['role']
            try:
                role = Role.objects.get(pk=role_id)
            except Role.DoesNotExist:
                role = Role.objects.get(pk=RoleEnum.MEMBER)

            if error is None:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
    
                account.role = role
                account.genre = genre
                account.address = address
                account.phone = phone
                account.whatsapp = whatsapp
                account.state = state
                account.city = city
                account.updated_at = datetime.datetime.now()
                account.updated_by = current_account.username
                account.save()

                messages.success (request, f'Cuenta {account} actualizada satisfactoriamente!')
                return redirect(reverse_lazy("auth_accounts"))
        else:
            error = "¡Error en la actualización de la cuenta!"
    if error is not None:
        messages.error(request, error)
    return redirect(reverse_lazy("auth_accounts"))


@login_required(login_url="/accounts/login/")
def delete_account_view(request, account_id):
    current_account = Account.getAccount(request.user)
    error = None
    try:
        account = Account.objects.get(pk=account_id)
        user = account.user
    except Account.DoesNotExist:
        error = 'No existe una cuenta con el id'
        account = None

    if error is None and request.method == 'POST':
        user.delete()
        account.delete()
        messages.success (request, f'Cuenta {account} eliminada satisfactoriamente!')

    if error is not None:
        messages.error(request, error)
    return redirect(reverse_lazy("auth_accounts"))


@login_required(login_url="/accounts/login/")
def activate_account_view(request, account_id):
    current_account = Account.getAccount(request.user)
    error = None
    try:
        account = Account.objects.get(pk=account_id)
        user = account.user
    except Account.DoesNotExist:
        error = 'No existe una cuenta con el id'
        account = None

    if error is None:
        user.is_active = True
        user.save()

        account.update_by = current_account.username
        account.updated_at = datetime.datetime.now()
        account.save()
        
        messages.success (request, f'Cuenta {account} activada satisfactoriamente!')

    if error is not None:
        messages.error(request, error)
    return redirect(reverse_lazy("auth_accounts"))


@login_required(login_url="/accounts/login/")
def get_account_view(request, account_id):
    account = None
    account_data = {}
    try:
        account = Account.objects.get(pk=account_id)
        account_data['id'] = str(account.id)
        account_data['first_name'] = account.user.first_name
        account_data['last_name'] = account.user.last_name
        account_data['username'] = account.username
        account_data['phone'] = account.phone
        account_data['whatsapp'] = account.whatsapp
        account_data['address'] = account.address
        account_data['password1'] = ''
        account_data['password2'] = ''
        account_data['genre'] = ''
        if account.genre is not None:
            account_data['genre'] = account.genre.id
        account_data['state'] = ''
        if account.state is not None:
            account_data['state'] = str(account.state.id)
        account_data['city'] = ''
        if account.city is not None:
            account_data['city'] = str(account.city.id)
        account_data['role'] = account.role.id
    except Account.DoesNotExist:
        return account_data

    return JsonResponse(data=account_data)


class AccountConfirmDoneView(View):

    def get(self, request, token):
        error = None
        account, is_expired = Token.decode(token, delete=True)
        html_template = loader.get_template('accounts/registerdone.html')
        if account is not None:
            if not is_expired:
                account.user.is_active = True
                account.user.save()

                account.updated_at = datetime.datetime.now()
                account.updated_by = account.username
                account.save()
            else:
                error = 'El enlace ha expirado, debe solicitar uno nuevo.'
        else:
            error = 'El enlace tiene un error, revisa el correo de origen y copia el enlace directamente en la barra de dirección del navegador.'

        context = {
           'segment': 'authentication',
           'account': account,
           'is_expired': is_expired
        }
        if error is not None:
            messages.error(request, error)
        return HttpResponse(html_template.render(context, request))


class UserPasswordResetConfirmView(View):

    def get(self, request, token):
        account, is_expired = Token.decode(token, delete=False)
        html_template = loader.get_template('accounts/passwordresetconfirm.html')
        errors = None
        form = None
        if account is not None:
            if not is_expired:
                form = AccountSetPasswordForm(account.user)
            else:
                errors = { '_': 'El enlace ha expirado, debe solicitar uno nuevo.' } 
        else:
            errors = { '_': 'El enlace tiene un error, revisa el correo de origen y copia el enlace directamente en la barra de dirección del navegador.' }

        context = {
            'segment': 'authentication',
            'form': form,
            'account': account,
            'is_expired': is_expired,
            'errors': errors
        }
        
        return HttpResponse(html_template.render(context, request))

    def post(self, request, token):
        account, is_expired = Token.decode(token, delete=True)
        errors = None
        if account is not None:
            if not is_expired:
                form = AccountSetPasswordForm(account.user, request.POST)
                if form.is_valid():
                    password = form.data['new_password1']

                    account.set_password(password)
                    account.updated_at = datetime.datetime.now()
                    account.updated_by = account.username
                    account.save()
                    html_template = loader.get_template('accounts/passwordresetcomplete.html')
                else:
                    errors = form.errors
            else:
                errors = { '_': 'El enlace ha expirado, debe solicitar uno nuevo.' } 
        else:
            errors = { '_': 'El enlace tiene un error, revisa el correo de origen y copia el enlace directamente en la barra de dirección del navegador.' }
        if errors is not None:
            html_template = loader.get_template('accounts/passwordresetconfirm.html')
            form = AccountSetPasswordForm(account.user)
        context = {
           'segment': 'authentication',
           'account': account,
           'is_expired': is_expired,
           'form': form,
           'errors': errors
        }
        
        return HttpResponse(html_template.render(context, request))

class AccountGenerateConfirmView(View):

    def get(self, request, account_id):
        account = Account.objects.get(pk=account_id)
        account.send_register_message()

        messages.success (request, f'Cuenta {account} creada satisfactoriamente!')

        return redirect(reverse_lazy("home"))        

