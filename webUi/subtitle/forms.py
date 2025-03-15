from django import forms


class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label="Upload Audio File", required=True)

    MODEL_CHOICES = [
        ("tiny", "Tiny"),
        ("base", "Base"),
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
        ("turbo", "Turbo"),
    ]
    model_choice = forms.ChoiceField(
        choices=MODEL_CHOICES, initial="turbo", label="Whisper Model"
    )

    language = forms.CharField(
        max_length=10,
        required=False,
        initial="en",
        label="Language (Optional)",
        help_text="Enter language code (e.g., en) or 'multiple' for auto-detection of multiple languages",
    )

    temperature = forms.FloatField(
        min_value=0.0, max_value=1.0, initial=0.0, required=True, label="Temperature"
    )

    best_of = forms.IntegerField(
        min_value=1, max_value=10, initial=5, required=True, label="Best Of (Beam Size)"
    )

    CONDITION_CHOICES = [("true", "Yes"), ("false", "No")]
    condition_on_previous_text = forms.ChoiceField(
        choices=CONDITION_CHOICES, initial="false", label="Condition on Previous Text"
    )

    OUTPUT_CHOICES = [
        ("srt", "SRT (Subtitles)"),
        ("txt", "TXT (Plain Text)"),
        ("vtt", "VTT (WebVTT)"),
        ("json", "JSON (Full Output)"),
    ]
    output_format = forms.ChoiceField(
        choices=OUTPUT_CHOICES, initial="srt", label="Output Format"
    )

    max_subtitle_length = forms.IntegerField(
        min_value=1,
        initial=3,
        required=True,
        label="Max Subtitle Length (words)",
        help_text="Maximum number of words per line when in 'line' mode. In 'full' mode, the entire subtitle is shown.",
    )

    MAX_LENGTH_MODE_CHOICES = [
        ("line", "Per Line (split into multiple lines)"),
        ("full", "Full Segment (show entire subtitle)"),
    ]
    max_length_mode = forms.ChoiceField(
        choices=MAX_LENGTH_MODE_CHOICES,
        initial="full",
        required=True,
        label="Max Length Mode",
        help_text="Choose whether to apply max length per line or display the full subtitle segment.",
    )
