# 🧾 Buscador de Categoría por RUT

Una aplicación web moderna y eficiente para consultar información de empresas chilenas por su RUT, utilizando datos del archivo ABC.xlsx. Desarrollada con Streamlit para una experiencia de usuario intuitiva y atractiva.

## 📋 Descripción

Esta aplicación permite buscar y visualizar información detallada de empresas chilenas basadas en su RUT (Rol Único Tributario). Utiliza un archivo Excel (ABC.xlsx) que contiene datos comerciales y geográficos, ofreciendo funcionalidades de búsqueda individual y masiva, además de visualización de ubicaciones en mapas interactivos.

## ✨ Características Principales

### 🔍 Búsqueda Individual

- **Consulta rápida por RUT**: Ingresa un RUT sin guion ni dígito verificador.
- **Información completa**: Muestra todos los campos del registro, incluyendo RUT, razón social, rubro económico, etc.
- **Categoría destacada**: La categoría se resalta prominentemente para identificación inmediata.
- **Mapa interactivo**: Visualiza la ubicación de la empresa en un mapa usando geocodificación basada en Provincia y Comuna.

### 📊 Búsqueda Masiva

- **Múltiples RUTs**: Ingresa una lista de RUTs separados por comas o saltos de línea.
- **Resultados tabulares**: Visualiza todos los resultados encontrados en una tabla ordenada.
- **Resumen estadístico**: Obtén un resumen con el total de RUTs encontrados y las categorías únicas.

### 🎨 Interfaz Moderna

- **Diseño responsivo**: Layout amplio con columnas organizadas.
- **Estilos CSS personalizados**: Colores atractivos, bordes redondeados y animaciones sutiles.
- **Emojis y tooltips**: Interfaz amigable con ayuda contextual.
- **Manejo de errores**: Mensajes claros para archivos bloqueados o RUTs no encontrados.

## 🛠️ Requisitos del Sistema

- **Python**: 3.8 o superior
- **Dependencias**: Ver `requirements.txt` (generado automáticamente por el entorno virtual)
- **Archivo de datos**: `ABC.xlsx` con las columnas requeridas (Rut_empresa, Dv_empresa, Razon_social, etc.)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/morpheomax/consulta_rut.git
cd consulta_rut
```

### 2. Configurar Entorno Virtual

```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install streamlit pandas openpyxl geopy folium streamlit-folium
```

### 4. Preparar Archivo de Datos

- Coloca el archivo `ABC.xlsx` en la raíz del proyecto.
- Asegúrate de que contenga las columnas necesarias (ver sección de Estructura de Datos).

### 5. Ejecutar la Aplicación

```bash
streamlit run app.py
```

Accede a `http://localhost:8501` en tu navegador.

## 📊 Estructura de Datos

El archivo `ABC.xlsx` debe contener las siguientes columnas principales:

| Columna               | Descripción                     |
| --------------------- | ------------------------------- |
| `Rut_empresa`         | RUT de la empresa (sin DV)      |
| `Dv_empresa`          | Dígito verificador del RUT      |
| `Razon_social`        | Nombre de la empresa            |
| `Tramo_ventas`        | Categoría de ventas             |
| `Annio_comercial`     | Año comercial                   |
| `Rubro_economico`     | Rubro económico principal       |
| `Subrubro_economico`  | Subrubro económico              |
| `Actividad_economica` | Actividad económica específica  |
| `Region`              | Región de Chile                 |
| `Provincia`           | Provincia                       |
| `Comuna`              | Comuna                          |
| `CAT`                 | Categoría (destacada en la app) |

## 📁 Estructura del Proyecto

```
consulta_rut/
├── app.py                 # Archivo principal de la aplicación
├── ABC.xlsx               # Archivo de datos (no incluido en repo)
├── README.md              # Este archivo
├── requirements.txt       # Dependencias (generar con pip freeze)
├── .venv/                 # Entorno virtual (no subir a repo)
└── .git/                  # Control de versiones
```

## 🎯 Uso de la Aplicación

### Búsqueda Individual

1. Selecciona la pestaña "🔍 Búsqueda Individual".
2. Ingresa el RUT (solo números, sin guion ni DV).
3. Presiona Enter o espera la búsqueda automática.
4. Revisa la información destacada y el mapa.

### Búsqueda Masiva

1. Selecciona la pestaña "📊 Búsqueda Masiva".
2. Ingresa múltiples RUTs separados por comas o líneas.
3. Haz clic en "🔍 Buscar RUTs".
4. Explora la tabla de resultados y el resumen.

## 🔧 Solución de Problemas

### Archivo Excel Bloqueado

- **Error**: "Permission denied" al cargar ABC.xlsx.
- **Solución**: Cierra Excel si tienes el archivo abierto. La app maneja este error y permite reintentar.

### Geocodificación Fallida

- **Mensaje**: "No se pudo geocodificar la ubicación".
- **Causa**: Provincia/Comuna no reconocida por el servicio de geocodificación.
- **Solución**: Verifica la ortografía en el Excel o usa nombres estándar.

### RUT No Encontrado

- Asegúrate de ingresar solo números (sin guion ni DV).
- Verifica que el RUT exista en ABC.xlsx.

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

- **Autor**: morpheomax
- **Repositorio**: [GitHub](https://github.com/morpheomax/consulta_rut)
- **Issues**: [Reportar problemas](https://github.com/morpheomax/consulta_rut/issues)

---

⭐ Si encuentras útil esta aplicación, ¡dale una estrella en GitHub!
