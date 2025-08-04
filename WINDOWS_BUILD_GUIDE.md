# 🪟 Crear Ejecutable para Windows - Guía Paso a Paso

## 📋 Requisitos Previos

### En Windows:
1. **Python 3.8 o superior** - Descargar desde [python.org](https://www.python.org/downloads/)
2. **Git** (opcional) - Para clonar el repositorio
3. **Terminal/CMD** - Símbolo del sistema o PowerShell

## 🚀 Método 1: Compilación Directa en Windows

### Paso 1: Preparar el Proyecto
```cmd
# Opción A: Clonar desde Git
git clone https://github.com/Saregom/Ordering-App-FIS.git
cd Ordering-App-FIS

# Opción B: Copiar archivos manualmente
# Descargar y descomprimir el proyecto en una carpeta
```

### Paso 2: Instalar Dependencias
```cmd
# Instalar PyInstaller
pip install pyinstaller

# Verificar que tkinter esté disponible
python -c "import tkinter; print('tkinter OK')"
```

### Paso 3: Compilar el Ejecutable
```cmd
# Usar el script universal (recomendado)
python build_universal.py

# O usar PyInstaller directamente
pyinstaller --onefile --windowed --name=SistemaGestionPedidos ^
  --add-data="bd;bd" ^
  --add-data="controladores;controladores" ^
  --add-data="interfaz;interfaz" ^
  --add-data="modelos;modelos" ^
  --hidden-import=tkinter ^
  --hidden-import=tkinter.ttk ^
  --hidden-import=tkinter.messagebox ^
  main.py
```

### Paso 4: Ejecutar
```cmd
# Ejecutar directamente
dist\SistemaGestionPedidos.exe

# O usar el script generado
ejecutar_app.bat
```

## 🔄 Método 2: Usando GitHub Actions (Automatizado)

### Crear Workflow para Compilación Automática:

Crea el archivo `.github/workflows/build-windows.yml`:

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller
    
    - name: Build executable
      run: python build_universal.py
    
    - name: Upload executable
      uses: actions/upload-artifact@v3
      with:
        name: windows-executable
        path: dist/SistemaGestionPedidos.exe
    
    - name: Create release (optional)
      if: github.ref == 'refs/heads/main'
      uses: softprops/action-gh-release@v1
      with:
        tag_name: v1.0-windows
        name: Sistema Gestión Pedidos - Windows
        files: dist/SistemaGestionPedidos.exe
```

## 🛠️ Solución de Problemas Comunes

### Error: "No module named 'tkinter'"
```cmd
# tkinter debe venir incluido con Python
# Reinstalar Python desde python.org con todas las opciones marcadas
```

### Error: "pyinstaller not found"
```cmd
# Instalar PyInstaller
pip install pyinstaller

# Verificar instalación
pyinstaller --version
```

### Error: "Permission denied"
```cmd
# Ejecutar como administrador o cambiar permisos de la carpeta
# Clic derecho en CMD -> "Ejecutar como administrador"
```

### Ejecutable muy grande
```cmd
# Es normal, incluye Python completo y todas las dependencias
# Tamaño esperado: 30-40 MB en Windows
```

## 📊 Diferencias Linux vs Windows

| Aspecto | Linux | Windows |
|---------|-------|---------|
| Ejecutable | `SistemaGestionPedidos` | `SistemaGestionPedidos.exe` |
| Script | `ejecutar_app.sh` | `ejecutar_app.bat` |
| Separador | `:` | `;` |
| Tamaño | ~26 MB | ~35 MB |
| Permisos | `chmod +x` | No necesario |

## 🎯 Pasos Específicos para Windows

### 1. Descargar Python
- Ir a [python.org](https://www.python.org/downloads/)
- Descargar Python 3.12 (versión recomendada)
- **Importante:** Marcar "Add Python to PATH" durante la instalación

### 2. Verificar Instalación
```cmd
python --version
pip --version
```

### 3. Preparar Proyecto
```cmd
# Crear carpeta para el proyecto
mkdir C:\SistemaGestionPedidos
cd C:\SistemaGestionPedidos

# Copiar todos los archivos del proyecto aquí
```

### 4. Compilar
```cmd
# Instalar PyInstaller
pip install pyinstaller

# Compilar usando el script universal
python build_universal.py
```

### 5. Resultado Final
```
C:\SistemaGestionPedidos\
├── dist\
│   └── SistemaGestionPedidos.exe  ← EJECUTABLE WINDOWS
├── ejecutar_app.bat               ← Script de ejecución
└── ... (otros archivos del proyecto)
```

## 🚀 Distribución del Ejecutable Windows

### Para distribuir a otros usuarios Windows:
1. Copiar solo el archivo `SistemaGestionPedidos.exe`
2. No requiere Python instalado en el sistema destino
3. Compatible con Windows 10/11 (64-bit)

### Crear instalador (opcional):
```cmd
# Usar herramientas como NSIS o Inno Setup para crear un .msi
# O simplemente comprimir en .zip
```

---

## 💡 Consejos

- ✅ **Usar Python oficial** de python.org (no de Microsoft Store)
- ✅ **Ejecutar como administrador** si hay problemas de permisos
- ✅ **Antivirus:** Algunos antivirus pueden marcar el ejecutable como sospechoso (falso positivo)
- ✅ **Probar en máquina limpia** para verificar que funciona sin dependencias

¿Necesitas ayuda con algún paso específico?
