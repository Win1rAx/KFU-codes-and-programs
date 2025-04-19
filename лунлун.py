import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class XorCipherLogic:
    def __init__(self):
        # Define alphabets
        self.eng_ab = 'abcdefghijklmnopqrstuvwxy0123456789'
        self.rus_ab = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789'
        
        # Create binary mappings
        self.eng_bin = {c: bin(i)[2:].zfill(6) for i, c in enumerate(self.eng_ab)}
        self.rus_bin = {c: bin(i)[2:].zfill(6) for i, c in enumerate(self.rus_ab)}
        
        # Create reverse mappings
        self.eng_bin_rev = {v: k for k, v in self.eng_bin.items()}
        self.rus_bin_rev = {v: k for k, v in self.rus_bin.items()}

    def xor_6bit(self, bits1, bits2):
        
        return ''.join('0' if b1 == b2 else '1' for b1, b2 in zip(bits1, bits2))

    def text_to_bin(self, text, key, alphabet):
        
        text = text.lower()
        text_bin = []
        key_bin = []
        
        bin_map = self.eng_bin if alphabet == self.eng_ab else self.rus_bin
        
        for char in text:
            if char in bin_map:
                text_bin.append(bin_map[char])
            else:
                raise ValueError(f"Invalid character '{char}' in text")
                
        for char in key:
            if char in bin_map:
                key_bin.append(bin_map[char])
            else:
                raise ValueError(f"Invalid character '{char}' in key")
                
        return ''.join(text_bin), ''.join(key_bin)

    def bin_to_text(self, bit_string, alphabet):
        text = []
        bin_rev = self.eng_bin_rev if alphabet == self.eng_ab else self.rus_bin_rev
        
        for i in range(0, len(bit_string), 6):
            chunk = bit_string[i:i+6]
            if chunk in bin_rev:
                text.append(bin_rev[chunk])
            else:
                return '-'
        return ''.join(text)

    def encrypt(self, text_bits, key_bits, iv):
        result = []
        key_iv = self.xor_6bit(key_bits, iv)
        
        # First block
        result.append(self.xor_6bit(key_iv, text_bits[:6]))
        
        # Subsequent blocks
        for i in range(6, len(text_bits), 6):
            result.append(self.xor_6bit(result[-1], text_bits[i:i+6]))
            
        return ''.join(result)

    def decrypt(self, encrypted_bits, key_bits, iv):
        decrypted = []
        key_iv = self.xor_6bit(key_bits, iv)
        
        # First block
        first_block = self.xor_6bit(encrypted_bits[:6], key_iv)
        decrypted.append(first_block)
        
        # Subsequent blocks
        for i in range(6, len(encrypted_bits), 6):
            decrypted.append(self.xor_6bit(encrypted_bits[i:i+6], encrypted_bits[i-6:i]))
            
        return ''.join(decrypted)

    def clean_text(self, text, alphabet):
        """Remove characters not in the specified alphabet"""
        return ''.join(c for c in text.lower() if c in alphabet)

    def generate_key(self, length):
        half = length // 2
        key = ['0'] * half + ['1'] * half
        random.shuffle(key)
        return ''.join(key)

    def generate_iv(self):
        """Generate a random 6-bit initialization vector"""
        return self.generate_key(6)


class XorCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XOR Cipher")
        self.root.geometry("800x800")
        
        self.cipher = XorCipherLogic()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Alphabet selection
        alphabet_frame = ttk.LabelFrame(main_frame, text="Alphabet", padding="10")
        alphabet_frame.pack(fill=tk.X, pady=5)
        
        self.alphabet_var = tk.StringVar(value="English")
        ttk.Radiobutton(alphabet_frame, text="English", variable=self.alphabet_var, 
                       value="English", command=self.update_alphabet).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(alphabet_frame, text="Russian", variable=self.alphabet_var, 
                       value="Russian", command=self.update_alphabet).pack(side=tk.LEFT, padx=5)
        
        # Key section
        key_frame = ttk.LabelFrame(main_frame, text="Key", padding="10")
        key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(key_frame, text="Key (1 symbol):").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(key_frame, width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.bind('<KeyRelease>', self.update_key_bin)
        
        ttk.Label(key_frame, text="Binary:").pack(side=tk.LEFT, padx=(10, 0))
        self.key_bin_entry = ttk.Entry(key_frame, width=25, state='readonly')
        self.key_bin_entry.pack(side=tk.LEFT)
        
        # Initialization Vector
        iv_frame = ttk.LabelFrame(main_frame, text="Initialization Vector", padding="10")
        iv_frame.pack(fill=tk.X, pady=5)
        
        self.iv_entry = ttk.Entry(iv_frame, width=25, state='readonly')
        self.iv_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(iv_frame, text="Generate New", command=self.generate_new_iv).pack(side=tk.LEFT)
        
        # Set initial IV
        self.iv_entry.config(state='normal')
        self.iv_entry.delete(0, tk.END)
        self.iv_entry.insert(0, self.cipher.generate_iv())
        self.iv_entry.config(state='readonly')
        
        # Input text
        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.input_text = tk.Text(input_frame, height=5, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind('<KeyRelease>', self.update_input_bin)
        
        ttk.Button(input_frame, text="Clean Text", command=self.clean_input_text).pack(pady=5)
        
        # Input binary
        input_bin_frame = ttk.LabelFrame(main_frame, text="Input Binary", padding="10")
        input_bin_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.input_bin_text = tk.Text(input_bin_frame, height=5, state='disabled')
        self.input_bin_text.pack(fill=tk.BOTH, expand=True)
        
        # Encryption buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT, padx=5)
        
        # Encrypted binary
        encrypted_frame = ttk.LabelFrame(main_frame, text="Encrypted Binary", padding="10")
        encrypted_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.encrypted_text = tk.Text(encrypted_frame, height=5)
        self.encrypted_text.pack(fill=tk.BOTH, expand=True)
        
        # Decrypted output
        decrypted_frame = ttk.LabelFrame(main_frame, text="Decrypted Output", padding="10")
        decrypted_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.decrypted_text = tk.Text(decrypted_frame, height=5, state='disabled')
        self.decrypted_text.pack(fill=tk.BOTH, expand=True)
        
        self.decrypted_bin_text = tk.Text(decrypted_frame, height=5)
        self.decrypted_bin_text.pack(fill=tk.BOTH, expand=True)
    
    def get_current_alphabet(self):
        return self.cipher.eng_ab if self.alphabet_var.get() == "English" else self.cipher.rus_ab
    
    def update_alphabet(self):
        """Handle alphabet change"""
        self.clean_input_text()
        self.update_key_bin(None)
    
    def validate_key(self):
        """Validate the key input"""
        key = self.key_entry.get().lower()
        alphabet = self.get_current_alphabet()
        
        if len(key) > 1:
            self.key_entry.delete(1, tk.END)
            messagebox.showerror("Error", "Key must be exactly one character!")
            return None
        
        if key and key[0] not in alphabet:
            self.key_entry.delete(0, tk.END)
            messagebox.showerror("Error", f"Key must be from the {self.alphabet_var.get()} alphabet!")
            return None
            
        return key
    
    def update_key_bin(self, event):
        """Update the binary representation of the key"""
        key = self.validate_key()
        if not key:
            self.key_bin_entry.config(state='normal')
            self.key_bin_entry.delete(0, tk.END)
            self.key_bin_entry.config(state='readonly')
            return
            
        alphabet = self.get_current_alphabet()
        _, key_bin = self.cipher.text_to_bin("", key, alphabet)
        
        self.key_bin_entry.config(state='normal')
        self.key_bin_entry.delete(0, tk.END)
        self.key_bin_entry.insert(0, key_bin)
        self.key_bin_entry.config(state='readonly')
    
    def generate_new_iv(self):
        """Generate a new initialization vector"""
        self.iv_entry.config(state='normal')
        self.iv_entry.delete(0, tk.END)
        self.iv_entry.insert(0, self.cipher.generate_iv())
        self.iv_entry.config(state='readonly')
    
    def clean_input_text(self):
        """Clean the input text to only contain alphabet characters"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        alphabet = self.get_current_alphabet()
        
        cleaned = self.cipher.clean_text(input_text, alphabet)
        
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", cleaned)
        self.update_input_bin(None)
    
    def update_input_bin(self, event):
        """Update the binary representation of the input text"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        alphabet = self.get_current_alphabet()
        
        try:
            text_bin, _ = self.cipher.text_to_bin(input_text, "", alphabet)
            
            self.input_bin_text.config(state='normal')
            self.input_bin_text.delete("1.0", tk.END)
            self.input_bin_text.insert("1.0", text_bin)
            self.input_bin_text.config(state='disabled')
        except ValueError as e:
            pass
    
    def encrypt(self):
        """Encrypt the input text"""
        # Validate key
        key_bin = self.key_bin_entry.get()
        if not key_bin:
            messagebox.showerror("Error", "Please enter a valid key!")
            return
            
        # Validate IV
        iv = self.iv_entry.get()
        if len(iv) != 6 or not all(c in '01' for c in iv):
            messagebox.showerror("Error", "Invalid initialization vector!")
            return
            
        # Validate input
        input_bin = self.input_bin_text.get("1.0", tk.END).strip()
        if not input_bin:
            messagebox.showerror("Error", "No input text to encrypt!")
            return
            
        if len(input_bin) % 6 != 0:
            messagebox.showerror("Error", "Input length must be a multiple of 6!")
            return
            
        # Perform encryption
        try:
            encrypted = self.cipher.encrypt(input_bin, key_bin, iv)
            self.encrypted_text.delete("1.0", tk.END)
            self.encrypted_text.insert("1.0", encrypted)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def decrypt(self):
        """Decrypt the encrypted text"""
        # Validate key
        key_bin = self.key_bin_entry.get()
        if not key_bin:
            messagebox.showerror("Error", "Please enter a valid key!")
            return
            
        # Validate IV
        iv = self.iv_entry.get()
        if len(iv) != 6 or not all(c in '01' for c in iv):
            messagebox.showerror("Error", "Invalid initialization vector!")
            return
            
        # Validate input
        encrypted_bin = self.encrypted_text.get("1.0", tk.END).strip()
        if not encrypted_bin:
            messagebox.showerror("Error", "No encrypted text to decrypt!")
            return
            
        if len(encrypted_bin) % 6 != 0:
            messagebox.showerror("Error", "Encrypted text length must be a multiple of 6!")
            return
            
        # Perform decryption
        try:
            decrypted_bin = self.cipher.decrypt(encrypted_bin, key_bin, iv)
            decrypted_text = self.cipher.bin_to_text(decrypted_bin, self.get_current_alphabet())
            
            self.decrypted_bin_text.delete("1.0", tk.END)
            self.decrypted_bin_text.insert("1.0", decrypted_bin)
            
            self.decrypted_text.config(state='normal')
            self.decrypted_text.delete("1.0", tk.END)
            self.decrypted_text.insert("1.0", decrypted_text)
            self.decrypted_text.config(state='disabled')
            
            if decrypted_text == '-':
                messagebox.showwarning("Warning", "Decryption produced invalid characters!")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def clear_all(self):
        """Clear all input and output fields"""
        self.input_text.delete("1.0", tk.END)
        self.input_bin_text.config(state='normal')
        self.input_bin_text.delete("1.0", tk.END)
        self.input_bin_text.config(state='disabled')
        
        self.encrypted_text.delete("1.0", tk.END)
        
        self.decrypted_text.config(state='normal')
        self.decrypted_text.delete("1.0", tk.END)
        self.decrypted_text.config(state='disabled')
        
        self.decrypted_bin_text.delete("1.0", tk.END)
        
        self.key_entry.delete(0, tk.END)
        self.key_bin_entry.config(state='normal')
        self.key_bin_entry.delete(0, tk.END)
        self.key_bin_entry.config(state='readonly')


def main():
    root = tk.Tk()
    app = XorCipherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    