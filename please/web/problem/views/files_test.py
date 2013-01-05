from unittest.mock import Mock
import django.test
from . import files


class AdditionalUploadTest(django.test.TestCase):
    fixtures = ['test']

    def setUp(self):
        files.copy_to_problem = Mock(side_effect=lambda: print('mock for copy_to_problem worx!'))

    def test_upload(self):
        response = self.client.get('/problems/1/files/upload/additional')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_additional.html')
