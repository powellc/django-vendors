from django.conf import settings
from django.conf.urls.defaults import *
from vendors import views
from vendors.models import Vendor
from tagging.views import tagged_object_list


# custom views vendors
urlpatterns = patterns('vendors.views',
    url(r'^$', view=views.vendor_index, name="vendor_index"),
    url(r'^create$', view=views.vendor_create, name="vendor_create"),
    #url(r'^products/$', view=views.vendor_tags, name="vendor_tag_list"),
    #url(r'^product/(?P<tag>[-_A-Za-z0-9]+)/$', view=views.vendors_with_tag, name="vendors_with_tag"), 
    #url(r'^product/(?P<tag>[-_A-Za-z0-9]+)/page/(?P<page>d+)/$', view=views.vendors_with_tag, name="vendors_with_tags_pages" ),
    url(r'^(?P<slug>[-\w]+)/edit/$', view=views.vendor_edit, name="vendor_edit"),
    url(r'^(?P<slug>[-\w]+)/signup/$', view=views.vendor_signup, name="vendor_signup"),
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_detail, name="vendor_detail"),
)
