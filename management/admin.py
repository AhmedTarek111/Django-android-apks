from django.contrib import admin
from .models import App
from modeltranslation.admin import TranslationAdmin

class AppAdmin(TranslationAdmin):
    fields = ('name_en', 'name_fr', 'uploaded_by', 'apk_file', 'first_screen_shot', 'second_screen_shot', 'video_recording', 'ui_hierarchy')

admin.site.register(App, AppAdmin)
