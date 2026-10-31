# Política de seguridad

## Versiones soportadas

Mientras el proyecto permanezca antes de su primera versión estable institucional, las correcciones de seguridad se aplican únicamente a la rama `main` y a la versión desplegada más reciente.

| Versión | Soporte de seguridad |
| --- | --- |
| `main` / despliegue vigente | Sí |
| Versiones anteriores | No garantizado |

Antes de declarar una versión estable, el equipo debe definir una política de mantenimiento, fechas de fin de soporte y responsables de publicación de parches.

## Cómo reportar una vulnerabilidad

No publique vulnerabilidades, credenciales, datos personales ni pruebas de concepto explotables en incidencias públicas.

Envíe el reporte a `soporte@mes.gob.cu` y solicite explícitamente su escalamiento confidencial al responsable de seguridad de EXPLORA. Incluya, cuando sea posible:

- componente, versión y entorno afectados;
- impacto estimado y condiciones necesarias para reproducirlo;
- pasos mínimos de reproducción y evidencias sin datos sensibles;
- medidas temporales que ya se hayan aplicado;
- datos de contacto y preferencia de coordinación.

No envíe contraseñas, tokens, llaves privadas, copias de bases de datos ni conjuntos de datos restringidos por correo. El equipo deberá acordar un canal institucional cifrado para intercambiar material sensible.

## Tratamiento esperado

Objetivos iniciales del proyecto, sujetos a la disponibilidad del equipo:

| Actividad | Objetivo |
| --- | --- |
| Acuse de recibo | 2 días laborables |
| Clasificación inicial y asignación | 5 días laborables |
| Plan de contención o corrección para severidad crítica | 2 días laborables desde la clasificación |
| Actualización al informante | Al menos cada 10 días laborables mientras el caso siga abierto |

La severidad debe evaluarse con CVSS 4.0 y con el impacto institucional sobre confidencialidad, integridad, disponibilidad, privacidad y preservación científica. El equipo coordinará la divulgación responsable después de disponer de una corrección o mitigación verificable.

## Alcance prioritario

- autenticación, autorización, sesiones y recuperación de cuentas;
- publicación, embargo y distribución de conjuntos de datos;
- carga, descarga y procesamiento de archivos y metadatos;
- DOI/DataCite, citación e integridad de registros científicos;
- preservación, OCFL, checksums, procedencia y auditoría;
- exposición de datos personales, secretos o infraestructura;
- dependencias, imágenes de contenedor y cadena de suministro.

## Gestión de secretos

Las credenciales no deben almacenarse en el repositorio, archivos de ejemplo, imágenes, registros ni documentación. Los secretos de desarrollo, pruebas y producción deben ser diferentes, rotarse al cambiar el personal o ante cualquier exposición, y suministrarse mediante el mecanismo seguro de configuración del entorno. Toda credencial compartida temporalmente debe considerarse comprometida y rotarse.

## Límites

Esta política no autoriza pruebas destructivas, denegación de servicio, ingeniería social, acceso a datos de terceros ni cambios sobre producción sin coordinación previa. Los hallazgos deben validarse en un entorno controlado siempre que sea posible.
