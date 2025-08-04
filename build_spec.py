#!/usr/bin/env python3
"""
Script para generar la especificación de PyInstaller para la aplicación de gestión de pedidos.
"""

import os
import sys

def create_spec_file():
    """Crea el archivo .spec para PyInstaller"""
    
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Obtener la ruta base del proyecto
base_path = Path(__file__).parent

a = Analysis(
    ['main.py'],
    pathex=[str(base_path)],
    binaries=[],
    datas=[
        # Incluir todos los módulos de la aplicación
        ('bd', 'bd'),
        ('controladores', 'controladores'),
        ('interfaz', 'interfaz'),
        ('modelos', 'modelos'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'datetime',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaGestionPedidos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambiar a True si necesitas ver mensajes de debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar un ícono aquí si tienes uno
)
'''
    
    with open('sistema_pedidos.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✅ Archivo .spec creado exitosamente")

if __name__ == "__main__":
    create_spec_file()
