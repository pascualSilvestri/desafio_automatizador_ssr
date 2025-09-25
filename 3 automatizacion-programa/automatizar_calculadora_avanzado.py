#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script avanzado para automatizar la calculadora de Windows
Realiza múltiples operaciones y captura resultados
"""
import time
import subprocess
import pyautogui
import logging
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Crear carpeta para capturas de pantalla
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capturas")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def tomar_captura(nombre):
    """Toma una captura de pantalla y la guarda con un nombre específico"""
    timestamp = datetime.now().strftime("%H%M%S")
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{nombre}_{timestamp}.png")
    pyautogui.screenshot(screenshot_path)
    logger.info(f"Captura guardada: {screenshot_path}")
    return screenshot_path

def abrir_calculadora():
    """
    Abre la aplicación de calculadora de Windows
    Devuelve True si se pudo abrir correctamente
    """
    logger.info("Abriendo la calculadora...")
    try:
        # Abrir la calculadora de Windows
        subprocess.Popen("calc.exe")
        
        # Esperar a que la calculadora se abra completamente
        time.sleep(2)
        
        # Tomar captura de la calculadora abierta
        tomar_captura("calculadora_abierta")
        
        # Verificar que se haya abierto correctamente
        # (aquí se podría implementar una verificación visual con pyautogui.locateOnScreen)
        
        return True
    except Exception as e:
        logger.error(f"Error al abrir la calculadora: {e}")
        return False

def realizar_operacion(operacion):
    """
    Realiza una operación matemática en la calculadora
    operacion: diccionario con las teclas a presionar y un nombre descriptivo
    """
    logger.info(f"Realizando operación: {operacion['nombre']}")
    
    try:
        # Limpiar calculadora con la tecla C
        pyautogui.press('escape')
        time.sleep(0.5)
        
        # Presionar cada tecla de la secuencia
        for tecla in operacion['teclas']:
            pyautogui.press(str(tecla))
            time.sleep(0.3)
        
        # Tomar captura del resultado
        tomar_captura(f"resultado_{operacion['nombre']}")
        time.sleep(1)
        
        return True
    except Exception as e:
        logger.error(f"Error durante la operación {operacion['nombre']}: {e}")
        return False

def cerrar_calculadora():
    """
    Cierra la aplicación de calculadora
    """
    logger.info("Cerrando la calculadora...")
    try:
        # Presionar Alt+F4 para cerrar la aplicación
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1)
        return True
    except Exception as e:
        logger.error(f"Error al cerrar la calculadora: {e}")
        return False

def main():
    """
    Función principal que ejecuta la automatización completa
    """
    logger.info("Iniciando automatización avanzada de la calculadora de Windows")
    
    # Lista de operaciones a realizar
    operaciones = [
        {
            'nombre': 'suma',
            'teclas': ['5', '6', '+', '4', '4', '=']
        },
        {
            'nombre': 'multiplicacion',
            'teclas': ['2', '5', '*', '4', '=']
        },
        {
            'nombre': 'division',
            'teclas': ['1', '0', '0', '/', '4', '=']
        },
        {
            'nombre': 'raiz_cuadrada',
            'teclas': ['1', '6', 'r']  # Suponiendo que 'r' es la tecla para raíz cuadrada
        }
    ]
    
    # Dar un momento para cambiar a la ventana correcta si es necesario
    logger.info("Esperando 3 segundos antes de comenzar...")
    time.sleep(3)
    
    # 1. Abrir la calculadora
    if not abrir_calculadora():
        logger.error("No se pudo abrir la calculadora. Abortando.")
        return
    
    # 2. Realizar cada operación de la lista
    for operacion in operaciones:
        if not realizar_operacion(operacion):
            logger.warning(f"Problema al realizar la operación {operacion['nombre']}, continuando con la siguiente...")
        time.sleep(1)  # Pausa entre operaciones
    
    # 3. Esperar para que se pueda ver el último resultado
    logger.info("Mostrando último resultado durante 3 segundos...")
    time.sleep(3)
    
    # 4. Cerrar la calculadora
    cerrar_calculadora()
    
    logger.info("Automatización completada con éxito")
    logger.info(f"Las capturas de pantalla están disponibles en: {SCREENSHOT_DIR}")

if __name__ == "__main__":
    main()