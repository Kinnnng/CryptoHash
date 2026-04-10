import tkinter as tk
from tkinter import ttk
import hashlib
import random
from tkinter import filedialog

def xor_encrypt(text, key):
    """
    Шифрует текст с помощью XOR с ключом.
    text - строка для шифрования
    key - строка-ключ
    возвращает зашифрованную строку в HEX формате (чтобы было читаемо)
    """
    result = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        # Берем символ ключа по кругу
        key_char = key[i % key_length]
        # XOR двух символов (преобразуем в числа, XOR, обратно в символ)
        encrypted_char = chr(ord(char) ^ ord(key_char))
        result.append(encrypted_char)
    
    # Преобразуем в HEX для читаемого отображения
    return ''.join(result).encode().hex()


def xor_decrypt(hex_text, key):
    encrypted_bytes = bytes.fromhex(hex_text)
    encrypted_str = encrypted_bytes.decode()
    
    result = []
    key_length = len(key)
    
    for i, char in enumerate(encrypted_str):
        key_char = key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        result.append(decrypted_char)
    
    return ''.join(result)

    
window = tk.Tk()
window.title("encryptor and decryptor")
window.geometry("600x500")




# Шапка с кнопками
header_frame = ttk.Frame(window)
header_frame.pack(fill='x', padx=10, pady=10)

# Основная область для контента
content_frame = ttk.Frame(window)
content_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Кнопки в шапке
encrypt_btn = ttk.Button(header_frame, text="Шифровать")
encrypt_btn.pack()

decrypt_btn = ttk.Button(header_frame, text="Расшифровать")
decrypt_btn.pack()

generation_btn = ttk.Button(header_frame, text="Генерировать")
generation_btn.pack()

encryptfile_btn = ttk.Button(header_frame, text="Encrypt File")
encryptfile_btn.pack()

decryptfile_btn = ttk.Button(header_frame, text="Decrypt File")
decryptfile_btn.pack()


ctf_btn = ttk.Button(header_frame, text="CTF task ")
ctf_btn.pack()


def hash_key(key):
    return hashlib.sha256(key.encode()).hexdigest()


def open_encrypt_window():
    encrypt=tk.Toplevel(window)
    encrypt.title("encryptor")
    encrypt.geometry("600x500")

    label = tk.Label(encrypt,text="Word")
    label.pack()

    text=ttk.Entry(encrypt)
    text.pack()

    label = tk.Label(encrypt,text="Cave")
    label.pack()

    key = ttk.Entry(encrypt)
    key.pack()

    label = tk.Label(encrypt, text="HEX")
    label.pack()

    result_label = ttk.Entry(encrypt, width=50)
    result_label.pack()

    def encrypt_action():
        input_text = text.get()
        input_key = hash_key(key.get())
        
        print(f"Текст: '{input_text}'")  
        print(f"Ключ (хеш): {input_key}")  
        print(f"Длина ключа: {len(input_key)}")  
    
        if input_key:
            result = xor_encrypt(input_text, input_key)
            result_label.delete(0, tk.END)      # очищаем поле
            result_label.insert(0, result) 
        else:
            result_label.delete(0, tk.END)
            result_label.insert(0, "Ошибка: введите ключ")

    encrypt_btn = ttk.Button(encrypt, text="encrypt", command=encrypt_action)
    encrypt_btn.pack()


def open_decrypt_window():
    decrypt = tk.Toplevel(window)
    decrypt.title("decrypt")
    decrypt.geometry("600x500")

    label = tk.Label(decrypt, text="Enter hex type")
    label.pack()

    text = ttk.Entry(decrypt)
    text.pack()

    label = tk.Label(decrypt, text="Switch decoding")
    label.pack()

    key = ttk.Entry(decrypt)
    key.pack()

    label = ttk.Label(decrypt, text="Transcript")
    label.pack()

    result_label = ttk.Entry(decrypt, width = 50)
    result_label.pack()
    
    def decrypt_action():
        input_text = text.get()
        input_key = hash_key(key.get())

        if input_key:
            result = xor_decrypt(input_text, input_key)  # возвращает ТЕКСТ
            result_label.delete(0, tk.END)
            result_label.insert(0, result)  # вставляем ТЕКСТ
        else:
           result_label.insert(0, "Ошибка: введите ключ")
        

    decrypt_btn = ttk.Button(decrypt, text = "decrypt", command= decrypt_action)
    decrypt_btn.pack(pady=10) 

def open_generation_password():
    generation = tk.Toplevel(window)
    generation.title("generation")
    generation.geometry("600x500")

    label = tk.Label(generation, text="key")
    label.pack()

    key = tk.Entry(generation, width=10)
    key.pack()

    label = tk.Label(generation, text="Generation password")
    label.pack()

    gw = tk.Entry(generation, width=50)
    gw.pack()

    label = tk.Label(generation, text="hex view")
    label.pack()

    hex_entry = tk.Entry(generation, width=50)
    hex_entry.pack()

    def generation_password():
        key_text = key.get()
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        password = ""
        for i in range(12):
            char = random.choice(chars)
            password += char
        gw.delete(0, tk.END)
        gw.insert(0, password)

        if not key_text:
            hex_entry.delete(0, tk.END)
            hex_entry.insert(0, "Ошибка: введите ключ")
            return

        hashed_key = hash_key(key_text)
        result = xor_encrypt(password, hashed_key)

        hex_entry.delete(0, tk.END)
        hex_entry.insert(0, result)

    btn = ttk.Button(generation, text="Generate", command=generation_password)
    btn.pack() 
    
    
def open_file():
    file = tk.Toplevel(window)
    file.title("encrypt file")
    file.geometry("600x500")   
    
    
    file_r = tk.Entry(file, width=50)
    file_r.pack()
    
    def browser_file():
        filepath = filedialog.askopenfilename()
        print(filepath)
        
        file_r.delete(0, tk.END)
        file_r.insert(0, filepath)
        
    def encrypt_file():
        filepath = file_r.get()  
        key_text = key.get()
        
        if not filepath:
            print("Выберите файл")
            return

        if not key_text:
            print("Введите ключ")
            return
        
        with open(filepath, "rb") as f:
            data = f.read()
                  
        key_bytes = hash_key_bytes(key_text)
        encrypted_data = xor_file_bytes(data, key_bytes)
        
        new_filepath = filepath + ".enc"

        with open(new_filepath, "wb") as f:
            f.write(encrypted_data)

            print("Файл сохранён:", new_filepath)
        
    def hash_key_bytes(key_text):
        return hashlib.sha256(key_text.encode()).digest()
    
    def xor_file_bytes(data, key_bytes):
        result = bytearray()

        for i, byte in enumerate(data):
            key_byte = key_bytes[i % len(key_bytes)]
            encrypted_byte = byte ^ key_byte
            result.append(encrypted_byte)

        return result
    
    btn = ttk.Button(file, text="Выбрать файл", command=browser_file)
    btn.pack()
    
    label = tk.Label(file, text="Key")
    label.pack()
    
    key = ttk.Entry(file, width=10)
    key.pack()
    
    encrypt = ttk.Button(file, text="Шифровать файл", command=encrypt_file)
    encrypt.pack()
    
def decrypt_file():
    file = tk.Toplevel(window)
    file.title("decrypt file")
    file.geometry("600x500") 
    
    file_d = tk.Entry(file, width=50)
    file_d.pack()
    
    label = tk.Label(file, text="Key")
    label.pack()
    
    key = ttk.Entry(file, width=10)
    key.pack()
    
    
    def open_file():
        filepath = filedialog.askopenfilename()
        print(filepath)
        
        file_d.delete(0, tk.END)
        file_d.insert(0, filepath)
        
    def hash_key_bytes(key_text):
        return hashlib.sha256(key_text.encode()).digest()


    def xor_file_bytes(data, key_bytes):
        result = bytearray()

        for i, byte in enumerate(data):
            key_byte = key_bytes[i % len(key_bytes)]
            decrypted_byte = byte ^ key_byte
            result.append(decrypted_byte)

        return result

    def decrypt_file_action():
        filepath = file_d.get()
        key_text = key.get()
        
        print("filepath:", filepath)
        print("key_text:", key_text)

        if not filepath:
            print("Выберите файл")
            return

        if not key_text:
            print("Введите ключ")
            return

        with open(filepath, "rb") as f:
            data = f.read()
            print("Размер входного файла:", len(data))

        key_bytes = hash_key_bytes(key_text)
        decrypted_data = xor_file_bytes(data, key_bytes)
        print("Размер расшифрованных данных:", len(decrypted_data))

        new_filepath = filepath + ".decoded"
        print("new_filepath:", new_filepath)

        with open(new_filepath, "wb") as f:
            f.write(decrypted_data)
            
        print("Файл точно записан")

        print("Файл расшифрован:", new_filepath)
            
     
    label = tk.Button(file, text="Выбрать файл", command=open_file)
    label.pack()
    
    encrypt = ttk.Button(file, text="Расшифровать файл", command=decrypt_file_action)
    encrypt.pack()  
    
    
def CTF_task():
    ctf = tk.Toplevel(window)
    ctf.title("CTF task")
    ctf.geometry("600x500")

    def task1_ez():
        task1 = tk.Toplevel(ctf)
        task1.title("TASK 1")
        task1.geometry("600x500")

        secret_text = "hello"
        real_key = "dragon"
        encrypted_key = "ftciqp"   # ключ, зашифрованный Цезарем
        hex_text = xor_encrypt(secret_text, hash_key(real_key))

        label = tk.Label(task1,text="Гай Юлий Цезарь — древнеримский государственный и политический деятель")
        label.pack(pady=10)

        label = tk.Label(task1, text=f"Зашифрованный ключ: {encrypted_key}")
        label.pack(pady=5)

        label = tk.Label(task1, text=f"HEX строка: {hex_text}")
        label.pack(pady=5)

        label = tk.Label(task1, text="Введи расшифрованный текст:")
        label.pack(pady=5)

        answer = tk.Entry(task1, width=50)
        answer.pack(pady=5)

        result_label = tk.Label(task1, text="")
        result_label.pack(pady=10)

        def check_answer():
            user_answer = answer.get()

            if user_answer == secret_text:
                result_label.config(text="Верно! Ты решил задачу.")
            else:
                result_label.config(text="Неверно. Попробуй ещё раз.")

        btn = tk.Button(task1, text="Проверить", command=check_answer)
        btn.pack(pady=10)
    
    
    def task2_mediun():
        task2 = tk.Toplevel(ctf)
        task2.title("Task2")
        task2.geometry("600x500")
        
        secret_text = "LOL"
        real_key = "Bear"
        encoded_key = "QmVhcg=="
        
        hex_text = xor_encrypt(secret_text, hash_key(real_key))
        
        label = tk.Label(task2,text="Base64")
        label.pack(pady=10)

        label = tk.Label(task2, text=f"Зашифрованный ключ: {encoded_key}")
        label.pack(pady=5)

        label = tk.Label(task2, text=f"HEX строка: {hex_text}")
        label.pack(pady=5)

        label = tk.Label(task2, text="Введи расшифрованный текст:")
        label.pack(pady=5)

        answer = tk.Entry(task2, width=50)
        answer.pack(pady=5)

        result_label = tk.Label(task2, text="")
        result_label.pack(pady=10)
        
        
        
        def check_task2():
            user_answer = answer.get()
            
            if user_answer == secret_text:
                result_label.config(text="Верно! Ты решил задачу.")
                
            else:
                result_label.config(text="Неверно. Попробуй ещё раз.")
                
        btn = tk.Button(task2, text="Проверить", command=check_task2)
        btn.pack(pady=10)
        
    def task3_hard():
        task3 = tk.Toplevel(ctf)
        task3.title("Task3")
        task3.geometry("600x500")

        secret_text = "hack"
        real_key = "lion"
        encoded_key = "noil"

        hex_text = xor_encrypt(secret_text, hash_key(real_key))

        label = tk.Label(task3, text="Reverse key")
        label.pack(pady=10)

        label = tk.Label(task3, text="Подсказка: ключ записан наоборот")
        label.pack(pady=5)

        label = tk.Label(task3, text=f"Зашифрованный ключ: {encoded_key}")
        label.pack(pady=5)

        label = tk.Label(task3, text=f"HEX строка: {hex_text}")
        label.pack(pady=5)

        label = tk.Label(task3, text="Введи расшифрованный текст:")
        label.pack(pady=5)

        answer = tk.Entry(task3, width=50)
        answer.pack(pady=5)

        result_label = tk.Label(task3, text="")
        result_label.pack(pady=10)
    

        def check_task3():
            user_answer = answer.get()

            if user_answer == secret_text:
                result_label.config(text="Верно! Ты решил задачу.")
            else:
                result_label.config(text="Неверно. Попробуй ещё раз.")

        btn = tk.Button(task3, text="Проверить", command=check_task3)
        btn.pack(pady=10)
            
    task1_btn = ttk.Button(ctf, text="TASK1", command=task1_ez)
    task1_btn.pack(pady=10)

    task2_btn = ttk.Button(ctf, text="TASK2", command=task2_mediun)
    task2_btn.pack(pady=10)

    task3_btn = ttk.Button(ctf, text="TASK3", command=task3_hard)
    task3_btn.pack(pady=10)      

    task1_btn.config(command=task1_ez) 

encrypt_btn.config(command=open_encrypt_window)

decrypt_btn.config(command=open_decrypt_window)

generation_btn.config(command=open_generation_password)

encryptfile_btn.config(command=open_file)

decryptfile_btn.config(command=decrypt_file)

ctf_btn.config(command=CTF_task)

window.mainloop()