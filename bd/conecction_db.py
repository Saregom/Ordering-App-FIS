from .database import DatabaseManager

# Instancia global de la base de datos
db = DatabaseManager()

# Funciones de acceso a datos que mantienen compatibilidad con el código existente
def get_articulos():
    return db.get_articulos()

def add_articulo(articulo):
    db.add_articulo(articulo)

def find_articulo_by_codigo(codigo):
    return db.find_articulo_by_codigo(codigo)

def update_articulo(codigo, cantidad=None, **kwargs):
    return db.update_articulo(codigo, cantidad, **kwargs)

def delete_articulo(codigo):
    db.delete_articulo(codigo)

def get_usuarios():
    return db.get_usuarios()

def add_usuario(usuario):
    db.add_usuario(usuario)

def find_usuario_by_id(id_usuario):
    return db.find_usuario_by_id(id_usuario)

def get_pedidos():
    return db.get_pedidos()

def add_pedido(pedido):
    db.add_pedido(pedido)

def find_pedido_by_direccion(direccion):
    return db.find_pedido_by_direccion(direccion)

# Exportar la planta para mantener compatibilidad
planta = db.get_planta()