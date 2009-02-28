from django.conf import settings
from django.conf.urls.defaults import *
from vendors import views

# custom views vendors
urlpatterns = patterns('vendors.views',
    url(r'^$', view=views.vendor_index, name="vendor_index"),
    url(r'^create$', view=views.vendor_create, name="vendor_create"),
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_detail, name="vendor_detail"),
    url(r'^(?P<slug>[-\w]+)/edit', view=views.vendor_edit, name="vendor_edit"),
)
