import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from collections import Counter

# Алфавиты (оставил без изменений)
RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789"
ENGLISH_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

# Изменил функцию шифрования/дешифрования для Виженера
def vigenere_cipher(text, key, alphabet, mode='encrypt'):
    result = ""
    m = len(alphabet)
    key_len = len(key)
    
    for i, char in enumerate(text): # i текущий индекс имвола в алфавите
        if char.lower() in alphabet:
            # Получаем сдвиг из ключа
            key_char = key[i % key_len] # символ ключа который используется для текущего символа
            key_shift = alphabet.find(key_char.lower()) # значение сдвига
            
            index = alphabet.find(char.lower()) # позиция текущего символа в алф
            #Если зашифровка то + если нет то -
            if mode == 'encrypt':
                new_index = (index + key_shift) % m
            else:
                new_index = (index - key_shift) % m
            #сохранение регистра    
            if char.isupper():
                result += alphabet[new_index].upper()
            else:
                result += alphabet[new_index]
        else:
            result += char
    return result

#Функция для проверки языка текста без изменений
def one_language(text, alphabet):
    for char in text:
        if char.lower() not in alphabet:
            return False
    return True

# Модифицировал проверку ключа
def is_valid_key(key_str, alphabet):
    # Проверяем, что ключ не пустой и состоит только из букв алфавита
    if not key_str:
        return False
    return one_language(key_str, alphabet)
'''
# Переработал функцию автоподбора (убрал, так как для Виженера это сложнее)
def auto_decr():
    try: 
        text = text_entry.get("1.0", "end-1c")
        
        if not text:
            messagebox.showerror("Ошибка", "Поле ввода текста пустое!")
            return
            
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
            common_char = 'о'
        else:
            alphabet = ENGLISH_ALPHABET
            common_char = 'e'
            
        # Проверка, что текст написан на одном языке
        if not one_language(text, alphabet):
            messagebox.showerror("Ошибка", "Текст содержит символы из другого языка!")
            return
            
        filtered_text = [c.lower() for c in text if c.lower() in alphabet]
        if not filtered_text:
            messagebox.showerror("Ошибка", "Нет символов из выбранного алфавита!")
            return
            
        most_common = Counter(filtered_text).most_common(1)[0][0]
        key = (alphabet.find(most_common) - alphabet.find(common_char)) % len(alphabet)
        
        # Показываем информацию о найденном ключе
        messagebox.showinfo("Автоподбор ключа", 
                          f"Найден ключ: {key}\n"
                          f"Самый частый символ: '{most_common}'\n"
                          f"Ожидаемый символ: '{common_char}'")
        
        # Устанавливаем найденный ключ в поле ввода
        key_entry.delete(0, tk.END)
        key_entry.insert(0, str(key))
        
        # Дешифруем текст и выводим в основном окне
        decrypted_text = caesar_cipher(text, -key, alphabet)
        result_text1.config(state="normal")
        result_text1.delete("1.0", tk.END)
        result_text1.insert("1.0", decrypted_text)
        result_text1.config(state="disabled")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
'''        
# Функция для чтения из файла
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
    except Exception as e:
        messagebox.showerror("ERROR", f"Не удалось прочитать файл: {str(e)}")

# Функция для очистки текста от лишних символов
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
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Переработал Обработчик для шифрования
def encrypt():
    try:
        key_str = key_entry.get()
        text = text_entry.get("1.0", "end-1c")
        # Проверка на пустую строку
        if not text:
            messagebox.showerror("Ошибка", "Поле ввода текста пустое!")
            return
        #Алфавит
        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET

        # Добавил проверку ключа на соответствие алфавиту
        if not is_valid_key(key_str, alphabet):
            messagebox.showerror("Ошибка", "Ключ должен содержать только буквы выбранного алфавита!")
            return
        # Проверка, что текст написан на одном языке
        if not one_language(text, alphabet):
            messagebox.showerror("Ошибка", "Текст содержит символы из другого языка!")
            return
        # Сама шифровка
        encrypted_text = vigenere_cipher(text, key_str, alphabet, 'encrypt')
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", encrypted_text)
        result_text.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Переработал функцию дешифрования
def decrypt():
    try:
        key_str = key_entry.get()
        text = text_entry.get("1.0", "end-1c")
        
        if not text:
            messagebox.showerror("Ошибка", "Поле ввода текста пустое!")
            return

        if language_var.get() == "Русский":
            alphabet = RUSSIAN_ALPHABET
        else:
            alphabet = ENGLISH_ALPHABET

        # Добавил проверку ключа на соответствие алфавиту
        if not is_valid_key(key_str, alphabet):
            messagebox.showerror("Ошибка", "Ключ должен содержать только символы выбранного алфавита!")
            return

        if not one_language(text, alphabet):
            messagebox.showerror("Ошибка", "Текст содержит символы из другого языка!")
            return

        decrypted_text = vigenere_cipher(text, key_str, alphabet, 'decrypt')
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", decrypted_text)
        result_text.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

#обработччик для замены текста 
def paste_encrypted_text():
    result_text.config(state="normal")
    encrypted_text = result_text.get("1.0", "end-1c")
    text_entry.delete("1.0", tk.END)
    text_entry.insert("1.0", encrypted_text)
    result_text.config(state="disabled")


#########################################################################################################



# Создание графического интерфейса
root = tk.Tk()
root.title("Шифр Виженера")  
root.geometry("450x500")

# Выбор языка
language_var = tk.StringVar(value="Русский")
language_label = tk.Label(root, text="Выберите язык:")
language_label.pack()
language_menu = tk.OptionMenu(root, language_var, "Русский", "Английский")
language_menu.pack()

# Поле для ввода текста
text_label = tk.Label(root, text="Введите текст:")
text_label.pack()
text_entry = tk.Text(root, height=5, width=40)
text_entry.pack()

# Фрейм для кнопок работы с текстом
text_buttons_frame = tk.Frame(root)
text_buttons_frame.pack()

load_button = tk.Button(text_buttons_frame, text="Загрузить из файла", command=read_file, bg="#9C27B0")
load_button.pack(side=tk.LEFT, padx=5)

clean_button = tk.Button(text_buttons_frame, text="Очистить текст", command=clean_text, bg="#607D8B")
clean_button.pack(side=tk.LEFT, padx=5)

# Поле для ввода ключа
key_label = tk.Label(root, text="Введите ключ:")
key_label.pack()
key_entry = tk.Entry(root)
key_entry.pack()

# Фрейм для кнопок шифрования
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Зашифровать", command=encrypt, bg="#4CAF50", width=12)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(button_frame, text="Расшифровать", command=decrypt, bg="#FF5722", width=12)
decrypt_button.pack(side=tk.LEFT, padx=5)
'''
# Упростил кнопку взлома, так как автоподбор для Виженера сложен
auto_decrypt_button = tk.Button(button_frame, text="Инфо", command=auto_decr, bg="#FFC107", width=12)
auto_decrypt_button.pack(side=tk.LEFT, padx=5)
'''
paste_button = tk.Button(root, text="⇅", command=paste_encrypted_text, bg="#2196F3")
paste_button.pack()

result_label = tk.Label(root, text="Результат:")
result_label.pack()
result_text = tk.Text(root, height=5, width=40, state="disabled")
result_text.pack()
'''
result_label1 = tk.Label(root, text="Результат:")
result_label1.pack()
result_text1 = tk.Text(root, height=5, width=40, state="disabled")
result_text1.pack()
'''
# Убрал второе поле результата, так как оно не нужно
root.mainloop()





