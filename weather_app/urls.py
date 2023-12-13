# weather_app/urls.py

from django.urls import path
from .views import index  # Import the index view from your views.py

urlpatterns = [
    path('', index, name='home'),  # This pattern points to your index view
]