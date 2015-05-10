from django.conf.urls import patterns, include, url
from erc_app.views import BakshiWizard, FORMS

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^$', BakshiWizard.as_view(FORMS)),
  url(r'^admin/', include(admin.site.urls)),
)
