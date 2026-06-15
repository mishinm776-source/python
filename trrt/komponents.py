from tkinter import *
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Личный финансовый учёт")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.balance_frame = Frame(self.root, bg="#2c3e50", height=80)
        self.balance_frame.pack(fill=X)
        self.balance_label = Label(self.balance_frame, text="Баланс: 0 руб.", font=("Arial", 20, "bold"),
                                   fg="white", bg="#2c3e50")
        self.balance_label.pack(pady=20)

        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.setup_transactions_table(main_frame)
        self.setup_form_panel(main_frame)
        self.setup_bottom_panel()

    def setup_transactions_table(self, parent):
        left_frame = LabelFrame(parent, text="Все транзакции", font=("Arial", 12), bg="#f0f0f0")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        columns = ("id", "date", "category", "amount", "type", "comment")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        
        headings = {"id": "ID", "date": "Дата", "category": "Категория", 
                   "amount": "Сумма", "type": "Тип", "comment": "Комментарий"}
        widths = {"id": 40, "date": 100, "category": 120, "amount": 80, "type": 60, "comment": 200}
        
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col])

        scrollbar = Scrollbar(left_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.controller.on_transaction_select)

    def setup_form_panel(self, parent):
        right_frame = LabelFrame(parent, text="Добавить / Редактировать", font=("Arial", 12), bg="#f0f0f0")
        right_frame.pack(side=RIGHT, fill=Y, padx=5, ipadx=10)

        Label(right_frame, text="Дата (ГГГГ-ММ-ДД):", bg="#f0f0f0").grid(row=0, column=0, sticky=W, pady=5)
        self.date_entry = Entry(right_frame, width=20)
        self.date_entry.grid(row=0, column=1, pady=5)

        Label(right_frame, text="Категория:", bg="#f0f0f0").grid(row=1, column=0, sticky=W, pady=5)
        self.category_combo = ttk.Combobox(right_frame, width=17)
        self.category_combo.grid(row=1, column=1, pady=5)

        Label(right_frame, text="Сумма:", bg="#f0f0f0").grid(row=2, column=0, sticky=W, pady=5)
        self.amount_entry = Entry(right_frame, width=20)
        self.amount_entry.grid(row=2, column=1, pady=5)

        Label(right_frame, text="Тип:", bg="#f0f0f0").grid(row=3, column=0, sticky=W, pady=5)
        self.type_var = StringVar(value="Расход")
        ttk.Radiobutton(right_frame, text="Доход", variable=self.type_var, value="Доход").grid(row=3, column=1, sticky=W)
        ttk.Radiobutton(right_frame, text="Расход", variable=self.type_var, value="Расход").grid(row=4, column=1, sticky=W)

        Label(right_frame, text="Комментарий:", bg="#f0f0f0").grid(row=5, column=0, sticky=W, pady=5)
        self.comment_entry = Entry(right_frame, width=20)
        self.comment_entry.grid(row=5, column=1, pady=5)

        Button(right_frame, text="Добавить", command=self.controller.add_transaction, 
               bg="#27ae60", fg="white", width=15).grid(row=6, column=0, pady=10)
        Button(right_frame, text="Редактировать", command=self.controller.edit_transaction,)
               
bg="#f39c12", fg="white", width=15; grid(row=6, column=1, pady=10)
Button(right_frame, text="Удалить", command=self.controller.delete_transaction, 
               bg="#e74c3c", fg="white", width=15).grid(row=7, column=0, pady=5)
Button(right_frame, text="Очистить форму", command=self.clear_form, 
               bg="#95a5a6", fg="white", width=15).grid(row=7, column=1, pady=5)
Button(right_frame, text="Показать график расходов", command=self.controller.show_chart, 
               bg="#3498db", fg="white", width=30).grid(row=8, column=0, columnspan=2, pady=10)

def setup_bottom_panel(self):
        bottom_frame = Frame(self.root, bg="#ecf0f1")
        bottom_frame.pack(fill=X, pady=5)
        Button(bottom_frame, text="Экспорт в JSON", command=self.controller.export_data, 
               bg="#34495e", fg="white").pack(side=LEFT, padx=10)
        Button(bottom_frame, text="Импорт из JSON", command=self.controller.import_data, 
               bg="#34495e", fg="white").pack(side=LEFT, padx=10)
        Button(bottom_frame, text="О программе", command=self.show_about, 
               bg="#7f8c8d", fg="white").pack(side=RIGHT, padx=10)

def refresh_transactions_table(self, transactions):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in transactions:
            self.tree.insert("", END, values=(t["id"], t["date"], t["category"],
                                              t["amount"], t["type"], t["comment"]))

def update_balance_display(self, balance):
        self.balance_label.config(text=f"Баланс: {balance:.2f} руб.")

def update_categories(self, categories):
        self.category_combo['values'] = categories

def get_form_data(self):
        return {
            "date": self.date_entry.get(),
            "category": self.category_combo.get(),
            "amount": self.amount_entry.get(),
            "type": self.type_var.get(),
            "comment": self.comment_entry.get()
        }

def set_form_data(self, data):
        self.date_entry.delete(0, END)
        self.date_entry.insert(0, data["date"])
        self.category_combo.set(data["category"])
        self.amount_entry.delete(0, END)
        self.amount_entry.insert(0, data["amount"])
        self.type_var.set(data["type"])
        self.comment_entry.delete(0, END)
        self.comment_entry.insert(0, data["comment"])

def clear_form(self):
        import datetime
        self.date_entry.delete(0, END)
        self.date_entry.insert(0, datetime.date.today().isoformat())
        self.category_combo.set("")
        self.amount_entry.delete(0, END)
        self.type_var.set("Расход")
        self.comment_entry.delete(0, END)

def get_selected_transaction_id(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return int(item["values"][0])
        return None

def show_chart_window(self, expenses):
        if not expenses:
            messagebox.showinfo("Нет данных", "Нет расходов для отображения")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(expenses.values(), labels=expenses.keys(), autopct="%1.1f%%")
        ax.set_title("Структура расходов")

        top = Toplevel(self.root)
        top.title("График расходов")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

def show_error(self, message):
        messagebox.showerror("Ошибка", message)

def show_warning(self, message):
        messagebox.showwarning("Внимание", message)

def show_info(self, message):
        messagebox.showinfo("Информация", message)

def show_about(self):
        messagebox.showinfo("О программе", "Личный финансовый учёт\nВерсия 1.0\nMVC Architecture")

def setup_advanced_panel(self):
        """Создать панель расширенной статистики"""
        advanced_frame = LabelFrame(self.root, text="Расширенная статистика", 
                                    font=("Arial", 12), bg="#f0f0f0")
        advanced_frame.pack(fill=X, padx=10, pady=5)
        
        btn_frame = Frame(advanced_frame, bg="#f0f0f0")
        btn_frame.pack(pady=5)
        
        Button(btn_frame, text="📊 Месячная статистика", 
               command=self.controller.show_monthly_stats,
               bg="#9b59b6", fg="white", width=18).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="🔍 Поиск транзакций", 
               command=self.controller.show_search_dialog,
               bg="#e67e22", fg="white", width=18).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="🏆 Топ расходов", 
               command=self.controller.show_top_expenses,
               bg="#1abc9c", fg="white", width=18).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="📈 Категории (детально)", 
               command=self.controller.show_category_details,
               bg="#3498db", fg="white", width=18).pack(side=LEFT, padx=5)

def show_monthly_stats_dialog(self, stats):
        """Показать окно с месячной статистикой"""
        dialog = Toplevel(self.root)
        dialog.title(f"Статистика за {stats['month']}.{stats['year']}")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f0f0")
        
        info_frame = Frame(dialog, bg="#f0f0f0")
        info_frame.pack(pady=20)
        
        Label(info_frame, text=f"Месяц: {stats['month']}/{stats['year']}", 
              font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
        Label(info_frame, text=f"📈 Доходы: {stats['income']:.2f} руб.", 
              font=("Arial", 12), fg="green", bg="#f0f0f0").pack(pady=5)
        Label(info_frame, text=f"📉 Расходы: {stats['expense']:.2f} руб.", 
              font=("Arial", 12), fg="red", bg="#f0f0f0").pack(pady=5)
        Label(info_frame, text=f"💰 Баланс: {stats['balance']:.2f} руб.", 
              font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=5)
        Label(info_frame, text=f"📝 Транзакций: {stats['count']}", 
              font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        
        Button(dialog, text="Закрыть", command=dialog.destroy,
               bg="#95a5a6", fg="white").pack(pady=10)

def show_search_results(self, results):
        """Показать результаты поиска"""
        dialog = Toplevel(self.root)
        dialog.title("Результаты поиска")
        dialog.geometry("800x400")
        
        tree = ttk.Treeview(dialog, columns=("date", "category", "amount", "type", "comment"),
                           show="headings", height=15)
        tree.heading("date", text="Дата")
        tree.heading("category", text="Категория")
        tree.heading("amount", text="Сумма")
        tree.heading("type", text="Тип")
        tree.heading("comment", text="Комментарий")
        
        tree.column("date", width=100)
        tree.column("category", width=120)
        tree.column("amount", width=80)
        tree.column("type", width=60)
        tree.column("comment", width=200)
        
        scrollbar = Scrollbar(dialog, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        for t in results:
            tree.insert("", END, values=(t["date"], t["category"], 
                                        t["amount"], t["type"], t["comment"]))
        
        Label(dialog, text=f"Найдено: {len(results)} транзакций", 
              font=("Arial", 10)).pack(pady=5)
def show_top_expenses_dialog(self, expenses):
      
 """Показать топ расходов"""
dialog = Toplevel(self.root)
dialog.title("Топ расходов")
dialog.geometry("500x400")
        
text_area = Text(dialog, wrap=WORD, font=("Arial", 11))
text_area.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
text_area.insert(END, " САМЫЕ БОЛЬШИЕ РАСХОДЫ \n\n")
for i, exp in enumerate(expenses, 1):
            text_area.insert(END, f"{i}. {exp['category']}\n")
            text_area.insert(END, f"   Сумма: {exp['amount']:.2f} руб.\n")
            text_area.insert(END, f"   Дата: {exp['date']}\n")
            text_area.insert(END, f"   Комментарий: {exp['comment']}\n\n")
        
text_area.config(state=DISABLED)
        
Button(dialog, text="Закрыть", command=dialog.destroy,
               bg="#95a5a6", fg="white").pack(pady=5)

def show_category_details_dialog(self, stats):
        """Показать детальную статистику по категориям"""
        dialog = Toplevel(self.root)
        dialog.title("Детальная статистика по категориям")
        dialog.geometry("600x500")
        
        text_area = Text(dialog, wrap=WORD, font=("Arial", 10))
        text_area.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        text_area.insert(END, "📊 СТАТИСТИКА ПО КАТЕГОРИЯМ 📊\n")
        text_area.insert(END, "="*50 + "\n\n")
        
        for category, data in stats.items():
            if data["count"] > 0:
                text_area.insert(END, f"📁 {category}\n")
                text_area.insert(END, f"   Доходы: {data['income']:.2f} руб.\n")
                text_area.insert(END, f"   Расходы: {data['expense']:.2f} руб.\n")
                text_area.insert(END, f"   Транзакций: {data['count']}\n")
                if data["expense"] > 0:
                    text_area.insert(END, f"   Средний расход: {data['expense']/data['count']:.2f} руб.\n")
                text_area.insert(END, "\n")
        
        text_area.config(state=DISABLED)
        Button(dialog, text="Закрыть", command=dialog.destroy,
               bg="#95a5a6", fg="white").pack(pady=5)