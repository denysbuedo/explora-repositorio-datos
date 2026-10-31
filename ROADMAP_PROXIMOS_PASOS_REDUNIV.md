# Roadmap de próximos pasos — Repositorio de Datos Científicos RedUniv

**Fecha:** 30 de octubre de 2026

**Punto de partida:** `main` en commit `5cfc48e`

**Documento base:** `LISTA_CHEQUEO_PROPUESTA_IMPLEMENTACION.md`

**Objetivo:** llevar el desarrollo actual desde un cierre local avanzado hasta un servicio institucional verificable y operable

## 1. Principios de ejecución

1. No desplegar una versión cuya suite obligatoria tenga fallos.
2. No confundir una función implementada con una función validada en producción.
3. No activar integraciones externas sin credenciales gestionadas como secretos y procedimiento de recuperación.
4. No declarar cumplimiento OAIS, CoreTrustSeal o WCAG sin evidencia y aprobación correspondientes.
5. No modificar todavía el diseño visual; se retomará después de recibir la identidad visual oficial.
6. Cada fase termina con evidencia reproducible, responsables y una decisión explícita de continuar.

## 2. Vista general

| Fase | Propósito | Duración orientativa | Resultado esperado |
|---|---|---:|---|
| 0 | Recuperar build verde y eliminar riesgos inmediatos | 1–2 semanas | Candidato técnico estable |
| 1 | Preparar automatización y cadena de suministro | 2–4 semanas | Entrega repetible y auditable |
| 2 | Validar staging institucional | 3–6 semanas | Aceptación técnica y funcional |
| 3 | Preparar salida a producción | 2–4 semanas | Release y plan de despliegue aprobados |
| 4 | Estabilizar producción | 2–4 semanas | Servicio medido, respaldado y operable |
| 5 | Madurez de repositorio confiable | 3–9 meses | Preservación y gobernanza institucional |
| 6 | Aplicar nueva identidad visual | Cuando se reciban los insumos | Interfaz institucional validada |

Las duraciones dependen de disponibilidad de infraestructura, responsables institucionales y credenciales externas. No deben interpretarse como fechas comprometidas.

# Fase 0 — Estabilización técnica inmediata

## Objetivo

Recuperar una línea base confiable antes de añadir funciones o preparar despliegues.

## Trabajo

### 0.1 Corregir la regresión del ZIP

- [x] Corregir `safeRelativePath` para que trate `/` como separador canónico de entradas ZIP en Windows y Linux.
- [x] Mantener el rechazo de rutas absolutas, `..`, saltos de línea, duplicados y colisiones archivo/directorio.
- [x] Añadir pruebas para rutas anidadas como `description/description.md`.
- [x] Añadir casos Windows/Linux independientes del sistema operativo del runner.
- [x] Ejecutar la prueba aislada y posteriormente la suite completa.

**Criterio de aceptación:** `DatasetArchiveControllerTest` pasa completamente y un ZIP con rutas anidadas puede leerse sin pérdida de archivos.

### 0.2 Recuperar la suite verde

- [x] Ejecutar la suite completa —ahora 1382 pruebas— con JDK 21.
- [x] Confirmar cero fallos, errores y pruebas omitidas inesperadamente.
- [x] Guardar reporte HTML/XML como evidencia del candidato.
- [x] Revisar los diagnósticos de codificación de `DataCiteMessageConverter.java` y convertir los fuentes a UTF-8 real.
- [x] Registrar versión exacta de Java, Gradle, sistema operativo y commit base.

**Evidencia local del 30 de octubre de 2026:** Windows, JDK 21, Gradle 8.12.1, base `5cfc48e`; 1382 pruebas, 0 fallos, 0 errores y 0 omitidas. Los reportes se generan en `build/reports/tests/test` y `build/test-results/test`.

**Criterio de aceptación:** `BUILD SUCCESSFUL`, sin errores de codificación ni pruebas fallidas.

### 0.3 Eliminar valores criptográficos obsoletos

- [x] Retirar TLS 1.0 y TLS 1.1 de `gradle.properties`.
- [x] Mantener TLS 1.2 y permitir TLS 1.3 donde la plataforma lo soporte.
- [x] Cambiar el algoritmo OCFL predeterminado de MD5 a SHA-256 o SHA-512.
- [x] Documentar el tratamiento de objetos existentes con hashes MD5 sin inventar nuevas huellas históricas.
- [ ] Probar compatibilidad y migración de configuración.

**Avance:** se añadió `tools/ocfl/audit_repository.py`, una auditoría de solo lectura con pruebas sintéticas para inventarios históricos MD5 y nuevos SHA-256. La compatibilidad real permanece abierta porque el runtime actual no incluye un plugin OCFL y todavía no se ha proporcionado una copia controlada de objetos existentes.

**Criterio de aceptación:** ninguna configuración recomendada genera nuevas huellas MD5 ni habilita TLS obsoleto.

### 0.4 Cerrar documentación mínima de seguridad

- [x] Crear `SECURITY.md` con canal privado, versiones soportadas y tiempos de respuesta.
- [x] Crear un modelo de amenazas inicial: cuentas, API, archivos, DOI, revisión externa, administración y cadena de suministro.
- [ ] Clasificar secretos y definir dónde se almacenan en desarrollo, staging y producción.
- [ ] Revisar que los ejemplos inseguros estén marcados exclusivamente como desarrollo.

**Criterio de aceptación:** el equipo sabe cómo reportar una vulnerabilidad y qué configuraciones nunca deben llegar a producción.

## Gate de salida de la fase 0

- [x] Suite completa verde.
- [x] TLS y hashing actualizados en la configuración del repositorio.
- [ ] `SECURITY.md` aprobado.
- [ ] Modelo de amenazas revisado por desarrollo y operaciones.
- [ ] No existen nuevos defectos críticos abiertos.

# Fase 1 — Automatización y cadena de suministro

## Objetivo

Hacer que cada cambio y release sea reproducible, verificable y bloqueable ante fallos.

## Trabajo

### 1.1 Integración continua

**Avance:** se añadió `.github/workflows/ci.yml` para `main`, `dev` y pull requests. Ejecuta JDK 21, la suite Gradle, pruebas de herramientas, auditoría de secretos y conserva evidencia durante 14 días. Falta publicar la rama y configurar la protección de ramas para convertir el check en obligatorio.

- [ ] Crear workflow de GitHub Actions o plataforma CI institucional.
- [ ] Compilar con JDK 21 y Gradle Wrapper.
- [ ] Ejecutar unitarias, integración y contrato OpenAPI.
- [ ] Ejecutar verificaciones de i18n y accesibilidad automática.
- [ ] Publicar reportes de pruebas y JaCoCo.
- [ ] Definir un umbral inicial de cobertura para código nuevo y componentes críticos.
- [ ] Proteger `main`: PR, revisión y checks obligatorios.

### 1.2 Seguridad automatizada

- [x] Ejecutar auditoría de secretos en cada PR mediante el workflow CI.
- [x] Definir OWASP Dependency-Check como SCA con reportes HTML/JSON/SARIF y umbral CVSS 7; falta la primera ejecución remota con NVD actualizada.
- [x] Añadir CodeQL SAST para Java/Kotlin y JavaScript/TypeScript.
- [ ] Escanear el contenedor con Trivy, Grype o herramienta institucional.
- [x] Definir política de severidades y excepciones documentadas en `docs/VULNERABILITY_MANAGEMENT.md`.

**Evidencia local:** OWASP Dependency-Check 13 carga y ejecuta, pero el primer análisis no pudo actualizar NVD porque no existe una API key institucional válida. El fallo se conserva como bloqueo operativo; no se generó ni se declara un resultado limpio.

### 1.3 SBOM, firma y procedencia

- [x] Generar SBOM CycloneDX directo para el JAR en cada ejecución CI.
- [x] Generar checksum SHA-256 del JAR en CI; falta publicarlo como activo de un release aprobado y cubrir la imagen.
- [ ] Firmar artefactos o imágenes con la solución institucional aprobada.
- [ ] Añadir attestations de procedencia del build cuando sea posible.
- [ ] Verificar correspondencia entre tag, commit, JAR, SBOM e imagen.

**Avance:** CycloneDX 3.5.1 genera `build/reports/cyclonedx-direct/bom.json` y `bom.xml` a partir de `compileClasspath` y `runtimeClasspath`. CI conserva esos archivos junto al JAR y `SHA256SUMS`. Esto crea evidencia, pero no constituye firma ni procedencia SLSA.

### 1.4 Migraciones versionadas

- [x] Adoptar Flyway para migraciones PostgreSQL versionadas.
- [x] Incorporar la migración científica actual como `V1__scientific_repository_extension.sql`.
- [ ] Probar migración desde la versión productiva conocida.
- [x] Mantener ensayo idempotente/restauración y añadir gates de configuración; falta una copia productiva conocida.
- [x] Impedir `ddl-auto:update` en el perfil y configuración generada de producción; usar `validate`.

**Límite:** `V1` amplía una base heredada; no representa el esquema inicial completo. La adopción en una base existente exige baseline explícito `0` después de respaldo y ensayo. El baseline automático y `flyway clean` permanecen deshabilitados.

## Gate de salida de la fase 1

- [ ] Ningún PR puede fusionarse con pruebas o seguridad obligatoria fallidas.
- [ ] Cada candidato contiene SBOM y checksums.
- [ ] Migraciones son explícitas, versionadas y repetibles.
- [ ] El proceso de release se ejecuta desde un tag inmutable.

# Fase 2 — Validación de staging institucional

## Objetivo

Probar el sistema completo con infraestructura y datos representativos sin afectar producción.

## Trabajo

### 2.1 Preparar staging

- [ ] Crear entorno con PostgreSQL, almacenamiento, Elasticsearch, SMTP y proxy equivalentes a producción.
- [ ] Usar secretos diferentes de producción.
- [ ] Bloquear acceso directo al backend si el diseño exige pasar por HAProxy/reverse proxy.
- [ ] Configurar autenticación, CORS HTTPS y Actuator mínimo.
- [ ] Verificar ejecución con usuario no-root.

### 2.2 Migración y recuperación

- [ ] Obtener una copia autorizada y saneada de base de datos y archivos.
- [ ] Ejecutar inventario de `contentUri` fuera de `repo.basepath`.
- [ ] Aplicar migraciones y registrar duración, volumen y errores.
- [ ] Restaurar backup en un entorno limpio.
- [ ] Confirmar metadatos, archivos, usuarios, relaciones y checksums.
- [ ] Medir RPO y RTO observados.
- [ ] Documentar procedimiento de rollback de aplicación sin revertir esquemas a ciegas.

### 2.3 DOI y DataCite

- [ ] Validar credenciales en DataCite Test.
- [ ] Reservar DOI de prueba conceptual y de versión.
- [ ] Publicar y resolver ambos DOI hacia landing pages HTTPS.
- [ ] Verificar relaciones `HasVersion`, `IsVersionOf`, sucesión, artículo y software.
- [ ] Probar recuperación tras timeout, respuesta parcial y reintento.
- [ ] Conciliar cualquier DOI manual existente antes de automatizar producción.

### 2.4 ORCID y ROR

- [ ] Registrar callback HTTPS en ORCID Sandbox.
- [ ] Probar vinculación, cancelación, expiración y replay con cuentas de prueba.
- [ ] Definir política para coautores que no autentican personalmente.
- [ ] Verificar salida ROR desde la VM o configurar proxy institucional.
- [ ] Aprobar ROR oficiales de las instituciones participantes.

### 2.5 Correo

- [ ] Configurar SMTP institucional con TLS y remitente aprobado.
- [ ] Probar registro, verificación, reenvío, expiración y fallos transitorios.
- [ ] Verificar que logs y respuestas no revelen códigos ni destinatarios.
- [ ] Configurar alertas de fijación con una dirección institucional.

### 2.6 Pruebas funcionales y científicas

- [ ] Investigador deposita Markdown, archivos sueltos y ZIP.
- [ ] Curador revisa calidad, privacidad, vocabularios y publicación.
- [ ] Revisor externo usa enlace temporal, descarga y revocación.
- [ ] Se crea una nueva versión sin modificar la anterior.
- [ ] Se retira una versión conservando landing page y relaciones.
- [ ] Biblioteca valida APA, Vancouver, Chicago, IEEE, BibTeX, RIS y CSL-JSON.
- [ ] Curadores validan DataCite, RO-Crate, PROV-O y BagIt.

### 2.7 Carga, archivos grandes y resiliencia

- [ ] Definir tamaños representativos y máximos institucionales.
- [ ] Probar subida interrumpida, almacenamiento lleno y timeout del proxy.
- [ ] Probar descarga ZIP pública, privada y de preservación.
- [ ] Medir catálogo y facetas con volumen representativo.
- [ ] Probar concurrencia editorial y rate limiting detrás del proxy.
- [ ] Dimensionar pool JDBC, heap, disco, I/O y workers.

### 2.8 Accesibilidad y aceptación humana

- [ ] Revisar teclado, foco, contraste, zoom al 200/400 % y reflow.
- [ ] Probar con NVDA u otro lector de pantalla aprobado.
- [ ] Evaluar recorridos con investigadores, curadores, biblioteca y administración.
- [ ] Registrar problemas por severidad y corregir los bloqueadores.
- [ ] No abordar todavía branding final; evaluar estructura, contenido y usabilidad.

## Gate de salida de la fase 2

- [ ] Acta de aceptación funcional firmada.
- [ ] Migración y restauración demostradas.
- [ ] DataCite Test, ORCID Sandbox, ROR y SMTP aprobados.
- [ ] Cero vulnerabilidades críticas abiertas.
- [ ] Rendimiento y capacidad aceptados para la carga estimada.
- [ ] Plan de corrección de accesibilidad aprobado.

# Fase 3 — Preparación de producción

## Objetivo

Crear un release aprobado y un procedimiento seguro de puesta en marcha.

## Trabajo

### 3.1 Decisiones operativas

- [ ] Definir responsables de aplicación, base de datos, almacenamiento, seguridad, DOI y soporte.
- [ ] Aprobar RPO, RTO, retención y ventanas de mantenimiento.
- [ ] Aprobar política de acceso, privacidad, licencias, retirada y preservación.
- [ ] Definir escalamiento de incidentes y comunicación a usuarios.

### 3.2 Preparar release

- [ ] Congelar alcance y ejecutar todas las verificaciones.
- [ ] Crear tag SemVer inmutable.
- [ ] Generar JAR, imagen, SBOM, checksums, firmas y notas de release.
- [ ] Documentar cambios de esquema y compatibilidad.
- [ ] Preparar plan de despliegue, smoke tests y rollback.
- [ ] Verificar que no se incluya configuración ni secretos dentro del JAR.

### 3.3 Preparar infraestructura

- [ ] Rotar todas las credenciales utilizadas previamente o compartidas durante pruebas.
- [ ] Configurar secretos mediante el mecanismo institucional.
- [ ] Verificar certificados, DNS, HAProxy, firewall y acceso administrativo.
- [ ] Configurar backups y copia independiente antes del despliegue.
- [ ] Configurar métricas, logs, alertas, capacidad y retención.

### 3.4 Ensayo final

- [ ] Ejecutar preflight productivo en modo de lectura.
- [ ] Ensayar despliegue con el mismo paquete que irá a producción.
- [ ] Ensayar parada, actualización, arranque, smoke tests y recuperación.
- [ ] Obtener aprobación Go/No-Go de todos los responsables.

## Gate de salida de la fase 3

- [ ] Release firmado y aprobado.
- [ ] Backup previo verificado.
- [ ] Rollback ensayado.
- [ ] Ventana y responsables confirmados.
- [ ] Decisión Go documentada.

# Fase 4 — Despliegue y estabilización

## Objetivo

Poner en producción el release aprobado y demostrar estabilidad operativa.

## Trabajo

### Día de despliegue

- [ ] Activar ventana de mantenimiento.
- [ ] Detener o bloquear escrituras según el runbook.
- [ ] Crear y verificar backup final.
- [ ] Aplicar migraciones aprobadas.
- [ ] Desplegar exactamente el artefacto firmado.
- [ ] Ejecutar health, login, verificación, catálogo, depósito, descarga y administración.
- [ ] Verificar métricas, logs, correo y almacenamiento.
- [ ] Registrar commit, tag, checksums, operador y tiempos.

### Primeras 24–72 horas

- [ ] Monitorizar errores HTTP, latencia, CPU, memoria, pool y disco.
- [ ] Revisar colas de búsqueda, DOI y correo.
- [ ] Confirmar backups automáticos.
- [ ] Revisar auditorías de seguridad y fijación.
- [ ] Mantener disponible el equipo de respuesta.

### Primeras 2–4 semanas

- [ ] Revisar incidencias y métricas con usuarios.
- [ ] Ejecutar primera restauración de control.
- [ ] Ejecutar primera auditoría de fijación completa.
- [ ] Ajustar capacidad y alertas.
- [ ] Elaborar informe de estabilización y deuda restante.

## Gate de salida de la fase 4

- [ ] Servicio estable durante el periodo acordado.
- [ ] Backup y restauración confirmados.
- [ ] Sin incidentes críticos pendientes.
- [ ] Operaciones acepta la plataforma como servicio regular.

# Fase 5 — Madurez y repositorio de confianza

## Objetivo

Pasar de una plataforma funcional a un repositorio institucional sostenible y evaluable.

## Trabajo

### Preservación

- [ ] Definir perfiles institucionales SIP, AIP y DIP.
- [ ] Aprobar formatos aceptados, preferidos y preservables.
- [ ] Definir migración de formatos y vigilancia tecnológica.
- [ ] Implementar y comprobar replicación geográfica.
- [ ] Definir tratamiento de contenido legado sin checksum original.
- [ ] Evaluar firma de manifiestos de preservación.

### CoreTrustSeal

- [ ] Asignar responsables a los 16 requisitos.
- [ ] Reunir políticas, evidencias y enlaces institucionales.
- [ ] Completar la autoevaluación interna.
- [ ] Realizar revisión independiente de la evidencia.
- [ ] Decidir si se solicita certificación formal.

### Gobierno y sostenibilidad

- [ ] Aprobar comunidad designada y alcance disciplinario.
- [ ] Aprobar plan de continuidad y transferencia/cese.
- [ ] Definir presupuesto, capacidad y ciclo de actualización.
- [ ] Revisar anualmente seguridad, privacidad y preservación.
- [ ] Publicar indicadores de servicio con metodología clara.

# Fase 6 — Nueva identidad visual

## Objetivo

Aplicar la identidad institucional sin perder claridad científica, accesibilidad ni compatibilidad funcional.

## Estado del kit

El kit **EXPLORA v1.1** fue recibido y revisado en
`EXPLORA_Kit_Identidad_Visual`. Contiene los insumos necesarios para iniciar el
trabajo visual cuando termine la estabilización prioritaria:

- manual de marca autocontenido en PDF y HTML;
- logotipo, isotipo, variantes claras/oscuras y favicons en SVG/PNG;
- tokens de color CSS/JSON y paleta documentada;
- especificación tipográfica Inter / IBM Plex Mono;
- textos, microtextos, SEO y mensajes de transparencia;
- banners, recursos responsive y vistas previas desktop/móvil;
- CSS y HTML de referencia para integración;
- biblioteca de iconos funcionales;
- criterios de aceptación para escritorio y móvil.

La demo del kit es una referencia de identidad, no un reemplazo directo de la
interfaz funcional. La integración debe conservar permisos, rutas, búsqueda en
servidor, filtros, paginación, internacionalización y estados científicos.

## Insumos necesarios

- [x] Manual de identidad visual EXPLORA v1.1.
- [x] Logotipos en SVG/PNG y variantes autorizadas.
- [x] Paleta y design tokens CSS/JSON.
- [x] Especificación de Inter e IBM Plex Mono.
- [x] Reglas y biblioteca de iconografía funcional.
- [x] Nombre, eslogan, posicionamiento y mensajes institucionales.
- [x] Criterios de aceptación responsive y de accesibilidad visual.
- [ ] Confirmar si las fuentes se alojarán localmente; el kit no incluye binarios.
- [ ] Confirmar aprobación final del kit por comunicación institucional.

## Trabajo

- [ ] Inventariar componentes y recorridos existentes.
- [ ] Mapear los tokens EXPLORA a las variables actuales sin duplicar estilos.
- [ ] Copiar sólo activos aprobados a una ruta de recursos versionada y estable.
- [ ] Crear tokens de diseño y biblioteca de componentes.
- [ ] Diseñar primero catálogo, ficha pública y depósito.
- [ ] Mantener DOI, versión, licencia, cita y acceso como jerarquía principal.
- [ ] Aplicar cabecera blanca de 72/64 px, contenido útil máximo de 1280 px y
      logo visible de 36/32 px según el manual.
- [ ] Validar que el menta no se utilice como texto pequeño sobre blanco.
- [ ] Mantener EXPLORA diferenciada de COSECHA en navegación y contenidos.
- [ ] Adaptar los textos del kit a las funciones realmente disponibles; no
      prometer apertura, descarga, DOI o preservación universal.
- [ ] Probar escritorio, móvil, teclado, zoom y lector de pantalla.
- [ ] Probar específicamente 1440, 1280, 768 y 390 px sin overflow horizontal.
- [ ] Validar prototipo con usuarios antes de modificar producción.
- [ ] Implementar por etapas sin mezclar rediseño con migraciones críticas.

## Gate de salida de la fase 6

- [ ] Identidad aprobada por comunicación institucional.
- [ ] Usabilidad aprobada por investigadores y curadores.
- [ ] WCAG 2.2 AA revisada manualmente.
- [ ] Regresión funcional y visual aprobada.

# 3. Roles sugeridos

| Rol | Responsabilidad principal |
|---|---|
| Product owner / responsable institucional | Prioridades, alcance y aceptación |
| Líder técnico | Arquitectura, calidad y releases |
| Desarrollo backend | API, seguridad, DOI, datos y preservación |
| Desarrollo frontend | Flujos, accesibilidad e identidad visual futura |
| DevOps / infraestructura | CI, staging, producción, backups y observabilidad |
| Seguridad | Threat model, secretos, auditoría y respuesta |
| Biblioteca / curación de datos | Metadatos, citas, vocabularios y DataCite |
| Responsable de preservación | OAIS, formatos, fijación y continuidad |
| Jurídico / privacidad | Datos sensibles, licencias, acceso y retirada |
| Investigadores piloto | Pruebas de depósito, descubrimiento y reutilización |

# 4. Tablero inicial recomendado

## Cierre técnico local completado el 30 de octubre de 2026

1. ZIP multiplataforma corregido y cubierto por pruebas.
2. Suite completa: 1382/1382 pruebas aprobadas.
3. Fuente problemático convertido a UTF-8 válido.
4. TLS 1.0/1.1 retirado de la configuración Gradle.
5. Digest OCFL predeterminado cambiado de MD5 a SHA-256.
6. `SECURITY.md` y modelo de amenazas inicial creados.

## Próximo sprint

1. Probar compatibilidad y transición OCFL con una copia controlada de datos existentes.
2. Diseñar el workflow CI mínimo, hacerlo obligatorio y proteger `main`.
3. Generar SBOM y escanear dependencias/contenedor.
4. Aprobar responsables, canal cifrado y modelo de amenazas.
3. Flyway o Liquibase.
4. Preparación de staging.
5. Ensayo de migración/restauración con copia representativa.
6. Validación DataCite Test, ORCID Sandbox, ROR y SMTP.
7. Pruebas humanas y de carga.

# 5. Indicadores de avance

- Porcentaje de pruebas aprobadas: objetivo 100 %.
- Vulnerabilidades críticas/altas sin decisión: objetivo 0.
- Tiempo de restauración medido frente al RTO.
- Pérdida máxima medida frente al RPO.
- Porcentaje de datasets publicados con licencia, versión, autor y checksum: objetivo 100 %.
- Porcentaje de DOI con resolución y relaciones válidas: objetivo 100 %.
- Auditorías de fijación completadas sin archivos no explicados.
- Recorridos críticos aprobados por usuarios y accesibilidad manual.
- Releases con SBOM, checksum, firma y procedencia: objetivo 100 %.

# 6. Condición de éxito

El proyecto estará listo para operación institucional cuando pueda demostrarse, no sólo declararse, que:

- el build es reproducible y está completamente verde;
- la actualización y la recuperación funcionan con datos representativos;
- los datasets publicados son inmutables, citables, íntegros y exportables;
- DOI, correo, almacenamiento y proxy funcionan en la infraestructura real;
- las políticas y responsables institucionales están aprobados;
- seguridad, observabilidad y backups forman parte de la operación diaria;
- el servicio puede evolucionar sin perder versiones, relaciones ni evidencias de preservación.
