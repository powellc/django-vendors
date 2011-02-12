from django.conf.urls.defaults import *
from vendors import views
from vendors.forms import VendorForm, ApplicationForm

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object
from django.shortcuts import get_list_or_404, get_object_or_404

''' 
Custom vendor views

These allow for:
  * public viewing of vendor profiles
  * private creation of a new profile
  * private submission of an application
  * private checking of application status
  * private editing of profile
  * private deletion of profile

The idea here is to wire them all to something like:
    vendors/
        <type>/
        edit/<slug>/
        delete/<slug>/
        create/
        <slug>/
            applications/
                edit/<year>
                delete/<year>
                create
                <year>

'''
urlpatterns = patterns('vendors.views',
    url(r'^$', object_list(request, queryset=get_list_or_404(Vendor, public=True)), name="vendor_list"), # List all public vendors
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_detail  name="vendor_detail"), # Display a vendor profile
    url(r'^signup/$', create_object(request, form_class=VendorForm, login_required=True), name="vendor_signup"), # Signup as a new vendor
    url(r'^(?P<slug>[-\w]+)/edit/$', update_object(request, form_class=VendorForm, login_required=True, slug=slug, slug_field='slug'), name="vendor_edit"), # Edit your vendor profile
    url(r'^(?P<slug>[-\w]+/delete/$', delete_object(request, Vendor, slug=slug, post_delete_redirect="/"), name="vendor_delete"), # Delete your vendor profile
    url(r'^(?P<slug>[-\w]+)/applications/$', view=views.vendor_application_list, name="vendor_application_list"), # Display a  list of apps for the vendor <slug>
    url(r'^(?P<slug>[-\w]+)/applications/new/$', create_object(request, form_class=ApplicationForm, login_required=True), name="application_create"), # Create a new app
    # NOTE: YOU  HAVE TO MOVE THE TWO BELOW TO THE VIEW FILE, AS YOU HAVE TO LOOK UP BOTH SLUG and YEAR!
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/edit/$', update_object(request, form_class=AppicationForm, login_required=True, slug=slug), name="application_edit"), # Edit an application (not sure if it's a good idea...)
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/delete/$', delete_object(request, Application, slug=slug, post_delete_redirect="/") , name="application_delete"), # Delete an application 
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/$', view=views.application_detail, name="application_detail"), # View an appliction
    url(r'^/applications/$', view=views.application_index, name="application_index"), # An admin-only index of all apps submitted
    # VENDOR TYPES
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_type_detail, name="vendor_type_detail"), # List all vendors of type <type>
)
