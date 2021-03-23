from django.contrib import admin
from .models import Person, Photo, PersonRole

admin.site.register(Person)
admin.site.register(Photo)


class PersonRoleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role_name'].required = False
        return form


admin.site.register(PersonRole, PersonRoleAdmin)
