import sys
import os
from datetime import datetime
from flask import Flask, session
from contextlib import redirect_stdout
from io import StringIO

# -------------------------------
# PROJECT ROOT (RPA-PROJECTS)
# -------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from Yugii_AI_güncel.yugii_brain_ai import BrainAIYugii

# Minimal Flask app (sadece context için)
app = Flask(__name__)
app.secret_key = "test"   # Flask session için zorunlu


def run_tests():

    brain = BrainAIYugii.get_instance()

    test_questions = [

        # --- PERSON STATUS ---
        "şirkette yarın kaç kişi var",
        "it departmanında cuma kaç kişi ofis",
        "it departmanında cuma kimler ofis",
        "şirkette yarın kaç kişi var",  
        "şirkette yarın kimler var",
        "it departmanında yarın kaç kişi var",
        "it departmanında yarın kimler var",
        "Sude ofiste mi?",
        "Sude nerede?",
        "Sude bugün nerede?",

        # --- DEPARTMENT ---
        "IT departmanında kimler var?",
        "IT departmanında kaç kişi var?",
        "IT departmanında bugün kimler ofiste?",

        # --- COMPANY TODAY ---
        "Şirkette bugün kimler var?",
        "Şirkette bugün kaç kişi var?",
        "Kimler ofiste bugün?",
        "Cuma kaç kişi ofis işaretlemiş?",

        # --- COMPANY FUTURE ---
        "Şirkette yarın kimler var?",

        # --- COMPANY STRUCTURE ---
        "Şirketteki departmanlar nelerdir?",
        "Şirketteki departman sayısı kaç?",

        # --- PAST QUERY ---
        "Geçen hafta cuma kimler ofisteymiş?",

        # --- OTHER MODULES ---
        "Bugün hava nasıl?",
        "Skoda hakkında bilgi ver",
        "Tüm çalışanların mail adreslerini Excel al",
        "Haftaya tüm günler ofis işaretle",

    ]


    output_file = os.path.join(
        PROJECT_ROOT,
        "Yugii_AI_güncel",
        "test",
        "outputs.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:

        # Flask request context aç
        with app.test_request_context():

            # -------------------------------
            # SESSION (Sude Bayhan)
            # -------------------------------
            session["ID"] = 5  # 👉 BURAYA DB'deki GERÇEK ID'ni yaz
            session["username"] = "sudeb"
            session["name"] = "Sude"
            session["surname"] = "Bayhan"
            session["fullname"] = "Sude Bayhan"
            session["departman"] = "Bilgi Teknolojileri"

            for i, question in enumerate(test_questions, 1):

                # Terminal printleri sustur
                fake_out = StringIO()
                with redirect_stdout(fake_out):
                    try:
                        answer = brain.process_message(question)
                    except Exception as e:
                        answer = f"❌ HATA: {e}"

                f.write(f"--- TEST {i} ---\n")
                f.write(f"SORU:\n{question}\n\n")
                f.write(f"CEVAP:\n{answer}\n\n")
                f.write("=" * 60 + "\n\n")

    print("✅ Test tamamlandı. Çıktı dosyaya yazıldı.")


if __name__ == "__main__":
    run_tests()
