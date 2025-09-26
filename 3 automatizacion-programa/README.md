# Parte 3: Automatización de la Calculadora

Este proyecto automatiza la calculadora de Windows usando PyAutoGUI para demostrar la automatización de aplicaciones de escritorio.

## 📋 Requisitos

- Python 3.8+
- PyAutoGUI
- Pillow (PIL)

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 💻 Uso

```bash
python automatizar_calculadora.py
```

## 🔄 Funcionamiento

El script realiza automáticamente:

1. ✅ Abre la calculadora de Windows
2. ✅ Realiza una operación matemática (25 × 4 = 100)
3. ✅ Toma una captura de pantalla del resultado
4. ✅ Cierra la calculadora

## ⚠️ Notas Importantes

- **No mover el mouse** ni usar el teclado durante la ejecución
- El script espera **3 segundos** antes de comenzar
- Las capturas se guardan en la carpeta `capturas/`
- Compatible con Windows (calc.exe)

## 🛠️ Dependencias

- `pyautogui`: Control de mouse y teclado
- `pillow`: Procesamiento de imágenes

---

**Desarrollado para el Desafío de Automatización SSR**
