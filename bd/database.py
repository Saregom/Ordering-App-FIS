from datetime import datetime
from typing import Dict, List, Optional, Any, Type
from modelos.usuario import Cliente, Proveedor, DirectorVentas
from modelos.articulo import Articulo
from modelos.pedido import Pedido
from modelos.planta import PlantaManufactura

import sys

class DatabaseManager:
    def __init__(self):
        self._articulos: List[Articulo] = []
        self._usuarios: List[Any] = []  # Cliente, Proveedor, DirectorVentas
        self._pedidos: List[Pedido] = []
        self._planta: PlantaManufactura = PlantaManufactura()
        self._initialize_data()
    
    def _initialize_data(self):
        """Inicializa la base de datos con datos de prueba"""
        # Inicializar artículos
        self._articulos = [
            Articulo("1122", "Laptop Acer B2C3", "Computadora personal", 1, 50),
            Articulo("3344", "Mouse Razer", "Mouse ergonómico", 2, 100)
        ]
        
        # Inicializar usuarios
        self._usuarios = [
            Cliente("33", "Jhojan Smirnoff", 5000000, 10000000, 10),
            DirectorVentas("11", "Saregom Gomez"),
            Proveedor("55", "Buñuelo Buitrago")
        ]
        
        # Inicializar pedidos
        pedido_inicial = Pedido("Cra 53C N12BA - 47", datetime(2025, 7, 22), 
                              {self._articulos[0]: 2, self._articulos[1]: 2})
        self._pedidos = [pedido_inicial]
        
        # Configurar planta
        self._planta.cant_art_pm = {"1122": 200, "3344": 400}
        self._planta.stock_min_pm = {"1122": 10, "3344": 20}
        
        # Asociar pedido inicial al cliente
        cliente = self.find_usuario_by_id("33")

        if isinstance(cliente, Cliente):
            cliente.realizar_pedido(pedido_inicial)
    
    # Operaciones con Artículos
    def get_articulos(self) -> List[Articulo]:
        """Retorna la lista de todos los artículos"""
        return self._articulos  # Retornamos la lista original para mantener las referencias
    
    def add_articulo(self, articulo: Articulo) -> None:
        """Agrega un nuevo artículo"""
        self._articulos.append(articulo)
    
    def find_articulo_by_codigo(self, codigo: str) -> Optional[Articulo]:
        """Busca un artículo por su código"""
        return next((art for art in self._articulos if art.codigo == codigo), None)
    
    def update_articulo(self, codigo: str, cantidad: Optional[int] = None, **kwargs) -> bool:
        """Actualiza un artículo existente"""
        art = self.find_articulo_by_codigo(codigo)
        if art:
            if cantidad is not None:
                art.cantidad = art.cantidad + cantidad if hasattr(art, 'cantidad') else cantidad
            for key, value in kwargs.items():
                if hasattr(art, key):
                    setattr(art, key, value)
            return True
        return False
    
    def delete_articulo(self, codigo: str) -> None:
        """Elimina un artículo por su código"""
        self._articulos = [art for art in self._articulos if art.codigo != codigo]
    
    # Operaciones con Usuarios
    def get_usuarios(self) -> List[Any]:
        """Retorna la lista de todos los usuarios"""
        return self._usuarios  # Retornamos la lista original para mantener las referencias
    
    def add_usuario(self, usuario: Any) -> None:
        """Agrega un nuevo usuario"""
        self._usuarios.append(usuario)
    
    def find_usuario_by_id(self, id_usuario: str) -> Optional[Any]:
        """Busca un usuario por su ID"""
        for user in self._usuarios:
            if user.cod_us == id_usuario:
                return user
        return None
    
    # Operaciones con Pedidos
    def get_pedidos(self) -> List[Pedido]:
        """Retorna la lista de todos los pedidos"""
        return self._pedidos  # Retornamos la lista original para mantener las referencias
    
    def add_pedido(self, pedido: Pedido) -> None:
        """Agrega un nuevo pedido"""
        self._pedidos.append(pedido)
    
    def find_pedido_by_direccion(self, direccion: str) -> Optional[Pedido]:
        """Busca un pedido por su dirección"""
        return next((ped for ped in self._pedidos if ped.direccion == direccion), None)
    
    def update_pedido_estado(self, direccion: str, fecha: datetime, nuevo_estado: str) -> bool:
        """Actualiza el estado de un pedido"""
        pedido = next((ped for ped in self._pedidos 
                      if ped.direccion == direccion and ped.fecha_ped.date() == fecha.date()), None)
        if pedido:
            pedido.estado = nuevo_estado
            return True
        return False
    
    # Operaciones con Planta
    def get_planta(self) -> PlantaManufactura:
        """Retorna la instancia de la planta de manufactura"""
        return self._planta
    
    def update_planta_config(self, cant_art: Dict[str, int] = None, 
                           stock_min: Dict[str, int] = None) -> None:
        """Actualiza la configuración de la planta"""
        if cant_art:
            self._planta.cant_art_pm.update(cant_art)
        if stock_min:
            self._planta.stock_min_pm.update(stock_min)
