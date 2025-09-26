# ARCHIVO ANAEROBICOS

- PARA QUITAR FILAS VACIAS, APLIQUE UN FILTRO Y QUITAR VACIOS.
- con la formula REGEXEXTRACT() y expreciones regulares extraigo los datos de producto numericos para el codigo tambien para formatear los valores de los precio

# ARCHIVO HARD

- para convertir de csv a hoja de calculo de google, importe el archivo y formate con la misma aplicacion de google.
- use =SUBSTITUTE(A2, ".", ",") para sustituir . por comas, tambien para eliminarla la , y darle formato al precio final luego use ROUNDDOWN(E2, 0) para truncar y que el precio final se vea con decimales a 0.

# ARCHIVO RASA

- Utilizo la misma aplicacion de google para convertir el txt a hoja de calculo de google
- Para obtener el precio en este archivo realmente si que me perdi, lo que hice fue obtener los 10 caracteres de la derecha y le di formato numerico
  -Para la descripcion uni la celda de articulo y la celda que tenia el nombre con la funcion =CONCAT(A2;B2)
