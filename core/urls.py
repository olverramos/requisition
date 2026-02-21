"""
URL configuration for needsworkflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from home import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("auth/", include('modules.auths.urls')),
    path("localization/", include("modules.localization.urls")),
    # path("parameters/", include("modules.parameters.urls")),
    # path("base/", include("modules.base.urls")),
    # path("operative/", include("modules.operative.urls")),
    # path("demo/", include('theme_soft_design.urls')),
    path("admin/", admin.site.urls),
    # path(".well-known/acme-challenge/Wa-TAMtdo-z8DSbMPQFlw1AZSCSiUHitYjPE0SpZFcM", views.domainfile),
    # path('.well-known/appspecific/com.chrome.devtools.json', views.devtools_json),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
