from datetime import datetime
from bd.conecction_db import (get_articulos, get_articulos_planta, get_usuarios, get_pedidos, 
                          add_articulo, add_pedido, find_usuario_by_id,
                          find_articulo_by_codigo, update_articulo, delete_articulo)
from modelos.pedido import Pedido
from modelos.articulo import Articulo
from modelos.usuario import Cliente, DirectorVentas, Proveedor

class Controlador:
    def __init__(self):
        self.articulos = get_articulos()
        self.usuarios = get_usuarios()
        self.pedidos = get_pedidos()
    
    def autenticar_usuario(self, username, password):
        if username == "cliente" and password == "cliente":
            return next((user for user in self.usuarios if isinstance(user, Cliente)), None)
        elif username == "proveedor" and password == "proveedor":
            return next((user for user in self.usuarios if isinstance(user, Proveedor)), None)
        elif username == "director" and password == "director":
            return next((user for user in self.usuarios if isinstance(user, DirectorVentas)), None)
        return None
    
    def get_articulos(self):
        return get_articulos()
    
    def get_articulos_planta(self):
        return get_articulos_planta()
    
    def actualizar_stock(self, codigo_articulo, cantidad):
        update_articulo(codigo_articulo, cantidad=cantidad)
        self.articulos = get_articulos()
        return True
    
    def agregar_articulo(self, codigo, nombre, precio, cantidad=0):
        try:
            nuevo_art = Articulo(codigo=codigo, nombre=nombre, descripcion="", precio=float(precio))
            add_articulo(nuevo_art)
            if cantidad > 0:
                self.actualizar_stock(codigo, cantidad)
            self.articulos = get_articulos()
            return True
        except ValueError:
            return False
    
    def realizar_pedido(self, usuario, direccion, articulos_cantidades):
        if not isinstance(usuario, Cliente):
            return {"success": False, "message": "Usuario no autorizado para realizar pedidos"}
        
        # Validar stock disponible para cada artículo
        articulos_actuales = self.get_articulos()
        for articulo, cantidad_solicitada in articulos_cantidades.items():
            # Buscar el artículo actual en la base de datos
            articulo_bd = find_articulo_by_codigo(articulo.codigo)
            if not articulo_bd:
                return {"success": False, "message": f"Artículo {articulo.nombre} no encontrado"}
            
            # Verificar si hay suficiente stock
            if articulo_bd.cantidad < cantidad_solicitada:
                return {"success": False, "message": f"Stock insuficiente para {articulo.nombre}. Stock disponible: {articulo_bd.cantidad}, solicitado: {cantidad_solicitada}"}
        
        # Si llegamos aquí, todos los artículos tienen stock suficiente
        pedido = Pedido(direccion, datetime.now(), articulos_cantidades)
        usuario.realizar_pedido(pedido)
        add_pedido(pedido)
        
        # Actualizar el stock de los artículos
        for articulo, cantidad_solicitada in articulos_cantidades.items():
            articulo_bd = find_articulo_by_codigo(articulo.codigo)
            self.actualizar_stock(articulo.codigo, -cantidad_solicitada)
        
        return {"success": True, "message": f"Pedido realizado exitosamente. Total: ${pedido.precio_total:.2f}"}
    
    def cambiar_estado_pedido(self, direccion, fecha, nuevo_estado):
        pedido = next((ped for ped in get_pedidos() 
                      if ped.direccion == direccion and 
                      ped.fecha_ped.strftime("%Y-%m-%d") == fecha), None)
        if pedido:
            pedido.estado = nuevo_estado
            return True
        return False
    
    def get_pedidos_usuario(self, usuario):
        return usuario.pedidos if hasattr(usuario, 'pedidos') else []
    
    def get_todos_pedidos(self):
        return get_pedidos()
    
    def get_stock_planta(self):
        """Retorna el stock actual y mínimo de la planta manufacturera con información de artículos"""
        from bd.conecction_db import db
        
        planta = db.get_planta()
        
        # Obtener información adicional de los artículos
        articulos_info = {}
        for articulo in self.get_articulos_planta():
            if articulo.codigo in planta.cant_art_pm or articulo.codigo in planta.stock_min_pm:
                articulos_info[articulo.codigo] = {
                    'nombre': articulo.nombre,
                    'precio': articulo.precio
                }
        
        return {
            'stock_actual': planta.cant_art_pm,
            'stock_minimo': planta.stock_min_pm,
            'articulos_info': articulos_info
        }
    
    def get_articulos_planta(self):
        """Retorna los artículos específicos de la planta manufacturera"""
        from bd.conecction_db import db
        return db.get_articulos_planta()
    
    def agregar_articulo_desde_planta(self, codigo_planta, cantidad_surtir, precio_venta):
        """Agrega un artículo del inventario de la planta al inventario principal"""
        try:
            from bd.conecction_db import db
            
            # Buscar el artículo en la planta
            articulos_planta = self.get_articulos_planta()
            articulo_planta = next((art for art in articulos_planta if art.codigo == codigo_planta), None)
            
            if not articulo_planta:
                return {"success": False, "message": "Artículo no encontrado en la planta"}
            
            # Verificar stock disponible en la planta
            planta = db.get_planta()
            stock_disponible = planta.cant_art_pm.get(codigo_planta, 0)
            
            if cantidad_surtir > stock_disponible:
                return {"success": False, "message": f"Solo hay {stock_disponible} unidades disponibles en la planta"}
            
            # Verificar si el artículo ya existe en el inventario principal
            articulo_existente = find_articulo_by_codigo(codigo_planta)
            
            if articulo_existente:
                # Actualizar stock del artículo existente
                self.actualizar_stock(codigo_planta, cantidad_surtir)
                # Actualizar precio si es diferente
                if precio_venta != articulo_existente.precio:
                    update_articulo(codigo_planta, precio=precio_venta)
                mensaje = f"Stock actualizado: {cantidad_surtir} unidades de {articulo_planta.nombre}"
            else:
                # Crear nuevo artículo en el inventario principal
                nuevo_articulo = Articulo(
                    codigo=articulo_planta.codigo,
                    nombre=articulo_planta.nombre,
                    descripcion=articulo_planta.descripcion,
                    precio=precio_venta,
                    cantidad=cantidad_surtir
                )
                add_articulo(nuevo_articulo)
                self.articulos = get_articulos()
                mensaje = f"Artículo agregado: {cantidad_surtir} unidades de {articulo_planta.nombre}"
            
            # Reducir el stock en la planta
            planta.cant_art_pm[codigo_planta] = stock_disponible - cantidad_surtir
            
            return {"success": True, "message": mensaje}
                
        except Exception as e:
            return {"success": False, "message": f"Error al procesar el artículo: {str(e)}"}
