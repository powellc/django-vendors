from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required 

from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from vendors.models import Vendor
from vendors.forms import VendorForm, ApplicationForm
from vendors.views import VendorApplicationList#, AdminApplicationList

urlpatterns = patterns('',
    url(r'^$', 
        ListView.as_view(
            queryset=Vendor.public_objects.all()),
            name="vendor-list",
        ),
    url(r'^(?P<slug>[-\w]+)/$',
        DetailView.as_view(
            model=Vendor, 
            queryset=Vendor.public_objects.all()),
            name="vendor-detail",
        ),
    url(r'^signup/$', 
        login_required(CreateView.as_view(
            form_class=VendorForm,)),
            name="vendor-signup",
        ), # Signup as a new vendor
    url(r'^(?P<slug>[-\w]+)/edit/$', 
        login_required(UpdateView.as_view(
            model=Vendor,
            form_class=VendorForm, 
            slug_field='slug', )),
            name="vendor-edit",
        ), # Edit your vendor profile
    url(r'^(?P<slug>[-\w]+)/delete/$', 
        login_required(DeleteView.as_view(
            model=Vendor, )),
            name="vendor-delete",
       ), # Delete your vendor profile

    # Having to do with applications for vendors
    #url(r'^(?P<slug>[-\w]+)/applications/$', 
    #    login_required(VendorApplicationList.as_view(
    #        name="vendor-application-list",
    #    ))),
    url(r'^(?P<slug>[-\w]+)/applications/create/$', 
        login_required(CreateView.as_view(
            form_class=ApplicationForm)),
            name="vendor-application-create",
        ),
    #url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/$', 
    #    login_required(VendorApplicationDetail.as_view(
    #        slug_field='year',)),
    #        name="vendor-application_detail"), # View an appliction
    #url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/edit/$', 
    #    login_required(VendorApplicationUpdate.as_view(
    #        form_class=AppicationForm, 
    #        slug_field='slug',)),
    #        name="vendor-application-edit"), # Edit an application (not sure if it's a good idea...)
    #url(r'^(?P<slug>[-\w]+)/applications/(?P<year>\d{4})/delete/$', 
    #    login_required(VendorApplicationDelete.as_view()),
    #        name="vendor-application-delete"), # Delete an application 
)
