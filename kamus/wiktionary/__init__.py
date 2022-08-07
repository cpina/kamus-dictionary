# LANGUAGES taken from
ALL_LANGUAGES = \
 {'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian', 'rup': 'Aromanian',
  'as': 'Assamese', 'ast': 'Asturian', 'az': 'Azerbaijani', 'mbf': 'Baba Malay', 'ba': 'Bashkir', 'eu': 'Basque',
  'be': 'Belarusian', 'bn': 'Bengali', 'br': 'Breton', 'kxd': 'Brunei Malay', 'bg': 'Bulgarian', 'my': 'Burmese',
  'bua': 'Buryat', 'ca': 'Catalan', 'ceb': 'Cebuano', 'dtp': 'Central Dusun', 'chg': 'Chagatai', 'ccc': 'Chamicuro',
  'ce': 'Chechen', 'chr': 'Cherokee', 'chy': 'Cheyenne', 'cv': 'Chuvash', 'coo': 'Comox', 'kw': 'Cornish',
  'crh': 'Crimean Tatar', 'cs': 'Czech', 'dlm': 'Dalmatian', 'da': 'Danish', 'dv': 'Dhivehi', 'sce': 'Dongxiang',
  'duu': 'Drung', 'nl': 'Dutch', 'wnm': 'Egyptian', 'myv': 'Erzya', 'eo': 'Esperanto', 'et': 'Estonian',
  'fo': 'Faroese', 'fi': 'Finnish', 'fr': 'French', 'fur': 'Friulian', 'gag': 'Gagauz', 'gl': 'Galician',
  'ka': 'Georgian', 'de': 'German', 'got': 'Gothic', 'el': 'Greek', 'gu': 'Gujarati', 'haw': 'Hawaiian', 'he': 'Hebrew',
  'mba': 'Higaonon', 'hi': 'Hindi', 'hu': 'Hungarian', 'hrx': 'Hunsrik', 'iba': 'Iban', 'is': 'Icelandic', 'io': 'Ido',
  'id': 'Indonesian', 'ia': 'Interlingua', 'ga': 'Irish', 'it': 'Italian', 'ium': 'Iu Mien', 'ja': 'Japanese',
  'jv': 'Javanese', 'kgp': 'Kaingang', 'xal': 'Kalmyk', 'kam': 'Kamba', 'kn': 'Kannada', 'cak': 'Kaqchikel',
  'krc': 'Karachay-Balkar', 'kaa': 'Karakalpak', 'csb': 'Kashubian', 'kk': 'Kazakh', 'kjh': 'Khakas', 'km': 'Khmer',
  'ki': 'Kikuyu', 'ko': 'Korean', 'kum': 'Kumyk', 'ky': 'Kyrgyz', 'lo': 'Lao', 'ltg': 'Latgalian', 'la': 'Latin',
  'lv': 'Latvian', 'lez': 'Lezgi', 'li': 'Limburgish', 'ln': 'Lingala', 'lt': 'Lithuanian', 'liv': 'Livonian',
  'lou': 'Louisiana Creole French', 'luy': 'Luhya', 'luo': 'Luo', 'lb': 'Luxembourgish', 'khb': 'Lü',
  'mk': 'Macedonian', 'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mnk': 'Mandinka', 'gv': 'Manx', 'mi': 'Maori',
  'mrw': 'Maranao', 'mr': 'Marathi', 'mrc': 'Maricopa', 'moh': 'Mohawk', 'nv': 'Navajo', 'ne': 'Nepali',
  'zdj': 'Ngazidja Comorian', 'niv': 'Nivkh', 'frr': 'North Frisian', 'se': 'Northern Sami', 'oc': 'Occitan',
  'oj': 'Ojibwe', 'orv': 'Old East Slavic', 'ang': 'Old English', 'or': 'Oriya', 'pau': 'Palauan', 'ps': 'Pashto',
  'fa': 'Persian', 'pdt': 'Plautdietsch', 'pl': 'Polish', 'pt': 'Portuguese', 'qu': 'Quechua', 'rom': 'Romani',
  'ro': 'Romanian', 'rm': 'Romansch', 'ru': 'Russian', 'rue': 'Rusyn', 'sa': 'Sanskrit', 'sc': 'Sardinian',
  'gd': 'Scottish Gaelic', 'cjs': 'Shor', 'ii': 'Sichuan Yi', 'scn': 'Sicilian', 'si': 'Sinhalese', 'sk': 'Slovak',
  'sl': 'Slovene', 'st': 'Sotho', 'alt': 'Southern Altai', 'sma': 'Southern Sami', 'es': 'Spanish', 'sw': 'Swahili',
  'sv': 'Swedish', 'tl': 'Tagalog', 'tg': 'Tajik', 'ta': 'Tamil', 'twf': 'Taos', 'tt': 'Tatar', 'te': 'Telugu',
  'th': 'Thai', 'bo': 'Tibetan', 'ti': 'Tigrinya', 'tr': 'Turkish', 'tk': 'Turkmen', 'tyv': 'Tuvan', 'udi': 'Udi',
  'udm': 'Udmurt', 'uga': 'Ugaritic', 'uk': 'Ukrainian', 'umb': 'Umbundu', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek',
  'vec': 'Venetian', 'vi': 'Vietnamese', 'wym': 'Vilamovian', 'wa': 'Walloon', 'war': 'Waray-Waray', 'cy': 'Welsh',
  'mww': 'White Hmong', 'win': 'Winnebago', 'yai': 'Yagnobi', 'sah': 'Yakut', 'yi': 'Yiddish', 'esu': "Yup'ik",
  'zza': 'Zazaki', 'za': 'Zhuang', 'zu': 'Zulu', 'en': 'English'}

FROM_LANGUAGES = {
    "en": "English",
}

ALL_LANGUAGES = dict(sorted(ALL_LANGUAGES.items()))
FROM_LANGUAGES = dict(sorted(FROM_LANGUAGES.items()))
