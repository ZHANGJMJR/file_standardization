import os
import sys
import locale
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

LANG_FILE = "last_language.txt"

LANGUAGES = {
    "zh": {
        "title": "固定资产文件标准化处理工具",
        "select_file": "选择文件",
        "start": "开始处理",
        "progress": "处理进度",
        "select_language": "语言",
        "done": "处理完成！已打开文件所在目录。",
    },
    "mn": {
        "title": "Бэлэгтийн бэлэгт файлын стандартизэлтийн бэлэглэх хэрэгсэл",
        "select_file": "Файл сонгох",
        "start": "Боловсруулж эхлэх",
        "progress": "Явц",
        "select_language": "Хэл",
        "done": "Боловсруулалт дууслаа! Файлын хавтас нээгдлээ。",
    },
    "en": {
        "title": "Fixed Asset File Standardization Tool",
        "select_file": "Select File",
        "start": "Start Processing",
        "progress": "Progress",
        "select_language": "Language",
        "done": "Processing complete! Folder opened.",
    },
}

def detect_system_language():
    sys_lang = locale.getdefaultlocale()[0]
    if sys_lang is None:
        return "en"
    if "zh" in sys_lang:
        return "zh"
    elif "mn" in sys_lang:
        return "mn"
    else:
        return "en"

def load_last_language():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            lang = f.read().strip()
            if lang in LANGUAGES:
                return lang
    return detect_system_language()

def save_language(lang):
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        f.write(lang)

class FileProcessorApp:
    def __init__(self, root, lang):
        self.root = root
        self.current_lang = lang
        self.texts = LANGUAGES.get(self.current_lang, LANGUAGES[detect_system_language()])
        self.file_path = None

        self.style = ttk.Style(theme="cosmo")
        self.root.title(self.texts["title"])
        self.root.geometry("1160x480")
        self.root.minsize(760, 480)

        self.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.texts = LANGUAGES.get(self.current_lang, LANGUAGES[detect_system_language()])
        self.root.title(self.texts["title"])

        # 顶部语言选择
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(top_frame, text=f"{self.texts['select_language']}: ", font=("Microsoft YaHei", 11)).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_combo = ttk.Combobox(
            top_frame,
            textvariable=self.lang_var,
            values=["中文", "ᠮᠣᠩᠭᠣᠯ", "English"],
            width=12,
            state="readonly",
            font=("Microsoft YaHei", 11)
        )
        lang_combo.pack(side=tk.LEFT, padx=5)
        lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=25)

        # 文件选择按钮
        self.select_button = ttk.Button(main_frame, text=self.texts["select_file"], command=self.select_file,
                                        bootstyle=INFO, width=22)
        self.select_button.pack(pady=15, ipady=10)

        # 开始按钮
        self.start_button = ttk.Button(main_frame, text=self.texts["start"], command=self.start_processing,
                                       bootstyle=SUCCESS, width=22)
        self.start_button.pack(pady=15, ipady=10)

        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=25)

        ttk.Label(progress_frame, text=self.texts["progress"], font=("Microsoft YaHei", 11)).pack(anchor=tk.W)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, bootstyle=SUCCESS,
                                            length=500)
        self.progress_bar.pack(fill=tk.X, expand=True, pady=8)

        # 百分比 Label 放在进度条上方
        self.percent_label = ttk.Label(progress_frame, text="0%", font=("Microsoft YaHei", 10, "bold"))
        self.percent_label.place(relx=0.5, rely=0.5, anchor="center")

    def select_file(self):
        path = filedialog.askopenfilename(title=self.texts["select_file"])
        if path:
            self.file_path = path
            messagebox.showinfo(self.texts["title"], f"{self.texts['select_file']}: {path}")

    def start_processing(self):
        if not self.file_path:
            messagebox.showwarning(self.texts["title"], self.texts["select_file"])
            return
        self.start_button.configure(state=tk.DISABLED)
        threading.Thread(target=self.process_file, daemon=True).start()

    def process_file(self):
        for i in range(101):
            time.sleep(0.03)
            self.root.after(0, self.update_progress, i)
        self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
        self.root.after(0, lambda: messagebox.showinfo(self.texts["title"], self.texts["done"]))

        output_dir = os.path.dirname(self.file_path)
        if sys.platform == "darwin":
            os.system(f'open "{output_dir}"')
        elif sys.platform == "win32":
            os.system(f'start "" "{output_dir}"')

    def update_progress(self, value):
        self.progress_var.set(value)
        self.percent_label.config(text=f"{value}%")
        self.root.update_idletasks()

    def on_language_change(self, event):
        selected = self.lang_var.get()
        if selected == "中文":
            self.current_lang = "zh"
        elif selected == "ᠮᠣᠩᠭᠣᠯ":
            self.current_lang = "mn"
        else:
            self.current_lang = "en"
        save_language(self.current_lang)
        self.create_widgets()


if __name__ == "__main__":
    lang = load_last_language()
    root = ttk.Window(themename="cosmo")
    app = FileProcessorApp(root, lang)
    root.mainloop()