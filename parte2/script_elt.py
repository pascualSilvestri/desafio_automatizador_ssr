#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ETL para procesamiento de datos de repuestos de proveedores
"""
from __future__ import annotations
import os
import sys
import argparse
from datetime import datetime
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
from config.config import DATABASE_URL

def generar_csv_repuestos_sin_actualizar(connection, output_dir):
    """
    Genera un CSV con todos los repuestos del proveedor Autofix 
    cuyo precio no se haya actualizado en el último mes
    """
    print("\n1. Generando CSV de repuestos sin actualizar en el último mes...")
    
    # Consulta SQL para obtener los repuestos del proveedor Autofix sin actualización en el último mes
    query = """
    SELECT r.id, r.codigo, r.descripcion, m.nombre AS marca, ROUND(r.precio, 2) AS precio, p.nombre AS proveedor, 
           a.fecha AS fecha_ultima_actualizacion
    FROM Repuesto r
    JOIN Proveedor p ON r.proveedor_id = p.id
    JOIN Marca m ON r.marca_id = m.id
    LEFT JOIN Actualizacion a ON r.ultima_actualizacion_id = a.id
    WHERE p.nombre = 'Autofix' 
      AND (a.fecha IS NULL OR a.fecha < DATE_SUB(NOW(), INTERVAL 1 MONTH))
    ORDER BY a.fecha DESC
    """
    
    # Ejecutar consulta y cargar en DataFrame
    df = pd.read_sql(text(query), connection)
    
    # Guardar como CSV
    csv_path = os.path.join(output_dir, "repuestos_sin_actualizar.csv")
    df.to_csv(csv_path, index=False)
    
    print(f"  ✅ Se encontraron {len(df)} repuestos sin actualizar")
    print(f"  📄 Archivo guardado en: {csv_path}")
    return df

def generar_csv_incremento_marcas(connection, output_dir):
    """
    Genera un CSV que propone un nuevo precio con un incremento del 15% 
    de los repuestos de las marcas "ELEXA", "BERU", "SH", "MASTERFILT" y "RN"
    """
    print("\n2. Generando CSV con propuesta de incremento del 15% para marcas específicas...")
    
    # Consulta SQL para obtener los repuestos de las marcas especificadas
    query = """
    SELECT r.id, r.codigo, r.descripcion, m.nombre AS marca, 
           ROUND(r.precio, 2) AS precio_actual,
           ROUND(r.precio * 1.15, 2) AS precio_propuesto,
           p.nombre AS proveedor
    FROM Repuesto r
    JOIN Marca m ON r.marca_id = m.id
    JOIN Proveedor p ON r.proveedor_id = p.id
    WHERE m.nombre IN ('ELEXA', 'BERU', 'SH', 'MASTERFILT', 'RN')
    ORDER BY m.nombre, r.precio DESC
    """
    
    # Ejecutar consulta y cargar en DataFrame
    df = pd.read_sql(text(query), connection)
    
    # Calcular el incremento absoluto
    df['incremento'] = df['precio_propuesto'] - df['precio_actual']
    
    # Guardar como CSV
    csv_path = os.path.join(output_dir, "incremento_marcas.csv")
    df.to_csv(csv_path, index=False)
    
    print(f"  ✅ Se encontraron {len(df)} repuestos para aplicar incremento del 15%")
    print(f"  📄 Archivo guardado en: {csv_path}")
    return df

def generar_csv_recargo_proveedores(connection, output_dir):
    """
    Genera un CSV que propone aplicar un recargo del 30% en los artículos 
    de los proveedores AutoRepuestos Express y Automax cuyo precio sea 
    mayor a $50000 y menor a $100000
    """
    print("\n3. Generando CSV con propuesta de recargo del 30% para artículos seleccionados...")
    
    # Consulta SQL para obtener los artículos de proveedores específicos con precios en rango
    query = """
    SELECT r.id, r.codigo, r.descripcion, m.nombre AS marca, 
           ROUND(r.precio, 2) AS precio_actual,
           ROUND(r.precio * 1.30, 2) AS precio_propuesto,
           p.nombre AS proveedor
    FROM Repuesto r
    JOIN Proveedor p ON r.proveedor_id = p.id
    JOIN Marca m ON r.marca_id = m.id
    WHERE p.nombre IN ('AutoRepuestos Express', 'Automax')
      AND r.precio > 50000 
      AND r.precio < 100000
    ORDER BY p.nombre, r.precio DESC
    """
    
    # Ejecutar consulta y cargar en DataFrame
    df = pd.read_sql(text(query), connection)
    
    # Calcular el recargo absoluto
    df['recargo'] = df['precio_propuesto'] - df['precio_actual']
    
    # Guardar como CSV
    csv_path = os.path.join(output_dir, "recargo_proveedores.csv")
    df.to_csv(csv_path, index=False)
    
    print(f"  ✅ Se encontraron {len(df)} repuestos para aplicar recargo del 30%")
    print(f"  📄 Archivo guardado en: {csv_path}")
    return df

def generar_csv_resumen_proveedores(connection, output_dir):
    """
    Genera un CSV de resumen por proveedor con:
    - Cantidad de repuestos de cada proveedor
    - Cantidad de repuestos sin descripción
    - Repuesto más caro de cada proveedor
    - Promedio de precios por marca
    """
    print("\n4. Generando CSV de resumen por proveedor...")
    
    # 1. Cantidad de repuestos por proveedor
    query_cantidad = """
    SELECT p.id, p.nombre AS proveedor, COUNT(r.id) AS cantidad_repuestos
    FROM Proveedor p
    LEFT JOIN Repuesto r ON p.id = r.proveedor_id
    GROUP BY p.id, p.nombre
    ORDER BY cantidad_repuestos DESC
    """
    
    # 2. Cantidad de repuestos sin descripción
    query_sin_descripcion = """
    SELECT p.id, p.nombre AS proveedor, 
           COUNT(r.id) AS repuestos_sin_descripcion
    FROM Proveedor p
    LEFT JOIN Repuesto r ON p.id = r.proveedor_id AND (r.descripcion IS NULL OR r.descripcion = '')
    GROUP BY p.id, p.nombre
    ORDER BY repuestos_sin_descripcion DESC
    """
    
    # 3. Repuesto más caro por proveedor
    query_mas_caro = """
    SELECT p.id, p.nombre AS proveedor, 
           ROUND(MAX(r.precio), 2) AS precio_mas_alto,
           (
               SELECT r2.codigo 
               FROM Repuesto r2 
               WHERE r2.proveedor_id = p.id 
                 AND r2.precio = MAX(r.precio) 
               LIMIT 1
           ) AS codigo_mas_caro,
           (
               SELECT r3.descripcion 
               FROM Repuesto r3 
               WHERE r3.proveedor_id = p.id 
                 AND r3.precio = MAX(r.precio) 
               LIMIT 1
           ) AS descripcion_mas_caro
    FROM Proveedor p
    LEFT JOIN Repuesto r ON p.id = r.proveedor_id
    GROUP BY p.id, p.nombre
    """
    
    # 4. Promedio de precios por marca
    query_promedio_marca = """
    SELECT m.nombre AS marca, 
           ROUND(AVG(r.precio), 2) AS precio_promedio,
           COUNT(r.id) AS cantidad_repuestos
    FROM Marca m
    JOIN Repuesto r ON m.id = r.marca_id
    GROUP BY m.nombre
    ORDER BY precio_promedio DESC
    """
    
    # Ejecutar consultas y cargar en DataFrames
    df_cantidad = pd.read_sql(text(query_cantidad), connection)
    df_sin_descripcion = pd.read_sql(text(query_sin_descripcion), connection)
    df_mas_caro = pd.read_sql(text(query_mas_caro), connection)
    df_promedio_marca = pd.read_sql(text(query_promedio_marca), connection)
    
    # Combinar los DataFrames por proveedor
    df_resumen = pd.merge(df_cantidad, df_sin_descripcion, on=['id', 'proveedor'], how='left')
    df_resumen = pd.merge(df_resumen, df_mas_caro, on=['id', 'proveedor'], how='left')
    
    # Guardar resúmenes como CSV
    csv_path_resumen = os.path.join(output_dir, "resumen_proveedores.csv")
    df_resumen.to_csv(csv_path_resumen, index=False)
    
    csv_path_marcas = os.path.join(output_dir, "promedio_marcas.csv")
    df_promedio_marca.to_csv(csv_path_marcas, index=False)
    
    print(f"  ✅ Se generó resumen para {len(df_resumen)} proveedores")
    print(f"  ✅ Se generó promedio para {len(df_promedio_marca)} marcas")
    print(f"  📄 Archivos guardados en: {csv_path_resumen} y {csv_path_marcas}")
    
    return df_resumen, df_promedio_marca

# Código para imprimir las tablas disponibles en la base de datos
def mostrar_tablas_disponibles(connection):
    """
    Muestra las tablas disponibles en la base de datos
    """
    query = "SHOW TABLES;"
    print("Ejecutando query:", query)
    result = connection.execute(text(query))
    tablas = result.fetchall()
    print("Tablas en la base de datos:")
    print(tablas)
    return tablas

# Configurar el parser de argumentos para recibir la carpeta de salida
parser = argparse.ArgumentParser(description='ETL para procesamiento de datos de repuestos')
parser.add_argument('output_dir', type=str, nargs='?', default='output', 
                    help='Directorio donde se guardarán los archivos CSV resultantes')
args = parser.parse_args()

# Crear carpeta de salida si no existe
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)
print(f"Los archivos CSV se guardarán en: {os.path.abspath(output_dir)}")

# Inicializar conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,  # evita 'MySQL server has gone away'
    connect_args={"connect_timeout": 10},
)

# Comprobar conexión y ejecutar el proceso ETL
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión a la base de datos exitosa:", result.fetchone())
        
        # Mostrar las tablas disponibles para debugging
        # mostrar_tablas_disponibles(connection)
        
        # Ejecutar todas las consultas y generar archivos CSV
        generar_csv_repuestos_sin_actualizar(connection, output_dir)
        generar_csv_incremento_marcas(connection, output_dir)
        generar_csv_recargo_proveedores(connection, output_dir)
        generar_csv_resumen_proveedores(connection, output_dir)
        
        print("\n¡Proceso ETL completado con éxito!")
        
except Exception as e:
    print(f"Error al conectar a la base de datos: {str(e)}")
    sys.exit(1)