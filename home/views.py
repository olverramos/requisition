from modules.localization.models import Country, State, City
from modules.operative.forms import SearchRequestForm
from modules.operative.models import OperativeRequest
from modules.authentication.models import Account
# from mongoengine.queryset.visitor import Q
from modules.parameters.models import Ramo
from fileprovider.utils import sendfile  
from django.views.generic import View
from django.http import HttpResponse
from django.template import loader
from django.conf import settings


class HomeView(View):

    def get(self, request, *args, **kwargs):

        current_account = Account.getAccount(request.user)

        form = SearchRequestForm()
        
        context = {
            'segment': 'index',
            'form': form,
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
