# Automatización de la Calculadora de Windows

Este proyecto contiene scripts para automatizar la calculadora de Windows como demostración de automatización de aplicaciones de escritorio.

## Requisitos

- Python 3.6+
- PyAutoGUI
- Pillow (PIL)

## Instalación

```bash
pip install -r requirements.txt
```

## Scripts disponibles

### 1. automatizar_calculadora.py

Script básico que:

- Abre la calculadora de Windows
- Realiza una operación matemática simple (25 × 4 = 100)
- Toma una captura de pantalla del resultado
- Cierra la calculadora

Para ejecutar:

```bash
python automatizar_calculadora.py
```

### 2. automatizar_calculadora_avanzado.py

Script avanzado que:

- Abre la calculadora de Windows
- Realiza múltiples operaciones matemáticas (suma, multiplicación, división, raíz cuadrada)
- Toma capturas de pantalla después de cada operación
- Cierra la calculadora

Para ejecutar:

```bash
python automatizar_calculadora_avanzado.py
```

## Notas importantes

1. Al ejecutar los scripts, no mueva el ratón ni use el teclado, ya que esto podría interferir con la automatización.

2. Los scripts esperan 3 segundos antes de comenzar para permitirle cambiar a la ventana correcta si es necesario.

3. Las capturas de pantalla se guardan en la carpeta "capturas" dentro del directorio del proyecto.

4. Si la calculadora tiene un diseño diferente o se ejecuta en un sistema operativo distinto a Windows, es posible que los scripts necesiten ajustes.

## Solución de problemas

- Si la calculadora no se abre correctamente, asegúrese de que "calc.exe" es el comando correcto para abrir la calculadora en su sistema.

- Si las teclas no funcionan según lo esperado, es posible que necesite ajustar los nombres de las teclas según el diseño de su calculadora específica.

- Ajuste los tiempos de espera (time.sleep()) si la automatización va demasiado rápido o demasiado lenta para su sistema.
