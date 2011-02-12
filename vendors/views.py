from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from vendors.forms import VendorForm, MarketSignUpForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from tagging.models import Tag, TaggedItem
from django.conf import settings

import datetime

def vendor_index(request):
    vendors=Vendor.public_objects.all()
    return render_to_response('vendors/vendor_index.html', locals(),
                              context_instance=RequestContext(request))

def vendor_detail(request, slug):
    if request.user.is_authenticated():
    try:
            vendor=Vendor.objects.get(slug__exact=slug)
        except:
        raise Http404
    else:
        try:
            vendor=Vendor.public_objects.get(slug__exact=slug)
        except:
            raise Http404

    google_api_key=settings.GOOGLE_API_KEY

    return render_to_response('vendors/vendor_detail.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def vendor_signup(request):
    form=VendorForm(request.POST or None)
    if form.is_valid():
        vendor=form.save(commit=False)
        vendor.owner=request.user
        vendor.slug=slugify(vendor.name)
        vendor.save()
        return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))
        
    return render_to_response('vendors/vendor_signup.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def vendor_edit(request, slug):
    instance = None
    if slug is not None:
        instance = Vendor.objects.get(slug__exact=slug)
        
    if request.method == 'POST':
        form=VendorForm(request.POST, instance=instance)
        if form.is_valid():
            vendor=form.save(commit=False)
            vendor.slug=slugify(vendor.name)
            vendor.save()
            return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))
    else:
        form = VendorForm(instance=instance)
        
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
            vendor.slug=slugify(vendor.name)
            vendor.save()
        return HttpResponseRedirect(reverse('application_detail', args=[application.vendor.slug]))

    return render_to_response('vendors/application_create.html', locals(),
                                context_instance=RequestContext(request))
