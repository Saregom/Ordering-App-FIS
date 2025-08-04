import tkinter as tk
from tkinter import ttk

class SaldoVista:
    def __init__(self, root, info_saldo):
        self.root = root
        self.info_saldo = info_saldo
        self.ventana_saldo = None
    
    def mostrar_saldo(self):
        """Muestra el saldo del cliente en una ventana emergente"""
        self.ventana_saldo = tk.Toplevel(self.root)
        self.ventana_saldo.title("Información de Saldo")
        self.ventana_saldo.geometry("400x300")
        self.ventana_saldo.configure(bg="#f0f0f0")
        
        # Centrar la ventana
        self.ventana_saldo.update_idletasks()
        screen_width = self.ventana_saldo.winfo_screenwidth()
        screen_height = self.ventana_saldo.winfo_screenheight()
        width = 400
        height = 300
        centerX = (screen_width // 2) - (width // 2)
        centerY = (screen_height // 2) - (height // 2)
        self.ventana_saldo.geometry(f"{width}x{height}+{centerX}+{centerY}")
        
        # Frame principal
        main_frame = ttk.Frame(self.ventana_saldo)
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Título
        titulo_label = ttk.Label(main_frame, text="Información Financiera", 
                                style='Header.TLabel')
        titulo_label.pack(pady=(0, 20))
        
        # Frame para la información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='both', expand=True)
        
        # Configurar grid
        info_frame.columnconfigure(1, weight=1)
        
        # Mostrar saldo actual
        ttk.Label(info_frame, text="Saldo Actual:", 
                 font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        saldo_color = '#2e8b57' if self.info_saldo['saldo'] >= 0 else '#dc143c'
        saldo_text = f"${self.info_saldo['saldo']:,.0f}"
        if self.info_saldo['saldo'] < 0:
            saldo_text += " (usando crédito)"
        saldo_label = ttk.Label(info_frame, text=saldo_text, 
                               font=('Helvetica', 12), foreground=saldo_color)
        saldo_label.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=10)
        
        # Mostrar límite de crédito
        ttk.Label(info_frame, text="Límite de Crédito:", 
                 font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        credito_label = ttk.Label(info_frame, text=f"${self.info_saldo['limite_credito']:,.0f}", 
                                 font=('Helvetica', 12), foreground='#4169e1')
        credito_label.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=10)
        
        # Mostrar descuento
        ttk.Label(info_frame, text="Descuento Aplicable:", 
                 font=('Helvetica', 12, 'bold')).grid(row=2, column=0, sticky='w', pady=10)
        descuento_label = ttk.Label(info_frame, text=f"{self.info_saldo['descuento']}%", 
                                   font=('Helvetica', 12), foreground='#ff6347')
        descuento_label.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=10)
        
        # Separador
        separator = ttk.Separator(info_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=2, sticky='ew', pady=20)
        
        # Crédito disponible total (saldo + límite de crédito)
        credito_total = self.info_saldo['saldo'] + self.info_saldo['limite_credito']
        ttk.Label(info_frame, text="Disponible Total:", 
                 font=('Helvetica', 12, 'bold')).grid(row=4, column=0, sticky='w', pady=10)
        disponible_label = ttk.Label(info_frame, text=f"${credito_total:,.0f}", 
                                    font=('Helvetica', 12), foreground='#228b22')
        disponible_label.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=10)
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", 
                  command=self.ventana_saldo.destroy).pack(pady=20)
        
        # Hacer que la ventana sea modal
        self.ventana_saldo.transient(self.root)
        self.ventana_saldo.grab_set()
        
        # Configurar estilo
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
