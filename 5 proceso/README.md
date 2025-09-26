### Proceso

#### Contexto

**Problema:** Proveedores envían listas de precios por email, obligando a chequeos manuales repetitivos del inbox, con flujos en ClickUp y Discord que generan demoras, ineficiencias y falta de trazabilidad.

**Objetivo:** Automatizar con N8N para eliminar chequeos manuales, reducir tareas repetitivas y asegurar trazabilidad vía logs y notificaciones. Incluye ramificaciones condicionales para validaciones, errores y reintentos, reflejando actualizaciones recientes en el workflow para mayor robustez.

#### Flujo Actual (Manual)

Proceso manual ineficiente con chequeos constantes:

1. **Recepción por Email:** Equipo chequea inbox varias veces al día; verifica y procesa listas nuevas.

2. **Creación en ClickUp:** Crea tarjeta en "Nueva Lista" con adjunto, cliente y proveedor.

3. **Revisión y Limpieza:** Encargado chequea ClickUp, limpia archivo y prepara para subida.

4. **Subida a Boxer:** Sube archivo limpio y cierra tarea en ClickUp.

5. **Comunicación en Discord:** Notificaciones manuales sobre avances.

#### Propuesta de Automatización (Reflejando Modificaciones en N8N)

Para automatizar este flujo, se propone un workflow en N8N que inicia con un trigger automático de email y ramifica según validaciones, incorporando modificaciones recientes como condiciones adicionales para manejar éxitos y fallos, reintentos en errores de red, y registros detallados. Aquí una descripción detallada de los puntos de automatización, basada en el diagrama y el workflow exportado:

- **Recepción de la Lista por Email:** Automatizar con un nodo "Email Trigger (IMAP)" en N8N para monitorear el inbox automáticamente cada pocos minutos, aplicando filtros por asunto o remitente. Seguido de un nodo "Code in JavaScript" para verificar el formato del adjunto. Justificación: Elimina chequeos manuales, reduce demoras y asegura detección inmediata; si no es válido, ramifica a notificación manual.

- **Creación de Tarea en ClickUp:** Integrar un nodo "ClickUp" con acción "Create Task" tras verificación exitosa, incluyendo datos del proveedor, cliente y adjunto. Justificación: Elimina intervención humana en la creación, asegura consistencia y trazabilidad automática.

- **Revisión, Procesamiento y Subida a Boxer:** Reemplazar chequeos manuales con un nodo "HTTP Request (GET)" para conectar al backend, procesar y subir el archivo a Boxer. Incluye un nodo "If" para ramificar según el resultado (éxito o fallo). Justificación: Minimiza tareas repetitivas del encargado de limpieza; en caso de éxito, actualiza la tarea en ClickUp automáticamente; en fallo (ej. errores 4xx/5xx), aplica reintentos con backoff y, si persiste, deriva a manual.

- **Actualización de Tarea y Notificación:** Usar nodos "Update a task" en ClickUp para marcar como completada en éxito, o crear una nueva con etiqueta "INCIDENTIA" en fallo. Integrar "Send a message" para notificaciones en Discord, y "Append or Update row in sheet" para logs en Google Sheets con detalles del error. Justificación: Garantiza cierre automático y comunicación institucional sin intervención humana, con trazabilidad en Sheets para auditoría.

El workflow en N8N ahora incluye dos branches principales post-validación: uno para procesamiento exitoso (crear tarea, enviar mensaje, append a sheet) y otro para fallos (actualizar tarea de riesgo, enviar alerta, registrar error). Esto refleja modificaciones para mayor resiliencia, como condiciones "If" adicionales y manejo de reintentos, asegurando que el proceso sea más robusto ante variaciones en los emails o conexiones.
