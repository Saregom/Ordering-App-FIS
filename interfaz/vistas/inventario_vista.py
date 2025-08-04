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
        win = self.create_window("Gestionar Inventario desde Planta", 850, 550)
        
        ttk.Label(win, text="Seleccione artículos de la planta manufacturera para surtir:", 
                 font=('Helvetica', 12)).pack(pady=10)
        
        # Obtener artículos de la planta
        if 'get_articulos_planta' in self.callbacks:
            articulos_planta = self.callbacks['get_articulos_planta']()
        else:
            messagebox.showerror("Error", "No se pueden obtener los artículos de la planta")
            win.destroy()
            return
        
        # Frame para la tabla de artículos de la planta
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Código', 'Nombre', 'Precio Base', 'Stock Planta', 'Precio Actual', 'Stock Actual'), show='headings')
        tree.heading('Código', text='Código')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Precio Base', text='Precio Base Planta')
        tree.heading('Stock Planta', text='Stock Planta')
        tree.heading('Precio Actual', text='Precio Inventario')
        tree.heading('Stock Actual', text='Stock Inventario')
        
        # Obtener stock de la planta
        if 'get_stock_planta' in self.callbacks:
            stock_data = self.callbacks['get_stock_planta']()
            stock_actual = stock_data.get('stock_actual', {})
        else:
            stock_actual = {}
            messagebox.showerror("Error", "No se puede obtener el stock de la planta")
            win.destroy()
            return
        
        # Verificar que se obtuvieron datos del stock
        if not stock_actual:
            messagebox.showerror("Error", "No hay datos de stock disponibles en la planta")
            win.destroy()
            return
        
        # Obtener artículos del inventario principal para comparar
        articulos_inventario = {}
        for art in self.articulos:
            articulos_inventario[art.codigo] = {
                'precio': art.precio,
                'stock': getattr(art, 'cantidad', 0)
            }
        
        # Llenar la tabla con artículos de la planta
        for art in articulos_planta:
            stock_planta = stock_actual.get(art.codigo, 0)
            
            # Obtener datos del inventario principal
            if art.codigo in articulos_inventario:
                precio_inventario = articulos_inventario[art.codigo]['precio']
                stock_inventario = articulos_inventario[art.codigo]['stock']
            else:
                precio_inventario = 0
                stock_inventario = 0
            
            tree.insert('', 'end', values=(
                art.codigo, 
                art.nombre, 
                f"${art.precio:.2f}", 
                stock_planta,
                f"${precio_inventario:.2f}",
                stock_inventario
            ))
        
        # Configurar columnas
        tree.column('Código', width=80, anchor='center')
        tree.column('Nombre', width=150, anchor='w')
        tree.column('Precio Base', width=100, anchor='center')
        tree.column('Stock Planta', width=90, anchor='center')
        tree.column('Precio Actual', width=100, anchor='center')
        tree.column('Stock Actual', width=90, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Frame para formulario de surtido
        form_frame = ttk.Frame(win)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Cantidad a surtir:", font=('Helvetica', 10)).grid(row=0, column=0, sticky='w', padx=5)
        entry_cantidad = ttk.Entry(form_frame, width=15)
        entry_cantidad.grid(row=0, column=1, padx=5)
        
        ttk.Label(form_frame, text="Precio de venta:", font=('Helvetica', 10)).grid(row=0, column=2, sticky='w', padx=5)
        entry_precio = ttk.Entry(form_frame, width=15)
        entry_precio.grid(row=0, column=3, padx=5)
        
        # Función para cuando se selecciona un artículo
        def on_select(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                values = item['values']
                # Pre-llenar el precio con el precio actual del inventario si existe, sino con el precio base
                entry_precio.delete(0, tk.END)
                precio_actual = values[4].replace('$', '')  # Precio Actual (inventario)
                precio_base = values[2].replace('$', '')    # Precio Base (planta)
                
                # Si el precio actual es 0, usar el precio base
                if float(precio_actual) > 0:
                    entry_precio.insert(0, precio_actual)
                else:
                    entry_precio.insert(0, precio_base)
        
        tree.bind('<<TreeviewSelect>>', on_select)
        
        # Botones
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)
        
        def confirmar_surtido():
            selection = tree.selection()
            if not selection:
                messagebox.showerror("Error", "Por favor seleccione un artículo")
                return
            
            try:
                cantidad = int(entry_cantidad.get())
                precio_venta = float(entry_precio.get())
                
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return
                
                if precio_venta <= 0:
                    messagebox.showerror("Error", "El precio debe ser mayor a 0")
                    return
                
                # Obtener código del artículo seleccionado
                item = tree.item(selection[0])
                codigo = str(item['values'][0])  # Convertir a string para asegurar compatibilidad
                nombre = item['values'][1]
                stock_planta_mostrado = item['values'][3]  # Stock de la planta mostrado en la tabla
                
                # Verificar stock disponible en la planta
                stock_disponible = stock_actual.get(codigo, 0)
                
                if cantidad > stock_disponible:
                    messagebox.showerror("Error", f"Solo hay {stock_disponible} unidades disponibles en la planta para {nombre}")
                    return
                
                # Llamar al callback para agregar el artículo
                if 'agregar_desde_planta' in self.callbacks:
                    resultado = self.callbacks['agregar_desde_planta'](codigo, cantidad, precio_venta)
                    if resultado['success']:
                        messagebox.showinfo("Éxito", resultado['message'])
                        win.destroy()
                    else:
                        messagebox.showerror("Error", resultado['message'])
                else:
                    messagebox.showerror("Error", "Función no disponible")
                    
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
        
        ttk.Button(btn_frame, text="Surtir Artículo", command=confirmar_surtido,
                  style='Provider.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side='left', padx=5)

    def mostrar_stock_planta(self, stock_data):
        """Muestra el stock actual y mínimo de la planta manufacturera"""
        win = self.create_window("Stock Planta Manufacturera", 600, 450)
        
        header_frame = ttk.Frame(win)
        header_frame.pack(fill='x', pady=10)
        ttk.Label(header_frame, text="Stock Planta Manufacturera", 
                 style='Header.TLabel').pack()
        
        # Frame principal con scroll
        main_frame = ttk.Frame(win)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview para mostrar el stock
        tree = ttk.Treeview(main_frame, columns=('Código', 'Nombre', 'Stock Actual', 'Stock Mínimo', 'Estado'), show='headings')
        tree.heading('Código', text='Código')
        tree.heading('Nombre', text='Nombre Artículo')
        tree.heading('Stock Actual', text='Stock Actual')
        tree.heading('Stock Mínimo', text='Stock Mínimo')
        tree.heading('Estado', text='Estado')
        
        # Obtener todos los códigos únicos
        codigos = set()
        codigos.update(stock_data['stock_actual'].keys())
        codigos.update(stock_data['stock_minimo'].keys())
        
        for codigo in sorted(codigos):
            stock_actual = stock_data['stock_actual'].get(codigo, 0)
            stock_minimo = stock_data['stock_minimo'].get(codigo, 0)
            
            # Obtener nombre del artículo
            nombre = "N/A"
            if 'articulos_info' in stock_data and codigo in stock_data['articulos_info']:
                nombre = stock_data['articulos_info'][codigo]['nombre']
            
            # Determinar el estado
            if stock_actual <= stock_minimo:
                estado = "⚠️ Crítico"
            elif stock_actual <= stock_minimo * 1.5:
                estado = "⚡ Bajo"
            else:
                estado = "✅ Suficiente"
            
            item = tree.insert('', 'end', values=(codigo, nombre, stock_actual, stock_minimo, estado))
        
        # Configurar columnas
        tree.column('Código', width=100, anchor='center')
        tree.column('Nombre', width=150, anchor='w')
        tree.column('Stock Actual', width=100, anchor='center')
        tree.column('Stock Mínimo', width=100, anchor='center')
        tree.column('Estado', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Frame para información adicional
        info_frame = ttk.Frame(win)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        total_articulos = len(codigos)
        articulos_criticos = sum(1 for codigo in codigos 
                               if stock_data['stock_actual'].get(codigo, 0) <= stock_data['stock_minimo'].get(codigo, 0))
        
        ttk.Label(info_frame, text=f"Total de artículos: {total_articulos} | Artículos en estado crítico: {articulos_criticos}",
                 font=('Helvetica', 10)).pack()
        
        # Botón cerrar
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cerrar", command=win.destroy).pack()
