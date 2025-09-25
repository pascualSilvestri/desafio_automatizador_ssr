#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para automatizar la calculadora de Windows
"""
import time
import subprocess
import pyautogui
import logging
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def abrir_calculadora():
    """
    Abre la aplicación de calculadora de Windows
    """
    logger.info("Abriendo la calculadora...")
    try:
        # Abrir la calculadora de Windows
        subprocess.Popen("calc.exe")
        
        # Esperar a que la calculadora se abra completamente
        time.sleep(2)
        return True
    except Exception as e:
        logger.error(f"Error al abrir la calculadora: {e}")
        return False

def realizar_operacion_matematica():
    """
    Realiza una operación matemática simple en la calculadora
    """
    logger.info("Realizando operación matemática: 25 × 4 = 100")
    
    try:
        # Secuencia de teclas para hacer un cálculo: 25 × 4 = 100
        pyautogui.press('2')
        time.sleep(0.5)
        pyautogui.press('5')
        time.sleep(0.5)
        
        # Multiplicar
        pyautogui.press('*')  # Símbolo de multiplicación
        time.sleep(0.5)
        
        pyautogui.press('4')
        time.sleep(0.5)
        
        # Presionar igual para obtener el resultado
        pyautogui.press('=')
        time.sleep(1)
        
        # Tomar captura de pantalla del resultado (opcional)
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculo_resultado.png")
        pyautogui.screenshot(screenshot_path)
        logger.info(f"Captura de pantalla guardada en: {screenshot_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error durante la operación matemática: {e}")
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
    logger.info("Iniciando automatización de la calculadora de Windows")
    
    # Dar un momento para cambiar a la ventana correcta si es necesario
    logger.info("Esperando 3 segundos antes de comenzar...")
    time.sleep(3)
    
    # 1. Abrir la calculadora
    if not abrir_calculadora():
        return
    
    # 2. Realizar operación matemática
    if not realizar_operacion_matematica():
        return
    
    # 3. Esperar para que se pueda ver el resultado
    logger.info("Mostrando resultado durante 3 segundos...")
    time.sleep(3)
    
    # 4. Cerrar la calculadora
    cerrar_calculadora()
    
    logger.info("Automatización completada con éxito")

if __name__ == "__main__":
    main()