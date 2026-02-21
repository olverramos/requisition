# from modules.localization.models import State, City
from django.contrib.auth.models import User
from core.utils import send_basic_mail
from django.conf import settings
from django.db import models
from enum import StrEnum
import pyshorteners
import datetime
import base64
import json

module_folder = 'modules/auths'

 
class Genre(models.Model):
    id = models.CharField(verbose_name='ID', max_length=10, primary_key=True)
    name = models.CharField(verbose_name='Nombre', max_length=50)
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/genres.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            genre = Genre.objects.get(pk=data["id"])
                        except Genre.DoesNotExist:
                            genre = Genre()
                            genre.id = data['id']
                            genre.name = data['name']
                            genre.save()

                            print (f'Género {genre} creado')

        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'auths'
        db_table = 'auths_genres'
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'
        ordering = ['name']

    
class RoleEnum(StrEnum):
    ADMIN = 'admin'
    ASSISTANT = 'assitant'
    APPLICANT = 'applicant'


class Role(models.Model):
    id = models.CharField(verbose_name='ID', max_length=10, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    
    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/roles.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    if 'id' in data.keys() and 'name' in data.keys():
                        try:
                            role = Role.objects.get(pk=data["id"])
                        except Role.DoesNotExist:
                            role = Role()
                            role.id = data['id']
                            role.name = data['name']
                            role.save()

                            print (f'Rol {role} creado')
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'auths'
        db_table = 'auths_roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['name']


class Account(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuario", unique=True, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name="Género", null=True, blank=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, verbose_name="Rol", on_delete=models.PROTECT)
    address = models.CharField(verbose_name='Dirección', null=True, blank=True, max_length=255)
    phone = models.CharField(verbose_name='Telefono', null=True, blank=True, max_length=20)
    whatsapp = models.CharField(verbose_name='Whatsapp', null=True, blank=True, max_length=20)
    state = models.ForeignKey('localization.State', verbose_name="Departamento", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('localization.City', verbose_name="Ciudad", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(verbose_name="Fecha Creación", auto_now_add=True)
    created_by = models.CharField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name="Fecha Actualización", auto_now=True)
    updated_by = models.CharField(verbose_name='Actualizado por', max_length=50, null=True, blank=True)
   
    def __str__(self):
        return f"{self.user.username}"
    
    @staticmethod
    def getAccount(userdata: User | str | None):
        account = None
        if type(userdata) == str:
            try:
                user = User.objects.get(username=userdata)
            except User.DoesNotExist:
                return None
        else:
            user = userdata
        if user is not None and user.username != '':
            try:
                account = Account.objects.get(user=user)
            except Account.DoesNotExist:
                account = None

        return account
    
    @property
    def username(self):
        if self.user is not None:
            return self.user.username
        return None
    
    @property
    def complete_name(self):
        if self.user is not None:
            return self.user.get_full_name()
        return None
    
    def set_password(self, raw_password):
        self.user.set_password(raw_password)
        self.user.save()

    @property
    def first_name(self):
        if self.user is not None:
            return self.user.first_name
        return None
    
    @property
    def last_name(self):
        if self.user is not None:
            return self.user.last_name
        return None
    
    @property
    def is_active(self):
        return self.user.is_active
    
    @is_active.setter
    def is_active(self, value):
        self.user.is_active = value

    def check_password(self, raw_password):
        return self.user.check_password(raw_password)

    @staticmethod
    def resetpassword(email):
        account = Account.getAccount(email)
        if account is not None:
            reset_password_url = settings.APP_URL
            reset_password_url += 'auth/passwordresetconfirm/'
            reset_password_url += Token.generate(account, 2)
            reset_password_url += '/'

            try:
                s = pyshorteners.Shortener()
                reset_password_short_url = s.tinyurl.short(reset_password_url)
            except:
                reset_password_short_url = reset_password_url

            context = {
                'complete_name': account.complete_name,
                'reset_password_url': reset_password_short_url
            }
            from_email = 'comunidades@arvii.com.co'
            html_template = 'mailing/passwordreset.html'
            text_template = 'mailing/passwordreset.txt'
            message_data= {
                'subject': f'{account.complete_name}, Reinicio de Contraseña.',
                'from_email': from_email,
                'to_email': [account.username]
            }
            send_basic_mail(message_data, 
                            context=context,
                            html_template=html_template,
                            text_template=text_template
                        )

    def send_register_message(self, role_description=None):
        confirm_url = settings.APP_URL
        confirm_url += 'auths/accounts/'
        confirm_url += Token.generate(self)
        confirm_url += '/confirm/'      
        try:
            s = pyshorteners.Shortener()
            confirm_short_url = s.tinyurl.short(confirm_url)
        except:
            confirm_short_url = confirm_url

        context = {
            'client_name': self.client.name,
            'complete_name': self.complete_name,
            'confirm_url': confirm_short_url,
            'role_description': role_description if role_description else 'usuarios'
        }

        from_email = 'comunidades@arvii.com.co'
        html_template = 'mailing/register.html'
        text_template = 'mailing/register.txt'
        message_data= {
            'subject': f'{self.complete_name}, Registro de Cuenta.',
            'from_email': from_email,
            'to_email': [self.email]
        }

        send_basic_mail(
            message_data,
            context=context,
            html_template=html_template,
            text_template=text_template
        )

    @staticmethod
    def init_table():
        try:
            with open(f'{module_folder}/scripts/data/accounts.json') as data_fp:
                data_list = json.load(data_fp)
                for data in data_list:
                    user = None
                    if 'username' in data.keys():
                        try:
                            user = User.objects.get(username=data["username"])
                        except User.DoesNotExist:
                            user = None

                        role = Role.objects.get(pk=RoleEnum.ASSISTANT)
                        if 'role_id' in data.keys() and data['role_id']:
                            role_id = data['role_id']
                            try:
                                role = Role.objects.get(pk=role_id)
                            except Role.DoesNotExist:
                                pass
                            
                        if user is None and \
                            'username' in data.keys() and data['username'] and \
                            'password' in data.keys() and data['password']:

                            user = User.create_user(data['username'], data['password'], data['username'])
                            user.first_name = data['first_name']
                            user.last_name = data['last_name']
                            user.is_active = True
                            if role.id == RoleEnum.ADMIN:
                                user.is_staff = True
                                user.is_superuser = True
                            user.save()
                        
                        try:
                            account = Account.objects.get(user=user)
                        except Account.DoesNotExist:
                            account = None
                        
                        if account is None:
                            account = Account()
                            account.user = user
                            account.address = data['address']
                            account.role = role
                            account.phone = data['phone']
                            account.whatsapp = data['whatsapp']

                            if 'genre_id' in data.keys() and data['genre_id']:
                                genre_id = data['genre_id']
                                try:
                                    account.genre = Genre.objects.get(pk=genre_id)
                                except Genre.DoesNotExist:
                                    account.genre = None
                            
                            if 'state_code' in data.keys() and data['state_code']:
                                state_code = data['state_code']
                                try:
                                    account.state = State.objects.get(country=settings.COUNTRY, code=state_code)
                                except State.DoesNotExist:
                                    account.state = None
                            
                            if 'city_code' in data.keys() and data['city_code']:
                                city_code = data['city_code']
                                try:
                                    account.city = City.objects.get(country=settings.COUNTRY, code=city_code)
                                except City.DoesNotExist:
                                    account.city = None
                            account.created_at = datetime.datetime.now()
                            account.save()

                            print (f'Cuenta {account} creada')
        except FileNotFoundError:
            pass

    class Meta:
        app_label = 'auths'
        db_table = 'auths_accounts'
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['user']


class Token(models.Model):
    token = models.CharField(verbose_name='Valor', max_length=255)
    times = models.IntegerField(verbose_name='Validaciones')
    max_times = models.IntegerField(verbose_name='Máximo de Validaciones')
    
    
    def __str__(self):
        return f"{self.token}"
    
    @staticmethod
    def generate(account, max_times=1):
        generate_at = datetime.datetime.now()
        expires_at = generate_at + datetime.timedelta(hours=24)
        token_data = f'{account.id}|{expires_at.strftime("%Y%m%d%H%M%S")}'
        token_bytes = token_data.encode('ascii')
        token_encoded = base64.b64encode(token_bytes)
        token = token_encoded.decode('ascii')

        token_object = Token()
        token_object.token = token
        token_object.times = 0
        token_object.max_times = max_times
        token_object.save()

        return token

    @staticmethod
    def decode(token, delete=False):
        base64_bytes = token.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        token_data = message_bytes.decode('ascii')
        userid, expire_str = token_data.split('|')
        try:
            expire_at = datetime.datetime.strptime(expire_str, "%Y%m%d%H%M%S")
        except ValueError:
            return None, True

        account = None
       
        try:
            account_id = userid
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return None, True

        if datetime.datetime.now() > expire_at:
            print('Expiró el token')
            return account, True

        try:
            token_object = Token.objects.get(token=token)
        except Token.DoesNotExist:
            print('Token ya usado')
            return account, True
        
        if delete:
            token_object.delete()

        return account, False

    class Meta:
        app_label = 'auths'
        db_table = 'auths_tokens'
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['token']
