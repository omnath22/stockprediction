from django.conf import settings
from celery import Celery
import os

# Set the default broker URL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockpredictionai.settings')

# Define the app name for Celery
app = Celery('stockpredictionai')

# Configure Celery with Django settings
app.config_from_object('django.conf:settings')

# Load tasks from the `tasks.py` module
app.autodiscover_tasks()

# Print a success message
print("Celery configuration is set up successfully.")