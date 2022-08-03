
# LANGUAGES taken from https://wiktionary.org HTML code
LANGUAGES = {
    "cs": "Čeština",
    "ca": "Català",
    "pl": "Polski",
    "de": "Deutsch",
    "et": "Eesti",
    "el": "Ελληνικά",
    "en": "English",
    "es": "Español",
    "eo": "Esperanto",
    "fa": "فارسی",
    "fr": "Français",
    "ko": "한국어",
    "hy": "Հայերեն",
    "hi": "हिन्दी",
    "io": "Ido",
    "id": "Bahasa Indonesia",
    "it": "Italiano",
    "kn": "ಕನ್ನಡ",
    "ku": "Kurdî / كوردی",
    "lt": "Lietuvių",
    "li": "Limburgs",
    "hu": "Magyar",
    "mg": "Malagasy",
    "ml": "മലയാളം",
    "my": "မြန်မာဘာသာ",
    "nl": "Nederlands",
    "ja": "日本語",
    "nb": "Norsk",
    "or": "ଓଡି଼ଆ",
    "uz": "Oʻzbekcha / Ўзбекча",
    "pt": "Português",
    "ro": "Română",
    "ru": "Русский",
    "sr": "Српски / Srpski",
    "sh": "Srpskohrvatski / Српскохрватски",
    "fi": "Suomi",
    "sv": "Svenska",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "th": "ภาษาไทย",
    "tr": "Türkçe",
    "vi": "Tiếng Việt",
    "zh": "中文<",
}

LANGUAGES_LIST = []

for short, long in LANGUAGES.items():
    LANGUAGES_LIST.append((short, long))

print()