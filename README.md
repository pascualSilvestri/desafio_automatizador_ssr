# AIT Solutions

## Desafío Técnico - Automation Engineer

¡Hola y bienvenido/a al desafío técnico para el puesto de Automation Engineer! Este desafío está diseñado para evaluar tus conocimientos y habilidades en Python, Selenium, SQL, Google Sheets entre otros, que son las herramientas que usamos en el día a día en la empresa, y tu capacidad para resolver problemas similares a los que tendrás si quedas seleccionado/a para el puesto. A continuación, encontrarás todos los pasos y requisitos de cada parte del desafío. Si tenés alguna duda respecto a las consignas del desafío, podés enviar un email a florencialopez@aitsolutions.com.ar con el asunto “Desafío técnico - AIT” y te responderemos en breve.

### Solución

Para completar el desafío, deberás hacer un fork de este repositorio de GitHub y subir tu solución.

- Organizá la solución en distintas carpetas, una por cada etapa del desafío:

1.  automatizacion-web
2.  etl
3.  automatizacion-programa
4.  listas-manuales
5.  proceso

👉 **NOTA**: Si se te complica resolver alguna consigna de forma completa o no llegas a terminar todo, te invitamos a enviar tu solución igualmente. Podés dejarnos un comentario indicando por qué no lo pudiste resolver, qué conocimientos creés que te hacen falta para poder hacerlo o si sabés cómo encarar la solución aunque no lo pudiste lograr. Esto nos ayudará a evaluar tu perfil de manera integral. Valoramos tu esfuerzo y honestidad :)

# Introducción

En [Boxer](https://www.instagram.com/boxergestion/?hl=es-la), nuestro sistema de gestión principal, tenemos muchos clientes que trabajan con artículos de diferentes proveedores. Estos proveedores disponen sus listas de precios para que se puedan obtener de distintas formas (vía API, descargando un archivo en su página web, a través de un programa instalable, enviando la lista por email de suscripción, entre otras). Nuestro equipo de listas se encarga de mantener actualizado el sistema de cada cliente con los artículos y precios que ofrecen sus proveedores.

## Parte 1: Automatización Web - Scrapping

Uno de los recursos que más utiliza nuestro equipo de listas para mantener actualizados los artículos y precios de cada sistema es la automatización y procesamiento de datos con Python y Selenium.

En esta parte del desafío, evaluaremos tu capacidad para trabajar con estas herramientas. Tu objetivo será automatizar la descarga y procesamiento de 3 listas de artículos de distintos proveedores, limpiar y transform los datos para que queden con el formato necesario para ingresarse al sistema.

### Requisitos

- **Python**: el código que desarrolles debe estar escrito en Python y debe poder ejecutarse de forma local.
- **Bibliotecas**: Es obligatorio el uso mínimo de Selenium y Pandas para la automatización, pero podés agregar cualquier otra biblioteca que consideres necesaria.
- **Solución**: Incluí todos los archivos de tu implementación en la carpeta "automatizacion-web" de la solución que subas.
  - Agregá un archivo requirements.txt con el listado de dependencias que se deben instalar para ejecutar la implementación.
  - Es de mucha utilidad si incluís instrucciones claras para que podamos ejecutarla.
- **Criterios de Evaluación**: Valoramos que apliques buenas prácticas de programación y comentarios en el código, además de un buen manejo de errores y excepciones, y el registro de logs y/o mensajes que indiquen el estado y avance de la ejecución.

### Consigna

Implementar el código Python que realice las siguientes tareas:

1. Descarga de listas de precios de proveedores desde una página web.
2. Procesamiento y limpieza de las listas de precios.
3. Generación de archivos .xlsx con la información y formato necesarios.
4. Envío de las listas de precios procesadas a una API.

#### 1. Descarga de Listas de Precios

Deberás ingresar a la siguiente página web [Desafío Data Entry](desafiodataentryait.vercel.app) que tiene un listado de 3 proveedores de autopartes. Cada proveedor tiene un enlace para descargar su lista de precios. Tu tarea es descargar las listas de precios de todos los proveedores.

Para obtener la lista de algunos proveedores es necesario iniciar sesión en la página. Usá las siguientes credenciales:

- **Usuario**: desafiodataentry
- **Contraseña**: desafiodataentrypass

#### 2. Procesamiento de Listas de Precios

Las listas de precios descargadas tendrán diferentes formatos y estructuras. Tu objetivo es procesarlas y realizar todas las operaciones necesarias para obtener un formato estándar.

El resultado final de descargar y procesar cada lista de precios debe ser un archivo .xlsx con las siguientes características:

- **Nombre del archivo**: nombre del proveedor + fecha de hoy.
- **Columnas**: CODIGO, DESCRIPCION, MARCA, PRECIO.

#### 3. Formato de los Archivos:

- La columna PRECIO debe usar un punto (.) como separador de decimales, y ningún separador de miles.
- La columna DESCRIPCION debe tener un máximo de 100 caracteres.
- La columna DESCRIPCION debe ser la combinación de las columnas “Descripción” y “Rubro” de la lista original del proveedor Mundo RepCar.
- La lista del proveedor Autofix se descarga con una hoja por cada marca seleccionada en la página. Se deberán descargar todas las marcas y unificarlas en una misma hoja de cálculo. Además, se debe agregar la columna MARCA a cada artículo según el nombre de la hoja en la que se encontraba el mismo.

#### 4. Subida de Listas a una API

Una vez que se procesan las listas de precios y se obtienen los archivos .xlsx finales, debés enviarlos para ser procesados a una API mediante una request POST.

- **URL de la API**: https://desafio.somosait.com/api/upload/
- El archivo se debe subir utilizando una request form-data con el nombre "file".
- La API analizará el archivo subido para validar que al menos estén presentes las columnas CODIGO, DESCRIPCIÓN, MARCA y PRECIO. En caso de que falte alguna de las columnas, se recibirá una respuesta con un error 400 y el mensaje "Missing required columns".
- La API realizará la subida de la lista a Google Drive. En caso de que la subida sea exitosa, se recibirá una respuesta con status 200 y un link de Google Drive para acceder al archivo subido.

##### Ejemplo de respuesta de la API:

```json
{
  "link": "https://docs.google.com/spreadsheets/d/16x-vqqjgT_URIbasRn2RTqbGCzeCbQhf6qOjYtYdzew/edit?usp=sharing"
}
```

## Parte 2: ETL

En Boxer utilizamos procesos ETL para adecuar la información que llega de los proveedores de nuestros clientes a Boxer. Por esto es importante que nuestro equipo de listas y automatización este familiarizado con este proceso y herramienta como SQL para resolver los problemas que se presenten.

En la carpeta "sql" del repositorio encontrarás un archivo .sql para que puedas crear una base de datos llamada “DesafioDataEntry” con varias tablas y datos. La base de datos tiene las siguientes tablas:

- **Repuesto**: id, codigo, descripción, id_marca, precio, proveedor_id, id_ultima_actualizacion.
- **Proveedor**: id, nombre.
- **Actualización**: id, fecha, id_proveedor.
- **Marca**: id, nombre.

### Requisitos

- **Solución**: Para completar esta parte del desafío, debés incluir las sentencias SQL que hayas utilizado en un archivo README.md subido en la carpeta "sql" al fork de la solución.

### Consigna

1. Crear la base de datos a partir del script SQL del repositorio.
2. Implementar las sentencias SQL que cumplan con cada ítem a continuación:
   - Obtener todos los repuestos del proveedor Autofix cuyo precio no se haya actualizado en el último mes.
   - Actualizar los repuestos de las marcas “ELEXA”, “BERU”, “SH”, “MASTERFILT” y “RN” realizando un incremento del 15% en sus precios.
   - Obtener el promedio de precios de los repuestos por cada marca.
   - Obtener los repuestos que no tienen una descripción asignada (descripción es NULL o vacía).
   - Contar el número de repuestos de cada proveedor y mostrar solo aquellos proveedores que tienen al menos 1000 repuestos.
   - Obtener el repuesto más caro de cada proveedor.
   - Aplicar un recargo del 30% en los artículos de los proveedores AutoRepuestos Express y Automax cuyo precio sea mayor a $50000 y menor a $100000.
3. Crear utilizando Python un archivo CSV que contenga la informacion rescatada de la BD en el paso 2.

## Parte 3: Automatización de Programas de Escritorio

Algunos proveedores de nuestros clientes disponen de un programa de escritorio instalable para poder descargar las listas de sus artículos, por lo que el equipo de listas mantiene automatizados ciertos procesos para descargar y procesar esos archivos.

En esta parte del desafío, evaluaremos tu capacidad para automatizar la ejecución e interacción con un programa o aplicación de escritorio. No tenemos disponible un programa específico para el desafío, ya que muchas veces depende del sistema operativo si se puede instalar y ejecutar. Por lo tanto, para evaluar esta parte usaremos la aplicación de escritorio de calculadora que tengas en tu computadora.

Tu objetivo será crear el código necesario que, al ejecutarse, abra la aplicación e interactúe con ella de alguna manera. Esa interacción puede ser cualquier cálculo simple que muestre un resultado. Finalizado esto, se deberá cerrar la aplicación.

### Requisitos

- **Python**: el código que desarrolles debe estar escrito en Python.
- **Bibliotecas**: Es obligatorio el uso mínimo de PyAutoGui, pero podés incluir cualquier otra librería necesaria para poder interactuar con la aplicación de

escritorio de forma visual.

- **Solución**: Incluí todos los archivos de tu implementación en la carpeta "automatizacion-programa" de la solución que subas.
  - Agregá un archivo requirements.txt con el listado de dependencias que se deben instalar para ejecutar la implementación.
  - Agregá un video con la grabación de pantalla que muestre la ejecución y funcionamiento de la solución que implementaste.

## Parte 4: Procesamiento de Listas Manuales

Ciertos proveedores de nuestros clientes no disponen de una página web o aplicación para descargar las listas de sus artículos, por lo que el equipo de listas debe recibir los archivos y procesarlos de forma manual para subirlos al sistema.

En esta parte del desafío, evaluaremos tu capacidad para trabajar con archivos xls, csv y txt, y procesarlos para lograr el formato necesario.

Tu objetivo será generar los archivos finales formateados para subir al sistema. Para ello, deberás seguir una serie de instrucciones y describir en un archivo README.md los pasos que fuiste realizando para obtener cada archivo final.

Las instrucciones y los archivos que debés utilizar se encuentran en esta [carpeta de Google Drive](https://drive.google.com/drive/folders/1ZMSARBPpxTbVwx-9u7wJUVgM9JREl9zL?usp=sharing). Podés crear una copia de la misma en tu almacenamiento local para realizar cambios en los archivos.

**Nota**: Si bien los archivos iniciales e instrucciones están en Google Drive, la solución debe subirse en el fork de GitHub junto al resto de las partes del desafío.

### Requisitos

- Debés utilizar Google Sheets para realizar operaciones sobre las listas, pero podés incluir otras herramientas que encuentres o consideres necesarias para llegar a la solución.
- **Solución**: Para completar esta parte del desafío, debés subir los archivos finales formateados en la carpeta "listas-manuales" de tu solución.
  - Debés incluir un archivo README.md describiendo los pasos que realizaste para obtener cada archivo final (operaciones de Google Sheets, uso de herramientas externas, etc.).
 
## Parte 5: Automatización de Procesos
