# Información Técnica - Compilación del Ejecutable

## 📋 Detalles de la Compilación

### Ejecutable Generado
- **Nombre:** `SistemaGestionPedidos`
- **Ubicación:** `./dist/SistemaGestionPedidos`
- **Tamaño:** ~26.44 MB
- **Tipo:** Ejecutable Linux x86_64
- **Herramienta:** PyInstaller

### Configuración Utilizada
```bash
PyInstaller --onefile --windowed --name=SistemaGestionPedidos \
  --add-data=bd:bd \
  --add-data=controladores:controladores \
  --add-data=interfaz:interfaz \
  --add-data=modelos:modelos \
  --hidden-import=tkinter \
  --hidden-import=tkinter.ttk \
  --hidden-import=tkinter.messagebox \
  main.py
```

## 🔧 Dependencias Incluidas

### Bibliotecas Python:
- `tkinter` - Interfaz gráfica
- `tkinter.ttk` - Widgets temáticos
- `tkinter.messagebox` - Cuadros de diálogo
- `datetime` - Manejo de fechas
- `typing` - Anotaciones de tipos

### Módulos de la Aplicación:
- `bd/` - Gestión de base de datos en memoria
- `controladores/` - Lógica de negocio
- `interfaz/` - Vistas y GUI
- `modelos/` - Modelos de datos

## 🚀 Formas de Ejecutar

### 1. Ejecutable Directo
```bash
./dist/SistemaGestionPedidos
```

### 2. Script de Ejecución
```bash
./ejecutar_app.sh
```

### 3. Desde Cualquier Ubicación
```bash
/ruta/completa/al/proyecto/dist/SistemaGestionPedidos
```

## 🔄 Regenerar el Ejecutable

Si modificas el código fuente, regenera el ejecutable:

```bash
# Opción 1: Usar el script automático
python build_executable.py

# Opción 2: Usar PyInstaller directamente
pyinstaller --onefile --windowed --name=SistemaGestionPedidos \
  --add-data=bd:bd --add-data=controladores:controladores \
  --add-data=interfaz:interfaz --add-data=modelos:modelos \
  --hidden-import=tkinter --hidden-import=tkinter.ttk \
  --hidden-import=tkinter.messagebox main.py
```

## 📊 Estructura Interna del Ejecutable

```
SistemaGestionPedidos (ejecutable)
├── Intérprete Python embebido
├── Bibliotecas estándar de Python
├── tkinter y widgets GUI
├── Código fuente de la aplicación:
│   ├── bd/
│   ├── controladores/
│   ├── interfaz/
│   ├── modelos/
│   └── main.py
└── Archivos de configuración PyInstaller
```

## ⚡ Optimizaciones Aplicadas

### Configuración de PyInstaller:
- `--onefile`: Un solo archivo ejecutable
- `--windowed`: Sin ventana de consola (GUI pura)
- `--add-data`: Inclusión de módulos personalizados
- `--hidden-import`: Importaciones explícitas para tkinter

### Scripts de Automatización:
- `build_executable.py` - Constructor automático
- `ejecutar_app.sh` - Script de ejecución
- Limpieza automática de archivos temporales

## 🛠️ Resolución de Problemas

### Error: "No module named 'tkinter'"
**Solución:** Instalar python3-tk en el sistema
```bash
sudo apt install python3-tk
```

### Error: "Permission denied"
**Solución:** Dar permisos de ejecución
```bash
chmod +x ./dist/SistemaGestionPedidos
```

### Error: "Display not found"
**Solución:** Asegurar que hay un servidor X corriendo
```bash
echo $DISPLAY  # Debe mostrar algo como :0
```

## 📦 Distribución

Para distribuir el ejecutable:

1. **Comprimir:**
   ```bash
   tar -czf SistemaGestionPedidos.tar.gz dist/SistemaGestionPedidos README_EJECUTABLE.md
   ```

2. **Copiar a otro sistema:**
   ```bash
   scp SistemaGestionPedidos.tar.gz usuario@servidor:/ruta/destino/
   ```

3. **Descomprimir y ejecutar:**
   ```bash
   tar -xzf SistemaGestionPedidos.tar.gz
   chmod +x dist/SistemaGestionPedidos
   ./dist/SistemaGestionPedidos
   ```

## 🔍 Verificación del Ejecutable

```bash
# Verificar que es ejecutable
file ./dist/SistemaGestionPedidos
# Output esperado: ELF 64-bit LSB executable

# Verificar dependencias
ldd ./dist/SistemaGestionPedidos
# Debe mostrar las bibliotecas del sistema necesarias

# Verificar tamaño
ls -lh ./dist/SistemaGestionPedidos
# ~26.44 MB aproximadamente
```

## 📈 Rendimiento

- **Tiempo de inicio:** 2-4 segundos
- **Uso de memoria:** ~50-80 MB en ejecución
- **Tiempo de construcción:** ~30-60 segundos
- **Compatible con:** Ubuntu 20.04+, Debian 10+, CentOS 8+

---

**Nota:** Este ejecutable incluye todo lo necesario para funcionar independientemente, sin requerir Python instalado en el sistema de destino.
