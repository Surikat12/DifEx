from tkinter import *
from tkinter import messagebox
from math_parser import ParsingError
from derivative_parser import DerivativeConvertingError
from diff_tree import DiffTree


class Menu:

    def __init__(self):

        # Дерево для дифференцирования
        self.__tree = None

        # Основное окно приложения
        self.__window = Tk()
        self.__window.geometry("640x240")
        self.__window.title("DifEx")
        self.__window.resizable(width=False, height=False)

        # Надпись-пояснение для ввода выражения
        self.__input_label = Label(self.__window, text="Выражение для дифференцирования")

        # Текстовое поле для ввода выражения
        self.__input_box = Entry(self.__window)

        # Надпись-пояснение для ввода переменной
        self.__var_label = Label(self.__window, text="Переменная:")

        # Текстовое поле для ввода переменной
        self.__var_box = Entry(self.__window)

        # Кнопка для взятия производной
        self.__diff_button = Button(self.__window, text="Взять производную", command=lambda: self.__diff())

        # Надпись-пояснение для результата
        self.__output_label = Label(self.__window, text="Производная")

        # Текстовое поле с результатом
        self.__output_box = Entry(self.__window)

    def __get_var(self):
        var = self.__var_box.get()

        if len(var) != 1:
            messagebox.showerror("Некорректная переменная", "Название переменой должно состоять из одной буквы")
            return None

        elif var == "e":
            messagebox.showerror("Некорректная переменная", "e - это константа (число Эйлера)")
            return None

        elif not var.isalpha():
            messagebox.showerror("Некорректная переменная", "Переменная должна быть буквой")
            return None

        else:
            return var

    def __diff(self):
        expression = self.__input_box.get()
        var = self.__get_var()
        if var is None:
            return
        else:
            try:
                self.__tree.from_str(expression)
                self.__output_box.delete(0, END)
                self.__output_box.insert(0, str(self.__tree.diff(var)))
            except ParsingError as e:
                messagebox.showerror("Некорректное выражение", e)
            except BaseException as e:
                messagebox.showerror("Ошибка", e)

    def show(self):
        try:
            self.__tree = DiffTree("operations.txt")
        except IOError as e:
            messagebox.showerror("Ошибка при чтении файла с определением операций", e)
            self.__window.destroy()
            return
        except DerivativeConvertingError as e:
            messagebox.showerror("Ошибка в файле с определением операций", e)
            self.__window.destroy()
            return

        for i in range(5):
            self.__window.grid_rowconfigure(i, minsize=30)
        for i in range(3):
            self.__window.grid_columnconfigure(i, weight=1, minsize=200)

        self.__input_label.grid(column=0, row=0, columnspan=3)
        self.__input_box.grid(column=0, row=1, columnspan=3, padx=30, sticky=W+E)
        self.__var_label.grid(column=0, row=2, pady=30, sticky=E)
        self.__var_box.grid(column=1, row=2, pady=30, sticky=W)
        self.__diff_button.grid(column=2, row=2, padx=30, pady=30, sticky=E)
        self.__output_label.grid(column=0, row=3, columnspan=3)
        self.__output_box.grid(column=0, row=4, columnspan=3, padx=30, sticky=W+E)

        self.__window.mainloop()
