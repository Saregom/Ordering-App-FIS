import tkinter as tk
from tkinter import ttk
from modelos.usuario import Cliente, DirectorVentas, Proveedor

class MenuVista:
    def __init__(self, root, usuario, callbacks):
        self.root = root
        self.usuario = usuario
        self.callbacks = callbacks
    
    def mostrar(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20, fill='x')
        ttk.Label(header_frame, text=f"Bienvenido/a {self.usuario.nombre_us}", 
                 style='Header.TLabel').pack()
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        # Configurar botones según tipo de usuario
        if isinstance(self.usuario, Cliente):
            ttk.Button(btn_frame, text="Ver Historial de Pedidos", 
                      command=self.callbacks['ver_historial_pedidos'],
                      style='Client.TButton', width=25).pack(pady=10)
            ttk.Button(btn_frame, text="Realizar Pedido", 
                      command=self.callbacks['realizar_pedido'],
                      style='Client.TButton', width=25).pack(pady=10)
        elif isinstance(self.usuario, Proveedor):
            ttk.Button(btn_frame, text="Actualizar Stock", 
                      command=self.callbacks['actualizar_stock'],
                      style='Provider.TButton', width=25).pack(pady=10)
            ttk.Button(btn_frame, text="Consultar Stock Planta", 
                      command=self.callbacks['consultar_stock_planta'],
                      style='Provider.TButton', width=25).pack(pady=10)
            ttk.Button(btn_frame, text="Consultar Stock Tienda", 
                      command=self.callbacks['consultar_stock_tienda'],
                      style='Provider.TButton', width=25).pack(pady=10)
        elif isinstance(self.usuario, DirectorVentas):
            ttk.Button(btn_frame, text="Consultar Inventario", 
                      command=self.callbacks['consultar_inventario'],
                      style='Director.TButton', width=25).pack(pady=10)
            ttk.Button(btn_frame, text="Cambiar Estado de Pedidos", 
                      command=self.callbacks['cambiar_estado_pedidos'],
                      style='Director.TButton', width=25).pack(pady=10)
        
        # Botón de logout
        ttk.Button(btn_frame, text="Cerrar Sesión", 
                  command=self.callbacks['logout']).pack(pady=20)
