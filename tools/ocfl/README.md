# Auditoría y transición OCFL

La aplicación usa actualmente `repo.plugin.versioning: simple`. Las propiedades OCFL no demuestran por sí solas que exista un plugin OCFL compatible en el classpath ni que haya un storage root activo. No habilite `ocfl` en producción hasta identificar y probar la implementación concreta.

La especificación OCFL 1.1 declara el algoritmo de contenido en cada `inventory.json`; su sidecar debe usar el mismo algoritmo. Por ello, cambiar el valor predeterminado a SHA-256 sirve para objetos nuevos, pero **no autoriza a reescribir inventarios MD5 existentes**.

## Auditoría de solo lectura

Trabaje sobre una copia consistente o un montaje de solo lectura:

```sh
python tools/ocfl/audit_repository.py /ruta/copia-ocfl --summary-only
python -m unittest discover -s tools/ocfl -p "test_*.py"
```

El comando devuelve `0` si todos los inventarios detectados y sus sidecars son válidos y no hay identificadores duplicados, `1` ante objetos inválidos y `2` si no puede leer la raíz. No modifica archivos. Su alcance es deliberadamente previo a la migración: no sustituye un validador OCFL completo.

## Gate antes de habilitar OCFL

1. Congelar escrituras y obtener una copia coherente de base de datos y storage.
2. Confirmar artefacto, versión y documentación del plugin OCFL; el runtime actual de este repositorio no lo incluye.
3. Ejecutar esta auditoría y un validador OCFL 1.1 independiente sobre la copia.
4. Conservar cada objeto histórico con su `digestAlgorithm` y sidecar originales.
5. Configurar SHA-256 para objetos nuevos y verificar que el plugin puede leer simultáneamente objetos históricos MD5 y nuevos SHA-256.
6. Crear y versionar un objeto sintético, validar su inventario, descargar su contenido y comprobar fixity.
7. Ensayar restauración y rollback antes de activar escrituras en staging.
8. Registrar conteos por algoritmo, errores, duración, versión del validador y aprobación del responsable de preservación.

Si el plugin no soporta algoritmos mixtos, detener el despliegue. Cualquier conversión debe realizarse con una herramienta específica que cree una transición preservable y validable; nunca mediante sustitución textual de `digestAlgorithm` o renombrado de sidecars.

Referencias normativas:

- OCFL 1.1: <https://ocfl.io/1.1/spec/>
- Códigos oficiales de validación: <https://ocfl.io/1.1/spec/validation-codes.html>
