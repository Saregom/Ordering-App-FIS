#!/bin/bash
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
