from django.conf.urls import patterns, url
from erc_app import views, forms
from erc_app.views import BakshiWizard, FORMS

urlpatterns = patterns('',
	url(r'^next$', BakshiWizard.as_view(FORMS)),
)
