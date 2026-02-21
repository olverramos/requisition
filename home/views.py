from modules.localization.models import Country, State, City
from modules.operative.forms import SearchRequestForm
from modules.operative.models import OperativeRequest
from django.http import HttpResponse, JsonResponse
from modules.parameters.models import Ramo
from fileprovider.utils import sendfile  
from django.views.generic import View
from django.template import loader
from django.conf import settings
from modules.auths.models import Account


class Home(View):

    def get(self, request, *args, **kwargs):
        current_account = None
        current_account = Account.getAccount(request.user)
        filter_form = SearchRequestForm()
        
        context = {
            'segment': 'index',
            'filter_form': filter_form,
            'current_account': current_account,
        }

        html_template = loader.get_template('home.html')
        return HttpResponse(
            html_template.render(
                context, 
                request
            )
        )

def domainfile(request):
    return sendfile('/app/staticfiles/file/Wa-TAMtdo-z8DSbMPQFlw1AZSCSiUHitYjPE0SpZFcM')

def devtools_json(request):
    # Replace with your actual project path and a unique UUID
    data = {
        "uuid": settings.SECRET_KEY,
        "paths": [str(settings.BASE_DIR)] 
    }
    return JsonResponse(data)