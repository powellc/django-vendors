from vendors.models import Vendor, Application, VendorType, VendorPhoto, Requirement, AppRequirement
from django.contrib import admin

class VendorAdmin(admin.ModelAdmin):
    list_display  = ['title', 'town','public', 'created', 'modified']
    list_filter   = ['town', 'public',]

    ordering = ['-created']
    search_fields = ['name', 'description']
    date_hierarchy='created'
    
admin.site.register(Vendor, VendorAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['vendor', 'submission_date', 'created', 'modified']
    ordering = ['-submission_date']
    date_hierarchy='submission_date'
    
admin.site.register(Application, ApplicationAdmin)
admin.site.register(VendorType)
admin.site.register(VendorPhoto)
admin.site.register(Requirement)
admin.site.register(AppRequirement)
