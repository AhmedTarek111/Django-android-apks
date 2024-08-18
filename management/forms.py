from django import forms
from .models import App

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name_en', 'name_fr', 'apk_file', 'first_screen_shot', 'second_screen_shot', 'video_recording', 'ui_hierarchy','screen_changed']

class AppCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name_en', 'name_fr', 'apk_file']