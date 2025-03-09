import os
import time
import threading
from django.apps import AppConfig
from django.conf import settings

class SubtitleConfig(AppConfig):
    name = 'subtitle'

    def ready(self):
        # Define a startup check function to update downloaded models.
        def startup_check():
            # Wait a few seconds to allow the server to finish starting up.
            time.sleep(5)
            from .views import update_model
            # Define the directory where models are stored.
            model_dir = os.path.join(settings.BASE_DIR, 'openaiWhisperModels')
            # List the models that you want to check for updates.
            models_to_check = ["tiny", "base", "small", "medium", "large"]
            for model in models_to_check:
                model_path = os.path.join(model_dir, model)
                # If the model folder exists, update the model.
                if os.path.exists(model_path):
                    try:
                        print(f"Updating model '{model}' on startup...")
                        update_model(model)
                        print(f"Model '{model}' updated successfully.")
                    except Exception as e:
                        print(f"Error updating model '{model}': {e}")
        
        # Run the startup check in a separate thread to avoid blocking the main thread.
        threading.Thread(target=startup_check).start()
