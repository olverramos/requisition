# from modules.community.models import Community, CommunityMember
from modules.localization.models import Country, State, City
from modules.authentication.models import Account
# from modules.bussiness.models import Category
# from mongoengine.queryset.visitor import Q
from fileprovider.utils import sendfile  
from django.views.generic import View
from django.http import HttpResponse
from django.template import loader
from django.conf import settings


class HomeView(View):

    def get(self, request, *args, **kwargs):

        current_account = Account.getAccount(request.user)

        country = None
        try:
            country = Country.objects.get(pk=settings.COUNTRY)
        except Country.DoesNotExist:
            country = None
        
        # category_list = Category.objects.all()
        # state_list = State.objects.filter(country=country)
        # city_list = City.objects.filter(country=country)

        # community_list = Community.objects.filter(is_active=True)
        # if current_account is not None:
        #     my_community_list = CommunityMember.objects.filter(
        #         member=current_account, 
        #         is_active=True,
        #         is_autorized=True
        #     ).values_list('community')   

        #     community_flat_list = [community.id for community in my_community_list]

        #     community_list = community_list.filter(
        #         pk__in=community_flat_list
        #     )
        # else:
        #     community_list = community_list.filter(
        #         community_type='OPEN'
        #     )
        
        context = {
            'segment': 'index',
            # 'state_list': state_list,
            # 'city_list': city_list,
            # 'community_list': community_list,
            # 'category_list': category_list,
        }

        html_template = loader.get_template('home.html')
        return HttpResponse(html_template.render(context, request))

def domainfile(request):
    return sendfile('/app/staticfiles/file/Wa-TAMtdo-z8DSbMPQFlw1AZSCSiUHitYjPE0SpZFcM')
