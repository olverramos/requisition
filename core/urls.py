from django.urls import path, include
from django_mongoengine import mongo_admin
from home import views

urlpatterns = [
    path("admin/", mongo_admin.site.urls),
    
    path('', views.HomeView.as_view(), name='home'),

    path("auth/", include('modules.authentication.urls')),
    path("localization/", include('modules.localization.urls')),
    path("base/", include('modules.base.urls')),
    # path("community/", include('modules.community.urls')),
    # path("ap/", include('modules.payments.urls')),

    path("demo/", include('theme_soft_design.urls')),
    
    path(".well-known/acme-challenge/Wa-TAMtdo-z8DSbMPQFlw1AZSCSiUHitYjPE0SpZFcM", views.domainfile)
]
