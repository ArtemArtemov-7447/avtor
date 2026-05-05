import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class QuoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор случайных цитат")
        self.geometry("700x600")
        self.quotes = [
            {"quote": "Будьте изменением, которое вы хотите видеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
            {"quote": "Жизнь - это то, что происходит с тобой, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            # Добавьте еще 8+ цитат
        ]
        self.history = []
        self.load_history()
        
        # UI элементы
        tk.Label(self, text="Текущая цитата:").pack(pady=5)
        self.quote_label = tk.Label(self, text="", wraplength=650, justify="center", font=("Arial", 12))
        self.quote_label.pack(pady=10)
        
        tk.Button(self, text="Сгенерировать цитату", command=self.generate_quote, bg="lightblue").pack(pady=5)
        
        # История
        tk.Label(self, text="История:").pack(anchor="w", padx=10)
        self.history_listbox = tk.Listbox(self, height=10)
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Фильтры
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр автора:").pack(side="left")
        self.author_filter = tk.Entry(filter_frame, width=15)
        self.author_filter.pack(side="left", padx=5)
        tk.Label(filter_frame, text="Тема:").pack(side="left")
        self.theme_filter = tk.Entry(filter_frame, width=15)
        self.theme_filter.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Фильтр", command=self.filter_history).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Очистить", command=self.update_history).pack(side="left", padx=5)
        
        # Добавление цитаты
        add_frame = tk.Frame(self)
        add_frame.pack(pady=10)
        tk.Label(add_frame, text="Новая цитата:").grid(row=0, column=0)
        self.quote_entry = tk.Entry(add_frame, width=40)
        self.quote_entry.grid(row=0, column=1, padx=5)
        tk.Label(add_frame, text="Автор:").grid(row=0, column=2)
        self.author_entry = tk.Entry(add_frame, width=15)
        self.author_entry.grid(row=0, column=3, padx=5)
        tk.Label(add_frame, text="Тема:").grid(row=1, column=0)
        self.theme_entry = tk.Entry(add_frame, width=15)
        self.theme_entry.grid(row=1, column=1, padx=5)
        tk.Button(add_frame, text="Добавить", command=self.add_quote).grid(row=1, column=2, padx=5)
        
        tk.Button(self, text="Сохранить историю", command=self.save_history).pack(pady=5)
        self.update_history()
    
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Нет цитат!")
            return
        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["quote"]}"\n— {quote["author"]} (Тема: {quote["theme"]})')
        self.history.append(quote)
        self.update_history()
    
    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for q in self.history:
            self.history_listbox.insert(tk.END, f'"{q["quote"][:50]}..." — {q["author"]} ({q["theme"]})')
    
    def filter_history(self):
        author_f = self.author_filter.get().lower()
        theme_f = self.theme_filter.get().lower()
        self.history_listbox.delete(0, tk.END)
        for q in self.history:
            if (author_f in q["author"].lower() or not author_f) and (theme_f in q["theme"].lower() or not theme_f):
                self.history_listbox.insert(tk.END, f'"{q["quote"][:50]}..." — {q["author"]} ({q["theme"]})')
    
    def add_quote(self):
        quote_t = self.quote_entry.get().strip()
        author_t = self.author_entry.get().strip()
        theme_t = self.theme_entry.get().strip()
        if not all([quote_t, author_t, theme_t]):
            messagebox.showerror("Ошибка", "Все поля обязательны!")
            return
        self.quotes.append({"quote": quote_t, "author": author_t, "theme": theme_t})
        self.quote_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.theme_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Цитата добавлена!")
    
    def save_history(self):
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", "История сохранена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

if __name__ == "__main__":
    app = QuoteApp()
    app.mainloop()