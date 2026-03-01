from deep_translator import GoogleTranslator

def translate_text(text, target_lang="hi"):
    """
    Translate text to target language.
    target_lang codes: hi (Hindi), ta (Tamil), kn (Kannada), te (Telugu), mr (Marathi)
    """
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return text  # fallback to original