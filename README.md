# Consulta RUT

Aplicación en `Streamlit` para consultar la clasificación de clientes por RUT empresa a partir de una base Excel.

El usuario ingresa el RUT sin puntos, sin guion y sin dígito verificador, y la app devuelve la información asociada al cliente.

## Funcionalidad

La aplicación busca el valor ingresado en la columna `Rut_empresa` y muestra:

- `Rut_empresa`
- `Dv_empresa`
- `Razon_social`
- `Actividad_economica`
- `Direccion`
- `Clasificacion`

La clasificación se muestra como dato principal.

## Regla de negocio

Si el RUT consultado no existe en la base, la aplicación devuelve por defecto:

- `Clasificacion = C3`

Y muestra el siguiente mensaje:

> Es posible que el cliente haya formalizado la empresa fuera del periodo que informa SII o que su facturación corresponda a C3.

## Requisitos

- Python 3.10 o superior
- `pip`
- Archivo Excel con la base de clientes

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/morpheomax/consulta_rut.git
cd consulta_rut
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual.

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Windows CMD:

```bat
.venv\Scripts\activate.bat
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Base de datos

El repositorio incluye `ABC_clientes.xlsx`, que es el archivo usado por la aplicación por defecto.

La app busca el archivo en la raíz del proyecto con este nombre exacto:

```text
ABC_clientes.xlsx
```

Si prefieres usar otra ruta o nombre de archivo, define la variable de entorno `CONSULTA_RUT_DATA_FILE` antes de ejecutar la app.

Ejemplo en PowerShell:

```powershell
$env:CONSULTA_RUT_DATA_FILE="C:\ruta\a\tu\archivo.xlsx"
```

## Estructura esperada del Excel

La hoja debe incluir estas columnas obligatorias:

- `Rut_empresa`
- `Dv_empresa`
- `Razon_social`
- `Actividad_economica`
- `Direccion`
- `Clasificacion`

La aplicación normaliza nombres de columnas, por lo que tolera pequeñas diferencias de mayúsculas, minúsculas, espacios y tildes.

## Ejecución

Con el entorno virtual activo, ejecuta:

```bash
streamlit run app.py
```

Luego abre en el navegador la URL que indique Streamlit, normalmente:

```text
http://localhost:8501
```

## Uso

1. Ingresa el RUT de la empresa usando solo números.
2. No agregues puntos, guion ni dígito verificador.
3. Presiona `Buscar cliente`.
4. Revisa la clasificación y el detalle del cliente.

## Errores comunes

- Si falta el archivo Excel, la app mostrará un error indicando la ruta esperada.
- Si faltan columnas obligatorias, la app informará cuáles son.
- Si el RUT no existe en la base, se devolverá `C3` por defecto.

## Estructura del proyecto

```text
consulta_rut/
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Publicación en GitHub

Antes de subir cambios:

- Verifica que `ABC_clientes.xlsx` sea la versión correcta que debe acompañar a la app.
- Mantén fuera de Git cualquier respaldo local o archivo temporal.
- Si haces pruebas con otras bases, usa `CONSULTA_RUT_DATA_FILE` para no reemplazar el archivo principal del proyecto.

## Tecnologías

- Streamlit
- Pandas
- OpenPyXL
