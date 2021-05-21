from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['image'].required = False
        return form


admin.site.register(News, NewsAdmin)
