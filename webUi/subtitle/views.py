import os
import shutil
import whisper
import mimetypes
import json
import urllib.parse  # For URL encoding the filename
import logging
import torch

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename  # For sanitizing filenames
from .forms import AudioUploadForm

# Configure logging
logger = logging.getLogger(__name__)

# Define model directory path and ensure it exists
MODEL_DIR = os.path.join(settings.BASE_DIR, "openaiWhisperModels")
os.makedirs(MODEL_DIR, exist_ok=True)

# Global model cache for optimization
MODEL_CACHE = {}


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
        # Invalidate cache for the model
        if model_name in MODEL_CACHE:
            del MODEL_CACHE[model_name]
        return True
    return False


def update_model(model_name):
    """Update a model by removing the old folder and re-downloading."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    if model_name in MODEL_CACHE:
        del MODEL_CACHE[model_name]
    return download_model(model_name)


def model_management(request):
    """Handles model download, update, and deletion requests."""
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
            if model_name in MODEL_CACHE:
                del MODEL_CACHE[model_name]
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
        lines = [
            " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
        ]
        return "\n".join(lines)
    return text


def format_time(seconds, fmt="srt"):
    """
    Converts seconds to timestamp format.
    For SRT: returns HH:MM:SS,mmm.
    For VTT: returns HH:MM:SS.mmm.
    """
    millisec = int(round((seconds % 1) * 1000))
    seconds_int = int(seconds)
    minutes = seconds_int // 60
    hours = minutes // 60
    minutes = minutes % 60
    seconds_int = seconds_int % 60
    if fmt == "vtt":
        return f"{hours:02}:{minutes:02}:{seconds_int:02}.{millisec:03}"
    return f"{hours:02}:{minutes:02}:{seconds_int:02},{millisec:03}"


def write_subtitles(
    file_handle, segments, max_subtitle_length, max_length_mode, fmt="srt"
):
    """
    Writes subtitle segments to an open file handle.
    Uses the appropriate timestamp format based on fmt.
    """
    for i, segment in enumerate(segments):
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        formatted_text = format_subtitle_text(
            text, max_subtitle_length, max_length_mode
        )
        file_handle.write(f"{i + 1}\n")
        file_handle.write(
            f"{format_time(start_time, fmt)} --> {format_time(end_time, fmt)}\n"
        )
        file_handle.write(formatted_text + "\n\n")


def transcribe_audio(request):
    """
    Handles the audio file upload, transcription using Whisper,
    and returns the transcription file in the requested output format.
    Also saves user settings in the session for persistence.
    """
    # Load saved settings from session if they exist
    saved_settings = request.session.get("audio_settings", {})

    if request.method == "POST":
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save settings in session for future use
            request.session["audio_settings"] = {
                "model_choice": form.cleaned_data["model_choice"],
                "language": form.cleaned_data["language"],
                "temperature": form.cleaned_data["temperature"],
                "best_of": form.cleaned_data["best_of"],
                "condition_on_previous_text": form.cleaned_data[
                    "condition_on_previous_text"
                ],
                "output_format": form.cleaned_data["output_format"],
                "max_subtitle_length": form.cleaned_data["max_subtitle_length"],
                "max_length_mode": form.cleaned_data["max_length_mode"],
            }

            # Save the uploaded audio file temporarily
            audio_file = request.FILES["audio_file"]
            original_name, ext = os.path.splitext(audio_file.name)
            safe_base_name = get_valid_filename(original_name)
            safe_audio_file_name = f"{safe_base_name}{ext}"
            temp_dir = "temp"
            file_path = default_storage.save(
                os.path.join(temp_dir, safe_audio_file_name),
                ContentFile(audio_file.read()),
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
            logger.info(f"Using device: {device}")

            # Load Whisper model from cache or download if necessary
            if model_choice in MODEL_CACHE:
                model = MODEL_CACHE[model_choice]
                logger.info(f"Loaded '{model_choice}' model from cache.")
            else:
                model = whisper.load_model(model_choice, download_root=MODEL_DIR).to(
                    device
                )
                MODEL_CACHE[model_choice] = model
                logger.info(f"Loaded '{model_choice}' model and added to cache.")

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
            output_filename = f"{safe_base_name}.{file_extension}"
            output_file_path = os.path.join(temp_dir, output_filename)

            try:
                if output_format == "srt":
                    with open(output_file_path, "w", encoding="utf-8") as subtitle_file:
                        write_subtitles(
                            subtitle_file,
                            result["segments"],
                            max_subtitle_length,
                            max_length_mode,
                            fmt="srt",
                        )
                elif output_format == "vtt":
                    with open(output_file_path, "w", encoding="utf-8") as subtitle_file:
                        subtitle_file.write("WEBVTT\n\n")
                        write_subtitles(
                            subtitle_file,
                            result["segments"],
                            max_subtitle_length,
                            max_length_mode,
                            fmt="vtt",
                        )
                elif output_format == "txt":
                    with open(output_file_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(result["text"])
                elif output_format == "json":
                    with open(output_file_path, "w", encoding="utf-8") as json_file:
                        json.dump(result, json_file, indent=4)
                else:
                    raise ValueError("Unsupported output format.")

                # Return file as download response
                with open(output_file_path, "rb") as f:
                    response = HttpResponse(
                        f.read(), content_type=mimetypes.guess_type(output_file_path)[0]
                    )
                    # Create an ASCII fallback filename
                    ascii_base = safe_base_name.encode("ascii", "ignore").decode(
                        "ascii"
                    )
                    fallback_filename = f"{ascii_base}.{file_extension}"
                    encoded_filename = urllib.parse.quote(output_filename)
                    response["Content-Disposition"] = (
                        f'attachment; filename="{fallback_filename}"; '
                        f"filename*=UTF-8''{encoded_filename}"
                    )
                return response
            finally:
                # Clean up temporary files
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(output_file_path):
                    os.remove(output_file_path)
    else:
        # Initialize form with saved settings if available
        form = AudioUploadForm(initial=saved_settings)
    return render(request, "upload.html", {"form": form})
