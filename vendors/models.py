from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from myutils.utils import google_lat_long
from myutils.fields import ZipCodeField, USAddressPhoneModel
import urllib
import settings
from taggit.managers import TaggableManager

class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(public=True)

class VendorType(TitleSlugDescriptionModel):
    """Vendor type model.
    
     What type of vendors do we have?
    
     Produce, Jewelry, Pottery, Meat, Cheese, etc...?"""
    
    craft=models.BooleanField(_('Craft'), default=False)
    
    class Meta:
        verbose_name=_('vendor type')
        verbose_name_plural=_('vendor types')
        ordering=('title',)
    
    def __unicode__(self):
        return u'%s' % self.title.

class Vendor(TitleSlugDescriptionModel, USAddressPhoneModel, TimeStampedModel):
    """Vendor model."""
    owner=models.ForeignKey(User, related_name='vendor_owner')
    email=models.EmailField(_('email'), unique=True)
    url=models.URLField(_('website'), blank=True, null=True)
    type=models.ManyToManyField(VendorType)
    markets=models.ManyToManyField(Event, null=True, blank=True)
    public=models.BooleanField(_('public'), default=False)
    committee_member=models.BooleanField(_('committee member'), default=False)
    insurance_on_file=models.BooleanField(_('insurance on file'), default=False)
    signed_bylaws=models.BooleanField(_('signed bylaws'), default=False)
    products=TaggableManager()

    objects=models.Manager()
    public=PublicManager()
    
    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('title',)
        get_latest_by='created'
        
    def __unicode__(self):
        return u'%s in %s' % (self.title, self.town)
        
    @property
    def status(self):
        ''' Return a string representing the state of the current year's application.'''
        try:
            app = Application.objects.get(vendor=self, year=datetime.now().year)
            return app.get_status_display()
        except:
            return 'No application found for %s' % (datetime.now().year)
    
    @property
    def in_order(self):
        ''' Is everything in order for this vendor to sell this year? '''
        return self.signed_bylaws && self.insurance_on_file && (self.status()=='Approved')

    @models.permalink
    def get_absolute_url(self):
        return ('vendor_detail', (), {'slug': self.slug})
        
    @property
    def get_previous_vendor(self):
        return self.get_previous_by_name(public=True)
    
    @property
    def get_next_vendor(self):
        return self.get_next_by_name(public=True)

class Application(TimeStampedModel):
    DENIED_STATUS = 0
    APPROVED_STATUS = 1
    PENDING_STATUS = 2

    APP_STATUSES=(
            (DENIED_STATUS, 'Denied'),
            (APPROVED_STATUS, 'Approved'),
            (PENDING_STATUS, 'Pending'),
    )
    vendor=models.ForeignKey(Vendor)
    status=models.IntegerField(_('Status'), max_length=1, choices=APP_STATUSES, default=PENDING_STATUS)
    submission_date=DateTimeField(_('Submission date'), default=datetime.now(), editable=False)
    approval_date=DateTimeField(_('Approval date'), blank=True, null=True)
    notes=modes.TextField(_('Notes'), blank=True, null=True)

    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')
        ordering = ('vendor', 'submission_date',)
        get_latest_by='submission_date'

    @models.permalink
    def get_absolute_url(self):
        return ('application_detail', (), {'slug': self.vendor.slug, 'year': self.submission_date.year})

    def __unicode__(self):
        return u'%s application for %s' % (self.submission_date.year, self.vendor)

