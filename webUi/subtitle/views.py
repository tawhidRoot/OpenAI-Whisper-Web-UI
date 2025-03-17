import os
import shutil
import whisper
import mimetypes
import json
import torch
import urllib.parse  # <-- Imported for URL encoding the filename

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename  # For sanitizing filenames
from .forms import AudioUploadForm

# Define model directory path
MODEL_DIR = os.path.join(settings.BASE_DIR, "openaiWhisperModels")

# Ensure the models directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)


def get_downloaded_models():
    """Returns a list of downloaded model names."""
    try:
        return os.listdir(MODEL_DIR)
    except FileNotFoundError:
        return []


def download_model(model_name):
    """Download a model if it doesn't exist locally."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(model_path):
        try:
            _ = whisper.load_model(model_name, download_root=MODEL_DIR)
        except RuntimeError as e:
            if "SHA256 checksum does not" in str(e):
                if os.path.exists(model_path):
                    shutil.rmtree(model_path)
                _ = whisper.load_model(model_name, download_root=MODEL_DIR)
            else:
                raise e
        return True
    return False


def update_model(model_name):
    """Update a model by removing the old folder and re-downloading."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    return download_model(model_name)


def model_management(request):
    downloaded_models = get_downloaded_models()
    if request.method == "POST":
        model_name = request.POST.get("model_name")
        action = request.POST.get("action")
        if action == "download":
            download_model(model_name)
        elif action == "update":
            update_model(model_name)
        elif action == "delete":
            model_path = os.path.join(MODEL_DIR, model_name)
            if os.path.exists(model_path):
                shutil.rmtree(model_path)
        downloaded_models = get_downloaded_models()
    return render(request, "model_management.html", {"models": downloaded_models})


def format_subtitle_text(text, max_words, mode):
    """
    Formats subtitle text based on the selected mode.
    - "line": splits the text into multiple lines, each containing at most max_words.
    - "full": returns the full subtitle text without truncation.
    """
    if mode == "line":
        words = text.split()
        lines = []
        for i in range(0, len(words), max_words):
            lines.append(" ".join(words[i : i + max_words]))
        return "\n".join(lines)
    elif mode == "full":
        return text
    else:
        return text


def transcribe_audio(request):
    if request.method == "POST":
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded audio file temporarily
            audio_file = request.FILES["audio_file"]
            # Split the original file name and extension
            original_name, ext = os.path.splitext(audio_file.name)
            # Sanitize the base filename using Django's helper
            safe_base_name = get_valid_filename(original_name)
            # Reconstruct the filename with its original extension
            safe_audio_file_name = f"{safe_base_name}{ext}"
            file_path = default_storage.save(
                f"temp/{safe_audio_file_name}", ContentFile(audio_file.read())
            )

            # Retrieve transcription options
            model_choice = form.cleaned_data["model_choice"]
            language = form.cleaned_data["language"] or None
            temperature = form.cleaned_data["temperature"]
            best_of = form.cleaned_data["best_of"]
            condition_on_previous_text = (
                form.cleaned_data["condition_on_previous_text"] == "true"
            )
            output_format = form.cleaned_data["output_format"]
            max_subtitle_length = form.cleaned_data.get("max_subtitle_length", 3)
            max_length_mode = form.cleaned_data.get("max_length_mode", "line")

            # Select device (GPU if available)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")

            # Load Whisper model
            model = whisper.load_model(model_choice, download_root=MODEL_DIR).to(device)

            # Transcribe audio file
            result = model.transcribe(
                file_path,
                language=language,
                temperature=temperature,
                best_of=best_of,
                condition_on_previous_text=condition_on_previous_text,
            )

            # Prepare output file
            file_extension = output_format
            # Use the sanitized base name for output filename
            output_filename = f"{safe_base_name}.{file_extension}"
            output_file_path = os.path.join("temp", output_filename)

            if output_format == "srt":
                with open(output_file_path, "w", encoding="utf-8") as srt_file:
                    for i, segment in enumerate(result["segments"]):
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"]
                        formatted_text = format_subtitle_text(
                            text, max_subtitle_length, max_length_mode
                        )
                        srt_file.write(f"{i+1}\n")
                        srt_file.write(
                            f"{format_time(start_time)} --> {format_time(end_time)}\n"
                        )
                        srt_file.write(formatted_text + "\n\n")
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
                        formatted_text = format_subtitle_text(
                            text, max_subtitle_length, max_length_mode
                        )
                        vtt_file.write(f"{i+1}\n")
                        vtt_file.write(
                            f"{format_time(start_time)} --> {format_time(end_time)}\n"
                        )
                        vtt_file.write(formatted_text + "\n\n")
            elif output_format == "json":
                with open(output_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(result, json_file, indent=4)

            # Return file as download response
            with open(output_file_path, "rb") as f:
                response = HttpResponse(
                    f.read(), content_type=mimetypes.guess_type(output_file_path)[0]
                )
                # Create an ASCII fallback filename by stripping non-ASCII characters
                ascii_base = safe_base_name.encode("ascii", "ignore").decode("ascii")
                fallback_filename = f"{ascii_base}.{file_extension}"
                # URL-encode the full output filename (which may include non-ASCII characters)
                encoded_filename = urllib.parse.quote(output_filename)
                # Set Content-Disposition header with both fallback and UTF-8 encoded filename
                response["Content-Disposition"] = (
                    f'attachment; filename="{fallback_filename}"; '
                    f"filename*=UTF-8''{encoded_filename}"
                )

            # Clean up temporary files
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
