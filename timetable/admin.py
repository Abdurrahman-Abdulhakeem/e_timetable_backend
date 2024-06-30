from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Day)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(Level)
admin.site.register(TimetableEntry) 

