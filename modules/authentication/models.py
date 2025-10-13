from django_mongoengine.mongo_auth.models import User
from modules.localization.models import State, City
from django_mongoengine import Document, fields
from core.utils import send_basic_mail
from django.conf import settings
from enum import StrEnum
import pyshorteners
import mongoengine
import datetime
import base64
import json

module_folder = 'modules/authentication'


class Genre(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    
    meta = {
        'collection': 'authentication_genre',
        'indexes': [
            ('name',), 
        ]
    }
    
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


class RoleEnum(StrEnum):
    ADMIN = 'admin'
    ASSISTANT = 'assitant'


class Role(Document):
    id = fields.StringField(verbose_name='ID', primary_key=True, max_length=10)
    name = fields.StringField(max_length=100, verbose_name='Nombre')
    
    meta = {
        'collection': 'authentication_role',
        'indexes': [
            ('name',), 
        ]
    }
    
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

class Account(Document):
    user = fields.ReferenceField(User, verbose_name="Usuario", unique=True, reverse_delete_rule=mongoengine.CASCADE)
    genre = fields.ReferenceField(Genre, verbose_name="Género", null=True, blank=True, reverse_delete_rule=mongoengine.NULLIFY)
    role = fields.ReferenceField(Role, verbose_name="Rol", reverse_delete_rule=mongoengine.DENY)
    address = fields.StringField(verbose_name='Dirección', null=True, blank=True, max_length=255)
    phone = fields.StringField(verbose_name='Telefono', null=True, blank=True, max_length=20)
    whatsapp = fields.StringField(verbose_name='Whatsapp', null=True, blank=True, max_length=20)
    state = fields.ReferenceField(State, verbose_name="Departamento", null=True, blank=True, reverse_delete_rule=mongoengine.NULLIFY)
    city = fields.ReferenceField(City, verbose_name="Ciudad", null=True, blank=True, reverse_delete_rule=mongoengine.NULLIFY)
    created_at = fields.DateTimeField(verbose_name="Fecha Creación", null=True, blank=True)
    created_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)
    updated_at = fields.DateTimeField(verbose_name="Fecha Actualización", null=True, blank=True)
    updated_by = fields.StringField(verbose_name='Creado por', max_length=50, null=True, blank=True)

    meta = {
        'collection': 'authentication_accounts',
    }
    
    def __str__(self):
        return f"{self.user.username}"
    
    @staticmethod
    def getAccount(userdata: User | str):
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
            # template_id = settings.SENDGRID_TEMPLATES['PASSWORD_RESET']

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

    def send_register_message(self):
        # template_id = settings.SENDGRID_TEMPLATES['REGISTER']

        confirm_url = settings.APP_URL
        confirm_url += 'auth/accounts/'
        confirm_url += Token.generate(self)
        confirm_url += '/confirm/'      
        try:
            s = pyshorteners.Shortener()
            confirm_short_url = s.tinyurl.short(confirm_url)
        except:
            confirm_short_url = confirm_url

        context = {
            'complete_name': self.complete_name,
            'confirm_url': confirm_short_url
        }

        from_email = 'comunidades@arvii.com.co'
        html_template = 'mailing/createaccount.html'
        text_template = 'mailing/createaccount.txt'
        message_data= {
            'subject': f'{self.complete_name}, Bienvenido(a) a Arvii Comunidades.',
            'from_email': from_email,
            'to_email': [self.username]
        }
        send_basic_mail(message_data, 
                        context=context,
                        html_template=html_template,
                        text_template=text_template,
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
        app_label = 'authentication'



class Token(Document):
    token = fields.StringField(verbose_name='Valor')
    times = fields.IntField(verbose_name='Validaciones')
    max_times = fields.IntField(verbose_name='Máximo de Validaciones')
    
    meta = {
        'collection': 'authentication_token',
        'indexes': [
            ('token',), 
        ]
    }
    
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
