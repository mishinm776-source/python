from tkinter import Tk
from views import FinanceView
from controller import FinanceController

def main():
    root = Tk()
    view = FinanceView(root, None)  # Временно без контроллера
    controller = FinanceController(view)
    view.controller = controller  # Связываем обратно
    root.mainloop()

if __name__ == "__main__":
    main()