import tkinter as tk
from tkinter import ttk, messagebox
from interfaz.vistas.base_vista import BaseVista

class PedidosVista(BaseVista):
    def __init__(self, parent, articulos, callbacks):
        super().__init__(parent)
        self.articulos = articulos
        self.callbacks = callbacks
        self.estados = ["Pendiente", "En proceso", "Enviado", "Entregado", "Cancelado"]
        
    def mostrar_realizar_pedido(self):
        win = self.create_window("Nuevo Pedido", 600, 400)
        
        form_frame = ttk.Frame(win)
        form_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        ttk.Label(form_frame, text="Dirección de envío:", font=('Helvetica', 12)).pack(anchor='w')
        entry_direccion = ttk.Entry(form_frame, font=('Helvetica', 12))
        entry_direccion.pack(fill='x', pady=10)
        
        # Artículos disponibles
        ttk.Label(form_frame, text="Artículos disponibles:", font=('Helvetica', 12)).pack(anchor='w', pady=5)
        
        # Frame para artículos con scroll
        art_frame = self._crear_frame_articulos(form_frame)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(pady=20)
        
        def confirmar():
            direccion = entry_direccion.get()
            if not direccion:
                messagebox.showerror("Error", "Por favor ingrese una dirección")
                return
                
            # Obtener artículos con cantidad > 0
            articulos = {art: var.get() for art, var in self.articulos_seleccionados.items() if var.get() > 0}
            
            if not articulos:
                messagebox.showerror("Error", "Debe seleccionar al menos un artículo")
                return
                
            self.callbacks['realizar_pedido'](direccion, articulos)
            win.destroy()
        
        ttk.Button(btn_frame, text="Realizar Pedido", command=confirmar, 
                  style='Client.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side='left', padx=5)
    
    def mostrar_historial(self, pedidos):
        win = self.create_window("Historial de Pedidos", 600, 400)
        
        scroll_frame = ttk.Frame(win)
        scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(scroll_frame)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if not pedidos:
            ttk.Label(scrollable_frame, text="No hay pedidos registrados").pack(pady=20)
            return
            
        for ped in pedidos:
            frame = ttk.LabelFrame(scrollable_frame, text=f"Pedido del {ped.fecha_ped.date()}")
            frame.pack(fill='x', pady=5, padx=5)
            
            ttk.Label(frame, text=f"Dirección: {ped.direccion}").pack(anchor='w')
            ttk.Label(frame, text=f"Estado: {ped.estado}").pack(anchor='w')
            
            for art, cant in ped.articulos_cant.items():
                ttk.Label(frame, text=f"• {art.nombre}: {cant} und").pack(anchor='w')
    
    def mostrar_cambiar_estado(self, todos_los_pedidos):
        """Muestra la interfaz para cambiar el estado de los pedidos"""
        win = self.create_window("Cambiar Estado de Pedidos", 600, 400)
        
        ttk.Label(win, text="Seleccione un pedido para cambiar su estado:", 
                 font=('Helvetica', 12)).pack(pady=10)
        
        # Treeview para mostrar pedidos
        tree_frame = ttk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Cliente', 'Artículos', 'Estado'), show='headings')
        tree.heading('#0', text='Fecha')
        tree.heading('Cliente', text='Cliente')
        tree.heading('Artículos', text='Artículos')
        tree.heading('Estado', text='Estado')
        
        if not todos_los_pedidos:
            ttk.Label(tree_frame, text="No hay pedidos disponibles").pack(pady=20)
            return
        
        for ped in sorted(todos_los_pedidos, key=lambda x: x.fecha_ped, reverse=True):
            articulos = ", ".join([f"{art.nombre} ({cant})" for art, cant in ped.articulos_cant.items()])
            tree.insert('', 'end', text=ped.fecha_ped.strftime("%Y-%m-%d"), 
                       values=(ped.direccion, articulos, ped.estado))
        
        tree.column('#0', width=120, anchor='w')
        tree.column('Cliente', width=150, anchor='w')
        tree.column('Artículos', width=250, anchor='w')
        tree.column('Estado', width=100, anchor='w')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Frame para cambiar estado
        estado_frame = ttk.Frame(win)
        estado_frame.pack(pady=10)
        
        ttk.Label(estado_frame, text="Nuevo estado:").pack(side='left')
        
        estado_var = tk.StringVar(value=self.estados[0])
        estado_combobox = ttk.Combobox(estado_frame, textvariable=estado_var, 
                                     values=self.estados, state='readonly')
        estado_combobox.pack(side='left', padx=5)
        
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)
        
        def confirmar():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Por favor seleccione un pedido")
                return
                
            nuevo_estado = estado_var.get()
            item = tree.item(selected_item)
            
            # Encontrar el pedido seleccionado
            fecha = item['text']
            cliente_dir = item['values'][0]
            
            if self.callbacks['cambiar_estado'](cliente_dir, fecha, nuevo_estado):
                messagebox.showinfo("Éxito", f"Estado del pedido cambiado a {nuevo_estado}")
                win.destroy()
            else:
                messagebox.showerror("Error", "No se pudo encontrar el pedido seleccionado")
        
        ttk.Button(btn_frame, text="Cambiar Estado", command=confirmar, 
                  style='Director.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=win.destroy).pack(side='left', padx=5)

    def _crear_frame_articulos(self, parent):
        art_frame = ttk.Frame(parent)
        art_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(art_frame, height=150)
        scrollbar = ttk.Scrollbar(art_frame, orient="vertical", command=canvas.yview)
        scrollable_art_frame = ttk.Frame(canvas)
        
        scrollable_art_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_art_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Variables para los artículos seleccionados
        self.articulos_seleccionados = {art: tk.IntVar(value=0) for art in self.articulos}
        
        for i, art in enumerate(self.articulos):
            ttk.Label(scrollable_art_frame, text=f"• {art.nombre} - ${art.precio}").grid(row=i, column=0, sticky='w')
            ttk.Spinbox(scrollable_art_frame, from_=0, to=10, 
                       textvariable=self.articulos_seleccionados[art], width=5).grid(row=i, column=1, padx=5)
        
        return art_frame
