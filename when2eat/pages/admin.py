from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TimeSlot)
admin.site.register(Status)
admin.site.register(Plan)
admin.site.register(Person)