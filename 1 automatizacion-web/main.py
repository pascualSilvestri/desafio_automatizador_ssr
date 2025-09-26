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
    
    ## Ejecutar descarga de archivos
    download_all_files_single_session(clean_download_dir=True)
    
    ### Procesar Datos y exportar a Excel
    print("\n" + "="*60)
    print("INICIANDO PROCESAMIENTO DE DATOS")
    print("="*60 + "\n")
    
    # Lista para almacenar resultados
    resultados = []
    
    # Procesar y exportar los datos de cada proveedor
    print("🔄 Procesando datos de AutoFix...")
    respuesta_autofix = procesar_datos_autofix()
    resultados.append(('AutoFix', respuesta_autofix))
   
    print("\n🔄 Procesando datos de Express...")
    respuesta_express = procesar_datos_express()
    resultados.append(('Express', respuesta_express))

    print("\n🔄 Procesando datos de RepCar...")
    respuesta_repcar = procesar_datos_repcar()
    resultados.append(('RepCar', respuesta_repcar))
    
    # Mostrar resumen final detallado
    print("\n" + "="*60)
    print("RESUMEN FINAL DE PROCESAMIENTO")
    print("="*60)
    
    archivos_exitosos = 0
    archivos_fallidos = 0
    links_api = []
    errores = []
    
    for proveedor, resultado in resultados:
        if resultado:
            if resultado.get('subida_exitosa', False):
                print(f"✅ {proveedor}: Procesado y subido exitosamente")
                if resultado.get('link_api'):
                    print(f"   🔗 Link: {resultado['link_api']}")
                    links_api.append((proveedor, resultado['link_api']))
                archivos_exitosos += 1
            else:
                print(f"⚠️ {proveedor}: Procesado pero falló la subida")
                if resultado.get('archivo_local'):
                    print(f"   📁 Archivo local: {resultado['archivo_local']}")
                if resultado.get('error'):
                    print(f"   ❌ Error: {resultado['error']}")
                    errores.append((proveedor, resultado['error']))
                archivos_fallidos += 1
        else:
            print(f"❌ {proveedor}: Error en el procesamiento")
            archivos_fallidos += 1
            errores.append((proveedor, "Error en procesamiento de datos"))
    
    # Resumen estadístico
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total de archivos: {len(resultados)}")
    print(f"   Exitosos: {archivos_exitosos}")
    print(f"   Fallidos: {archivos_fallidos}")
    
    if links_api:
        print(f"\n🔗 ENLACES DE LA API ({len(links_api)}):")
        for proveedor, link in links_api:
            print(f"   {proveedor}: {link}")
    
    if errores:
        print(f"\n⚠️ ERRORES ENCONTRADOS ({len(errores)}):")
        for proveedor, error in errores:
            print(f"   {proveedor}: {error}")
    
    print("\n" + "="*60)
    print("PROCESO COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()