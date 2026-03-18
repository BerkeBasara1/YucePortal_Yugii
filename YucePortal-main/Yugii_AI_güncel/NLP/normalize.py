# Yugii_AI_güncel/NLP/normalize.py
import re
import difflib

def normalize_people_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()

    replacements = {
        "ı": "i", "ğ": "g", "ş": "s",
        "ö": "o", "ü": "u", "ç": "c",
        "’": "", "'": "",
        ",": " ", ".": " ", "-": " "
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r"(\w+)(mi|mı|mu|mü)\b", r"\1 \2", text)

    return " ".join(text.split())

def normalize_calendar_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    replacements = {
        "ı": "i", "İ": "i",
        "ğ": "g", "ş": "s",
        "ö": "o", "ü": "u",
        "ç": "c",
        "’": "", "'": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    DAY_ALIASES = {
        "pzt":"pazartesi","pzrt":"pazartesi","pts":"pazartesi","pzrts":"pazartesi","pazrts":"pazartesi","paztesi":"pazartesi","pazrtesi":"pazartesi","pazrt":"pazartesi",
        "sal":"salı","sali":"salı","sl":"salı","salii":"salı",
        "cars":"çarşamba","crs":"çarşamba","crsb":"çarşamba","crsmb":"çarşamba","carsmb":"çarşamba","carsamba":"çarşamba","carsm":"çarşamba","carsmbe":"çarşamba",
        "per":"perşembe","prs":"perşembe","prsb":"perşembe","pers":"perşembe","persembe":"perşembe","persmbe":"perşembe","perş":"perşembe",
        "cum":"cuma","cm":"cuma",
        "cmt":"cumartesi","cmrts":"cumartesi","cumrts":"cumartesi","cumrtesi":"cumartesi","cumar":"cumartesi","cumrt":"cumartesi",
        "paz":"pazar","pzr":"pazar","pzrgn":"pazar"
    }

    for short, full in DAY_ALIASES.items():
        text = re.sub(rf"\b{short}\b", full, text)

    return " ".join(text.split())

def normalize_intent_text(text: str) -> str:
    return normalize_people_text(text)

def normalize_field_name(field: str) -> str:
    f = normalize_people_text(field)
    SUFFIXES = [
        "inda", "inde", "unda", "unde",
        "dan", "den", "da", "de",
        "i", "ı", "u", "ü",
        "ni", "nı", "nu", "nü"
    ]
    for suf in SUFFIXES:
        if f.endswith(suf) and len(f) > len(suf) + 1:
            return f[:-len(suf)]
    return f

def normalize_people_name_token(token: str) -> str:
    if not token:
        return ""
    token = token.lower()

    token = token.replace("seyler", "sey")
    token = token.replace("birsey", "bir sey")
    token = token.replace("bisey", "bir sey")
    token = token.replace("bişey", "bir şey")

    SUFFIXES = [
        "ninki","ndaki","daki",
        "nin","nın","nun","nün",
        "dan","den","tan","ten",
        "yla","yle",
        "yi","yı","yu","yü",
        "in","ın","un","ün",
        "ya","ye"
    ]
    for s in SUFFIXES:
        if token.endswith(s) and len(token) > len(s) + 1:
            return token[:-len(s)]
    return token

def normalize_department_suffixes(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\b(\w+?)larin\b", r"\1lari", text)
    text = re.sub(r"\b(\w+?)lerin\b", r"\1leri", text)
    text = re.sub(r"\b(\w+?)larinin\b", r"\1lari", text)
    text = re.sub(r"\b(\w+?)lerinin\b", r"\1leri", text)
    text = re.sub(r"\b([a-z]{2,5})(nin|nın|nun|nün)\b", r"\1", text)

    SUFFIXES = [
        "lerden","lardan","nin","nın","nun","nün","den","dan","ten","tan",
        "de","da","te","ta","nde","nda","inde","ında","ine","ına","ya","ye"
    ]
    for suf in SUFFIXES:
        text = re.sub(
            rf"\b([\wçğıöşü]+(?:\s+[\wçğıöşü]+)*)[' ]?{suf}\b",
            r"\1",
            text
        )

    text = re.sub(r"\b([a-z]{2,5})(den|dan|de|da|ten|tan|nde|nda)\b", r"\1", text)
    return text

def fuzzy_match(word, options, threshold=0.75):
    matches = difflib.get_close_matches(word, options, n=1, cutoff=threshold)
    return matches[0] if matches else None

def fuzzy_match_in_text(msg: str, keywords: list, threshold=0.75) -> bool:
    if not msg:
        return False
    tokens = msg.split()
    for t in tokens:
        if fuzzy_match(t, keywords, threshold):
            return True
    return False

#noramlize extract history date
def normalize_month_with_suffixes( text: str) -> str:
    """
    Türkçe ay adlarına gelen çekim eklerini temizler.
    ocakta, ocaktan, ocağın, ocakta → ocak
    """
    if not text:
        return ""

    months = [
        "ocak","şubat","mart","nisan","mayıs","haziran",
        "temmuz","ağustos","eylül","ekim","kasım","aralık"
    ]

    suffixes = [
        "ta","te","da","de",
        "tan","ten","dan","den",
        "in","ın","un","ün",
        "nin","nın","nun","nün",
        "inda","inde","ında","inde",
        "ine","ina","una","une"
    ]

    for m in months:
        for s in suffixes:
            text = re.sub(rf"\b{m}{s}\b", m, text)

    return text

def format_date_with_day( date_obj):
    days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    return f"{date_obj.strftime('%d.%m.%Y')} {days[date_obj.weekday()]}"

   
