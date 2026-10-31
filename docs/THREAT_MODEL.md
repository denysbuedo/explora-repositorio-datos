# Modelo de amenazas inicial de EXPLORA

**Estado:** borrador operativo

**Fecha de revisión:** 2026-10-30

**Revisión siguiente:** antes de la primera puesta en producción posterior a este documento

## 1. Objetivo y alcance

Este modelo cubre el portal web, las API, la autenticación, el almacenamiento de metadatos y archivos, la publicación y descarga, la preservación OCFL, las integraciones DOI/DataCite, el correo y la infraestructura de despliegue. Debe actualizarse cuando cambien la arquitectura, los proveedores, los niveles de acceso o el flujo de publicación.

No sustituye una evaluación de riesgos institucional, una revisión de privacidad ni pruebas de penetración independientes.

## 2. Activos críticos

- conjuntos de datos, incluidos datos restringidos o bajo embargo;
- metadatos, identificadores persistentes, citas y relaciones entre versiones;
- credenciales, sesiones, tokens y secretos de servicios;
- evidencias de integridad, checksums, inventarios OCFL y trazas de auditoría;
- disponibilidad del catálogo y capacidad de depositar, revisar y recuperar datos;
- identidad y reputación de autores, instituciones, curadores y EXPLORA.

## 3. Actores y límites de confianza

Actores: visitantes, depositantes, curadores, administradores, servicios institucionales, proveedores externos y atacantes anónimos o con una cuenta comprometida.

Límites que requieren controles explícitos:

1. navegador público ↔ portal/API;
2. aplicación ↔ base de datos y almacenamiento de archivos;
3. aplicación ↔ repositorio de preservación OCFL;
4. aplicación ↔ DataCite, correo y otros servicios externos;
5. canal de integración/despliegue ↔ entorno de producción;
6. administradores/operadores ↔ consola, configuración y copias de seguridad.

## 4. Amenazas y controles mínimos

| Área | Amenaza principal | Controles requeridos | Evidencia esperada |
| --- | --- | --- | --- |
| Identidad | robo de sesión, fuerza bruta, escalamiento de privilegios | contraseñas robustas, MFA para cuentas privilegiadas, expiración y revocación de sesiones, autorización en servidor | pruebas de roles, registros de acceso y revisión periódica de cuentas |
| Archivos | traversal, ZIP malicioso, carga ejecutable, agotamiento de recursos | rutas canónicas, nombres ZIP portables, límites de tamaño/cuota, validación de tipo, análisis antimalware, almacenamiento no ejecutable | pruebas de rutas, límites documentados y eventos de rechazo |
| Publicación | fuga de borradores, datos restringidos o embargados | denegación por defecto, estados explícitos, controles de autorización antes de leer bytes, pruebas de embargo | pruebas automatizadas por estado y auditoría de cambios |
| Integridad científica | alteración silenciosa de datos o metadatos | SHA-256 o superior, fijación de versiones, procedencia, verificación programada y copias independientes | informes de fixity y capacidad de reconstrucción |
| Identificadores | DOI incorrecto, duplicado o mutable sin trazabilidad | validación DataCite, idempotencia, revisión curatorial, relación clara entre versiones | pruebas contractuales y registro de solicitudes/respuestas sin secretos |
| Aplicación web/API | inyección, XSS, CSRF, abuso de API | validación de entrada, codificación de salida, CSP, protección CSRF según el modelo de sesión, rate limiting | cabeceras verificadas, análisis SAST/DAST y pruebas negativas |
| Dependencias | componente vulnerable o artefacto manipulado | inventario SBOM, versiones fijadas, análisis continuo, firmas/procedencia del build | SBOM por versión y política de actualización |
| Operación | secretos expuestos, configuración insegura, TLS obsoleto | gestor de secretos, rotación, TLS 1.2/1.3, mínimo privilegio y separación de entornos | revisión de configuración y simulacro de rotación |
| Disponibilidad | denegación de servicio, pérdida de almacenamiento | límites, observabilidad, copias 3-2-1, restauración probada, objetivos RPO/RTO | métricas, alertas y actas de restauración |
| Auditoría y privacidad | registros insuficientes o con información sensible | eventos inmutables, minimización, retención definida y acceso restringido | catálogo de eventos y revisión de logs |

## 5. Riesgos residuales prioritarios

1. El correo de soporte es un punto inicial de contacto, no un canal adecuado para secretos; falta formalizar un canal cifrado y un responsable de seguridad nominal.
2. Cambiar el digest predeterminado de OCFL a SHA-256 no migra automáticamente objetos existentes; se necesita inventario, compatibilidad y plan de verificación antes de operar sobre un repositorio previo.
3. La validación automática de accesibilidad, dependencias y código no equivale a auditorías profesionales independientes.
4. Sin RPO, RTO y pruebas documentadas de restauración no puede afirmarse capacidad real de recuperación.
5. Debe verificarse en despliegue que el proxy, las cookies, CORS, CSP y TLS conserven la política definida por la aplicación.

## 6. Criterios de aceptación antes de producción

- ninguna credencial conocida en el historial o los artefactos de construcción;
- controles de acceso probados para borrador, embargo, acceso restringido y publicación;
- pruebas de carga/descarga adversarial y límites operativos configurados;
- TLS 1.2 o 1.3, cookies seguras y cabeceras web verificadas externamente;
- SBOM, análisis de dependencias y proceso de parcheo operativo;
- backup y restauración probados, con RPO/RTO aprobados;
- verificación de fixity y alerta ante corrupción;
- procedimiento de incidentes y reporte de vulnerabilidades ensayado;
- evaluación de privacidad y licencias de los datos;
- revisión del modelo de amenazas firmada por desarrollo, operación y responsable científico.

## 7. Mantenimiento

El propietario técnico convoca la revisión; desarrollo aporta cambios de arquitectura, operaciones aporta evidencias del entorno y el responsable científico valida impacto sobre datos y citación. Cada riesgo debe convertirse en una tarea trazable con responsable, fecha y criterio verificable de cierre.
