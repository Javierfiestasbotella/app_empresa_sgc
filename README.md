# Aplicación de Gestión de Clientes y Citas

## Descripción
Esta aplicación permite gestionar una base de datos de clientes y citas médicas, además de realizar copias de seguridad de los datos y exportarlos en formato CSV. Utiliza una interfaz gráfica creada con **Tkinter** y se conecta a una base de datos **PostgreSQL** mediante la librería **psycopg2**. 

## Funciones Principales
- **Conexión a la Base de Datos**: Utiliza `psycopg2` para conectarse a una base de datos PostgreSQL.
- **Interfaz Gráfica (GUI)**: Implementada con **Tkinter**, permite realizar CRUD (crear, leer, actualizar y borrar) de clientes y citas.
- **Copia de Seguridad**: Usa `pg_dump` para realizar una copia de seguridad de la base de datos.
- **Exportación a CSV**: Exporta los datos de las tablas a archivos CSV mediante `pandas`.
- **Ordenación de Datos**: Permite ordenar los datos de clientes por ID.
- **Soporte de Marca de Agua**: Carga un logo como marca de agua en la tabla de datos.

## Estructura de la Aplicación
- **Ventana Principal**: Permite la visualización y manipulación de los datos de clientes y citas.
- **Botones CRUD**: Facilitan la gestión de clientes y citas a través de botones para agregar, editar, buscar, y eliminar registros.
- **Backup y Exportación**: Incluye botones para realizar la copia de seguridad de la base de datos y exportar los datos a CSV.

## Instalación
1. Instalar los paquetes necesarios: `tkinter`, `psycopg2`, `pandas`, y `Pillow`.
2. Configurar la base de datos PostgreSQL.
3. Ejecutar la aplicación.

## Dependencias
- **Python** (Tkinter, subprocess, psycopg2, pandas)
- **PostgreSQL** (para la base de datos)
- **Pillow** (para cargar y redimensionar imágenes)

