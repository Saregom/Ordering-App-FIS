import tkinter as tk
from tkinter import ttk, messagebox

from interfaz.vistas.base_vista import BaseVista

class InventarioVista(BaseVista):
    def __init__(self, parent, articulos, callbacks):
        super().__init__(parent)
        self.articulos = articulos
        self.callbacks = callbacks
    
    def mostrar_inventario(self):
        win = self.create_window("Inventario Actual", 600, 450)
        
        header_frame = ttk.Frame(win)
        header_frame.pack(fill='x', pady=10)
        ttk.Label(header_frame, text="Inventario Disponible", 
                 style='Header.TLabel').pack()
        
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, columns=('Código', 'Nombre', 'Descripción', 'Precio', 'Stock'), show='headings')
        tree.heading('Código', text='Código')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Descripción', text='Descripción')
        tree.heading('Precio', text='Precio')
        tree.heading('Stock', text='Stock')
        
        for art in self.articulos:
            codigo = art.codigo
            cantidad = getattr(art, 'cantidad', 0)
            tree.insert('', 'end', values=(codigo, art.nombre, art.descripcion, f"${art.precio}", f"{cantidad} unidades"))

        tree.column('Código', width=100, anchor='center')
        tree.column('Nombre', width=100, anchor='w')
        tree.column('Descripción', width=100, anchor='w')
        tree.column('Precio', width=100, anchor='center')
        tree.column('Stock', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
    
    def mostrar_actualizar_stock(self):
        win = self.create_window("Actualizar Stock", 600, 450)
        
        ttk.Label(win, text="Seleccione una opción:", font=('Helvetica', 12)).pack(pady=10)
        
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Agregar a producto existente", 
                  command=lambda: self.mostrar_agregar_stock(win),
                  style='Provider.TButton', width=25).pack(pady=10)
        ttk.Button(btn_frame, text="Agregar producto nuevo", 
                  command=lambda: self.mostrar_agregar_producto(win),
                  style='Provider.TButton', width=25).pack(pady=10)
    
    def mostrar_agregar_stock(self, parent_win):
        win = self.create_window("Agregar a Producto Existente", 600, 450)
        
        ttk.Label(win, text="Seleccione el producto:", font=('Helvetica', 12)).pack(pady=10)
        
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tree = ttk.Treeview(tree_frame, columns=('Codigo', 'Precio', 'Stock'), show='headings')
        tree.heading('Codigo', text='Código')
        tree.heading('Precio', text='Precio')
        tree.heading('Stock', text='Stock Actual')
        
        # Insertar datos
        for art in self.articulos:
            cantidad = getattr(art, 'cantidad', 0)
            tree.insert('', 'end', text=art.nombre, values=(f"{art.codigo}", f"${art.precio}", f"{cantidad} unidades"))

        tree.column('Codigo', width=100, anchor='center')
        tree.column('Precio', width=100, anchor='center')
        tree.column('Stock', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        cantidad_frame = ttk.Frame(win)
        cantidad_frame.pack(pady=10)
        
        ttk.Label(cantidad_frame, text="Cantidad a agregar:").pack(side='left')
        cantidad_var = tk.IntVar(value=1)
        ttk.Spinbox(cantidad_frame, from_=1, to=100, textvariable=cantidad_var, width=5).pack(side='left', padx=5)
        
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)
        
        def confirmar():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Por favor seleccione un producto")
                return
            
            item = tree.item(selected_item)
            producto_nombre = item['text']
            cantidad = cantidad_var.get()
            
            if self.callbacks['actualizar_stock'](producto_nombre, cantidad):
                win.destroy()
                parent_win.destroy()
        
        ttk.Button(btn_frame, text="Confirmar", command=confirmar,
                  style='Provider.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side='left', padx=5)
    
    def mostrar_agregar_producto(self, parent_win):
        win = self.create_window("Agregar Producto Nuevo", 600, 450)
        
        form_frame = ttk.Frame(win)
        form_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        campos = [
            ("Nombre del producto:", 'nombre'),
            ("Código:", 'codigo'),
            ("Precio:", 'precio'),
            ("Cantidad inicial:", 'cantidad')
        ]
        
        variables = {}
        
        for i, (label, field) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if field == 'precio':
                var = tk.DoubleVar(value=0.0)
                entry = ttk.Entry(form_frame, textvariable=var, font=('Helvetica', 12))
            elif field == 'cantidad':
                var = tk.IntVar(value=1)
                entry = ttk.Spinbox(form_frame, from_=1, to=1000, textvariable=var, width=5)
            else:
                var = tk.StringVar()
                entry = ttk.Entry(form_frame, textvariable=var, font=('Helvetica', 12))
            
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
            variables[field] = var
        
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=20)
        
        def confirmar():
            if not all(var.get() for var in variables.values()):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            try:
                datos = {
                    'codigo': variables['codigo'].get(),
                    'nombre': variables['nombre'].get(),
                    'precio': float(variables['precio'].get()),
                    'cantidad': variables['cantidad'].get()
                }
                
                if self.callbacks['agregar_producto'](**datos):
                    win.destroy()
                    parent_win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo agregar el producto")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores válidos")
        
        ttk.Button(btn_frame, text="Agregar Producto", command=confirmar,
                  style='Provider.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side='left', padx=5)
