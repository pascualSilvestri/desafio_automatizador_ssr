from __future__ import annotations
import os
import time
import random
from pathlib import Path
from typing import Any, Dict, Optional
from config.config import URL_API

import requests
from requests.exceptions import RequestException, Timeout, ReadTimeout, ConnectionError as ReqConnectionError

API_URL = URL_API

def upload_files(
    file_ruta: str | Path,
    max_retries: int = 3,
    retry_delay: float = 5.0,
    connect_timeout: float = 10.0,
    read_timeout: float = 180.0,
    verify_ssl: bool = True,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Sube un archivo .xlsx a la API (multipart/form-data, campo 'file') con reintentos
    y timeouts separados para conexión y lectura.

    Args:
        file_ruta: Ruta al archivo .xlsx a subir.
        max_retries: Reintentos ante fallos transitorios (timeouts/5xx/429).
        retry_delay: Delay base entre reintentos (se aplica backoff exponencial + jitter).
        connect_timeout: Timeout al establecer conexión (segundos).
        read_timeout: Timeout para leer la respuesta completa (segundos).
        verify_ssl: Verifica certificado SSL (deje True en prod).
        verbose: Imprime logs simples por intento.

    Returns:
        dict con la respuesta JSON {"link": "..."} en caso de éxito.

    Raises:
        FileNotFoundError, ValueError, RuntimeError, RequestException
    """
    path = Path(file_ruta)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {path!s}")
    if path.stat().st_size == 0:
        raise ValueError(f"El archivo está vacío: {path!s}")

    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    headers = {
        "Accept": "application/json",
        "User-Agent": "AutomatizacionWeb/1.0 (+selenium-pandas-ait-challenge)"
    }
    timeout_tuple = (connect_timeout, read_timeout)

    attempt = 0
    last_exc: Optional[Exception] = None

    while attempt <= max_retries:
        try:
            if verbose:
                print(f"[upload_files] Intento {attempt + 1}/{max_retries + 1} | timeout={timeout_tuple} | archivo={path.name}")

            with path.open("rb") as f:
                files = {"file": (path.name, f, mime_type)}
                resp = requests.post(
                    API_URL,
                    headers=headers,
                    files=files,
                    timeout=timeout_tuple,
                    verify=verify_ssl,
                )

            # Éxito
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except ValueError:
                    raise RuntimeError(f"200 OK pero la respuesta no es JSON. Texto: {resp.text[:500]}")
                if "link" not in data:
                    raise RuntimeError(f"200 OK pero falta 'link' en la respuesta: {data}")
                if verbose:
                    print(f"[upload_files] Subida OK: {data['link']}")
                return data

            # 400: validar mensaje
            if resp.status_code == 400:
                try:
                    err = resp.json()
                except ValueError:
                    err = {"detail": resp.text}
                msg = (err.get("message") or err.get("detail") or "").lower()
                if "missing required columns" in msg:
                    raise ValueError("Missing required columns: faltan columnas obligatorias (CODIGO, DESCRIPCION, MARCA, PRECIO).")
                raise RuntimeError(f"Error 400 de la API: {err}")

            # 5xx y 429 => reintentar
            if resp.status_code >= 500 or resp.status_code == 429:
                attempt += 1
                if attempt > max_retries:
                    raise RuntimeError(f"Error {resp.status_code} persistente. Última respuesta: {resp.text[:500]}")
                sleep_s = retry_delay * (2 ** (attempt - 1)) + random.uniform(0, 1.5)
                if verbose:
                    print(f"[upload_files] HTTP {resp.status_code}. Reintentando en {sleep_s:.1f}s...")
                time.sleep(sleep_s)
                continue

            # Otros 4xx: no vale reintento
            raise RuntimeError(f"Error de la API ({resp.status_code}): {resp.text[:500]}")

        except (ReadTimeout, Timeout, ReqConnectionError) as e:
            # Reintento en fallos de red/timeout
            last_exc = e
            attempt += 1
            if attempt > max_retries:
                raise RequestException(f"Fallo de red persistente tras {max_retries} reintentos: {e}") from e
            sleep_s = retry_delay * (2 ** (attempt - 1)) + random.uniform(0, 1.5)
            if verbose:
                print(f"[upload_files] {type(e).__name__}: {e}. Reintento en {sleep_s:.1f}s...")
            time.sleep(sleep_s)

        except RequestException as e:
            # Otros errores de requests (no suele ayudar reintentar)
            raise

    # Falla inesperada
    if last_exc:
        raise RequestException(f"Fallo al subir el archivo: {last_exc}") from last_exc
    raise RuntimeError("Fallo desconocido al subir el archivo.")
