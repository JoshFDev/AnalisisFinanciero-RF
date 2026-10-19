#!/usr/bin/env python3
"""
Script para diagnosticar problemas de importación
"""
import sys
import os

print("Diagnóstico de importaciones...")
print(f"Directorio actual: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Verificar estructura de carpetas
print("\nEstructura de carpetas:")
for root, dirs, files in os.walk('.'):
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py'):
            print(f"{subindent}{file}")

# Probar importaciones
print("\n🔄 Probando importaciones...")
try:
    from analisis import graficas
    print("analisis.graficas importado correctamente")
except ImportError as e:
    print(f"Error importando analisis.graficas: {e}")

try:
    from analisis.graficas import generar_grafica_random_forest
    print("generar_grafica_random_forest importado correctamente")
except ImportError as e:
    print(f"Error importando generar_grafica_random_forest: {e}")

try:
    from scripts.prediccion_manual import predecir_manual
    print("✅ scripts.prediccion_manual importado correctamente")
except ImportError as e:
    print(f"Error importando scripts.prediccion_manual: {e}")

print("\nDiagnóstico completado")