#!/usr/bin/env python3
"""
Script universal para construir ejecutables en Windows y Linux
Detecta automáticamente el sistema operativo y ajusta la configuración
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def get_system_info():
    """Detecta información del sistema operativo"""
    system = platform.system().lower()
    architecture = platform.machine()
    
    return {
        'system': system,
        'architecture': architecture,
        'is_windows': system == 'windows',
        'is_linux': system == 'linux',
        'is_mac': system == 'darwin'
    }

def clean_build_dirs():
    """Limpia los directorios de construcción anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado directorio: {dir_name}")
    
    # Limpiar archivos .pyc recursivamente
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                os.remove(file_path)

def build_executable_universal():
    """Construye el ejecutable detectando automáticamente el SO"""
    system_info = get_system_info()
    
    print("🚀 Iniciando construcción del ejecutable...")
    print(f"🖥️  Sistema detectado: {system_info['system'].title()} ({system_info['architecture']})")
    
    # Limpiar directorios previos
    clean_build_dirs()
    
    # Configurar nombre del ejecutable según el SO
    if system_info['is_windows']:
        exe_name = "SistemaGestionPedidos.exe"
        separator = ";"
        print("🪟 Compilando para Windows...")
    else:
        exe_name = "SistemaGestionPedidos"
        separator = ":"
        print("🐧 Compilando para Linux/Unix...")
    
    # Comando base para PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Crear un solo archivo ejecutable
        '--windowed',  # Sin ventana de consola (para GUI)
        f'--name={exe_name.replace(".exe", "")}',  # PyInstaller añade .exe automáticamente en Windows
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=.',
        f'--add-data=bd{separator}bd',
        f'--add-data=controladores{separator}controladores', 
        f'--add-data=interfaz{separator}interfaz',
        f'--add-data=modelos{separator}modelos',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        'main.py'
    ]
    
    try:
        print("📦 Ejecutando PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Construcción completada exitosamente!")
        
        # Detectar el nombre real del ejecutable creado
        dist_path = Path('./dist')
        exe_files = list(dist_path.glob('*'))
        if exe_files:
            exe_path = exe_files[0]  # Tomar el primer archivo encontrado
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📄 Ejecutable creado: {exe_path.absolute()}")
            print(f"📏 Tamaño del archivo: {size_mb:.2f} MB")
            print(f"🔥 Para ejecutar: {exe_path.absolute()}")
        
        return True, exe_path if exe_files else None
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la construcción:")
        print(f"Código de salida: {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False, None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False, None

def create_run_script(exe_path):
    """Crea un script para ejecutar la aplicación según el SO"""
    system_info = get_system_info()
    
    if system_info['is_windows']:
        # Script .bat para Windows
        script_content = f'''@echo off
REM Script para ejecutar el Sistema de Gestión de Pedidos en Windows

set "SCRIPT_DIR=%~dp0"
set "EXECUTABLE=%SCRIPT_DIR%dist\\{exe_path.name}"

if exist "%EXECUTABLE%" (
    echo 🚀 Iniciando Sistema de Gestión de Pedidos...
    "%EXECUTABLE%"
) else (
    echo ❌ Error: No se encontró el ejecutable en %EXECUTABLE%
    echo Por favor, ejecuta primero el script de construcción.
    pause
)
'''
        script_name = 'ejecutar_app.bat'
    else:
        # Script .sh para Linux/Unix
        script_content = f'''#!/bin/bash
# Script para ejecutar el Sistema de Gestión de Pedidos

SCRIPT_DIR="$( cd "$( dirname "${{BASH_SOURCE[0]}}" )" &> /dev/null && pwd )"
EXECUTABLE="$SCRIPT_DIR/dist/{exe_path.name}"

if [ -f "$EXECUTABLE" ]; then
    echo "🚀 Iniciando Sistema de Gestión de Pedidos..."
    "$EXECUTABLE"
else
    echo "❌ Error: No se encontró el ejecutable en $EXECUTABLE"
    echo "Por favor, ejecuta primero el script de construcción."
fi
'''
        script_name = 'ejecutar_app.sh'
    
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Hacer el script ejecutable en sistemas Unix
    if not system_info['is_windows']:
        os.chmod(script_name, 0o755)
    
    print(f"📜 Script de ejecución creado: {script_name}")

def show_instructions():
    """Muestra instrucciones específicas del sistema"""
    system_info = get_system_info()
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES DE USO")
    print("=" * 60)
    
    if system_info['is_windows']:
        print("🪟 WINDOWS:")
        print("  • Ejecutar: .\\dist\\SistemaGestionPedidos.exe")
        print("  • O usar: ejecutar_app.bat")
        print("  • Doble clic también funciona")
    else:
        print("🐧 LINUX/UNIX:")
        print("  • Ejecutar: ./dist/SistemaGestionPedidos")
        print("  • O usar: ./ejecutar_app.sh")
        print("  • Dar permisos si es necesario: chmod +x dist/SistemaGestionPedidos")
    
    print("\n👥 USUARIOS DE PRUEBA:")
    print("  • Cliente: usuario='cliente', contraseña='cliente'")
    print("  • Proveedor: usuario='proveedor', contraseña='proveedor'")
    print("  • Director: usuario='director', contraseña='director'")

def main():
    """Función principal"""
    system_info = get_system_info()
    
    print("=" * 60)
    print("🏗️  CONSTRUCTOR UNIVERSAL DE EJECUTABLE")
    print("   Sistema de Gestión de Pedidos")
    print("=" * 60)
    print(f"🖥️  Detectado: {system_info['system'].title()} {system_info['architecture']}")
    
    # Verificar si tkinter está disponible
    try:
        import tkinter
        print("✅ tkinter disponible")
    except ImportError:
        print("❌ tkinter no disponible")
        if system_info['is_windows']:
            print("   Instala Python desde python.org (incluye tkinter)")
        else:
            print("   Ejecuta: sudo apt install python3-tk")
        return False
    
    success, exe_path = build_executable_universal()
    
    if success and exe_path:
        create_run_script(exe_path)
        print("\n" + "=" * 60)
        print("✅ ¡CONSTRUCCIÓN COMPLETADA!")
        print("=" * 60)
        show_instructions()
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ ¡ERROR EN LA CONSTRUCCIÓN!")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
