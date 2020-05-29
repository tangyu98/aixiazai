from django.contrib import admin
from . import models


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "sex", "stuNo", "birth")
    search_fields = ("name", "sex", "stuNo", "birth")
    # date_hierarchy = "sex"

admin.site.register(models.Student, StudentAdmin)
