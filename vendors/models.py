from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField 
from django_extensions.db.models import TimeStampedModel
from schedule.models import Event
import tagging
import urllib
import settings

def get_lat_long(location):
    key = settings.GOOGLE_API_KEY_CFM
    output = "csv"
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        return "%s, %s" % (dlist[2], dlist[3])
    else:
        return ''

class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(public=True)

class ZipCodeField(models.CharField):
    def __unicode__(self):
        return self.rjust(5, '0')

class VendorType(models.Model):
	"""Vendor type model.

	   What type of vendors do we have?

	   Produce, Jewelry, Pottery, Meat, Cheese, etc...?"""

    name=models.CharField(_('name'), max_length=50)
	slug=models.SlugField(_('slug'), unique=True)
    
    class Meta:
		verbose_name=_('vendor type')
		verbose_name_plural=_('vendor types')
		ordering=('name',)
  
    def __unicode__(self):
		return u'%s' % self.name

class Vendor(TimeStampedModel):
    """Vendor model."""
    name=models.CharField(_('title'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True)
    owner=models.ForeignKey(User, related_name='vendor_owner')
    email=models.EmailField(_('email'), unique=True)
    phone=PhoneNumberField(_('phone'), blank=True, null=True)
    url=models.URLField(_('website'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    town=models.CharField(_('town'), max_length=100)
    state=USStateField(_('state'))
    zipcode=ZipCodeField(_('zip'), max_length=5)
    description=models.TextField()
    products=TagField()
    type=models.ManyToManyField(VendorType)
    markets=models.ManyToManyField(Event, null=True, blank=True)
    public=models.BooleanField(_('public'), default=False)
    lat_long=models.CharField(_('coordinates'), max_length=255)
    committee_member=models.BooleanField(_('committee member'), default=False)
    
    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('name',)
        get_latest_by='created'
        
    def save(self):
        if not self.lat_long:
            location = "%s +%s +%s +%s" % (self.address, self.town, self.state, self.zipcode)
            self.lat_long = get_lat_long(location)
            if not self.lat_long:
                location = "%s +%s +%s" % (self.town, self.state, self.zipcode)
                self.lat_long = get_lat_long(location)
        
        super(Vendor, self).save()
        
    def __unicode__(self):
        return u'%s in %s' % (self.name, self.town)
        
    def get_absolute_url(self):
        return u'%s/' % (self.slug)
        
    def get_previous_vendor(self):
        return self.get_previous_by_name(public=True)

    def get_next_vendor(self):
        return self.get_next_by_name(public=True)


class Application(TimeStampedModel):
    vendor=models.ForeignKey(Vendor, unique_for_year="submission_date")
    submission_date=models.DateField(default=datetime.now())
    approval_date=models.DateField(blank=True, null=True)
    reapplying=models.BooleanField(_('reapplying'), default=False)
    signed_bylaws=models.BooleanField(_('signed bylaws'), default=False)
    insurance_on_file=models.BooleanField(_('insurance on file'), default=False)

	class Meta:
        verbose_name=_('application')
        verbose_name_plural=_('applications')
        ordering=('vendor', 'submission_date',)
        get_latest_by='submission_date'
		
	def __unicode__(self):
        return u'%s %s application' % (self.vendor, self.submission_date.year)

	def get_absolute_url(self):
        return u'%s/applications/%s/' %s (self.vendor.slug, self.submission_date.year)

        STATUS_OPTIONS={
            ('P', 'Pending'),
            ('A', 'Approved'),
            ('D', 'Denied'),
        }

class ApplicationStatus(models.Model):
	"""Application status model.

	   i.e. Approved, Pending, Denied, ... """

    status=models.CharField(_('status'), max_length=1, options=STATUS_OPTIONS, default='P')
    application=models.ForeignKey(Application)
    explanation=models.TextField(_('explanation'), blank=True, null=True)

    class Meta:
        verbose_name=_('application status')
       	verbose_name_plural=_('application statuses')
        ordering=('name',)

    def __unicode__(self):
        return u'%s' % self.name