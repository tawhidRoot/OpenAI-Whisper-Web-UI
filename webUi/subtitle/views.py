import os
import shutil
import whisper
import mimetypes
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import AudioUploadForm

# Define model directory path
MODEL_DIR = os.path.join(settings.BASE_DIR, 'openaiWhisperModels')

# Ensure the models directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Function to check downloaded models
def get_downloaded_models():
    try:
        downloaded_models = os.listdir(MODEL_DIR)
        return downloaded_models
    except FileNotFoundError:
        return []

# Function to download a new model using load_model with a custom download_root.
# If the model download results in a checksum error, remove the model folder and try again.
def download_model(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        try:
            _ = whisper.load_model(model_name, download_root=MODEL_DIR)
        except RuntimeError as e:
            if "SHA256 checksum does not" in str(e):
                # Remove the corrupted/incomplete model folder and retry
                if os.path.exists(model_path):
                    shutil.rmtree(model_path)
                _ = whisper.load_model(model_name, download_root=MODEL_DIR)
            else:
                raise e
        return True
    return False

# Function to update the model:
# Remove the current version (if it exists) and re-download it.
def update_model(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path):
        shutil.rmtree(model_path)  # Remove the old model folder
    return download_model(model_name)

def model_management(request):
    downloaded_models = get_downloaded_models()

    if request.method == 'POST':
        model_name = request.POST.get('model_name')
        action = request.POST.get('action')

        if action == 'download':
            download_model(model_name)
        elif action == 'update':
            update_model(model_name)

        # Reload the models list after performing the action.
        downloaded_models = get_downloaded_models()

    return render(request, 'model_management.html', {'models': downloaded_models})

def transcribe_audio(request):
    if request.method == "POST":
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file temporarily.
            audio_file = request.FILES["audio_file"]
            file_name = os.path.splitext(audio_file.name)[0]  # File name without extension.
            file_path = default_storage.save(f"temp/{audio_file.name}", ContentFile(audio_file.read()))

            # Retrieve form data for transcription options.
            model_choice = form.cleaned_data["model_choice"]
            language = form.cleaned_data["language"] or None  # Auto-detect if not provided.
            temperature = form.cleaned_data["temperature"]
            best_of = form.cleaned_data["best_of"]
            condition_on_previous_text = form.cleaned_data["condition_on_previous_text"] == "true"
            output_format = form.cleaned_data["output_format"]

            # Load the Whisper model with our custom download_root.
            model = whisper.load_model(model_choice, download_root=MODEL_DIR)

            # Transcribe audio.
            result = model.transcribe(
                file_path,
                language=language,
                temperature=temperature,
                best_of=best_of,
                condition_on_previous_text=condition_on_previous_text,
            )

            # Generate the output file.
            file_extension = output_format
            output_filename = f"{file_name}.{file_extension}"
            output_file_path = os.path.join("temp", output_filename)

            if output_format == "srt":
                with open(output_file_path, "w", encoding="utf-8") as srt_file:
                    for i, segment in enumerate(result["segments"]):
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"]

                        srt_file.write(f"{i+1}\n")
                        srt_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                        srt_file.write(text + "\n\n")
            elif output_format == "txt":
                with open(output_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(result["text"])
            elif output_format == "vtt":
                with open(output_file_path, "w", encoding="utf-8") as vtt_file:
                    vtt_file.write("WEBVTT\n\n")
                    for i, segment in enumerate(result["segments"]):
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"]

                        vtt_file.write(f"{i+1}\n")
                        vtt_file.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                        vtt_file.write(text + "\n\n")
            elif output_format == "json":
                with open(output_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(result, json_file, indent=4)

            # Prepare response for file download.
            with open(output_file_path, "rb") as f:
                response = HttpResponse(f.read(), content_type=mimetypes.guess_type(output_file_path)[0])
                response["Content-Disposition"] = f'attachment; filename="{output_filename}"'

            # Clean up temporary files.
            os.remove(file_path)
            os.remove(output_file_path)

            return response
    else:
        form = AudioUploadForm()

    return render(request, "upload.html", {"form": form})

def format_time(seconds):
    """Converts seconds to SRT/VTT timestamp format (HH:MM:SS,mmm)"""
    millisec = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"
