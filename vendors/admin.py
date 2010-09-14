from vendors.models import Vendor, Application
from django.contrib import admin

class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display  = ['name', 'town','public', 'created', 'updated']
    list_filter   = ['town', 'public', 'markets']
    ordering = ['-created']
    search_fields = ['name', 'description']
    date_hierarchy='created'
    
admin.site.register(Vendor, VendorAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['vendor', 'submission_date', 'created', 'updated']
    list_filter   = ['insurance_on_file', 'bylaws_signed', 'reapplying']
    ordering = ['-submission_date']
    date_hierarchy='submission_date'
    
admin.site.register(Application, ApplicationAdmin)
