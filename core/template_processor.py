import datetime
from django.conf import settings
from modules.authentication.models import Account

def generic_variables(request):
    account = None
    if request.user.is_authenticated:
        account = Account.getAccount(request.user)
    return {    
                'ACCOUNT': account,
                'CURRENT_YEAR': datetime.date.today().strftime("%Y"),
                'APP_NAME': settings.APP_NAME,
                'COMERCIAL_APP_NAME': settings.COMERCIAL_APP_NAME,
                'APP_VERSION': settings.APP_VERSION,
                'APP_URL': settings.APP_URL,
                'STATIC_URL': settings.STATIC_URL,
                'ENTERPRISE': settings.ENTERPRISE,
            }
