from modeltranslation.translator import translator, TranslationOptions
from .models import App

class AppTranslationOptions(TranslationOptions):
    fields = ('name',)
    # fields = ('name','uploaded_by','apk_file','first_screen_shot','second_screen_shot','video_recording','ui_hierarchy','created_at','updated_at')

translator.register(App, AppTranslationOptions)