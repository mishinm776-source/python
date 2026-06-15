from models import FinanceModel
import datetime

class FinanceController:
    def __init__(self, view):
        self.model = FinanceModel()
        self.view = view
        self.view.update_categories(self.model.get_categories())
        self.current_edit_id = None
        self.refresh_all()

    def refresh_all(self):
        self.view.refresh_transactions_table(self.model.get_transactions())
        self.view.update_balance_display(self.model.calculate_balance())

    def add_transaction(self):
        try:
            form_data = self.view.get_form_data()
            
            if not form_data["category"] or form_data["category"] not in self.model.get_categories():
                self.view.show_error("Выберите категорию из списка")
                return
                
            amount = float(form_data["amount"])
            
            transaction = {
                "date": form_data["date"],
                "category": form_data["category"],
                "amount": amount,
                "type": form_data["type"],
                "comment": form_data["comment"]
            }
            
            self.model.add_transaction(transaction)
            self.refresh_all()
            self.view.clear_form()
            
        except ValueError:
            self.view.show_error("Сумма должна быть числом")

    def edit_transaction(self):
        if self.current_edit_id is None:
            self.view.show_warning("Сначала выберите транзакцию в таблице")
            return
            
        try:
            form_data = self.view.get_form_data()
            amount = float(form_data["amount"])
            
            updated_data = {
                "date": form_data["date"],
                "category": form_data["category"],
                "amount": amount,
                "type": form_data["type"],
                "comment": form_data["comment"]
            }
            
            self.model.update_transaction(self.current_edit_id, updated_data)
            self.refresh_all()
            self.view.clear_form()
            self.current_edit_id = None
            
        except ValueError:
            self.view.show_error("Сумма должна быть числом")

    def delete_transaction(self):
        trans_id = self.view.get_selected_transaction_id()
        if trans_id is None:
            self.view.show_warning("Выберите транзакцию для удаления")
            return
            
        if self.view.show_about and False:  # Встроенного confirm нет, добавим
            pass
            
        from tkinter import messagebox
        if messagebox.askyesno("Удаление", "Удалить транзакцию?"):
            self.model.delete_transaction(trans_id)
            self.refresh_all()
            self.view.clear_form()
            self.current_edit_id = None

    def on_transaction_select(self, event):
        trans_id = self.view.get_selected_transaction_id()
        if trans_id:
            self.current_edit_id = trans_id
            # Найти транзакцию по ID
            for transaction in self.model.get_transactions():
                if transaction["id"] == trans_id:
                    self.view.set_form_data({
                        "date": transaction["date"],
                        "category": transaction["category"],
                        "amount": transaction["amount"],
                        "type": transaction["type"],
                        "comment": transaction["comment"]
                    })
                    break

    def show_chart(self):
        expenses = self.model.get_expenses_by_category()
        self.view.show_chart_window(expenses)

    def export_data(self):
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filepath:
            self.model.export_data(filepath)
            self.view.show_info("Данные экспортированы")
    def import_data(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            if self.model.import_data(filepath):
                self.refresh_all()
                self.view.show_info("Данные импортированы")
            else:
                self.view.show_error("Неверный формат файла")