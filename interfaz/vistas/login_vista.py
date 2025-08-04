import tkinter as tk
from tkinter import ttk

class LoginVista:
    def __init__(self, root, mostrar_error_callback, autenticar_callback):
        self.root = root
        self.mostrar_error = mostrar_error_callback
        self.autenticar = autenticar_callback
        self.error_label = None  # Se inicializará cuando se cree la interfaz
        
    def mostrar(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, fill='x')
        ttk.Label(header_frame, text="Inicio de Sesión", 
                 style='Header.TLabel').pack()
        
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)
        
        # Campos de login
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.username_entry = ttk.Entry(form_frame, font=('Helvetica', 12))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.password_entry = ttk.Entry(form_frame, font=('Helvetica', 12), show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Crear el label de error y guardarlo como atributo de la clase
        self.error_label = ttk.Label(form_frame, text="", style='Error.TLabel')
        self.error_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Iniciar Sesión", command=self._autenticar,
                  style='Login.TButton', width=15).pack(pady=10)
    
    def _autenticar(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.mostrar_error("Por favor ingrese usuario y contraseña")
            return
            
        self.autenticar(username, password)
