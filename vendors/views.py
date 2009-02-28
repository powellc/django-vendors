from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from vendors.forms import VendorForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

import datetime

def vendor_index(request):
    vendors=Vendor.objects.filter(public=True)
    return render_to_response('vendors/vendor_index.html', locals(),
                              context_instance=RequestContext(request))

def vendor_detail(request, slug):
    vendor=Vendor.public_objects.get(slug__exact=slug)
    return render_to_response('vendors/vendor_detail.html', locals(),
                              context_instance=RequestContext(request))


@login_required
def vendor_create(request):
    form=VendorForm(request.POST or None)
    if form.is_valid():
        vendor=form.save(commit=False)
        vendor.owner=request.user
	vendor.slug=slugify(vendor.name)
        vendor.save()
        return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))

    return render_to_response('vendors/vendor_create.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def vendor_edit(request, slug):
    pass
