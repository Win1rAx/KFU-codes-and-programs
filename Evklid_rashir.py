import tkinter as tk
from tkinter import ttk, messagebox


def check_for_spaces():
    """Проверяет поля ввода на наличие пробелов."""
    if ' ' in entry_a.get() or ' ' in entry_b.get():
        messagebox.showerror("Ошибка", "Поля не должны содержать пробелов!")
        return True
    return False



def extended_gcd(a, b):
    """Реализация расширенного алгоритма Евклида."""
    steps = []
    # Прямой ход алгоритма (вычисление остатков)
    while b != 0:
        quotient = a // b  # Целая часть от деления
        remainder = a % b  # Остаток от деления
        # Сохраняем шаг вычисления (a, b, частное, остаток)
        steps.append((a, b, quotient, remainder))
        a, b = b, remainder  # Обновляем значения для следующей итерации
    
    gcd = a  # НОД - последний ненулевой остаток
    
    # Обратный ход для нахождения коэффициентов x и y
    x, y = 0, 1  # Базовые значения для последнего шага
    coefficients = [(x, y)]  # Список для хранения коэффициентов
    
    # Идем по шагам в обратном порядке (кроме последнего)
    for step in reversed(steps[:-1]):
        a, b, quotient, remainder = step
        # Вычисляем новые коэффициенты по формулам:
        # x_new = y_prev
        # y_new = x_prev - quotient * y_prev
        x, y = y, x - quotient * y
        coefficients.append((x, y))
    
    # Разворачиваем коэффициенты в правильном порядке
    coefficients.reverse()
    
    # Объединяем шаги с коэффициентами для отображения
    full_steps = []
    for i in range(len(steps)):
        full_steps.append((*steps[i], *coefficients[i]))
    
    return gcd, coefficients[0][0], coefficients[0][1], full_steps

def calculate_gcd():
    """Обработчик нажатия кнопки для вычисления НОД."""
    try:
        
        # Проверка на пробелы
        if check_for_spaces():
           return
        # Получаем значения из полей ввода
        a = int(entry_a.get())
        b = int(entry_b.get())
        
        # Проверка на положительные числа
        if a <= 0 or b <= 0:
            messagebox.showerror("Ошибка", "Числа должны быть положительными!")
            return
        
        # Вызываем алгоритм
        gcd, x, y, steps = extended_gcd(a, b)
        
        # Очищаем предыдущие результаты в таблице
        for row in result_tree.get_children():
            result_tree.delete(row)
        
        # Заполняем таблицу новыми данными
        for step in steps:
            result_tree.insert("", "end", values=step)
        
        # Отображаем результат
        result_label.config(text=f"НОД({a}, {b}) = {gcd} = {a}*{x} + {b}*{y}")
        
    except ValueError:
        # Обработка ошибки, если введены не числа
        messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа!")

## Создание графического интерфейса ##

# Главное окно
root = tk.Tk()
root.title("Расширенный алгоритм Евклида")
root.geometry("800x600")  # Размер окна

# Фрейм для ввода данных
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.X)  # Растягиваем по ширине

# Элементы ввода:
# Метка и поле для числа A
ttk.Label(input_frame, text="Число A:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
entry_a = ttk.Entry(input_frame)
entry_a.grid(row=0, column=1, padx=5, pady=5)

# Метка и поле для числа B
ttk.Label(input_frame, text="Число B:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
entry_b = ttk.Entry(input_frame)
entry_b.grid(row=1, column=1, padx=5, pady=5)

# Кнопка для вычислений
calculate_btn = ttk.Button(input_frame, text="Вычислить НОД", command=calculate_gcd)
calculate_btn.grid(row=2, column=0, columnspan=2, pady=10)

# Фрейм для результатов
result_frame = ttk.Frame(root, padding="10")
result_frame.pack(fill=tk.BOTH, expand=True)  # Растягиваем на все доступное пространство

# Метка для отображения результата
result_label = ttk.Label(result_frame, text="", font=('Arial', 12))
result_label.pack(pady=10)

# Таблица для отображения шагов алгоритма
columns = ("A", "B", "A div B", "A mod B", "x", "y")
result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)

# Настройка столбцов таблицы
for col in columns:
    result_tree.heading(col, text=col)  # Заголовки
    result_tree.column(col, width=100, anchor=tk.CENTER)  # Ширина и выравнивание

# Добавление вертикальной прокрутки
scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_tree.yview)
result_tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_tree.pack(fill=tk.BOTH, expand=True)

# Пояснение работы алгоритма
explanation = """
Расширенный алгоритм Евклида находит:
1. Наибольший общий делитель (НОД) чисел A и B
2. Коэффициенты x и y, такие что: A*x + B*y = НОД(A, B)

Алгоритм работает в два этапа:
1. Прямой ход: последовательное вычисление остатков (как в обычном алгоритме Евклида)
2. Обратный ход: вычисление коэффициентов x и y
"""
explanation_label = ttk.Label(root, text=explanation, padding=10, wraplength=700)
explanation_label.pack(fill=tk.X)

# Запуск главного цикла обработки событий
root.mainloop()