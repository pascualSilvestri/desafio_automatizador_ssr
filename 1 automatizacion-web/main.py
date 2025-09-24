import os
import pandas as pd
import math
# import zipfile  # Ya no se utiliza
from datetime import datetime
from controller.obtener_datos_controller import download_all_files_single_session
from controller.procesar_datos_controller import procesar_datos_autofix, procesar_datos_express, procesar_datos_repcar


def main():
    """
    Función principal que ejecuta la automatización para descargar archivos, 
    procesarlos y enviarlos a la API.
    """
    
    ### Ejecutar descarga de arcivos
    # download_all_files_single_session(clean_download_dir=True)
    
    
    ### Procesar Datos y exportar a Excel
    print("\n" + "="*60)
    print("INICIANDO PROCESAMIENTO DE DATOS")
    print("="*60 + "\n")
    
    # Procesar y exportar los datos de cada proveedor
    respuesta_autofix = procesar_datos_autofix()
    if respuesta_autofix:
        print(f"AutoFix: {respuesta_autofix}")
    else:
        print("AutoFix: No se pudo exportar")
   
    # respuesta_express = procesar_datos_express()
    # if respuesta_express:
    #     print(f"Express: {respuesta_express}")
    # else:
    #     print("Express: No se pudo exportar")

    # respuesta_repcar = procesar_datos_repcar()
    # if respuesta_repcar:
    #     print(f"RepCar: {respuesta_repcar}")
    # else:
    #     print("RepCar: No se pudo exportar")
        
    # # Mostrar resumen final
    # print("\n" + "="*60)
    # print("RESUMEN DE EXPORTACIÓN")
    # print("="*60)

   
    # print("="*60)
    # respuestas = [respuesta_autofix, respuesta_express, respuesta_repcar]


    # if respuestas:
    #     print(f"Archivos subidos: {respuestas}")
    # else:
    #     print("No se pudo subir el archivo.")

if __name__ == "__main__":
    main()