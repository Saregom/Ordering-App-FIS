from tkinter import ttk, messagebox
from controladores.controlador import Controlador
from interfaz.vistas.inventario_vista import InventarioVista
from interfaz.vistas.login_vista import LoginVista
from interfaz.vistas.menu_vista import MenuVista
from interfaz.vistas.pedidos_vista import PedidosVista

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Pedidos")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")
        
        # Centrar ventana principal
        self.root.update_idletasks()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        width = 600
        height = 450
        self.centerX = (self.screen_width // 2) - (width // 2)
        self.centerY = (self.screen_height // 2) - (height // 2 + 100)
        self.root.geometry(f"{width}x{height}+{self.centerX}+{self.centerY}")

        self.controlador = Controlador()
        self.current_user = None
        self.articulos_disponibles = self.controlador.get_articulos()  # Lista de artículos disponibles
        
        # Estilo general
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar colores y fuentes
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Error.TLabel', foreground='red')
        
        # Mostrar pantalla de login inicial
        self.show_login()

    def show_login(self):
        """Muestra la pantalla de login"""
        self.clear_window()
        self.style.configure('Login.TButton', foreground='white', background='#4a6baf')
        self.login_vista = LoginVista(self.root, self._mostrar_error_login, self._autenticar)
        self.login_vista.mostrar()

    def _mostrar_error_login(self, mensaje):
        """Muestra un mensaje de error en la pantalla de login"""
        if hasattr(self, 'login_vista'):
            self.login_vista.error_label.config(text=mensaje)

    def _autenticar(self, username, password):
        """Autentica al usuario"""
        self.current_user = self.controlador.autenticar_usuario(username, password)
        if self.current_user:
            self.show_main_menu()
            return True
        else:
            self._mostrar_error_login("Usuario o contraseña incorrectos")
            return False

    def show_main_menu(self):
        """Muestra el menú principal según el tipo de usuario"""
        self.clear_window()
        self.style.configure('Client.TButton', foreground='white', background='#5cb85c')
        self.style.configure('Provider.TButton', foreground='white', background='#f0ad4e')
        self.style.configure('Director.TButton', foreground='white', background='#d9534f')
        
        callbacks = {
            'ver_historial_pedidos': self.ver_historial_pedidos,
            'realizar_pedido': self.realizar_pedido,
            'actualizar_stock': self.actualizar_stock_menu,
            'consultar_stock_planta': self.consultar_stock_planta,
            'consultar_inventario': self.consultar_inventario,
            'cambiar_estado_pedidos': self.cambiar_estado_pedidos,
            'logout': self.logout
        }
        
        menu_vista = MenuVista(self.root, self.current_user, callbacks)
        menu_vista.mostrar()

    def logout(self):
        """Cierra la sesión del usuario"""
        self.current_user = None
        self.show_login()

    def clear_window(self):
        """Limpia la ventana principal"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def ver_historial_pedidos(self):
        """Muestra el historial de pedidos del cliente"""
        pedidos_vista = PedidosVista(self.root, self.articulos_disponibles, {})
        pedidos_vista.mostrar_historial(self.current_user.pedidos)

    def realizar_pedido(self):
        """Permite al cliente realizar un nuevo pedido"""
        pedidos_vista = PedidosVista(self.root, self.articulos_disponibles, {
            'realizar_pedido': self._realizar_pedido_callback
        })
        pedidos_vista.mostrar_realizar_pedido()
        
    def _realizar_pedido_callback(self, direccion, articulos):
        """Callback para realizar un pedido"""
        resultado = self.controlador.realizar_pedido(self.current_user, direccion, articulos)
        if resultado["success"]:
            messagebox.showinfo("Éxito", resultado["message"])
        else:
            messagebox.showerror("Error", resultado["message"])

    def actualizar_stock_menu(self):
        """Menú para actualizar el stock (proveedor)"""
        inventario_vista = InventarioVista(self.root, self.articulos_disponibles, {
            'actualizar_stock': self._actualizar_stock_callback,
            'agregar_producto': self._agregar_producto_callback,
            'get_articulos_planta': self._get_articulos_planta_callback,
            'get_stock_planta': self._get_stock_planta_callback,
            'agregar_desde_planta': self._agregar_desde_planta_callback
        })
        inventario_vista.mostrar_actualizar_stock()

    def _actualizar_stock_callback(self, producto_nombre, cantidad):
        """Callback para actualizar el stock de un producto"""
        art = next((a for a in self.articulos_disponibles if a.nombre == producto_nombre), None)
        if art:
            self.controlador.actualizar_stock(art.codigo, cantidad)
            messagebox.showinfo("Éxito", f"Se agregaron {cantidad} unidades de {producto_nombre}")
            self.articulos_disponibles = self.controlador.get_articulos()
            return True
        return False

    def _agregar_producto_callback(self, codigo, nombre, precio, cantidad):
        """Callback para agregar un nuevo producto"""
        if self.controlador.agregar_articulo(codigo, nombre, precio, cantidad):
            self.articulos_disponibles = self.controlador.get_articulos()
            messagebox.showinfo("Éxito", f"Producto {nombre} agregado al inventario")
            return True
        return False

    def consultar_stock_planta(self):
        """Consultar el stock de la planta manufacturera (proveedor)"""
        from interfaz.vistas.inventario_vista import InventarioVista
        
        stock_data = self.controlador.get_stock_planta()
        inventario_vista = InventarioVista(self.root, [], {})
        inventario_vista.mostrar_stock_planta(stock_data)

    def _get_articulos_planta_callback(self):
        """Callback para obtener artículos de la planta"""
        return self.controlador.get_articulos_planta()
    
    def _get_stock_planta_callback(self):
        """Callback para obtener stock de la planta"""
        return self.controlador.get_stock_planta()
    
    def _agregar_desde_planta_callback(self, codigo, cantidad, precio_venta):
        """Callback para agregar artículo desde la planta"""
        resultado = self.controlador.agregar_articulo_desde_planta(codigo, cantidad, precio_venta)
        if resultado['success']:
            self.articulos_disponibles = self.controlador.get_articulos()
        return resultado

    def cambiar_estado_pedidos(self):
        """Permite al director cambiar el estado de los pedidos"""
        pedidos_vista = PedidosVista(self.root, self.articulos_disponibles, {
            'cambiar_estado': self._cambiar_estado_callback
        })
        todos_los_pedidos = self.controlador.get_todos_pedidos()
        pedidos_vista.mostrar_cambiar_estado(todos_los_pedidos)

    def _cambiar_estado_callback(self, cliente_dir, fecha, nuevo_estado):
        """Callback para cambiar el estado de un pedido"""
        return self.controlador.cambiar_estado_pedido(cliente_dir, fecha, nuevo_estado)

    def consultar_inventario(self):
        """Muestra el inventario actual (director)"""
        inventario_vista = InventarioVista(self.root, self.articulos_disponibles, {})
        inventario_vista.mostrar_inventario()

