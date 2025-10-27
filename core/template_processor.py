import datetime
from django.conf import settings
from modules.authentication.models import Account

def generic_variables(request):
    account = None
    if request.user.is_authenticated:
        account = Account.getAccount(request.user)
    
    menu_list = {
        'admin': [
            {
                'url': 'auth_accounts',
                'title': 'Usuarios'
            },
            {
                'url': 'parameters_ramos',
                'title': 'Ramos'
            },
            {
                'url': 'base_applicants',
                'title': 'Solicitantes'
            },
            {
                'url': 'base_takers',
                'title': 'Tomadores'
            },
        ]
    }

    return {    
                'ACCOUNT': account,
                'CURRENT_YEAR': datetime.date.today().strftime("%Y"),
                'TODAY': datetime.date.today().strftime("%Y-%m-%d"),
                'APP_NAME': settings.APP_NAME,
                'COMERCIAL_APP_NAME': settings.COMERCIAL_APP_NAME,
                'APP_VERSION': settings.APP_VERSION,
                'APP_URL': settings.APP_URL,
                'STATIC_URL': settings.STATIC_URL,
                'ENVIRONMENT': settings.ENVIRONMENT,
                'ENTERPRISE': settings.ENTERPRISE,
                'MENU': menu_list
            }
