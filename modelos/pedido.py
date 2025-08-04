class Pedido:
    def __init__(self, direccion, fecha_ped, articulos_cant, estado="Pendiente"):
        self.direccion = direccion
        self.fecha_ped = fecha_ped
        self.articulos_cant = articulos_cant  # {Articulo: cantidad}
        self.estado = estado
        self.precio_total = self._calcular_precio_total()

    def _calcular_precio_total(self):
        """Calcula el precio total del pedido basado en los artículos y cantidades"""
        total = 0
        for articulo, cantidad in self.articulos_cant.items():
            total += articulo.precio * cantidad
        return total

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado