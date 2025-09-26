# Parte 2: Sistema ETL para Análisis de Repuestos

Este proyecto implementa un sistema ETL (Extract, Transform, Load) que se conecta a una base de datos MySQL para generar reportes en formato CSV sobre repuestos de proveedores.

## 🗂️ Estructura del Proyecto

```
parte2/
├── setup/                      # Configuración de Docker
│   ├── docker-compose.yml      # Orquestación de contenedores
│   └── mysql-init/             # Scripts de inicialización de BD
│       ├── init-db.sh          # Script de inicialización
│       └── repuestosDB_init.sql # Datos iniciales de la BD
├── config/                     # Configuración de la aplicación
│   └── config.py              # Variables de configuración
├── respuestas/                # Archivos CSV generados
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias Python
├── run.bat                    # Script de ejecución para Windows
└── script_elt_corregido.py    # Script principal del ETL
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Docker y Docker Compose
- Git (opcional)

### 1. Configurar el entorno

**Opción A: Entorno virtual (recomendado)**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

**Opción B: Usar el script run.bat (Windows)**

```bash
# El script automáticamente crea y activa el entorno virtual
run.bat
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos

#### Iniciar contenedores Docker:

```bash
cd setup
docker-compose up -d
```

Este comando:

- ✅ Descarga y configura MySQL 8.0
- ✅ Crea la base de datos `repuestosDB`
- ✅ Ejecuta el script de inicialización con datos de ejemplo
- ✅ Configura el puerto 3306 para conexiones

#### Verificar que los contenedores estén funcionando:

```bash
docker ps
```

### 4. Variables de entorno

```env
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=
```

## 🔧 Uso del Sistema

### Ejecución con run.bat (Windows - Recomendado)

```bash
run.bat
```

Este script automáticamente:

1. Crea/activa un entorno virtual
2. Instala las dependencias
3. Ejecuta el script ETL
4. Guarda los resultados en la carpeta `respuestas`

### Ejecución manual

```bash
# Con entorno virtual activado
python script_elt.py

# Especificar carpeta de salida personalizada
python script_elt.py mi_carpeta_salida
```

## 📊 Reportes Generados

El sistema genera 5 archivos CSV con los siguientes análisis:

### 1. `repuestos_sin_actualizar.csv`

- **Descripción**: Repuestos del proveedor "Autofix" sin actualizar en el último mes
- **Columnas**: id, codigo, descripcion, marca, precio, proveedor, fecha_ultima_actualizacion

### 2. `incremento_marcas.csv`

- **Descripción**: Propuesta de incremento del 15% para marcas específicas
- **Marcas incluidas**: ELEXA, BERU, SH, MASTERFILT, RN
- **Columnas**: id, codigo, descripcion, marca, precio_actual, precio_propuesto, proveedor, incremento

### 3. `recargo_proveedores.csv`

- **Descripción**: Propuesta de recargo del 30% para artículos específicos
- **Proveedores**: AutoRepuestos Express, Automax
- **Criterio**: Precio entre $50,000 y $100,000
- **Columnas**: id, codigo, descripcion, marca, precio_actual, precio_propuesto, proveedor, recargo

### 4. `resumen_proveedores.csv`

- **Descripción**: Resumen estadístico por proveedor
- **Columnas**: id, proveedor, cantidad_repuestos, repuestos_sin_descripcion, precio_mas_alto, codigo_mas_caro, descripcion_mas_caro

### 5. `promedio_marcas.csv`

- **Descripción**: Promedio de precios por marca
- **Columnas**: marca, precio_promedio, cantidad_repuestos
