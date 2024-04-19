from django.test import TestCase

class WeatherAppTestCase(TestCase):
    def test_weather_form_submission(self):
        
        response = self.client.post('http://127.0.0.1:8000/', {'city': '1234567'})  

    
        self.assertEqual(response.status_code, 200)

    
        self.assertIn(b'Toronto', response.content)  


