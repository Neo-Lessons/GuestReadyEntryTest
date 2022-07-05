from django.test import TestCase

class URLTest(TestCase):
    def test_01_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, msg='connection error')
