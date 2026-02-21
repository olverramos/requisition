from modules.auths.models import Account
from modules.menu.models import Option
from django.utils import timezone
from django.conf import settings


def generic_variables(request):
    account = None
    menu = []
    
    if request.user.is_authenticated:
        account = Account.getAccount(request.user)
        
        if account:
            menu = Option.getMenu(account)
    
    return {    
        'ACCOUNT': account,
        'CURRENT_YEAR': timezone.now().strftime("%Y"),
        'TODAY': timezone.now().strftime("%Y-%m-%d"),
        'APP_NAME': settings.APP_NAME,
        'COMERCIAL_APP_NAME': settings.COMERCIAL_APP_NAME,
        'COMPANY_NAME': settings.COMPANY_NAME,
        'APP_URL': settings.APP_URL,
        'STATIC_URL': settings.STATIC_URL,
        'VERSION': settings.VERSION,
        'ENVIRONMENT': settings.ENVIRONMENT,
        'MENU': menu
    }
