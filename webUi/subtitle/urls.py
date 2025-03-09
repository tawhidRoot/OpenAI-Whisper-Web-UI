from django.urls import path
from .views import transcribe_audio, model_management

urlpatterns = [
    path("", transcribe_audio, name="transcribe_audio"),
    path("models/", model_management, name="model_management"),
]
