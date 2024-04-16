from django.test import TestCase
class WeatherAppTest(TestCase):
    def test_get_weather(self):
        response = self.client.get('http://127.0.0.1:8000/') 
        self.assertEqual(response.status_code, 200)       
        self.assertIn(b'Toronto', response.content)
