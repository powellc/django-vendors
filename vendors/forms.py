import django.forms as forms
from vendors.models import Vendor, Application
from django.db.models import TextField

class VendorForm(forms.ModelForm):
    class Meta:
        model=Vendor
        exclude=('public','owner', 'markets', 'slug',)

    def save(self, commit=True):
        f = super(VendorForm, self).save(commit=False)
        if not f.pk: f.owner = request.user
        if commit: f.save()
        return f
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model=Application
        exclude=('vendor','status', 'approval_date', 'submission_date', )

    def save(self, commit=True):
        f = super(ApplicationForm, self).save(commit=False)
        vendor = Vendor.objects.get(slug=request.GET["slug"])
        if not f.pk: 
            f.status = PENDING_STATUS
            f.vendor = vendor
        if commit: f.save()
        return f

