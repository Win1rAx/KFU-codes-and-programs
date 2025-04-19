# Импорт необходимых библиотек
import tkinter as tk  # Основная библиотека для GUI
from tkinter import ttk, messagebox, scrolledtext  # Виджеты и диалоговые окна
import math  # Математические функции (для sqrt)
import time  # Для замера времени выполнения

# =============================================
# ФУНКЦИИ ДЛЯ ВЫЧИСЛЕНИЙ
# =============================================

def sieve_of_eratosthenes(n):
    """Оптимизированная реализация решета Эратосфена"""
    if n < 2:  # Простые числа начинаются с 2
        return []  # Пустой список, если n < 2
    
    # Создаем решето только для нечетных чисел (экономия памяти)
    # bytearray вместо list для экономии памяти
    sieve = bytearray([1]) * ((n + 1) // 2)
    sieve[0] = 0  # Число 1 - не простое (индекс 0 соответствует числу 1)
    
    # Основной алгоритм решета:
    for i in range(1, int(math.sqrt(n)) // 2 + 1):
        if sieve[i]:  # Если число не вычеркнуто
            current = 2 * i + 1  # Получаем нечетное число (3, 5, 7...)
            start = current * current  # Начинаем с квадрата числа
            # Вычеркиваем кратные числа с шагом current*2 (оптимизация)
            sieve[start // 2::current] = b'\x00' * len(sieve[start // 2::current])
            '''
            index = start // 2
            step = current
            while index < len(sieve):
                sieve[index] = 0
                index += step
            '''
    
    # Формируем результат:
    primes = [2] if n >= 2 else []  # 2 - единственное четное простое
    # Добавляем нечетные простые числа
    primes.extend(2 * i + 1 for i in range(1, len(sieve)) if sieve[i])
    
    '''
    for i in range(1, len(sieve)):
        if sieve[i]:  # Если число не вычеркнуто (простое)
            primes.append(2 * i + 1)  # Добавляем соответствующее нечётное число
    '''
    
    
    return primes

def format_results(primes, limit, elapsed_time):
    """Форматирование результатов для вывода"""
    result = []  # Список для строк результата
    
    # Добавляем заголовок и статистику
    result.append(f"Простые числа до {limit:,}:")
    result.append(f"Всего найдено: {len(primes):,}")
    result.append(f"Время вычисления: {elapsed_time:.2f} сек\n")
    
    # Форматируем вывод по 10 чисел в строке
    numbers_per_line = 10
    for i in range(0, len(primes), numbers_per_line):
        # Форматируем строку с выравниванием чисел (по 8 символов на число)
        line = ", ".join(f"{p:>8}" for p in primes[i:i+numbers_per_line])
        '''
        primes[i:i+numbers_per_line] - берёт срез из 10 чисел
        f"{p:>8}" - форматирует каждое число в 8 символов с выравниванием вправо
        ", ".join() - объединяет через запятую и пробел
        
        '''
        result.append(line)
    
    # Объединяем все строки через перенос
    return "\n".join(result)

# =============================================
# ОБРАБОТЧИКИ СОБЫТИЙ
# =============================================

def calculate_primes(entry_widget, output_widget, status_var):
    """Обработка нажатия кнопки 'Вычислить'"""
    try:
        '''
        # Получаем ввод пользователя
        user_input = entry_widget.get()
        
        # Проверка на пробелы
        if ' ' in user_input:
            messagebox.showerror("Ошибка", "Поле ввода не должно содержать пробелов")
            return
        '''
        # Получаем и очищаем ввод пользователя (удаляем пробелы)
        user_input = entry_widget.get().replace(' ', '')
        if not user_input:
           messagebox.showerror("Ошибка", "Поле ввода не может быть пустым")
           return
        # Получаем и проверяем ввод пользователя
        n = int(user_input)
        if n < 2:
            messagebox.showerror("Ошибка", "Число должно быть ≥ 2")
            return
        '''if n > 10**9:
            messagebox.showerror("Ошибка", "Число слишком большое")
            return
        '''
    except ValueError:
        messagebox.showerror("Ошибка", "Введите целое число")
        return
    
    # Обновляем статус
    status_var.set("Вычисление...")
    entry_widget.winfo_toplevel().update()  # Принудительное обновление GUI
    
    start_time = time.time()  # Засекаем время
    
    try:
        # Основные вычисления
        primes = sieve_of_eratosthenes(n)
        elapsed_time = time.time() - start_time
        
        # Вывод результатов
        result = format_results(primes, n, elapsed_time)
        
        # Обновляем текстовое поле
        output_widget.config(state='normal')
        output_widget.delete(1.0, tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state='disabled')
        
        # Обновляем статус
        status_var.set(f"Готово. Найдено {len(primes)} чисел")
    except MemoryError:
        status_var.set("Ошибка: не хватает памяти")
        messagebox.showerror("Ошибка", "Недостаточно памяти")
    except Exception as e:
        status_var.set(f"Ошибка: {str(e)}")
        messagebox.showerror("Ошибка", str(e))

def clear_output(output_widget, status_var):
    """Очистка текстового поля"""
    output_widget.config(state='normal')
    output_widget.delete(1.0, tk.END)
    output_widget.config(state='disabled')
    status_var.set("Готово")

# =============================================
# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
# =============================================

def create_main_window():
    """Создание и настройка главного окна"""
    root = tk.Tk()  # Создаем корневое окно
    root.title("Решето Эратосфена")  # Заголовок окна
    root.geometry("700x600")  # Размер окна
    
    # Основной контейнер (для отступов)
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Фрейм для элементов ввода
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X)  # Растягиваем по ширине
    
    # Метка для поля ввода
    ttk.Label(input_frame, text="Верхняя граница (2 - 1 000 000 000):").pack(anchor=tk.W)
    
    # Поле ввода числа
    entry = ttk.Entry(input_frame)
    entry.pack(fill=tk.X, pady=5)  # Растягиваем по ширине + отступ
    entry.insert(0, "")  # Значение по умолчанию
    
    # Фрейм для кнопок
    btn_frame = ttk.Frame(input_frame)
    btn_frame.pack(fill=tk.X, pady=5)
    
    # Текстовая область с прокруткой
    output_text = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,  # Перенос по словам
        width=80,      # Ширина в символах
        height=25,     # Высота в строках
        state='disabled',  # Только для чтения
        font=('Courier New', 10)  # Моноширинный шрифт
    )
    output_text.pack(fill=tk.BOTH, expand=True)  # Растягиваем на все пространство
    
    # Переменная для строки состояния
    status_var = tk.StringVar()
    status_var.set("Готово")  # Начальное значение
    
    # Кнопка "Вычислить" с привязкой обработчика
    ttk.Button(
        btn_frame,
        text="Вычислить",
        command=lambda: calculate_primes(entry, output_text, status_var)
    ).pack(side=tk.LEFT, padx=2)
    
    # Кнопка "Очистить" с привязкой обработчика
    ttk.Button(
        btn_frame,
        text="Очистить",
        command=lambda: clear_output(output_text, status_var)
    ).pack(side=tk.LEFT)
    
    # Строка состояния внизу окна
    ttk.Label(
        root,
        textvariable=status_var,  # Привязываем переменную
        relief=tk.SUNKEN,        # Стиль "утопленной" панели
        anchor=tk.W               # Выравнивание текста по левому краю
    ).pack(fill=tk.X, side=tk.BOTTOM)
    
    return root


if __name__ == "__main__":
    window = create_main_window()  # Создаем окно
    window.mainloop()  # Запускаем главный цикл обработки событий