from django.contrib import admin
from wall.models import Group


# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    model = Group
    readonly_fields = ('id', )


admin.site.register(Group, GroupAdmin)
