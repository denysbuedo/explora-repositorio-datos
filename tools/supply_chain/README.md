# Evidencia de cadena de suministro

El build genera un SBOM CycloneDX directo para la aplicación y sus dependencias de compilación/runtime. El SBOM, el JAR y `SHA256SUMS` deben producirse en la misma ejecución:

```sh
./gradlew test bootJar cyclonedxDirectBom --no-daemon
sha256sum build/libs/base-repo.jar > build/libs/SHA256SUMS
python tools/supply_chain/verify_evidence.py \
  build/libs/base-repo.jar \
  build/libs/SHA256SUMS \
  build/reports/cyclonedx-direct/bom.json
```

La verificación comprueba el digest del JAR, el nombre de archivo, la identidad y versión del componente principal, la presencia de componentes y el grafo de dependencias. No comprueba vulnerabilidades ni firma criptográficamente los artefactos.

La publicación de releases debe adjuntar como mínimo:

- `base-repo.jar`;
- `SHA256SUMS` obtenido en el build confiable;
- `bom.json` y, si el consumidor lo necesita, `bom.xml`;
- referencia al commit y tag inmutables;
- resultado del análisis de vulnerabilidades y excepciones aprobadas.

No se debe afirmar procedencia SLSA o autenticidad mientras el repositorio no firme o atestigüe el JAR y el SBOM desde un workflow protegido con permisos OIDC controlados.
