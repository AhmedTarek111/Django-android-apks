from django.test import TestCase
from django.contrib.auth.models import User
from .models import App
from django.core.files.uploadedfile import SimpleUploadedFile

class AppModelTest(TestCase):
# create objects 
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # sample apk file and screenshots for testing
        self.apk_file = SimpleUploadedFile("test.apk", b"apk content")
        self.first_screenshot = SimpleUploadedFile("screenshot1.jpg", b"image content")
        self.second_screenshot = SimpleUploadedFile("screenshot2.jpg", b"image content")
        self.video_recording = SimpleUploadedFile("video.mp4", b"video content")
        
        # create  app object
        self.app = App.objects.create(
            name="Test App",
            uploaded_by=self.user,
            apk_file=self.apk_file,
            first_screen_shot=self.first_screenshot,
            second_screen_shot=self.second_screenshot,
            video_recording=self.video_recording,
            ui_hierarchy="Test UI Hierarchy",
            screen_changed=True
        )
        
# test creation
    def test_app_creation(self):
        self.assertEqual(self.app.name, "Test App")
        self.assertEqual(self.app.uploaded_by.username, "testuser")
        self.assertTrue(self.app.screen_changed)
        self.assertIsNotNone(self.app.created_at)
        self.assertIsNotNone(self.app.updated_at)
        self.assertEqual(str(self.app), "Test App")

# test stored pathes 
    def test_app_fields(self):
        app = App.objects.get(id=self.app.id)
        
        # check that the file name starts with the expected value
        self.assertTrue(app.apk_file.name.startswith('apks/test'))
        self.assertTrue(app.first_screen_shot.name.startswith('f_screenshot/screenshot1'))
        self.assertTrue(app.second_screen_shot.name.startswith('s_screenshot/screenshot2'))
        self.assertTrue(app.video_recording.name.startswith('video_recording/video'))
        
        self.assertEqual(app.ui_hierarchy, "Test UI Hierarchy")

# check if the string method work
    def test_app_string_representation(self):
        self.assertEqual(str(self.app), "Test App")

# test update
    def test_app_update(self):
        self.app.name = "Updated Test App"
        self.app.save()
        updated_app = App.objects.get(id=self.app.id)
        self.assertEqual(updated_app.name, "Updated Test App")
        self.assertNotEqual(updated_app.updated_at, self.app.created_at)

# test delete 
    def test_app_delete(self):
        app_id = self.app.id
        self.app.delete()
        with self.assertRaises(App.DoesNotExist):
            App.objects.get(id=app_id)
