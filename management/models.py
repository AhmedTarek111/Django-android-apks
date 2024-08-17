from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class App(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='app_uploaded_by', verbose_name=_("Uploaded by"))
    apk_file = models.FileField(upload_to='apks/', verbose_name=_("APK File"))
    first_screen_shot = models.ImageField(upload_to='f_screenshot/', verbose_name=_("First Screenshot"),null=True,blank=True)
    second_screen_shot = models.ImageField(upload_to='s_screenshot/', verbose_name=_("Second Screenshot"),null=True,blank=True)
    video_recording = models.FileField(upload_to='video_recording/', verbose_name=_("Video Recording"),null=True,blank=True)
    ui_hierarchy = models.TextField(verbose_name=_("UI Hierarchy"),blank=True, null=True,)
    screen_changed = models.BooleanField(default=False, verbose_name=_("Screen Changed"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name