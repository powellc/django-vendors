import datetime
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from django.http import Http404

from vendors.models import Vendor, Application, VendorType
from vendors.forms import VendorForm, ApplicationForm

class VendorApplicationList(ListView):

    def get_queryset(self):
        vendor= get_object_or_404(Vendor, slug__iexact=self.kwargs['slug'])
        if self.request.user == vendor.owner:
            return Application.objects.filter(vendor=vendor)
        else:
            raise Http404

class VendorApplicationForm(CreateView):

    def get_form_class(self):
        vendor= get_object_or_404(Vendor, slug__iexact=self.kwargs['slug'])
        if self.request.user == vendor.owner:
            return ApplicationForm
        else:
            raise Http404

class VendorApplicationDetail(DetailView):
    model=Application

    def get_queryset(self):
        vendor= get_object_or_404(Vendor, slug__iexact=self.kwargs['slug'])
        if self.request.user == vendor.owner:
            return ApplicationForm
        else:
            raise Http404
