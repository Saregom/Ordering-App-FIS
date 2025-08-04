# Sistema de Gestión de Pedidos - Ejecutable

## 📋 Descripción
Sistema completo de gestión de pedidos con interfaz gráfica desarrollado en Python usando Tkinter. Permite gestionar inventarios, realizar pedidos y administrar el sistema según el tipo de usuario.

## 🚀 Ejecución Rápida

### Opción 1: Ejecutable Directo
```bash
./dist/SistemaGestionPedidos
```

### Opción 2: Script de Ejecución
```bash
./ejecutar_app.sh
```

## 👥 Usuarios del Sistema

El sistema tiene tres tipos de usuarios predefinidos:

### 🟢 Cliente
- **Usuario:** `cliente`
- **Contraseña:** `cliente`
- **Funciones:**
  - Ver historial de pedidos
  - Realizar nuevos pedidos

### 🟡 Proveedor  
- **Usuario:** `proveedor`
- **Contraseña:** `proveedor`
- **Funciones:**
  - Actualizar stock desde planta manufacturera
  - Consultar stock de planta
  - Consultar stock de tienda

### 🔴 Director de Ventas
- **Usuario:** `director`
- **Contraseña:** `director`
- **Funciones:**
  - Consultar inventario completo
  - Cambiar estado de pedidos

## 📦 Estructura del Sistema

```
SistemaGestionPedidos/
├── dist/
│   └── SistemaGestionPedidos    # ← Ejecutable principal
├── bd/                          # Gestión de base de datos
├── controladores/               # Lógica de negocio  
├── interfaz/                    # Interfaz gráfica
├── modelos/                     # Modelos de datos
├── main.py                      # Punto de entrada
├── build_executable.py          # Constructor del ejecutable
└── ejecutar_app.sh             # Script de ejecución
```

## 🔧 Funcionalidades

### Para Clientes:
- ✅ Realizar pedidos con múltiples artículos
- ✅ Ver historial de pedidos realizados
- ✅ Cálculo automático de totales
- ✅ Validación de stock disponible

### Para Proveedores:
- ✅ Gestionar stock desde planta manufacturera
- ✅ Agregar nuevos artículos al inventario
- ✅ Consultar estados de stock (crítico, bajo, suficiente)
- ✅ Transferir artículos de planta a tienda

### Para Directores:
- ✅ Ver inventario completo con detalles
- ✅ Cambiar estados de pedidos
- ✅ Monitoreo general del sistema

## 📊 Datos Incluidos

El sistema viene con datos de demostración:
- **Artículos:** Laptop Acer, Mouse Razer, Teclado Logitech, Monitor Dell, Impresora HP
- **Usuarios:** Un cliente, un proveedor, un director de ventas
- **Pedido inicial:** Ejemplo de pedido realizado

## ⚙️ Requisitos del Sistema

- **Sistema Operativo:** Linux (compatible con distribuciones principales)
- **Memoria RAM:** Mínimo 2GB recomendado
- **Espacio en disco:** ~10MB para el ejecutable
- **Dependencias:** Ninguna (todo incluido en el ejecutable)

## 🛠️ Regenerar el Ejecutable

Si necesitas modificar el código y regenerar el ejecutable:

1. **Instalar PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Ejecutar el constructor:**
   ```bash
   python build_executable.py
   ```

3. **El nuevo ejecutable estará en:**
   ```bash
   ./dist/SistemaGestionPedidos
   ```

## 🐛 Solución de Problemas

### El ejecutable no inicia:
- Verifica que el archivo tenga permisos de ejecución:
  ```bash
  chmod +x ./dist/SistemaGestionPedidos
  ```

### Error de dependencias:
- El ejecutable incluye todas las dependencias necesarias
- Si persisten errores, ejecuta en modo consola para ver detalles:
  ```bash
  ./dist/SistemaGestionPedidos --console
  ```

### Problemas de interfaz gráfica:
- Asegúrate de tener un entorno gráfico funcionando
- En servidores, usa X11 forwarding si es necesario

## 📝 Notas Técnicas

- **Tamaño del ejecutable:** ~26.44 MB
- **Tiempo de inicio:** 2-3 segundos aproximadamente
- **Base de datos:** En memoria (datos se reinician al cerrar)
- **Interfaz:** Tkinter con temas personalizados

## 🎯 Casos de Uso Ejemplo

1. **Cliente realiza pedido:**
   - Login como cliente → Realizar Pedido → Seleccionar artículos → Confirmar

2. **Proveedor actualiza stock:**
   - Login como proveedor → Actualizar Stock → Seleccionar artículo de planta → Definir cantidad y precio

3. **Director revisa inventario:**
   - Login como director → Consultar Inventario → Ver todos los artículos y stock

---

## 📞 Información del Proyecto

**Desarrollado con:**
- Python 3.12+
- Tkinter (GUI)
- PyInstaller (Ejecutable)

**Características:**
- ✅ Interfaz gráfica intuitiva
- ✅ Gestión completa de inventarios
- ✅ Sistema de usuarios con roles
- ✅ Validaciones de negocio
- ✅ Ejecutable autocontenido
