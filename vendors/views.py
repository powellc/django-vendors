import datetime
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings

from vendors.models import Vendor, Application, VendorType
from vendors.forms import VendorForm, MarketSignUpForm

def vendor_detail(request, slug):
    if request.user.is_authenticated(): # If this user has an account that matches the vendor, let them at it
        vendor = get_object_or_404(Vendor, slug=slug)
        if vendor.owner == request.user:
            qs=Vendor.objects.all()
        else:
            qs=Vendor.public_objects.all()
    else:
        qs=Vendor.public_objects.all()
    try:
        key=settings.GOOGLE_API_KEY
    except:
        key=''
    return object_detail(request, queryset=qs, slug=slug, extra_context={'google_api_key': key})


@login_required
def vendor_application_list(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    if request.user == vendor.owner:
        return object_list(request, queryset=Application.objects.filter(vendor=vendor))
    else:
        raise Http404

'''@login_required
def vendor_signup(request, slug):
    if slug is not None:
        instance = Vendor.objects.get(slug__exact=slug)
        
    if request.method == 'POST':
        form=MarketSignUpForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vendor_detail', args=[instance.slug]))
    else:
        form = MarketSignUpForm(instance=instance)
        
    return render_to_response('vendors/vendor_signup.html', locals(),
                              context_instance=RequestContext(request))
                              '''
