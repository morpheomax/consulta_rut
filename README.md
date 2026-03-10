# Buscador de Clasificación por RUT

Aplicación desarrollada en **Streamlit** para consultar la **clasificación de clientes por RUT empresa** a partir de un archivo Excel.

El usuario ingresa el **RUT sin puntos, sin guion y sin dígito verificador**, y la app devuelve la información asociada del cliente.

## Qué hace esta aplicación

La app busca por la columna `Rut_empresa` dentro del archivo Excel y muestra los siguientes campos:

- `Rut_empresa`
- `Dv_empresa`
- `Razon_social`
- `Actividad_economica`
- `Direccion`
- `Clasificacion`

La **clasificación** se destaca como el dato principal.

### Regla de negocio
Si el RUT consultado **no existe en la base**, la aplicación devuelve por defecto:

- **Clasificación: `C3`**

junto con la siguiente leyenda:

> Es posible que el cliente haya formalizado la empresa fuera del periodo que informa SII o que su facturación corresponda a C3.

---

## Estructura esperada del archivo Excel

La aplicación espera un archivo llamado:

```text
ABC_clientes.xlsx