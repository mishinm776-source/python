import json
import os
import datetime

DATA_FILE = "finance_data.json"

class FinanceModel:
    def __init__(self):
        self.data = {
            "transactions": [],
            "categories": ["Еда", "Транспорт", "ЖКХ", "Зарплата", "Развлечения", "Здоровье"]
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                return False
        return True

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_transactions(self):
        return self.data["transactions"]

    def get_categories(self):
        return self.data["categories"]

    def add_transaction(self, transaction):
        new_id = max([t["id"] for t in self.data["transactions"]], default=0) + 1
        transaction["id"] = new_id
        self.data["transactions"].append(transaction)
        self.save_data()
        return new_id

    def update_transaction(self, trans_id, updated_data):
        for i, t in enumerate(self.data["transactions"]):
            if t["id"] == trans_id:
                self.data["transactions"][i].update(updated_data)
                self.save_data()
                return True
        return False

    def delete_transaction(self, trans_id):
        self.data["transactions"] = [t for t in self.data["transactions"] if t["id"] != trans_id]
        self.save_data()

    def calculate_balance(self):
        total = 0
        for t in self.data["transactions"]:
            if t["type"] == "Доход":
                total += t["amount"]
            else:
                total -= t["amount"]
        return total

    def get_expenses_by_category(self):
        expenses = {}
        for t in self.data["transactions"]:
            if t["type"] == "Расход":
                expenses[t["category"]] = expenses.get(t["category"], 0) + t["amount"]
        return expenses

    def import_data(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if "transactions" in imported and "categories" in imported:
                self.data = imported
                self.save_data()
                return True
        except:
            return False
        return False

    def export_data(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_monthly_stats(self, year=None, month=None):
        """Получить статистику за конкретный месяц"""
        if year is None:
            year = datetime.datetime.now().year
        if month is None:
            month = datetime.datetime.now().month
            
        monthly_transactions = []
        for t in self.data["transactions"]:
            try:
                trans_date = datetime.datetime.strptime(t["date"], "%Y-%m-%d")
                if trans_date.year == year and trans_date.month == month:
                    monthly_transactions.append(t)
            except:
                continue
                
        income = sum(t["amount"] for t in monthly_transactions if t["type"] == "Доход")
        expense = sum(t["amount"] for t in monthly_transactions if t["type"] == "Расход")
        
        return {
            "year": year,
            "month": month,
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "count": len(monthly_transactions)
        }
    
    def get_category_stats(self):
        """Детальная статистика по категориям"""
        stats = {}
        for category in self.data["categories"]:
            stats[category] = {
                "income": 0,
                "expense": 0,
                "count": 0
            }
        
        for t in self.data["transactions"]:
            if t["category"] in stats:
                stats[t["category"]][t["type"].lower()] += t["amount"]
                stats[t["category"]]["count"] += 1
                
        return stats
    
    def search_transactions(self, keyword):
        """Поиск транзакций по ключевому слову"""
        keyword = keyword.lower()
        results = []
        for t in self.data["transactions"]:
            if (keyword in t["category"].lower() or 
                keyword in t["comment"].lower() or
                keyword in str(t["amount"])):
                results.append(t)
        return results
    
    def get_top_expenses(self, limit=5):
        """Получить топ N самых больших расходов"""
        expenses = [t for t in self.data["transactions"] if t["type"] == "Расход"]
        expenses.sort(key=lambda x: x["amount"], reverse=True)
        return expenses[:limit]