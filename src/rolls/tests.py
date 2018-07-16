from django.test import TestCase

# Create your tests here.
class ViewGet(TestCase):

    def test_home_serves_correct_html(self):
        response = self.client.get('/roll/')
        self.assertTemplateUsed(response,'rolls/home.html')

    def test_upload_serves_correct_html(self):
        response = self.client.get('/roll/upload/')
        self.assertTemplateUsed(response,'rolls/upload.html')
    
    def test_manage_serves_correct_html(self):
        response = self.client.get('/roll/manage/')
        self.assertTemplateUsed(response,'rolls/manage.html')
