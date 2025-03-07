import os
import whisper
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioUploadForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import mimetypes
import json

def transcribe_audio(request):
    if request.method == "POST":
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file temporarily
            audio_file = request.FILES["audio_file"]
            file_name = os.path.splitext(audio_file.name)[0]  # Get file name without extension
            file_path = default_storage.save(f"temp/{audio_file.name}", ContentFile(audio_file.read()))

            # Load Whisper with user-selected options
            model_choice = form.cleaned_data["model_choice"]
            language = form.cleaned_data["language"] or None  # Auto-detect if not provided
            temperature = form.cleaned_data["temperature"]
            best_of = form.cleaned_data["best_of"]
            condition_on_previous_text = form.cleaned_data["condition_on_previous_text"] == "true"
            output_format = form.cleaned_data["output_format"]

            # Load the Whisper model
            model = whisper.load_model(model_choice)

            # Transcribe audio
            result = model.transcribe(
                file_path,
                language=language,
                temperature=temperature,
                best_of=best_of,
                condition_on_previous_text=condition_on_previous_text,
            )

            # Generate the correct file format
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

            # Prepare response for file download
            with open(output_file_path, "rb") as f:
                response = HttpResponse(f.read(), content_type=mimetypes.guess_type(output_file_path)[0])
                response["Content-Disposition"] = f'attachment; filename="{output_filename}"'

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
