from ckeditor.fields import RichTextField
from django.contrib import admin
# from redactor.widgets import RedactorEditor

from .models import News

# admin.site.register(News)
# admin.site.register(NewsPhoto)


class NewsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['image'].required = False
        return form


admin.site.register(News, NewsAdmin)
