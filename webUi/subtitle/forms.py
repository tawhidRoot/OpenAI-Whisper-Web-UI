from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label="Upload Audio File", required=True)

    # Whisper model selection
    MODEL_CHOICES = [
        ("tiny", "Tiny"),
        ("base", "Base"),
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
        ("turbo", "Turbo"),
    ]
    model_choice = forms.ChoiceField(choices=MODEL_CHOICES, initial="base", label="Whisper Model")

    # Language selection (optional)
    language = forms.CharField(
        max_length=10, required=False, label="Language (Optional)", help_text="e.g., en, es, fr"
    )

    # Temperature setting (randomness in output)
    temperature = forms.FloatField(
        min_value=0.0, max_value=1.0, initial=0.0, required=True, label="Temperature"
    )

    # Beam size (number of best outputs)
    best_of = forms.IntegerField(min_value=1, max_value=10, initial=5, required=True, label="Best Of (Beam Size)")

    # Condition on previous text
    CONDITION_CHOICES = [("true", "Yes"), ("false", "No")]
    condition_on_previous_text = forms.ChoiceField(choices=CONDITION_CHOICES, initial="false", label="Condition on Previous Text")

    # Output format selection
    OUTPUT_CHOICES = [
        ("srt", "SRT (Subtitles)"),
        ("txt", "TXT (Plain Text)"),
        ("vtt", "VTT (WebVTT)"),
        ("json", "JSON (Full Output)"),
    ]
    output_format = forms.ChoiceField(choices=OUTPUT_CHOICES, initial="srt", label="Output Format")
