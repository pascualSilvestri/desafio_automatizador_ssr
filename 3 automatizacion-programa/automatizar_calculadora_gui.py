#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script con interfaz gráfica para automatizar la calculadora de Windows
"""
import time
import subprocess
import threading
import pyautogui
import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox
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

class CalculadoraAutomatizadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatizador de Calculadora")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Variables
        self.cuenta_regresiva_activa = False
        self.automatizacion_ejecutandose = False
        
        # Crear y configurar widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame, 
            text="Automatización de la Calculadora de Windows",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Marco para operaciones
        operations_frame = ttk.LabelFrame(main_frame, text="Operaciones a realizar")
        operations_frame.pack(fill=tk.X, pady=10)
        
        # Checkboxes para operaciones
        self.op_suma = tk.BooleanVar(value=True)
        self.op_resta = tk.BooleanVar(value=True)
        self.op_multiplicacion = tk.BooleanVar(value=True)
        self.op_division = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(operations_frame, text="Suma (56 + 44 = 100)", variable=self.op_suma).grid(row=0, column=0, sticky="w", padx=20, pady=5)
        ttk.Checkbutton(operations_frame, text="Resta (75 - 25 = 50)", variable=self.op_resta).grid(row=1, column=0, sticky="w", padx=20, pady=5)
        ttk.Checkbutton(operations_frame, text="Multiplicación (25 × 4 = 100)", variable=self.op_multiplicacion).grid(row=0, column=1, sticky="w", padx=20, pady=5)
        ttk.Checkbutton(operations_frame, text="División (100 ÷ 4 = 25)", variable=self.op_division).grid(row=1, column=1, sticky="w", padx=20, pady=5)
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones")
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(options_frame, text="Tiempo entre operaciones (segundos):").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        self.tiempo_operaciones = ttk.Spinbox(options_frame, from_=0.5, to=5.0, increment=0.5, width=5)
        self.tiempo_operaciones.set(1.0)
        self.tiempo_operaciones.grid(row=0, column=1, sticky="w", pady=10)
        
        # Frame para acciones
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=20)
        
        # Botón de inicio
        self.btn_iniciar = ttk.Button(
            actions_frame, 
            text="Iniciar Automatización", 
            command=self.iniciar_cuenta_regresiva,
            style="Accent.TButton"
        )
        self.btn_iniciar.pack(pady=10)
        
        # Etiqueta de estado
        self.lbl_estado = ttk.Label(
            actions_frame, 
            text="Estado: Listo para iniciar",
            font=("Arial", 10)
        )
        self.lbl_estado.pack(pady=5)
        
        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(
            actions_frame, 
            orient="horizontal", 
            length=450, 
            mode="determinate"
        )
        self.barra_progreso.pack(pady=10)
        
        # Configurar estilo para botones
        style = ttk.Style()
        if "Accent.TButton" not in style.theme_names():
            style.configure("Accent.TButton", font=("Arial", 11, "bold"))
    
    def iniciar_cuenta_regresiva(self):
        """Inicia la cuenta regresiva antes de comenzar la automatización"""
        if self.cuenta_regresiva_activa or self.automatizacion_ejecutandose:
            return
        
        self.cuenta_regresiva_activa = True
        self.btn_iniciar.configure(state="disabled")
        
        # Verificar que al menos una operación esté seleccionada
        if not any([self.op_suma.get(), self.op_resta.get(), self.op_multiplicacion.get(), self.op_division.get()]):
            messagebox.showerror("Error", "Seleccione al menos una operación")
            self.cuenta_regresiva_activa = False
            self.btn_iniciar.configure(state="normal")
            return
        
        # Iniciar cuenta regresiva en un hilo separado
        threading.Thread(target=self._cuenta_regresiva, daemon=True).start()
    
    def _cuenta_regresiva(self):
        """Realiza la cuenta regresiva de 5 segundos"""
        for i in range(5, 0, -1):
            if not self.cuenta_regresiva_activa:
                break
            self.lbl_estado.configure(text=f"Comenzando en {i} segundos... Prepare la ventana")
            time.sleep(1)
        
        self.cuenta_regresiva_activa = False
        
        if self.root.winfo_exists():  # Verificar que la ventana siga abierta
            # Iniciar la automatización
            self.iniciar_automatizacion()
    
    def iniciar_automatizacion(self):
        """Inicia el proceso de automatización en un hilo separado"""
        self.automatizacion_ejecutandose = True
        self.lbl_estado.configure(text="¡Automatización en curso! No toque el mouse ni el teclado.")
        
        # Iniciar automatización en un hilo separado
        threading.Thread(target=self._ejecutar_automatizacion, daemon=True).start()
    
    def _ejecutar_automatizacion(self):
        """Ejecuta la automatización completa"""
        try:
            # Preparar lista de operaciones seleccionadas
            operaciones = []
            
            if self.op_suma.get():
                operaciones.append({
                    'nombre': 'suma',
                    'teclas': ['5', '6', '+', '4', '4', '=']
                })
            
            if self.op_resta.get():
                operaciones.append({
                    'nombre': 'resta',
                    'teclas': ['7', '5', '-', '2', '5', '=']
                })
            
            if self.op_multiplicacion.get():
                operaciones.append({
                    'nombre': 'multiplicacion',
                    'teclas': ['2', '5', '*', '4', '=']
                })
            
            if self.op_division.get():
                operaciones.append({
                    'nombre': 'division',
                    'teclas': ['1', '0', '0', '/', '4', '=']
                })
            
            # Obtener tiempo entre operaciones
            try:
                tiempo_espera = float(self.tiempo_operaciones.get())
            except ValueError:
                tiempo_espera = 1.0
            
            # 1. Abrir calculadora
            self.actualizar_progreso("Abriendo calculadora...", 10)
            if not self.abrir_calculadora():
                self.actualizar_progreso("Error al abrir calculadora", 0)
                return
            
            # 2. Realizar operaciones
            total_ops = len(operaciones)
            for i, operacion in enumerate(operaciones):
                progreso = 10 + int((i / total_ops) * 80)  # 10% - 90%
                self.actualizar_progreso(f"Realizando operación: {operacion['nombre']}", progreso)
                
                if not self.realizar_operacion(operacion, tiempo_espera):
                    self.actualizar_progreso(f"Error en operación {operacion['nombre']}", progreso)
                    # Continuar con las demás operaciones
            
            # 3. Esperar un momento con el último resultado
            self.actualizar_progreso("Completado. Cerrando calculadora...", 90)
            time.sleep(2)
            
            # 4. Cerrar calculadora
            self.cerrar_calculadora()
            
            # Completado
            self.actualizar_progreso("Automatización completada con éxito", 100)
            
            # Mostrar mensaje de éxito
            if self.root.winfo_exists():
                messagebox.showinfo(
                    "Éxito", 
                    f"Automatización completada con éxito.\n"
                    f"Las capturas de pantalla se guardaron en:\n{SCREENSHOT_DIR}"
                )
        
        except Exception as e:
            logger.error(f"Error durante la automatización: {e}")
            self.actualizar_progreso(f"Error: {str(e)}", 0)
            
            if self.root.winfo_exists():
                messagebox.showerror("Error", f"Ocurrió un error durante la automatización:\n{str(e)}")
        
        finally:
            # Restablecer estado
            self.automatizacion_ejecutandose = False
            if self.root.winfo_exists():
                self.btn_iniciar.configure(state="normal")
    
    def actualizar_progreso(self, mensaje, valor):
        """Actualiza la barra de progreso y el mensaje de estado"""
        if self.root.winfo_exists():
            self.lbl_estado.configure(text=f"Estado: {mensaje}")
            self.barra_progreso["value"] = valor
            self.root.update_idletasks()
    
    def abrir_calculadora(self):
        """Abre la calculadora de Windows"""
        logger.info("Abriendo calculadora...")
        try:
            # Abrir calculadora
            subprocess.Popen("calc.exe")
            time.sleep(2)
            
            # Tomar captura
            self.tomar_captura("calculadora_abierta")
            
            return True
        except Exception as e:
            logger.error(f"Error al abrir calculadora: {e}")
            return False
    
    def realizar_operacion(self, operacion, tiempo_espera):
        """Realiza una operación matemática en la calculadora"""
        logger.info(f"Realizando operación: {operacion['nombre']}")
        
        try:
            # Limpiar calculadora
            pyautogui.press('escape')
            time.sleep(tiempo_espera / 2)
            
            # Presionar cada tecla
            for tecla in operacion['teclas']:
                pyautogui.press(str(tecla))
                time.sleep(tiempo_espera / 2)
            
            # Tomar captura del resultado
            self.tomar_captura(f"resultado_{operacion['nombre']}")
            time.sleep(tiempo_espera)
            
            return True
        except Exception as e:
            logger.error(f"Error en operación {operacion['nombre']}: {e}")
            return False
    
    def cerrar_calculadora(self):
        """Cierra la calculadora"""
        logger.info("Cerrando calculadora...")
        try:
            pyautogui.hotkey('alt', 'f4')
            return True
        except Exception as e:
            logger.error(f"Error al cerrar calculadora: {e}")
            return False
    
    def tomar_captura(self, nombre):
        """Toma una captura de pantalla"""
        timestamp = datetime.now().strftime("%H%M%S")
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{nombre}_{timestamp}.png")
        pyautogui.screenshot(screenshot_path)
        logger.info(f"Captura guardada: {screenshot_path}")
        return screenshot_path

def main():
    # Crear ventana principal
    root = tk.Tk()
    app = CalculadoraAutomatizadorApp(root)
    
    # Iniciar bucle de eventos
    root.mainloop()

if __name__ == "__main__":
    main()