from django.contrib import admin
from . models import UserProfile, Employe, Conge, ApplicationConge,ManageConge, DisableDays, RangeDisableDays


admin.site.register(UserProfile)
admin.site.register(Employe)
admin.site.register(Conge)
admin.site.register(ApplicationConge)
admin.site.register(ManageConge)
admin.site.register(DisableDays)
admin.site.register(RangeDisableDays)