import pandas as pd
import os
import numpy as np
from controller.fetch_data_controller import upload_files
from utils.utils import renombrar_columnas, formatear_precio, filtrar_columnas, export_data, print_data




pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
# Establecer opciones para evitar notación científica
pd.set_option('display.float_format', '{:.2f}'.format)


def procesar_datos_autofix():
    download_dir = "data_sin_procesar"
    file_path = os.path.join(download_dir, "autofix.xlsx")
    dfs = []
    viejas_columnas = ['CODIGO', 'DESCR', 'NROORI', 'PRECIO', 'DESCR2', 'CODPRO', 'ORIGEN',
       'CANPED', 'FOTO', 'COEF', 'CODRUB']
    nuevas_columnas = {'DESCR':'DESCRIPCION','DESCR2':'DESCRIPCION2'}
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return

    # Leer el archivo Excel
    xls = pd.read_excel(file_path, engine='openpyxl',sheet_name=None)
    
    for sheet_name, df in xls.items():
        
        # Renombrar columnas
        df = renombrar_columnas(df, viejas_columnas, nuevas_columnas)
        df = df.dropna(subset=['CODIGO'])
        # Agregar columna MARCA con el nombre de la hoja
        df['MARCA'] = sheet_name

        # Combinar DESCRIPCION y DESCRIPCION2
        df['CODIGO'] = df['CODIGO'].astype(str).str.strip().fillna('')
        df['PRECIO'] = df['PRECIO'].fillna('')
        df['DESCRIPCION'] = df['DESCRIPCION'].fillna('')
        df['DESCRIPCION2'] = df['DESCRIPCION2'].fillna('')
        df['DESCRIPCION'] = df['DESCRIPCION'] + ' ' + df['DESCRIPCION2']
        
        # Limpiar DESCRIPCION: quitar comas y truncar a 100 caracteres
        df['DESCRIPCION'] = df['DESCRIPCION'].str.replace(',', '').str[:100]
        
        # Formatear precios
        df = formatear_precio(df)
        
        # Filtrar columnas requeridas
        df = filtrar_columnas(df)
        
        # Agregar DataFrame procesado a la lista
        dfs.append(df)
        
    # Unificar todos los DataFrames
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
    else:
        print("No se encontraron datos válidos en las hojas.")
        return None
    # Aquí puedes agregar la lógica para procesar los datos según tus necesidades
    print("Datos de Auto Fix:")

    
    # Exportar datos a Excel
    respuesta = export_data(final_df, "autofix")
    return respuesta

def procesar_datos_express():
    download_dir = "data_sin_procesar"
    file_path = os.path.join(download_dir, "express.xlsx")

    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return

    # Leer el archivo Excel
    df = pd.read_excel(file_path, engine='openpyxl',skiprows=10)
    
    viejas_columnas = ['CODIGO PROVEEDOR', 'DESCRIPCION', 'PRECIO DE LISTA',
       'PRECIO OFERTA/OUTLET', 'CODIGO RUBRO', 'RUBRO', 'CODIGO MARCA',
       'MARCA', 'IVA', 'CODIGO BARRA']
    nuevas_columnas = {'CODIGO PROVEEDOR':'CODIGO', 'PRECIO DE LISTA':'PRECIO' }

    df = renombrar_columnas(df, viejas_columnas, nuevas_columnas)
    df = df.dropna(subset=['CODIGO'])
    # Formatear precios
    df = formatear_precio(df)

    df = filtrar_columnas(df)
    # Aquí puedes agregar la lógica para procesar los datos según tus necesidades
    print("Datos de Express:")

    
    # Exportar datos a Excel
    respuesta = export_data(df, "express")
    return respuesta

def procesar_datos_repcar():
    download_dir = "data_sin_procesar"
    file_path = os.path.join(download_dir, "repcar.csv")

    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe.")
        return

    # Leer el archivo CSV con punto y coma como separador
    try:
        # Intentamos con codificación utf-8 primero
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
    except Exception as e:
        print(f"Error al leer con utf-8, intentando con latin-1: {e}")
        try:
            # Si falla, intentamos con codificación latin-1
            df = pd.read_csv(file_path, sep=';', encoding='latin-1')
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            return
    viejas_columnas = ['Cod. Fabrica', 'Marca', 'Cod. Articulo', 'Descripcion', 'Rubro',
       'Importe', 'Iva 105', 'Imagen']
    nuevas_columnas = {'Cod. Articulo':'CODIGO', 'Importe':'PRECIO', 'Descripcion':'DESCRIPCION','Marca':'MARCA'}
    
    df = renombrar_columnas(df, viejas_columnas, nuevas_columnas)
    df = df.dropna(subset=['CODIGO'])
    df['DESCRIPCION'] = df['DESCRIPCION'].fillna('')
    df['Rubro'] = df['Rubro'].fillna('')
    df['DESCRIPCION'] = df['DESCRIPCION'] + ' ' + df['Rubro']
    df['DESCRIPCION'] = df['DESCRIPCION'].str[:100]
    
    # Formatear precios
    df = formatear_precio(df)
    
    df = filtrar_columnas(df)
    # Aquí puedes agregar la lógica para procesar los datos según tus necesidades
    
    print("Datos de RepCar:")
    
    # Exportar datos a Excel
    respuesta = export_data(df, "repcar")
    return respuesta
