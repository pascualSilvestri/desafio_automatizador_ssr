import os
import pandas as pd
from controller.fetch_data_controller import upload_files


columnas_requeridas = ['CODIGO', 'DESCRIPCION', 'MARCA', 'PRECIO']


def renombrar_columnas(df, viejas_columnas, nuevas_columnas):
    """
    Renombra las columnas de un DataFrame según un diccionario de mapeo.
    """
    df.rename(columns=nuevas_columnas, inplace=True)
    return df

def formatear_precio(df):
    """
    Formatea la columna PRECIO para usar punto como separador decimal y eliminar separadores de miles.
    Retorna el DataFrame con PRECIO como float.
    """
    if 'PRECIO' in df.columns:
        # Convertir a string para limpiar comas/puntos
        df['PRECIO'] = df['PRECIO'].astype(str)
        # Reemplazar comas y puntos de separadores de miles
        df['PRECIO'] = df['PRECIO'].str.replace(',', '').str.replace('.', '', regex=False)
        # Convertir a float
        df['PRECIO'] = pd.to_numeric(df['PRECIO'], errors='coerce') / 100  # Dividir por 100 para ajustar decimales
        # Reemplazar NaN con 0
        df['PRECIO'] = df['PRECIO'].fillna(0)
    return df

def filtrar_columnas(df):
    """
    Filtra el DataFrame para mantener solo las columnas requeridas.
    """
    df = df[columnas_requeridas]
    return df

def print_data(df):
    # Imprimir información básica
    print(f"Total de registros: {len(df)}")
    print("Primeras 5 filas:")
    print(df.head())

def export_data(df, proveedor, directorio="datos_procesados"):
    """
    Exporta el DataFrame a un archivo Excel con el nombre del proveedor y la fecha actual.
    
    Returns:
        Ruta del archivo exportado
    """
    import datetime
    
    # Obtener la fecha actual en formato YYYYMMDD
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
    
    # Crear el nombre de archivo
    nombre_archivo = f"{proveedor}_{fecha_actual}.xlsx"
    
    # Crear el directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Directorio creado: {directorio}")
    
    # Ruta completa del archivo
    ruta_completa = os.path.join(directorio, nombre_archivo)
    
    # Exportar a Excel
    df.to_excel(ruta_completa, index=False, engine='openpyxl')
    
    return upload_files(ruta_completa)
