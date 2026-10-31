# Lista de chequeo: propuesta inicial frente al estado implementado

**Proyecto:** `base-repo-mes`

**Revisión:** 30 de octubre de 2026

**Versión revisada:** commit `5cfc48e` en `main`

**Comparación base:** informes de septiembre de 2026 y cambios recibidos desde `c0ef5d4`

**Decisión de producto:** el rediseño y la nueva identidad visual se posponen para una fase posterior

## Leyenda

- ✅ **Implementado y con evidencia local:** existe código y prueba o evidencia reproducible en el repositorio.
- 🟡 **Parcial o pendiente de validación externa:** existe una base funcional, pero falta producción, aprobación institucional o prueba real.
- ⛔ **Pendiente:** no se encontró implementado o sigue siendo un bloqueador.
- ⚪ **Pospuesto por decisión:** se conserva como trabajo futuro, pero no forma parte de la fase actual.

## 1. Resultado ejecutivo de esta revisión

- ✅ El repositorio se actualizó mediante `fast-forward` de `c0ef5d4` a `5cfc48e`.
- ✅ No se realizó ningún `push`, commit, cambio de credenciales ni operación sobre producción.
- ✅ Los informes, PDF y prototipo locales no versionados se conservaron.
- ✅ Se incorporó una implementación extensa de funciones científicas, preservación, seguridad, búsqueda y operación.
- ✅ La suite completa está verde en Windows con JDK 21: `1382` pruebas ejecutadas, sin fallos, errores ni omisiones.
- ✅ Se corrigió `DatasetArchiveControllerTest.pagesAllFilesAndProducesReadableZip` mediante validación de rutas ZIP independiente de la plataforma.
- ✅ La compilación confirma que `DataCiteMessageConverter.java` está en UTF-8 válido; no reaparecen los errores de caracteres no representables.
- ⚪ El diseño visual no se evaluará ni modificará hasta recibir la nueva identidad visual.

### Regresión corregida

La creación del ZIP interno rechaza una ruta válida como `description/description.md` en Windows con:

```text
409 CONFLICT "Ruta de contenido no apta para el ZIP."
```

La causa estaba en `PublicDatasetArchiveController.safeRelativePath`: comparaba literalmente la cadena recibida con `Path.normalize().toString()`. En Windows, Java devuelve separadores `\`, mientras el nombre ZIP utiliza `/`.

**Corrección aplicada:** validación por segmentos `/`, rechazo explícito de rutas absolutas Windows/POSIX, traversal, segmentos vacíos y separadores invertidos. La prueba anidada y el caso `C:/...` pasan junto con la suite completa.

## 2. Calidad, pruebas y entrega

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| Reparar la suite heredada | ✅ | 1382 pruebas ejecutadas con JDK 21: 0 fallos, 0 errores y 0 omitidas. |
| Probar registro, verificación, login y recuperación | ✅ | Existen pruebas unitarias, integración SMTP sintética, recuperación ante error SMTP y `VerificationAccessTest`. |
| Probar roles, ownership y autorización por recurso | ✅ | Guards por recurso/estado/autoría, matrices de permisos y pruebas de rutas alternativas legacy. |
| Pruebas PostgreSQL reales | ✅ | Herramientas y evidencias de ensayos aislados PostgreSQL, dos JVM, migración y restauración sintética. |
| Testcontainers | ⛔ | No se encontró adopción de Testcontainers; los ensayos usan infraestructura y scripts propios. |
| Cobertura JaCoCo con umbral obligatorio | 🟡 | JaCoCo está configurado para informes, pero no se encontró un umbral de cobertura que falle el build. |
| CI obligatoria en GitHub | 🟡 | Existe workflow para `main`, `dev` y PR con suite completa, herramientas y evidencia; falta publicarlo y exigir el check mediante protección de ramas. |
| Contrato OpenAPI y compatibilidad | ✅ | Baseline y herramientas de comprobación de compatibilidad presentes. |
| Pruebas E2E de navegador | ✅ | Existen fixtures para flujos científicos, autenticación, administración, transferencia e i18n. |
| Accesibilidad automática | ✅ | Herramienta axe y pruebas de teclado/marcado; múltiples estados documentados sin infracciones automáticas. |
| Revisión manual WCAG 2.2 AA | 🟡 | Sigue pendiente con usuarios, lector de pantalla, zoom y recorridos reales. |
| Pruebas de carga y volumen real | 🟡 | Hay ensayos funcionales y de concurrencia; no se ha demostrado rendimiento con volumen productivo. |

## 3. Seguridad

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| Eliminar secreto JWT fijo del repositorio | ✅ | Los archivos usan variable o valor vacío; el preflight rechaza secretos de plantilla. |
| Eliminar administrador y contraseña predeterminados | ✅ | Bootstrap exige contraseña explícita, única y de al menos 12 caracteres; no crea admin por defecto. |
| Rate limiting para login/registro/verificación | ✅ | Servicio persistente y prueba de concurrencia compartida entre instancias. |
| Invalidar sesiones tras cambio de contraseña | ✅ | Versionado de contraseña y pruebas de tokens anteriores/nuevos. |
| Hacer públicos `verify` y `resend-verification` | ✅ | Prueba explícita para cuentas aún no verificadas. |
| Autorización por recurso y estado editorial | ✅ | Se protegen borradores, archivos, rutas codificadas, notas privadas y mutaciones de publicados. |
| Protección de ZIP y rutas de almacenamiento | ✅ | Confinamiento, límites y validación portable; se prueban rutas anidadas, traversal y rutas absolutas Windows. |
| Secret scanning | ✅ | Herramienta local de auditoría de secretos y pruebas asociadas. |
| Autenticación obligatoria en producción | 🟡 | El preflight de producción la exige, pero los archivos `application-default` y `application-docker` aún declaran `repo.auth.enabled:false`. |
| CORS restrictivo por defecto | 🟡 | El preflight exige origen HTTPS explícito, pero Docker conserva `allowedOriginPattern:*`. |
| Actuator mínimo y protegido | 🟡 | La preparación productiva lo valida, pero los ejemplos aún exponen `*`; Docker muestra detalles `ALWAYS`. |
| Sustituir `ddl-auto:update` por `validate` en producción | 🟡 | Preflight/update exigen `validate`; los archivos base siguen usando `update`. |
| Eliminar TLS 1.0 y TLS 1.1 | ✅ | `gradle.properties` permite únicamente TLS 1.2 y TLS 1.3. |
| Sustituir MD5 de OCFL por SHA-256/SHA-512 | 🟡 | La configuración predeterminada usa SHA-256 y existe una auditoría de inventarios/sidecars; falta probar el plugin y una copia de objetos OCFL existentes. |
| `SECURITY.md` y canal de reporte | 🟡 | Se añadió política, contacto y tiempos objetivo; falta aprobación institucional y formalizar un canal cifrado. |
| Modelo formal de amenazas | 🟡 | Se añadió `docs/THREAT_MODEL.md`; falta revisión y firma de desarrollo, operaciones y responsable científico. |
| SAST/SCA dentro de pipeline | 🟡 | CodeQL y OWASP Dependency-Check están definidos con política y umbral; falta primera ejecución en GitHub, NVD institucional y checks obligatorios. |

## 4. Identidad, publicación y citación científica

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| Ciclo borrador → revisión → publicación → nueva versión | ✅ | `ScientificRecord`, estados editoriales, revisión, guards e historial público. |
| Inmutabilidad de versiones publicadas | ✅ | Mutaciones bloqueadas y correcciones mediante nueva versión. |
| DOI conceptual y DOI por versión | ✅ | Workflow recuperable, relaciones familiares y registro local de confirmaciones. |
| Reserva y publicación DOI idempotentes | ✅ | `DoiWorkflowService`, concurrencia, conciliación y pruebas de fallos parciales. |
| Integración real con DataCite | 🟡 | Cliente y workflow completos con HTTP simulado; la evidencia de esta revisión no publica DOI reales ni valida resolución pública productiva. |
| DataCite 4.6 y validación externa | 🟡 | Existe mapper y herramienta de validación externa; debe confirmarse con la cuenta y esquema operativos de DataCite. |
| Citación de la versión exacta | ✅ | Endpoints y ficha pública ofrecen cita ligada a versión. |
| APA, Vancouver, Chicago, IEEE | 🟡 | Existen formatos y pruebas de round-trip; la validación bibliotecaria figura pendiente. |
| Exportar BibTeX, RIS y CSL-JSON | ✅ | Controladores, exportaciones y herramientas de comprobación presentes. |
| Relaciones con artículos, software y datasets | ✅ | Relaciones tipadas DataCite y relaciones inversas/familiares. |
| ORCID por creador | ✅ | Identidad estructurada y OAuth server-side con protección de state/replay. |
| Validación ORCID Sandbox/producción | 🟡 | Implementación y pruebas locales completas; callback y credenciales institucionales requieren validación externa. |
| ROR para afiliaciones | ✅ | Afiliaciones múltiples y búsqueda ROR acotada. |
| ROR desde VM productiva | 🟡 | Falta verificar conectividad/proxy y valores institucionales reales. |
| Proyectos y financiación | ✅ | Modelo estructurado, filtros y proyección DataCite. |
| Licencia y acceso explícitos | ✅ | Metadatos, privacidad, embargo y reglas de publicación. |
| Retirada con landing permanente | ✅ | Estados retirados e historial público sin exponer borradores. |
| Metadatos multilingües | ✅ | Modelo localizado y catálogos español/inglés. |
| Vocabularios controlados | 🟡 | Registro, propuestas y aprobación implementados; falta aprobación institucional y migración antes del modo estricto. |
| Perfiles institucionales de metadatos | 🟡 | Herramienta y congelación por versión implementadas; perfiles definitivos requieren aprobación. |

## 5. Catálogo y flujo de depósito

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| Búsqueda y paginación en servidor | ✅ | Catálogo científico con paginación estable y pruebas JPA/PostgreSQL. |
| Filtros facetados | ✅ | Autor, área/tipo, año, licencia, institución, disciplina, idioma, acceso, formato y DOI. |
| Estado vacío, sin permisos y error de servicio diferenciados | ✅ | Estados y acciones de recuperación implementados. |
| Mantener filtros/página en URL e historial | ✅ | Implementado y probado en navegador. |
| Asistente guiado de depósito | ✅ | Nueve etapas, autosave, requisitos, vista previa y recuperación. |
| Carga Markdown, ZIP descriptivo y ZIP completo | ✅ | Flujos, límites y pruebas E2E presentes. |
| Acceso temporal para revisores | ✅ | Enlaces con expiración, revocación, descarga protegida y `no-store`. |
| Privacidad y datos sensibles | ✅ | Declaración, evaluación curatorial y bloqueo de publicación cuando corresponde. |
| Colecciones temáticas/institucionales | ✅ | CRUD curatorial, membresías y visibilidad pública controlada. |
| Prueba con investigadores/curadores reales | 🟡 | Sólo se acredita validación local/sintética; falta aceptación humana institucional. |
| Nuevo diseño visual | ⚪ | Pospuesto hasta recibir la nueva identidad visual. No deben consolidarse los prototipos anteriores como interfaz final. |

## 6. Integridad, procedencia y preservación

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| SHA-256 al ingresar archivos | ✅ | Cálculo streaming, baseline y evento de procedencia append-only. |
| Auditorías periódicas de fijación | ✅ | Auditoría, resultados persistentes, locks y alertas opcionales por correo. |
| Mostrar integridad y manifestaciones | ✅ | Endpoints y paquetes de preservación con hashes. |
| RO-Crate | ✅ | Generador y paquete curatorial implementados y probados localmente. |
| W3C PROV-O | ✅ | Exportación de eventos técnicos y declaración científica sin inventar ejecuciones. |
| BagIt | ✅ | Manifiestos payload/tag SHA-256 y exportación curatorial. |
| SIP/AIP/DIP conforme a OAIS | 🟡 | Existe una base técnica, pero faltan perfiles institucionales aprobados y evidencia de conformidad. |
| Autoevaluación CoreTrustSeal | 🟡 | Herramienta interna de 16 requisitos implementada; evidencia organizativa y certificación externa pendientes. |
| Replicación geográfica | ⛔ | No se encontró acreditación de varias copias geográficas operativas. |
| Backups y restauración | 🟡 | Herramientas seguras y ensayos sintéticos aprobados; falta copia real de staging/producción, tiempos, RPO/RTO y restauración institucional. |
| Plan de continuidad y salida | 🟡 | Hay documentación operativa, pero requiere responsables, aprobación y evidencia institucional. |
| Planificación/migración de formatos | 🟡 | Metadatos de formato y políticas parciales; falta política institucional operativa de formatos obsoletos. |
| Archivos heredados fuera de `repo.basepath` | 🟡 | Existe herramienta de inventario; debe ejecutarse sobre copia real y resolverse cada anomalía. |

## 7. Operación, despliegue y cadena de suministro

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| PostgreSQL de referencia | ✅ | Migración SQL y ensayos PostgreSQL documentados. |
| Flyway o Liquibase | ⛔ | Hay migración SQL y scripts propios, pero no un motor de migración versionada integrado. |
| Ensayo de migración y restauración | ✅ | Automatización local idempotente con datos sintéticos. |
| Actualización manual segura | ✅ | `update.sh`, checksum, bloqueo, backup y rollback controlado sin recrear DB. |
| Preflight de producción | ✅ | Valida configuración, secretos, PostgreSQL, CORS, SMTP, Actuator y persistencia. |
| Contrato y compatibilidad de API | ✅ | Baseline y validadores presentes. |
| Métricas locales de uso | ✅ | Implementadas con controles de privacidad; no se presentan como COUNTER certificado. |
| Logs estructurados, correlation ID y OpenTelemetry | 🟡 | Hay auditoría y métricas, pero no se encontró una instrumentación OpenTelemetry completa. |
| Prometheus/alertas operativas | 🟡 | Actuator y alertas específicas de fijación; falta demostrar plataforma de monitorización y alertado productiva. |
| SBOM SPDX | ⛔ | No se encontró generación de SBOM SPDX/CycloneDX dentro del build/release. |
| Firma de imagen/JAR y procedencia SLSA | ⛔ | Se verifican hashes, pero no firma criptográfica ni attestations de procedencia. |
| Contenedor sin root y runtime mínimo | 🟡 | No se encontró evidencia suficiente de cierre; debe revisarse en la imagen candidata final. |
| Escaneo de contenedor | ⛔ | No se encontró Trivy/Grype u otro gate de imagen integrado. |
| CI/CD alojado | ⛔ | No hay workflows GitHub; la entrega sigue siendo manual. |
| Publicación por tag y release inmutable | 🟡 | Política y herramientas preparadas; la evidencia local indica que no se creó Release/tag productivo durante esos trabajos. |

## 8. Documentación y gobernanza

| Propuesta original | Estado | Evidencia y observación |
|---|---:|---|
| Política de versión y despliegue | ✅ | `docs/VERSIONING.md`, runbook y herramientas de release. |
| Guía de citación y uso | ✅ | Ayuda pública y documentación DataCite. |
| Política de privacidad y workflow | 🟡 | Workflow técnico documentado; aprobación jurídica/institucional sigue externa. |
| Política de preservación | 🟡 | Capacidades y documentación técnica; falta política institucional aprobada. |
| Política de acceso y licencias | 🟡 | Reglas técnicas implementadas; la administración debe aprobarlas. |
| Responsables institucionales | 🟡 | `INSTITUTIONAL_ACCEPTANCE.md` identifica entregas y roles; deben asignarse formalmente. |
| RPO/RTO y recuperación | ⛔ | Deben definirse, aprobarse y probarse con infraestructura real. |
| Canal de seguridad | 🟡 | `SECURITY.md` define recepción y escalamiento; falta aprobar el responsable nominal y el canal cifrado. |
| Manual de operación | ✅ | `PRODUCTION_RUNBOOK.md` y documentación de consola/actualización. |
| Evidencia de cumplimiento/certificación | 🟡 | La herramienta evita afirmar certificación; CoreTrustSeal, OAIS y WCAG continúan sin certificación externa. |

## 9. Prioridades recomendadas a partir de ahora

### P0 — Antes de aceptar otro cierre técnico

- [x] Corregir la prueba ZIP y la validación multiplataforma de rutas.
- [x] Ejecutar nuevamente la suite —1382 pruebas— hasta obtener cero fallos.
- [x] Eliminar TLS 1.0/1.1 de `gradle.properties`.
- [x] Cambiar MD5 por SHA-256 en la configuración OCFL.
- [x] Añadir `SECURITY.md` y un modelo de amenazas inicial.
- [ ] Probar la transición OCFL con una copia controlada de objetos existentes.
- [x] Incorporar auditoría OCFL de solo lectura y pruebas sintéticas MD5/SHA-256.
- [ ] Decidir si los ejemplos inseguros deben convertirse en perfiles explícitos de desarrollo para evitar despliegues accidentales.

### P1 — Antes de staging institucional

- [ ] Ejecutar migración y restauración con copia real de staging y medir duración.
- [ ] Inventariar `contentUri` heredados fuera de `repo.basepath`.
- [ ] Validar DataCite real, DOI conceptual/de versión y resolución pública.
- [ ] Validar ORCID Sandbox y ROR desde la infraestructura institucional.
- [ ] Aprobar vocabularios, perfiles de metadatos, licencias y política de privacidad.
- [ ] Validar citas con biblioteca/servicio editorial.
- [ ] Probar archivos grandes, interrupciones reales y concurrencia detrás de HAProxy.
- [ ] Realizar revisión funcional y WCAG manual con usuarios reales.

### P2 — Antes de producción o certificación

- [ ] Definir RPO, RTO, retención, replicación y restauraciones periódicas.
- [ ] Completar perfiles institucionales OAIS SIP/AIP/DIP.
- [ ] Completar expediente y evidencias CoreTrustSeal sin afirmar certificación anticipada.
- [ ] Incorporar CI obligatoria, SBOM, firma/procedencia y escaneo de artefactos.
- [ ] Ejecutar auditoría de seguridad y carga independiente.
- [ ] Validar supervisión no-root, HAProxy, SMTP y alertas en la VM real.

### P3 — Diseño e identidad visual

- [x] Recibir manual de identidad, logotipos, paleta, tipografía y recursos disponibles en `EXPLORA_Kit_Identidad_Visual`.
- [ ] Definir componentes visuales reutilizables sin alterar el modelo científico ya implementado.
- [ ] Prototipar catálogo, depósito y ficha pública con la nueva identidad.
- [ ] Validar con investigadores, curadores y biblioteca antes de implementar.

## 10. Conclusión

La mayor parte del **núcleo funcional científico** propuesto ya tiene una implementación local sustancial: publicación versionada, DOI, DataCite, citación, ORCID/ROR, relaciones, búsqueda facetada, revisión, privacidad, fijación, RO-Crate, PROV-O y BagIt.

El proyecto todavía no debe considerarse completamente cerrado porque:

1. falta validar en staging la migración/compatibilidad OCFL tras adoptar SHA-256;
2. permanecen configuraciones base inseguras o heredadas —CORS/Actuator y autenticación desactivada en ejemplos— aunque exista un preflight productivo;
3. faltan CI, SBOM, firma y gates modernos de cadena de suministro;
4. OAIS, CoreTrustSeal y WCAG requieren decisiones, pruebas y evidencia institucional externa;
5. staging y producción reales todavía deben demostrar migración, recuperación, DOI, correo, proxy, capacidad y seguridad.

El rediseño visual queda correctamente pospuesto. La siguiente etapa debe cerrar primero la regresión, los valores criptográficos obsoletos y la validación institucional de staging.
