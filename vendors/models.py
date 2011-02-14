from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from myutils.utils import google_lat_long
from myutils.models import RandomIDMixin, USAddressPhoneMixin
import urllib
import settings

from taggit.managers import TaggableManager
from vendors.managers import PublicManager
from schedule.models import Event
from photologue.models import ImageModel

class VendorPhoto(ImageModel, RandomIDMixin, TimeStampedModel):
    """Vendor photo model.

    A model derived from Photologue's ImageModel for managing photos of vendors and their products.

    It also includes a mixin for making it's ids random and adding created/modified stamps.
    """
    vendor=models.ForeignKey('Vendor')
    caption=models.CharField(_('Caption'), max_length=255, blank=True, null=True)
    public=models.BooleanField(_('Public'), default=False)

    class Meta:
        ordering=['created',]
        get_latest_by='created'
        verbose_name=_('vendor photo')
        verbose_name_plural=_('vendor photos')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        # example.com/vendors/goodtime-farm/photos/23ra2f9a
        return ('vendor_photo_detail', (), {'slug': self.vendor.slug, 'id': self.id})
        

class VendorType(TitleSlugDescriptionModel):
    """Vendor type model.
     
    What type of vendors do we have?
     
    Produce, Jewelry, Pottery, Meat, Cheese, etc...?"""
     
    crafter=models.BooleanField(_('Crafter'), default=False)
     
    class Meta:
        verbose_name=_('vendor type')
        verbose_name_plural=_('vendor types')
        ordering=('title',)
    
    def __unicode__(self):
        return u'%s' % self.title

class Vendor(TitleSlugDescriptionModel, USAddressPhoneMixin, TimeStampedModel):
    """Vendor model."""
    owner=models.ForeignKey(User, related_name='vendor_owner')
    email=models.EmailField(_('email'), unique=True)
    url=models.URLField(_('website'), blank=True, null=True)
    type=models.ManyToManyField(VendorType)
    markets=models.ManyToManyField(Event, null=True, blank=True)
    public=models.BooleanField(_('Public'), default=False)
    committee_member=models.BooleanField(_('committee member'), default=False)
    products=TaggableManager()

    objects=models.Manager()
    public_objects=PublicManager()
    
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
            app = Application.objects.get(vendor=self, submission_date__year=datetime.now().year)
            return app.get_status_display()
        except:
            return 'No application found for %s' % (datetime.now().year)
    
    @property
    def in_order(self):
        ''' Is everything in order for this vendor to sell this year? '''
        app = Application.objects.get(vendor=self, submission_date__year=datetime.now().year)
        try:
            state = app.apprequirement_set.all()[0].complete
            try:
                for req in app.apprequirement_set.all()[1:]:
                    state &= req.complete
            except:
                pass
        except:
            state = True
        state &= (self.status=='Approved')
        return state

    @models.permalink
    def get_absolute_url(self):
        return ('vendor_detail', (), {'slug': self.slug})
        
    @property
    def get_previous_vendor(self):
        return self.get_previous_by_name(public=True)
    
    @property
    def get_next_vendor(self):
        return self.get_next_by_name(public=True)

class Requirement(models.Model):
    """Requirement model.

    A model that allows markets to set requirements for a vendor to complete before they are approved.

    i.e. insurance on file?, bylaws signed?
    """
    title=models.CharField(_('Title'), max_length=150)
    instructions=models.TextField(_('Instructions'), blank=True, null=True)
    active=models.BooleanField(_('Active'), default=False)

    class Meta:
        verbose_name=_('requirement')
        verbose_name_plural=_('requirements')
        ordering=('title',)
    
    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        super(Requirement, self).save(*args, **kwargs)

        require_save=self.do_update_apps()

        if require_save:
            super(Requirement, self).save()
            
    def do_update_apps(self):
        changed=True
        if self.active:
            # If active, add yourself to any apps that you don't belong to already
            apps = Application.objects.exclude(id__in=self.apprequirement_set.all())
            for a in apps:
                appreq = AppRequirement.objects.create(app=a, req=self)
                appreq.save()
        elif not self.active:
            # Else, delete all appreqs that involve you.
            for a in AppRequirement.objects.filter(req=self):
                a.delete()
            
        return changed


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
    submission_date=models.DateTimeField(_('Submission date'), default=datetime.now(), editable=False)
    approval_date=models.DateTimeField(_('Approval date'), blank=True, null=True)
    added_products=models.TextField(_('Added products'), blank=True, null=True)
    removed_products=models.TextField(_('Removed products'), blank=True, null=True)
    extra_notes=models.TextField(_('Extra notes'), blank=True, null=True)

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

    def save(self, *args, **kwargs):
        super(Application, self).save(*args, **kwargs)

        require_save=self.do_set_reqs()

        if require_save:
            super(Application, self).save()
            
    def do_set_reqs(self):
        changed=True
        active_reqs = Requirement.objects.filter(active=True)
        deactivated_reqs=Requirement.objects.filter(active=False)
        existing_reqs = self.apprequirement_set.all()
        # Check if any existing app reqs are deactivated and delete them
        if existing_reqs:
            for r in deactivated_reqs.filter(id=existing_reqs):
                existing_reqs.delete(r)
        # Check against existing app reqs if any new app reqs are created/activated and add them
        new_reqs = active_reqs.exclude(id__in=existing_reqs)
        for r in new_reqs:
            appreq = AppRequirement.objects.create(app=self, req=r)
            appreq.save()
        return changed

class AppRequirement(models.Model):
    app=models.ForeignKey(Application)
    req=models.ForeignKey(Requirement)
    complete=models.BooleanField(_('Complete'), default=False)

    class Meta:
        verbose_name=_('application requirement')
        verbose_name_plural = _('application requirements')
        ordering = ('app', 'req',)
        
    def __unicode__(self):
        return u'%s requirement for %s' % (self.req, self.app)
