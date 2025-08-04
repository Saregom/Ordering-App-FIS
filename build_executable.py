#!/usr/bin/env python3
"""
Script para construir el ejecutable de la aplicación de gestión de pedidos
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

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

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print("🚀 Iniciando construcción del ejecutable...")
    
    # Limpiar directorios previos
    clean_build_dirs()
    
    # Comando para construir con PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # Crear un solo archivo ejecutable
        '--windowed',  # Sin ventana de consola (para GUI)
        '--name=SistemaGestionPedidos',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=.',
        '--add-data=bd:bd',
        '--add-data=controladores:controladores', 
        '--add-data=interfaz:interfaz',
        '--add-data=modelos:modelos',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        'main.py'
    ]
    
    try:
        print("📦 Ejecutando PyInstaller...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Construcción completada exitosamente!")
        
        # Mostrar información del ejecutable creado
        exe_path = Path('./dist/SistemaGestionPedidos')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📄 Ejecutable creado: {exe_path.absolute()}")
            print(f"📏 Tamaño del archivo: {size_mb:.2f} MB")
            print(f"🔥 Para ejecutar: {exe_path.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la construcción:")
        print(f"Código de salida: {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_run_script():
    """Crea un script para ejecutar la aplicación fácilmente"""
    script_content = '''#!/bin/bash
# Script para ejecutar el Sistema de Gestión de Pedidos

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
EXECUTABLE="$SCRIPT_DIR/dist/SistemaGestionPedidos"

if [ -f "$EXECUTABLE" ]; then
    echo "🚀 Iniciando Sistema de Gestión de Pedidos..."
    "$EXECUTABLE"
else
    echo "❌ Error: No se encontró el ejecutable en $EXECUTABLE"
    echo "Por favor, ejecuta primero el script de construcción."
fi
'''
    
    with open('ejecutar_app.sh', 'w') as f:
        f.write(script_content)
    
    # Hacer el script ejecutable
    os.chmod('ejecutar_app.sh', 0o755)
    print("📜 Script de ejecución creado: ejecutar_app.sh")

def main():
    """Función principal"""
    print("=" * 60)
    print("🏗️  CONSTRUCTOR DE EJECUTABLE")
    print("   Sistema de Gestión de Pedidos")
    print("=" * 60)
    
    if build_executable():
        create_run_script()
        print("\n" + "=" * 60)
        print("✅ ¡CONSTRUCCIÓN COMPLETADA!")
        print("=" * 60)
        print("📁 El ejecutable se encuentra en: ./dist/SistemaGestionPedidos")
        print("🔧 También puedes usar: ./ejecutar_app.sh")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ ¡ERROR EN LA CONSTRUCCIÓN!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
