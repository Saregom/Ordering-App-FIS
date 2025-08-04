class Pedido:
    def __init__(self, direccion, fecha_ped, articulos_cant, estado="Pendiente"):
        self.direccion = direccion
        self.fecha_ped = fecha_ped
        self.articulos_cant = articulos_cant  # {Articulo: cantidad}
        self.estado = estado

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado