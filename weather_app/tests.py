# weather_app/tests.py

# from django.test import TestCase, Client
# from django.urls import reverse

# class IndexViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_index_view_status_code(self):
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)
# weather_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .forms import CityForm

class CityFormTest(TestCase):
    """Test cases for the city form used to input city names."""

    def test_city_form_valid(self):
        """The form should be valid when given a non-empty city name."""
        form_data = {'city': 'London'}
        form = CityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        """The form should be invalid if the city name is empty."""
        form_data = {'city': ''}
        form = CityForm(data=form_data)
        self.assertFalse(form.is_valid())

class IndexViewTest(TestCase):
    """Test cases for the index view."""

    def setUp(self):
        """Set up a test client to make requests to the view."""
        self.client = Client()

    def test_index_view_status_code(self):
        """The index view should return a 200 status code for a GET request."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        """The index view should render the weather_app/index.html template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'weather_app/index.html')

    def test_index_view_form_in_context(self):
        """The index view should include a form in its context."""
        response = self.client.get(reverse('home'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CityForm)

    # If you have logic in your view that changes the context based on POST data,
    # you can test that as well. For example:
    def test_index_view_post_request(self):
        """The index view should handle POST requests and return weather data."""
        response = self.client.post(reverse('home'), {'city': 'London'})
        # Check for a 200 status code even on POST
        self.assertEqual(response.status_code, 200)
        # Check if the response context contains weather data
        # This assumes you add weather data to the context in your view
        self.assertIn('weather', response.context)


# Create your tests here.
