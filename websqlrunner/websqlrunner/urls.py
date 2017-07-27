from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from . import views

urlpatterns = [
    url(r"^$", views.homepage, name="home"),
#    url(r"^save_script", views.homepage, name="save_script"),
    url(r"^scripts", views.scripts, name="scripts"),
#    url(r"^createrun/(?P<script_id>[0-9]+)/$", views.create_run, name="create_run"),
    url(r"^run/(?P<script_id>[0-9]+)", views.run, name="run"),
    url(r"^runs", views.runs, name="runs"),
#    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
