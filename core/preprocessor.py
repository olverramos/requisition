from modules.auths.models import Account
from modules.menu.models import Option
from django.conf import settings
import datetime as dt

def generic_variables(request):
    account = None
    if request.user.is_authenticated:
        account = Account.getAccount(request.user)
    
    menu_list = Option.getMenu(account)

    return {    
        'ACCOUNT': account,
        'CURRENT_YEAR': dt.date.today().strftime("%Y"),
        'TODAY': dt.date.today().strftime("%Y-%m-%d"),
        'APP_NAME': settings.APP_NAME,
        'COMERCIAL_APP_NAME': settings.COMERCIAL_APP_NAME,
        'APP_VERSION': settings.APP_VERSION,
        'APP_URL': settings.APP_URL,
        'STATIC_URL': settings.STATIC_URL,
        'ENVIRONMENT': settings.ENVIRONMENT,
        'ENTERPRISE': settings.ENTERPRISE,
        'MENU': menu_list
    }
