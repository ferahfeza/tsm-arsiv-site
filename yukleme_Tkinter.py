
import os
import json
import shutil
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# Ana dizin ve dosya yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTALAR_DIR = os.path.join(BASE_DIR, "notalar")
ROWS_JSON_PATH = os.path.join(BASE_DIR, "rows.json")

NOTALAR_DIR = "notalar"
ROWS_JSON_PATH = "rows.json"

def add_pdf_to_json(pdf_filename, eser, form, makam, usul, bestekar):
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

def git_push(pdf_filename):
    try:
        os.chdir(BASE_DIR)  # Ana dizine geç
        subprocess.run(["git", "add", os.path.join("notalar", pdf_filename)], check=True)
        subprocess.run(["git", "add", "rows.json"], check=True)
        subprocess.run(["git", "commit", "-m", f"{pdf_filename} ve rows.json eklendi/güncellendi"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        messagebox.showerror("Git Hatası", f"Git işlemi sırasında hata oluştu: {e}")
        return False

def upload():
    pdf_path = pdf_path_var.get()
    if not pdf_path or not os.path.isfile(pdf_path):
        messagebox.showerror("Hata", "Geçerli bir PDF dosyası seçmelisiniz.")
        return

    pdf_filename = os.path.basename(pdf_path)
    if not os.path.exists(NOTALAR_DIR):
        os.makedirs(NOTALAR_DIR)
    hedef_path = os.path.join(NOTALAR_DIR, pdf_filename)
    shutil.copy(pdf_path, hedef_path)

    eser = eser_var.get()
    form = form_var.get()
    makam = makam_var.get()
    usul = usul_var.get()
    bestekar = bestekar_var.get()

    if not eser or not form or not makam or not usul or not bestekar:
        messagebox.showerror("Hata", "Tüm alanları doldurmalısınız.")
        return

    add_pdf_to_json(pdf_filename, eser, form, makam, usul, bestekar)
    if git_push(pdf_filename):
        messagebox.showinfo("Başarılı", f"{pdf_filename} ve rows.json başarıyla eklendi ve repoya gönderildi.")

def select_pdf():
    file_path = filedialog.askopenfilename(title="PDF Seç", filetypes=[("PDF Dosyaları", "*.pdf")])
    pdf_path_var.set(file_path)

root = tk.Tk()
root.title("PDF ve rows.json Yükleyici")

tk.Label(root, text="PDF Dosyası:").grid(row=0, column=0, sticky="e")
pdf_path_var = tk.StringVar()
tk.Entry(root, textvariable=pdf_path_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Seç...", command=select_pdf).grid(row=0, column=2)

eser_var = tk.StringVar()
form_var = tk.StringVar()
makam_var = tk.StringVar()
usul_var = tk.StringVar()
bestekar_var = tk.StringVar()

tk.Label(root, text="Eser Adı:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=eser_var, width=40).grid(row=1, column=1, columnspan=2)

tk.Label(root, text="Form:").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=form_var, width=40).grid(row=2, column=1, columnspan=2)

tk.Label(root, text="Makam:").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=makam_var, width=40).grid(row=3, column=1, columnspan=2)

tk.Label(root, text="Usul:").grid(row=4, column=0, sticky="e")
tk.Entry(root, textvariable=usul_var, width=40).grid(row=4, column=1, columnspan=2)

tk.Label(root, text="Bestekar:").grid(row=5, column=0, sticky="e")
tk.Entry(root, textvariable=bestekar_var, width=40).grid(row=5, column=1, columnspan=2)

tk.Button(root, text="Yükle ve Gönder", command=upload, width=20).grid(row=6, column=1, pady=10)

root.mainloop()