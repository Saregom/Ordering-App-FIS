from datetime import datetime
from bd.conecction_db import (get_articulos, get_usuarios, get_pedidos, 
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
            print(f"Actualizando stock de {articulo.nombre} por {cantidad_solicitada} unidades")
            articulo_bd = find_articulo_by_codigo(articulo.codigo)
            print(f"Stock actual de {articulo_bd.nombre}: {articulo_bd.cantidad} - {cantidad_solicitada}")
            self.actualizar_stock(articulo.codigo, -cantidad_solicitada)
        
        return {"success": True, "message": "Pedido realizado exitosamente"}
    
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
