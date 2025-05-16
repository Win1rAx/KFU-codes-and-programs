
import tkinter as tk 
from tkinter import ttk, messagebox  



def check_for_spaces():
    """Проверяет поля ввода на наличие пробелов."""
    if ' ' in a_entry.get() or ' ' in n_entry.get() or ' ' in e_entry.get():
        messagebox.showerror("Ошибка", "Поля не должны содержать пробелов!")
        return True
    return False


def binary_expansion(e):
    """Функция для преобразования числа в двоичное представление"""
    # Преобразуем число в двоичную строку (начинается с '0b'), берем часть после '0b'
    # Каждый символ преобразуем в int, получаем список битов (старший бит первый)
    return [int(bit) for bit in bin(e)[2:]]

def fast_exponentiation(a, e, n):
    """Функция быстрого возведения в степень по модулю"""
    # Получаем двоичное представление степени
    binary_e = binary_expansion(e)
    # Инициализируем результат (a^0 = 1)
    result = 1
    # Список для хранения шагов вычисления
    steps = []
    
    # Проходим по каждому биту двоичного представления
    for bit in binary_e:
        # Добавляем текущий бит и результат в список шагов
        steps.append((bit, result))
        # Возводим в квадрат по модулю n (основная операция алгоритма)
        result = (result * result) % n
        # Если бит равен 1, умножаем на основание a по модулю n
        if bit == 1:
            result = (result * a) % n
    
    # Добавляем финальный результат в шаги (пустая строка вместо бита)
    steps.append(('', result))
    # Возвращаем результат и список шагов
    return result, steps

def calculate():
    """Функция, вызываемая при нажатии кнопки 'Вычислить'"""
    try:
        
        # Проверка на пробелы
        if check_for_spaces():
           return
        # Получаем значения из полей ввода
        a = int(a_entry.get())
        e = int(e_entry.get())
        n = int(n_entry.get())
        
        # Проверка корректности ввода
        if n <= 0:
            messagebox.showerror("Ошибка", "Модуль N должен быть положительным числом")
            return
        if e < 0:
            messagebox.showerror("Ошибка", "Степень e должна быть неотрицательной")
            return
        if a <= 0:
            messagebox.showerror("Ошибка", "Число a должна быть неотрицательной")
            return
            
        # Вычисляем результат и шаги
        result, steps = fast_exponentiation(a, e, n)
        # Обновляем метку с результатом
        result_label.config(text=f"Результат: {a}^{e} mod {n} = {result}")
        
        # Очищаем предыдущие результаты в таблице
        for row in result_tree.get_children():
            result_tree.delete(row)
        
        # Формируем двоичное представление для отображения
        binary_str = ''.join(str(bit) for bit, _ in steps[:-1])
        binary_label.config(text=f"Двоичное представление степени: {binary_str}")
        
        # Заполняем таблицу шагов вычисления
        for i, (bit, value) in enumerate(steps[:-1]):
            # Формируем описание операции
            operation = "Квадрат" if i == 0 else f"Квадрат {'и умножение' if bit == 1 else ''}"
            operation = operation.strip()
            # Добавляем строку в таблицу
            result_tree.insert("", "end", values=(i+1, bit, operation, value))
        
        # Добавляем финальный результат в таблицу
        result_tree.insert("", "end", values=("Результат", "", "", steps[-1][1]))
            
    except ValueError:
        # Обработка ошибки нечислового ввода
        messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа")

# Создаем главное окно приложения
root = tk.Tk()
# Устанавливаем заголовок окна
root.title("Быстрое возведение в степень по модулю (RSA)")
# Устанавливаем начальный размер окна
root.geometry("700x500")

# Создаем фрейм для ввода данных
input_frame = ttk.LabelFrame(root, text="Входные параметры")
input_frame.pack(padx=10, pady=10, fill="x")

# Создаем и размещаем элементы интерфейса:

# Поле для ввода основания (a)
ttk.Label(input_frame, text="Основание (a):").grid(row=0, column=0, padx=5, pady=5)
a_entry = ttk.Entry(input_frame)
a_entry.grid(row=0, column=1, padx=5, pady=5)
# Устанавливаем значение по умолчанию
a_entry.insert(0, "5")

# Поле для ввода степени (e)
ttk.Label(input_frame, text="Степень (e):").grid(row=1, column=0, padx=5, pady=5)
e_entry = ttk.Entry(input_frame)
e_entry.grid(row=1, column=1, padx=5, pady=5)
# Устанавливаем значение по умолчанию
e_entry.insert(0, "13")

# Поле для ввода модуля (N)
ttk.Label(input_frame, text="Модуль (N):").grid(row=2, column=0, padx=5, pady=5)
n_entry = ttk.Entry(input_frame)
n_entry.grid(row=2, column=1, padx=5, pady=5)
# Устанавливаем значение по умолчанию
n_entry.insert(0, "19")

# Кнопка для выполнения вычислений
calculate_button = ttk.Button(input_frame, text="Вычислить", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Метка для отображения результата
result_label = ttk.Label(root, text="Результат: ")
result_label.pack(pady=5)

# Метка для отображения двоичного представления степени
binary_label = ttk.Label(root, text="Двоичное представление степени: ")
binary_label.pack(pady=5)

# Фрейм для отображения шагов вычисления
result_frame = ttk.LabelFrame(root, text="Шаги вычисления")
result_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Создаем таблицу (Treeview) для отображения шагов
result_tree = ttk.Treeview(result_frame, 
                         columns=("step", "bit", "operation", "value"), 
                         show="headings")
# Настраиваем заголовки столбцов
result_tree.heading("step", text="Шаг")
result_tree.heading("bit", text="Бит")
result_tree.heading("operation", text="Операция")
result_tree.heading("value", text="Текущий результат")
# Настраиваем ширину столбцов
result_tree.column("step", width=50, anchor="center")
result_tree.column("bit", width=50, anchor="center")
result_tree.column("operation", width=150, anchor="center")
result_tree.column("value", width=150, anchor="center")

result_tree.pack(fill="both", expand=True)

# Добавляем вертикальную полосу прокрутки
scrollbar = ttk.Scrollbar(result_tree, orient="vertical", command=result_tree.yview)
scrollbar.pack(side="right", fill="y")
result_tree.configure(yscrollcommand=scrollbar.set)

# Запускаем главный цикл обработки событий
root.mainloop()