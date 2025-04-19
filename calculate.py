import tkinter as tk
from tkinter import messagebox, filedialog
import random

# Алфавиты
RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789"
ENGLISH_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

def generate_balanced_binary_key(length):
    
    if length % 2 != 0:
        length += 1  # Делаем длину четной для баланса
    
    half = length // 2
    key = ['0'] * half + ['1'] * half
    random.shuffle(key)
    return ''.join(key)

# Функция для генерации и вставки ключа
def generate_random_key():
    try:
        text = text_entry.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для определения длины ключа!")
            return
        
        # Определяем длину ключа (равную длине двоичного представления текста)
        alphabet = RUSSIAN_ALPHABET if language_var.get() == "Русский" else ENGLISH_ALPHABET
        binary_text = text_to_binary(text, alphabet)
        key_length = len(binary_text)
        
        if not one_language(text, alphabet):
            messagebox.showerror("Ошибка", "Текст содержит символы из другого языка!")
            return
        
        # Генерируем сбалансированный двоичный ключ
        binary_key = generate_balanced_binary_key(key_length)
        
        # Вставляем ключ в поле ключа (как двоичный)
        key_entry.delete(0, tk.END)
        key_entry.insert(0, binary_key)
        
        # Обновляем двоичные представления
        update_binary_views()
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        
# Функция для преобразования текста в двоичный вид (по алфавиту) без пробелов
def text_to_binary(text, alphabet):
    binary_str = ""
    for char in text.lower():
        if char in alphabet:
            index = alphabet.find(char)
            binary_str += format(index, '06b')  # 6 бит на символв
    return binary_str

# Функция для выполнения XOR между двоичными строками
def xor_binary(bin_text, bin_key):
    result = ""
    key_len = len(bin_key)
    
    for i in range(len(bin_text)):
        # XOR между соответствующими битами
        result += str(int(bin_text[i]) ^ int(bin_key[i % key_len]))
    
    return result

# Функция для выполнения XOR между текстом и ключом
def xor_encrypt_decrypt(text, key, alphabet):
    # Получаем двоичные представления без пробелов
    bin_text = text_to_binary(text, alphabet)
    bin_key = key
    
    
    if not bin_text or not bin_key:
        return ""
    
    # Выполняем XOR между двоичными строками
    encrypted_bin = xor_binary(bin_text, bin_key)
    
    # Форматируем с пробелами для отображения (но храним без пробелов)
    return ''.join([encrypted_bin[i:i+6] for i in range(0, len(encrypted_bin), 6)])

# Функция для расшифровки XOR
def xor_decrypt(binary_text, key, alphabet):
    # Удаляем все пробелы из двоичной строки
    binary_str = binary_text.replace(" ", "")
    #bin_key = text_to_binary(key, alphabet)
    bin_key = key
                             
    if not binary_str or not bin_key:
        return ""
    
    # Выполняем XOR между двоичными строками
    decrypted_bin = xor_binary(binary_str, bin_key)
    
    # Преобразуем двоичную строку обратно в текст
    decrypted_text = ""
    for i in range(0, len(decrypted_bin), 6):
        binary = decrypted_bin[i:i+6]
        if len(binary) == 6:
            index = int(binary, 2)
            if 0 <= index < len(alphabet):
                decrypted_text += alphabet[index]
    
    return decrypted_text

# Обновление двоичных представлений (без пробелов)
def update_binary_views():
    try:
        text = text_entry.get("1.0", "end-1c")
        key_str = key_entry.get()
        
        alphabet = RUSSIAN_ALPHABET if language_var.get() == "Русский" else ENGLISH_ALPHABET
        
        # Обновляем двоичный вид текста (без пробелов)
        text_binary.delete("1.0", tk.END)
        if text:
            text_binary_str = text_to_binary(text, alphabet)
            # Форматируем с пробелами для отображения
            formatted = ''.join([text_binary_str[i:i+6] for i in range(0, len(text_binary_str), 6)])
            text_binary.insert("1.0", formatted)
        '''
        # Обновляем двоичный вид ключа (без пробелов)
        key_binary.delete("1.0", tk.END)
        if key_str:
            key_binary_str = text_to_binary(key_str, alphabet)
            # Форматируем с пробелами для отображения
            formatted = ''.join([key_binary_str[i:i+6] for i in range(0, len(key_binary_str), 6)])
            key_binary.insert("1.0", formatted)
        '''
    except Exception as e:
        print(f"Ошибка при обновлении двоичных представлений: {e}")

# Проверка языка текста
def one_language(text, alphabet):
    for char in text:
        if char.lower() not in alphabet:
            return False
    return True

# Проверка ключа
def is_valid_key(key_str, alphabet):
    if not key_str:
        return False
    return one_language(key_str, alphabet)

# Чтение из файла
def read_file():
    try:
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")))
            
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", content)
                update_binary_views()  # Обновляем двоичные представления
    except Exception as e:
        messagebox.showerror("ERROR", f"Не удалось прочитать файл: {str(e)}")
        # Очистка текста
def clean_text():
    try:
        text = text_entry.get("1.0", "end-1c")
        
        if not text:
            messagebox.showwarning("Предупреждение", "Поле ввода пустое!")
            return
            
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET
            
        cleaned_text = ''.join([c for c in text if c.lower() in alphabet])
        
        text_entry.delete("1.0", tk.END)
        text_entry.insert("1.0", cleaned_text)
        update_binary_views()  # Обновляем двоичные представления
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")


# Шифрование XOR
def encrypt_xor():
    try:
        key_str = key_entry.get()
        text = text_entry.get("1.0", "end-1c")
        
        if not text or not key_str:
            messagebox.showerror("Ошибка", "Текст и ключ не могут быть пустыми!")
            return
            
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET

        if not is_valid_key(key_str, alphabet):
            messagebox.showerror("Ошибка", "Ключ должен содержать только буквы выбранного алфавита!")
            return

        if not one_language(text, alphabet):
            messagebox.showerror("Ошибка", "Текст содержит символы из другого языка!")
            return
        # Получаем двоичный вид зашифрованного текста
        encrypted_binary = xor_encrypt_decrypt(text, key_str, alphabet)
        
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", encrypted_binary)
        result_text.config(state="disabled")
        
        update_binary_views()  # Обновляем двоичные представления
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Дешифрование XOR
def decrypt_xor():
    try:
        key_str = key_entry.get()
        binary_text = result_text.get("1.0", "end-1c").strip()
        
        if not binary_text or not key_str:
            messagebox.showerror("Ошибка", "Зашифрованный текст и ключ не могут быть пустыми!")
            return
            
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET

        if not is_valid_key(key_str, alphabet):
            messagebox.showerror("Ошибка", "Ключ должен содержать только буквы выбранного алфавита!")
            return

        # Расшифровываем двоичный текст
        decrypted_text = xor_decrypt(binary_text, key_str, alphabet)
        
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", decrypted_text)
        result_text.config(state="disabled")
        
        update_binary_views()  # Обновляем двоичные представления
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Обновление двоичных представлений
'''
def update_binary_views():
    try:
        text = text_entry.get("1.0", "end-1c")
        key_str = key_entry.get()
        
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET
        
        # Обновляем двоичный вид текста
        text_binary.delete("1.0", tk.END)
        if text:
            text_binary_str = text_to_binary(text, alphabet)
            text_binary.insert("1.0", text_binary_str)
        
        # Обновляем двоичный вид ключа
        key_binary.delete("1.0", tk.END)
        if key_str:
            key_binary_str = text_to_binary(key_str, alphabet)
            key_binary.insert("1.0", key_binary_str)
    except:
        pass
'''
# Вставка зашифрованного текста
def paste_encrypted_text():
    result_text.config(state="normal")
    encrypted_text = result_text.get("1.0", "end-1c")
    text_entry.delete("1.0", tk.END)
    text_entry.insert("1.0", encrypted_text)
    result_text.config(state="disabled")
    update_binary_views()
    
def decrypt_from_result():
    try:
        # Получаем зашифрованный текст из поля результата
        encrypted_text = result_text.get("1.0", "end-1c").strip()
        key_str = key_entry.get()
        
        if not encrypted_text or not key_str:
            messagebox.showerror("Ошибка", "Нет данных для расшифровки или ключ пустой!")
            return
            
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET

        if not is_valid_key(key_str, alphabet):
            messagebox.showerror("Ошибка", "Ключ должен содержать только буквы выбранного алфавита!")
            return

        # Проверяем, является ли текст двоичным (XOR зашифрованным)
        if all(c in '01 ' for c in encrypted_text):
            # Это двоичный текст - используем XOR дешифровку
            decrypted_text = xor_decrypt(encrypted_text, key_str, alphabet)
        else:
            # Это обычный текст - можно добавить другие методы дешифровки
            messagebox.showerror("Ошибка", "Поле результата не содержит двоичных данных для XOR расшифровки!")
            return
        
        # Создаем новое окно для вывода результата
        result_window = tk.Toplevel(root)
        result_window.title("Результат расшифровки")
        result_window.geometry("500x300")
        
        tk.Label(result_window, text="Расшифрованный текст:", font=('Arial', 12)).pack(pady=10)
        
        output_text = tk.Text(result_window, height=10, width=60)
        output_text.pack(padx=10, pady=5)
        output_text.insert("1.0", decrypted_text)
        
        # Кнопка для копирования результата
        copy_button = tk.Button(result_window, text="Копировать", 
                              command=lambda: root.clipboard_append(decrypted_text))
        copy_button.pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при расшифровке: {str(e)}")


# Создание графического интерфейса
root = tk.Tk()
root.title("Шифр XOR гаммирование")  
root.geometry("600x800")


# Выбор языка
language_var = tk.StringVar(value="Русский")
language_label = tk.Label(root, text="Выберите язык:")
language_label.pack()
language_menu = tk.OptionMenu(root, language_var, "Русский", "Английский")
language_menu.pack()

# Поле для ввода текста
text_label = tk.Label(root, text="Введите текст:")
text_label.pack()
text_entry = tk.Text(root, height=5, width=70)
text_entry.pack()
text_entry.bind("<KeyRelease>", lambda event: update_binary_views())

# Двоичный вид текста
text_binary_label = tk.Label(root, text="Двоичный вид текста:")
text_binary_label.pack()
text_binary = tk.Text(root, height=3, width=70, state="normal")
text_binary.pack()

# Поле для ввода ключа
key_label = tk.Label(root, text="Ключ:")
key_label.pack()
key_entry = tk.Entry(root, width=70)
key_entry.pack()
key_entry.bind("<KeyRelease>", lambda event: update_binary_views())

'''
# Двоичный вид ключа
key_binary_label = tk.Label(root, text="Двоичный вид ключа:")
key_binary_label.pack()

key_binary = tk.Text(root, height=3, width=70, state="normal")
key_binary.pack()
'''

# Фрейм для кнопок работы с текстом
text_buttons_frame = tk.Frame(root)
text_buttons_frame.pack()
load_button = tk.Button(text_buttons_frame, text="Загрузить из файла", command=read_file, bg="#9C27B0")
load_button.pack(side=tk.LEFT, padx=5)

clean_button = tk.Button(text_buttons_frame, text="Очистить текст", command=clean_text, bg="#607D8B")
clean_button.pack(side=tk.LEFT, padx=5)

# Фрейм для кнопок шифрования
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
'''
encrypt_button = tk.Button(button_frame, text="Зашифровать (Виженер)", command=encrypt_vigenere, bg="#4CAF50", width=20)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(button_frame, text="Расшифровать (Виженер)", command=decrypt_vigenere, bg="#FF5722", width=20)
decrypt_button.pack(side=tk.LEFT, padx=5)
'''
text_buttons_frame = tk.Frame(root)
text_buttons_frame.pack()



# Новая кнопка для генерации ключа
generate_key_button = tk.Button(text_buttons_frame, text="Сгенерировать ключ", command=generate_random_key, bg="#FFC107")
generate_key_button.pack(side=tk.LEFT, padx=5)

xor_encrypt_button = tk.Button(button_frame, text="XOR Зашифровать", command=encrypt_xor, bg="#2196F3", width=15)
xor_encrypt_button.pack(side=tk.LEFT, padx=5)
'''
xor_decrypt_button = tk.Button(button_frame, text="XOR Расшифровать", command=decrypt_xor, bg="#FF9800", width=15)
xor_decrypt_button.pack(side=tk.LEFT, padx=5)
'''
decrypt_result_button = tk.Button(button_frame, text="Расш. из результата", command=decrypt_from_result, bg="#4CAF50", width=15)
decrypt_result_button.pack(side=tk.LEFT, padx=5)
'''
paste_button = tk.Button(root, text="Вставить результат в поле ввода", command=paste_encrypted_text, bg="#9E9E9E")
paste_button.pack()
'''
# Поле результата
result_label = tk.Label(root, text="Результат:")
result_label.pack()
result_text = tk.Text(root, height=5, width=70, state="disabled")
result_text.pack()

root.mainloop()

