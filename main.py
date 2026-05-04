import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

HISTORY_FILE = 'history.json'

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x650")
        self.root.configure(padx=10, pady=10)

        self.quotes_db = [
            {"text": "Жизнь — это то, что происходит, пока вы строите другие планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "theme": "Наука"},
            {"text": "Сложнейшее в любом деле — сделать первый шаг.", "author": "Марк Твен", "theme": "Мотивация"},
            {"text": "Успех — это способность шагать от одной неудачи к другой, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Успех"},
            {"text": "Будьте тем изменением, которое вы хотите видеть в мире.", "author": "Махатма Ганди", "theme": "Жизнь"}
        ]
        
        self.history = self.load_history()

        self.setup_ui()
        self.update_history_listbox()

    def setup_ui(self):
        frame_top = tk.LabelFrame(self.root, text="Генерация цитаты", padx=10, pady=10)
        frame_top.pack(fill="x", pady=5)

        tk.Label(frame_top, text="Фильтр по автору:").grid(row=0, column=0, sticky="w", pady=2)
        self.author_filter = ttk.Combobox(frame_top, state="readonly", width=20)
        self.author_filter.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_top, text="Фильтр по теме:").grid(row=1, column=0, sticky="w", pady=2)
        self.theme_filter = ttk.Combobox(frame_top, state="readonly", width=20)
        self.theme_filter.grid(row=1, column=1, padx=5, pady=2)

        self.update_filters()

        btn_generate = tk.Button(frame_top, text="Сгенерировать цитату", command=self.generate_quote, bg="#e0e0e0")
        btn_generate.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

        self.lbl_current_quote = tk.Label(frame_top, text="Нажмите кнопку, чтобы получить цитату", wraplength=550, font=("Arial", 11, "italic"), fg="blue", justify="center")
        self.lbl_current_quote.grid(row=3, column=0, columnspan=2, pady=10)

        frame_add = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=10)
        frame_add.pack(fill="x", pady=5)

        tk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky="w")
        self.entry_text = tk.Entry(frame_add, width=60)
        self.entry_text.grid(row=0, column=1, pady=2, padx=5)

        tk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky="w")
        self.entry_author = tk.Entry(frame_add, width=60)
        self.entry_author.grid(row=1, column=1, pady=2, padx=5)

        tk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky="w")
        self.entry_theme = tk.Entry(frame_add, width=60)
        self.entry_theme.grid(row=2, column=1, pady=2, padx=5)

        btn_add = tk.Button(frame_add, text="Добавить в базу", command=self.add_quote)
        btn_add.grid(row=3, column=0, columnspan=2, pady=5)

        frame_history = tk.LabelFrame(self.root, text="История сгенерированных цитат", padx=10, pady=10)
        frame_history.pack(fill="both", expand=True, pady=5)

        self.history_listbox = tk.Listbox(frame_history, width=80, height=10)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_history, orient="vertical")
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

    def update_filters(self):
        authors = list(set([q["author"] for q in self.quotes_db]))
        themes = list(set([q["theme"] for q in self.quotes_db]))
        
        self.author_filter['values'] = ["Все"] + authors
        self.author_filter.current(0)
        
        self.theme_filter['values'] = ["Все"] + themes
        self.theme_filter.current(0)

    def generate_quote(self):
        selected_author = self.author_filter.get()
        selected_theme = self.theme_filter.get()

        filtered_quotes = self.quotes_db

        if selected_author != "Все":
            filtered_quotes = [q for q in filtered_quotes if q["author"] == selected_author]
        
        if selected_theme != "Все":
            filtered_quotes = [q for q in filtered_quotes if q["theme"] == selected_theme]

        if not filtered_quotes:
            messagebox.showinfo("Инфо", "По заданным фильтрам цитат не найдено.")
            return

        quote = random.choice(filtered_quotes)
        display_text = f"«{quote['text']}»\