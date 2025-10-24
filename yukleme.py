import os
import json
from datetime import datetime

# Ayarlar
NOTALAR_DIR = "notalar"
ROWS_JSON_PATH = "rows.json"

def add_pdf_to_json(pdf_filename, eser, form, makam, usul, bestekar):

    # PDF dosyasının tam yolu
    pdf_path = os.path.join(NOTALAR_DIR, pdf_filename)
    if not os.path.exists(pdf_path):
        print(f"Dosya bulunamadı: {pdf_path}")
        return

    # rows.json'u oku veya oluştur
    if os.path.exists(ROWS_JSON_PATH):
        with open(ROWS_JSON_PATH, "r", encoding="utf-8") as f:
            try:
                rows = json.load(f)
            except json.JSONDecodeError:
                rows = []
    else:
        rows = []

    # id otomatik arttır
    max_id = 0
    for row in rows:
        if isinstance(row, dict) and "id" in row:
            max_id = max(max_id, row["id"])
    new_id = max_id + 1

    # Yeni kayıt
    new_row = {
        "id": new_id,
        "eser": eser,
        "form": form,
        "makam": makam,
        "usul": usul,
        "bestekar": bestekar,
        "dosya": pdf_filename
    }

    rows.append(new_row)

    # JSON dosyasına yaz
    with open(ROWS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"{pdf_filename} rows.json dosyasına eklendi.")


if __name__ == "__main__":
    # notalar klasörü yoksa oluştur
    os.makedirs(NOTALAR_DIR, exist_ok=True)


    # Dosya seçme penceresi aç
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        print("PDF dosyanızı seçmek için dosya penceresi açılıyor...")
        pdf_path_input = filedialog.askopenfilename(title="PDF Seç", filetypes=[("PDF Dosyaları", "*.pdf")])
        if not pdf_path_input:
            print("Herhangi bir dosya seçilmedi!")
            exit(1)
    except Exception as e:
        print(f"Dosya seçme penceresi açılamadı: {e}\nAlternatif olarak terminalden yol girin:")
        pdf_path_input = input().strip()
        if not os.path.isfile(pdf_path_input):
            print("PDF dosyası bulunamadı!")
            exit(1)

    pdf_filename = os.path.basename(pdf_path_input)
    hedef_path = os.path.join(NOTALAR_DIR, pdf_filename)
    import shutil
    shutil.copy(pdf_path_input, hedef_path)
    print(f"PDF dosyası {hedef_path} konumuna kopyalandı.")

    print("Eser adı:")
    eser = input().strip()
    print("Form:")
    form = input().strip()
    print("Makam:")
    makam = input().strip()
    print("Usul:")
    usul = input().strip()
    print("Bestekar:")
    bestekar = input().strip()

    add_pdf_to_json(pdf_filename, eser, form, makam, usul, bestekar)

    import subprocess
    try:
        subprocess.run(["git", "add", os.path.join("notalar", pdf_filename), "rows.json"], check=True)
        subprocess.run(["git", "commit", "-m", f"{pdf_filename} ve rows.json eklendi/güncellendi"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Değişiklikler repoya gönderildi.")
    except Exception as e:
        print(f"Git işlemi sırasında hata oluştu: {e}")