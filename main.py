import tkinter as tk
from tkinter import messagebox
import random
import json
import os

FILE_NAME = "history.json"

quotes = [
    {"text": "Жизнь — это то, что с тобой происходит.", "author": "Джон Леннон", "theme": "Жизнь"},
    {"text": "Я думаю, значит существую.", "author": "Декарт", "theme": "Философия"},
    {"text": "Время — деньги.", "author": "Бенджамин Франклин", "theme": "Бизнес"},
    {"text": "Сила в правде.", "author": "Неизвестно", "theme": "Мораль"},
]

history = []

def load_history():
    global history
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            history = json.load(f)
            update_history_list()

def save_history():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_quote():
    quote = random.choice(quotes)
    text = f"{quote['text']} — {quote['author']} ({quote['theme']})"
    label.config(text=text)
    history.append(quote)
    update_history_list()
    save_history()

def update_history_list(filtered=None):
    listbox.delete(0, tk.END)
    data = filtered if filtered else history
    for q in data:
        listbox.insert(tk.END, f"{q['text']} — {q['author']} ({q['theme']})")

def filter_quotes():
    author = author_entry.get().strip()
    theme = theme_entry.get().strip()
    filtered = []
    for q in history:
        if (not author or q["author"] == author) and (not theme or q["theme"] == theme):
            filtered.append(q)
    update_history_list(filtered)

def add_quote():
    text = text_entry.get().strip()
    author = author_entry_add.get().strip()
    theme = theme_entry_add.get().strip()
    if not text or not author or not theme:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return
    quotes.append({"text": text, "author": author, "theme": theme})
    messagebox.showinfo("Успех", "Цитата добавлена!")

root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")

label = tk.Label(root, text="Нажми кнопку", wraplength=500)
label.pack(pady=10)

btn = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
btn.pack(pady=10)

listbox = tk.Listbox(root, width=80)
listbox.pack(pady=10)

tk.Label(root, text="Фильтр по автору").pack()
author_entry = tk.Entry(root)
author_entry.pack()

tk.Label(root, text="Фильтр по теме").pack()
theme_entry = tk.Entry(root)
theme_entry.pack()

filter_btn = tk.Button(root, text="Фильтровать", command=filter_quotes)
filter_btn.pack(pady=5)

tk.Label(root, text="Добавить новую цитату").pack(pady=10)

text_entry = tk.Entry(root)
text_entry.pack()

author_entry_add = tk.Entry(root)
author_entry_add.pack()

theme_entry_add = tk.Entry(root)
theme_entry_add.pack()

add_btn = tk.Button(root, text="Добавить", command=add_quote)
add_btn.pack(pady=5)

load_history()

root.mainloop()
