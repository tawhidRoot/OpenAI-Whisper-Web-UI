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

    LANGUAGE_CHOICES = [
        ("", "Auto-Detect (Multiple)"),
        ("af", "Afrikaans"),
        ("am", "Amharic"),
        ("ar", "Arabic"),
        ("as", "Assamese"),
        ("az", "Azerbaijani"),
        ("ba", "Bashkir"),
        ("be", "Belarusian"),
        ("bg", "Bulgarian"),
        ("bn", "Bengali"),
        ("bo", "Tibetan"),
        ("br", "Breton"),
        ("bs", "Bosnian"),
        ("ca", "Catalan"),
        ("cs", "Czech"),
        ("cy", "Welsh"),
        ("da", "Danish"),
        ("de", "German"),
        ("el", "Greek"),
        ("en", "English"),
        ("eo", "Esperanto"),
        ("es", "Spanish"),
        ("et", "Estonian"),
        ("eu", "Basque"),
        ("fa", "Persian"),
        ("fi", "Finnish"),
        ("fo", "Faroese"),
        ("fr", "French"),
        ("gl", "Galician"),
        ("gu", "Gujarati"),
        ("ha", "Hausa"),
        ("haw", "Hawaiian"),
        ("he", "Hebrew"),
        ("hi", "Hindi"),
        ("hr", "Croatian"),
        ("ht", "Haitian Creole"),
        ("hu", "Hungarian"),
        ("hy", "Armenian"),
        ("id", "Indonesian"),
        ("is", "Icelandic"),
        ("it", "Italian"),
        ("ja", "Japanese"),
        ("jw", "Javanese"),
        ("ka", "Georgian"),
        ("kk", "Kazakh"),
        ("km", "Khmer"),
        ("kn", "Kannada"),
        ("ko", "Korean"),
        ("la", "Latin"),
        ("lb", "Luxembourgish"),
        ("ln", "Lingala"),
        ("lo", "Lao"),
        ("lt", "Lithuanian"),
        ("lv", "Latvian"),
        ("mg", "Malagasy"),
        ("mi", "Maori"),
        ("mk", "Macedonian"),
        ("ml", "Malayalam"),
        ("mn", "Mongolian"),
        ("mr", "Marathi"),
        ("ms", "Malay"),
        ("mt", "Maltese"),
        ("my", "Burmese"),
        ("ne", "Nepali"),
        ("nl", "Dutch"),
        ("nn", "Norwegian Nynorsk"),
        ("no", "Norwegian"),
        ("oc", "Occitan"),
        ("pa", "Punjabi"),
        ("pl", "Polish"),
        ("ps", "Pashto"),
        ("pt", "Portuguese"),
        ("ro", "Romanian"),
        ("ru", "Russian"),
        ("sa", "Sanskrit"),
        ("sd", "Sindhi"),
        ("si", "Sinhala"),
        ("sk", "Slovak"),
        ("sl", "Slovenian"),
        ("sn", "Shona"),
        ("so", "Somali"),
        ("sq", "Albanian"),
        ("sr", "Serbian"),
        ("su", "Sundanese"),
        ("sv", "Swedish"),
        ("sw", "Swahili"),
        ("ta", "Tamil"),
        ("te", "Telugu"),
        ("tg", "Tajik"),
        ("th", "Thai"),
        ("tk", "Turkmen"),
        ("tl", "Tagalog"),
        ("tr", "Turkish"),
        ("tt", "Tatar"),
        ("uk", "Ukrainian"),
        ("ur", "Urdu"),
        ("uz", "Uzbek"),
        ("vi", "Vietnamese"),
        ("xh", "Xhosa"),
        ("yi", "Yiddish"),
        ("yo", "Yoruba"),
        ("zh", "Chinese"),
        ("zu", "Zulu"),
    ]

    language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=False,
        initial="",
        label="Language",
        help_text="Select the language or choose Auto-Detect",
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
