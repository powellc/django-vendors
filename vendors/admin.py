from vendors.models import *
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
    
class AppReqAdmin(admin.ModelAdmin):
    list_display = ['app', 'req', 'complete']
    list_filter = ['app', 'req']
    
admin.site.register(AppRequirement, AppReqAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(VendorType)
admin.site.register(VendorPhoto)
admin.site.register(Requirement)
admin.site.register(MarketSeason)
admin.site.register(MarketLocation)
