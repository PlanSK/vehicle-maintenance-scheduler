from django.contrib import admin

from maintenance.models import Vehicle, WorkPattern, Work


admin.site.register(Vehicle)
admin.site.register(WorkPattern)
admin.site.register(Work)
