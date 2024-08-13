from django.contrib import admin
from .models import App
from modeltranslation.admin import TranslationAdmin

class AppAdmin(TranslationAdmin):
    pass

admin.site.register(App, AppAdmin)
