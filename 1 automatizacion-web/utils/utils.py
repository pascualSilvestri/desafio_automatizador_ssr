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
    Maneja errores de subida sin interrumpir el proceso.
    
    Returns:
        Dict con información sobre el proceso de exportación y subida
    """
    import datetime
    
    try:
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
        print(f"Archivo exportado: {ruta_completa}")
        
        # Intentar subir a la API
        try:
            print(f"\n🔄 Intentando subir {nombre_archivo} a la API...")
            resultado_subida = upload_files(ruta_completa)
            
            if resultado_subida and 'link' in resultado_subida:
                print(f"✅ Archivo subido exitosamente: {resultado_subida['link']}")
                return {
                    'archivo_local': ruta_completa,
                    'subida_exitosa': True,
                    'link_api': resultado_subida['link'],
                    'error': None,
                    'proveedor': proveedor
                }
            else:
                print(f"⚠️ Subida completada pero sin enlace válido")
                return {
                    'archivo_local': ruta_completa,
                    'subida_exitosa': False,
                    'link_api': None,
                    'error': 'Sin enlace válido en respuesta',
                    'proveedor': proveedor
                }
                
        except Exception as e:
            print(f"❌ Error al subir {nombre_archivo} a la API: {str(e)}")
            print(f"📁 Archivo guardado localmente en: {ruta_completa}")
            return {
                'archivo_local': ruta_completa,
                'subida_exitosa': False,
                'link_api': None,
                'error': str(e),
                'proveedor': proveedor
            }
        
    except Exception as e:
        print(f"❌ Error al exportar archivo para {proveedor}: {str(e)}")
        return {
            'archivo_local': None,
            'subida_exitosa': False,
            'link_api': None,
            'error': str(e),
            'proveedor': proveedor
        }
