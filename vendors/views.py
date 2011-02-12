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

from vendors.models import Vendor, Application, VendorType, A
from vendors.forms import VendorForm, MarketSignUpForm

def vendor_list(request):
    vendors=get_list_or_404(Vendor, public=True)
    return object_list(request, queryset=vendors)

def vendor_detail(request, slug):
    if request.user.is_authenticated(): # If this user has an account, let them at it
        qs=Vendor.objects.all()
    else:
        qs=Vendor.public.all()

    return object_detail(request, queryset=qs, slug=slug,
                         extra_content={'google_api_key': settings.GOOGLE_API_KEY})

def vendor_create(request):
    return create_object(request, form_class=VendorForm, login_required=True)

@login_required
def vendor_edit(request, slug):
    vendor = None
    if slug is not None:
        vendor = get_object_or_404(slug__exact=slug, owner=request.user)
    if request.method == 'POST':
        form=VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))
    else:
        form = VendorForm(instance=vendor)
        
    return render_to_response('vendors/vendor_edit.html', locals(),
                              context_instance=RequestContext(request))

    '''
@login_required
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

@login_required
def application_create(request):
    form=ApplicationForm(request.POST or None)
    if form.is_valid():
        application=form.save(commit=False)
        application.status=ApplicationStatus.objects.get(slug='created')
        application.save()
        return HttpResponseRedirect(reverse('application_detail', args=[application.vendor.slug]))

    return render_to_response('vendors/application_create.html', locals(),
                                context_instance=RequestContext(request))
