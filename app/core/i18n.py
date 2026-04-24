import gettext
from pathlib import Path

LOCALES_DIR = Path("locales")

translations = {}


def load_translations():
    for lang in ["en", "fa"]:
        translations[lang] = gettext.translation(
            "messages", localedir=LOCALES_DIR, languages=[lang], fallback=True
        )


def translate(lang: str, message: str):
    trans = translations.get(lang)
    if not trans:
        trans = translations["en"]
    return trans.gettext(message)
