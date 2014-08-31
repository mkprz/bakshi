from django.conf.urls import patterns, url
from erc_app import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^?P<interview_id>\d+)/query_response/$', views.query, name='query_response')
)
