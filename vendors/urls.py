from django.conf.urls.defaults import *
from vendors import views

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
    url(r'^$', view=views.vendor_index, name="vendor_index"), # List all vendors
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_detail, name="vendor_detail"), # Display a vendor profile
    #PRIVATE
    url(r'^signup$', view=views.vendor_signup, name="vendor_signup"), # Signup as a new vendor
    url(r'^(?P<slug>[-\w]+)/edit/$', view=views.vendor_edit, name="vendor_edit"), # Edit your vendor profile
    url(r'^(?P<slug>[-\w]+/delete/$', view=views.vendor_delete, name="vendor_delete"), # Delete your vendor profile
    url(r'^(?P<slug>[-\w]+)/applications/$', view=views.application_vendor_index, name="application_vendor_index"), # Display a  list of apps for the vendor <slug>
    url(r'^(?P<slug>[-\w]+)/applications/new/$', view=views.application_create, name="application_create"), # Create a new app
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/edit/$', view=views.application_edit, name="application_edit"), # Edit an application (not sure if it's a good idea...)
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/delete/$', view=views.application_delete, name="application_delete"), # Delete an application 
    url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/$', view=views.application_detail, name="application_detail"), # View an appliction
    url(r'^/applications/$', view=views.application_index, name="application_index"), # An admin-only index of all apps submitted
    # VENDOR TYPES
    url(r'^(?P<slug>[-\w]+)/$', view=views.vendor_type_detail, name="vendor_type_detail"), # List all vendors of type <type>
)
