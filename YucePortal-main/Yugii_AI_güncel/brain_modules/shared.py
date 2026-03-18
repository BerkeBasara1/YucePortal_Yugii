# shared.py
import os
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("USE_TF", "0")
import builtins
import sys
import pyodbc   
from openai import OpenAI
from config import OPENAI_API_KEY, YA_2El_AracSatis,YA_RPA_MYSQL
from datetime import datetime, timedelta ,time
from flask import session
import re
import dateutil.parser
import random
import mysql.connector
import calendar
import difflib
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
from datetime import date
import requests
import oracledb

from ..yugii_general_assistant_fonk import GeneralAssistant
from ..NLP.yugii_brain_lists import *
from ..NLP import normalize as nrm
from ..NLP.people_schema import *
from pathlib import Path
from ..logger.yugii_logger import log_process_message
from ..logger.yugii_logger import YugiiLogger


def _safe_print(*args, **kwargs):
    sep = kwargs.pop("sep", " ")
    end = kwargs.pop("end", "\n")
    file = kwargs.pop("file", sys.stdout)
    flush = kwargs.pop("flush", False)
    text = sep.join(str(arg) for arg in args)
    try:
        builtins.print(text, sep="", end=end, file=file, flush=flush, **kwargs)
    except UnicodeEncodeError:
        encoding = getattr(file, "encoding", None) or "utf-8"
        safe_text = text.encode(encoding, errors="backslashreplace").decode(encoding, errors="ignore")
        builtins.print(safe_text, sep="", end=end, file=file, flush=flush, **kwargs)


print = _safe_print


def _build_openai_client():
    if not OPENAI_API_KEY:
        return None
    try:
        return OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"OpenAI client olusturulamadi: {e}")
        return None


general_assistant = GeneralAssistant()

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "instructions" / "yugii_personality.txt"


def _mysql_conn():
    """MySQL bağlantısını (config üzerinden) oluşturur ve döndürür."""
    try:
        conn = mysql.connector.connect(
            host=YA_RPA_MYSQL["host"],
            user=YA_RPA_MYSQL["user"],
            password=YA_RPA_MYSQL["password"],
            database=YA_RPA_MYSQL["database"]
        )
        return conn
    except Exception as e:
        print(f"❌ MySQL bağlantı hatası: {e}")
        return None

client = _build_openai_client()

WEEKDAY_MAP = {
    "pazartesi": 0, "salı": 1, "çarşamba": 2,
    "perşembe": 3, "cuma": 4, "cumartesi": 5, "pazar": 6
}

def contains_next_week_relative(text: str, rel_key: str, max_gap: int = 2) -> bool:
    tokens = text.split()

    next_idxs = [
        i for i, t in enumerate(tokens)
        if any(p in t for p in NEXT_WEEK_PREFIXES)   
    ] 
    rel_idxs = [
        i for i, t in enumerate(tokens)
        if any(r in t for r in RELATIVE_DAY_TRIGGERS[rel_key])
    ]

    for i in next_idxs:
        for j in rel_idxs:
            if abs(i - j) <= max_gap:
                return True
    return False

def gpt_fix_text(text):
    if client is None:
        return text
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sadece yazım hatalarını düzelt.\n"
                        "AY ve GÜN ifadelerini düzeltebilirme sadece anlamaya çalış kullanıcının yazdığı tarih veya tarihleri yazım yanlışları olsa bile doğruya çevirmeye çalış.\n"
                        "❗YILI ASLA değiştirme.\n"
                        "❗Tarihi yeniden yorumlama, sadece yazım/karakter hatalarını düzelt.\n"
                        "ÖRNEK: '17 kasim 2025' → '17 kasım 2025'.\n"
                        "ÖRNEK: '18 kasım için' → '18 kasım için'.\n"
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=40
        )
        return response.choices[0].message.content.strip()
    except:
        return text



#otopark Önümüzdeki 7 gün  kuralı  sabah 08:00
def get_effective_today():
    now = datetime.now()
    if now.time() < time(8, 0):
        return now.date() - timedelta(days=1)
    return now.date()


__all__ = [name for name in globals() if not name.startswith("__")]

