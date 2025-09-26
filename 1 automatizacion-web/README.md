# Parte 1: Automatización Web

Este proyecto automatiza la descarga de archivos Excel desde sitios web de proveedores, procesa los datos y los sube a una API.

## 📁 Estructura del Proyecto

```
1 automatizacion-web/
├── config/               # Configuración de URLs y API
├── controller/           # Lógica de descarga, procesamiento y subida
├── utils/               # Utilidades para procesamiento de datos
├── data_sin_procesar/   # Archivos descargados originales
├── datos_procesados/    # Archivos Excel procesados para la API
├── main.py              # Script principal
└── requirements.txt     # Dependencias Python
```

## 🚀 Instalación

1. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   - Editar `config/config.py` con las URLs correctas
   - Configurar la URL de la API

## 💻 Uso

Ejecutar el script principal:

```bash
python main.py
```

## 🔄 Proceso Automatizado

El sistema realiza las siguientes tareas:

1. **Descarga archivos** de 3 proveedores usando Selenium
2. **Procesa los datos** para estandarizar columnas y formatos
3. **Sube los archivos** procesados a la API
4. **Genera reportes** de éxito/error para cada archivo

### Proveedores Configurados:

- **AutoFix**: Archivo Excel con datos de repuestos
- **Express**: Archivo Excel con listado de productos
- **RepCar**: Archivo CSV con información de piezas

## 📊 Archivos Generados

- **Archivos originales**: `data_sin_procesar/`
- **Archivos procesados**: `datos_procesados/`
- **Capturas de pantalla**: `data_sin_procesar/screenshots/`

## ⚙️ Características

- ✅ Manejo robusto de errores de subida
- ✅ Reintentos automáticos para fallos temporales
- ✅ División automática de archivos grandes
- ✅ Procesamiento de múltiples formatos (Excel, CSV)
- ✅ Generación de reportes detallados
- ✅ Capturas de pantalla para depuración

## 🛠️ Dependencias Principales

- `selenium`: Automatización web
- `pandas`: Procesamiento de datos
- `requests`: Comunicación con API
- `openpyxl`: Manejo de archivos Excel

## 📋 Requisitos del Sistema

- Python 3.8+
- ChromeDriver (se instala automáticamente)
- Conexión a internet estable

## 🔧 Configuración

Editar `config/config.py` para ajustar:

- URLs de los proveedores
- URL de la API
- Timeouts y reintentos
- Rutas de descarga

---

## Problemas al enviar los archivos al backend, el servidor respondia con status 500 errores del servidor.
