from django.contrib import admin
from wall.models import Group


# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('name', 'id',)


admin.site.register(Group, GroupAdmin)
