# AuthLens

**Análisis offline de autenticaciones con evidencia que podés inspeccionar.**

[English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md)

Python 3.11+ · MIT · v0.1.0 · sin dependencias de runtime. **Portfolio ready con limitaciones documentadas**; la evaluación controlada sigue siendo sintética y no se afirma revisión editorial por hablantes nativos. [Evidencia de release](docs/release-readiness.md).

## Por qué existe

Investigar una exportación de autenticaciones no debería exigir subir logs sensibles ni desplegar un SIEM. AuthLens correlaciona eventos y muestra qué registros sustentan cada indicio y qué datos descartó. Un indicio requiere investigación; no demuestra compromiso.

## Funciones

Parsers SSH y JSONL estricto; normalización UTC; ventanas inclusivas; detección de fallos repetidos, fallos contra varias cuentas y éxito posterior a fallos. Incluye exclusiones, deduplicación, hash SHA-256, referencias a líneas, calidad de entrada, logs estructurados y reportes text/JSON/CSV/Markdown/HTML en cuatro idiomas. No hace conexiones ni intenta autenticaciones.

## Demo

Los datos son sintéticos y usan IPs reservadas para documentación:

```console
authlens analyze examples/ssh-demo.log --input-format ssh --lang es
authlens analyze examples/events.jsonl --format html --output informe-demo.html --lang es
```

La demo genera AL-001 (cinco fallos de alice), AL-003 (éxito posterior) y AL-002 (cinco cuentas distintas). [Resultado esperado](examples/expected-findings.json).

## Arquitectura

Archivo acotado + hash → parser → eventos UTC → exclusiones/deduplicación → ventanas con deques y contadores → findings con evidencia → exportadores localizados. El motor no depende de la CLI ni del formato de reporte. [Arquitectura](docs/architecture.md), [decisiones técnicas](docs/adr/0001-language.md).

## Instalación

Python 3.11–3.14. En Linux/macOS, desde el directorio del proyecto:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
```

En Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install .
.venv\Scripts\authlens.exe --help
```

Sin activar el entorno, reemplazá `authlens` por `.venv\Scripts\authlens.exe`. La instalación puede descargar herramientas de build; la ejecución es offline. No se afirma publicación en PyPI. GitHub Actions valida Ubuntu, Windows y macOS con Python 3.11–3.14; la verificación local de release también se realizó en Windows/Python 3.12.

## Inicio rápido

```console
authlens analyze examples/events.jsonl --lang es
authlens analyze examples/events.jsonl --format json --output reporte.json
```

La salida debe tener un nombre nuevo. Guardala en un directorio privado: contiene usuarios e IPs.

## Uso

```console
authlens analyze --help
authlens analyze examples/events.jsonl --window-seconds 60 --burst-threshold 5
authlens analyze examples/events.jsonl --exclude-cidr 198.51.100.0/24 --exclude-user healthcheck
authlens analyze examples/events.jsonl --strict --fail-on MEDIUM --format json --log-file ejecucion.log
authlens analyze auth.log --input-format ssh --year 2026 --timezone=-03:00
```

Códigos: 0 completo; 1 umbral de `--fail-on`; 2 argumentos/config; 3 I/O/límite; 4 entrada parcial, malformada o sin eventos analizables; 130 cancelación. La entrada parcial tiene prioridad sobre los findings. stdout contiene el reporte; stderr, los diagnósticos. `--quiet` mantiene reporte y errores; `--verbose` agrega conteos. El texto no usa colores.

## Salida

JSON `schema_version=1.0` conserva versión, fecha UTC, hash, conteos, diagnósticos y configuración efectiva. Cada finding separa observación, inferencia, hipótesis, recomendación y explicaciones benignas; incluye severidad, confianza cualitativa, parámetros, referencias y hasta 20 eventos de evidencia. IDs/claves/enums no se traducen. Solo se reporta el primer episodio que alcanza el umbral por regla/grupo. CSV vacío contiene solo cabeceras; usá JSON para conservar calidad cuando no hay findings. [Esquema](docs/report-schema.json).

## Configuración

`--config examples/config.toml`; CLI > TOML explícito > valores predeterminados. Claves desconocidas o tipos/rangos incorrectos producen error. Predeterminados: ventana de 300 segundos, umbrales de 5, 16 MiB de archivo, 16 KiB por línea y 50.000 registros válidos antes de excluir/deduplicar. [Referencia completa](docs/configuration.md).

## Idiomas

`--lang es`, `en`, `ru` o `zh-CN`; también `language = "es"` en TOML. Sin selección, se consulta el locale del sistema y se usa inglés como fallback. Catálogos reales instalados en el paquete; pruebas de claves y placeholders. Se agradece revisión por hablantes nativos, sin afirmar una certificación lingüística.

## Seguridad

No se conservan líneas originales ni sufijos SSH en reportes. Los logs de ejecución omiten identidades, rutas y contenido de entrada. Los reportes escapan contenido y neutralizan fórmulas CSV. Nunca se sobrescriben archivos. POSIX usa 0600; Windows hereda ACLs del directorio. [Política](SECURITY.md), [modelo de amenazas](THREAT_MODEL.md).

## Alcance / autorización

Analizá solo logs propios o autorizados. El scope es un archivo local y sus exclusiones. Usá exportaciones inmutables y directorios bajo tu control. El hash identifica bytes procesados; no certifica autenticidad ni cadena de custodia.

## Limitaciones

No admite cualquier variante de syslog, EVTX, VPN ni logs web nativos. JSONL exige el esquema documentado. Timestamps tradicionales necesitan año y offset fijo; se rechazan retrocesos sin adivinar cambio de año ni DST. No hay GeoIP, reputación, atribución, ML ni detección de ataques lentos/distribuidos. Duplicados exactos pueden ser eventos legítimos a precisión temporal baja; `--keep-duplicates` los conserva. Los límites reducen riesgo, pero no garantizan un consumo fijo de RAM.

## Falsos positivos

Reintentos, credenciales vencidas de automatización, NAT compartido, QA y problemas de SSO pueden generar los mismos patrones. Un éxito tras fallos puede ser recuperación legítima. Sin contraseñas intentadas no se confirma password spraying. MEDIUM/HIGH indican prioridad de revisión, no CVSS. [Semántica de reglas](docs/detection-logic.md).

## Desarrollo

```console
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m ruff check src tests scripts evaluation
python -m ruff format --check src tests scripts evaluation
```

[Cómo contribuir](CONTRIBUTING.md). Cada nueva regla necesita un problema concreto, evidencia, contraejemplos y pruebas. La documentación técnica detallada está en inglés.

## Pruebas

```console
python -m pytest --cov=authlens --cov-report=term-missing
python -m bandit -r src -q
python -m pip_audit -r requirements-dev.txt
python -m build
python scripts/benchmark.py
```

La suite incluye ventanas, Unicode, entradas hostiles, i18n, exportadores y CLI real. Coverage incluye subprocesos. Las pruebas que requieran privilegios no disponibles informan el skip. La auditoría de dependencias requiere red.

## Roadmap

Trabajo futuro: validación con datos representativos, episodios múltiples, nuevos adapters y pseudonimización; no son funciones implementadas. [Fases](docs/development-phases.md), [texto para portfolio](docs/portfolio.md).

## Licencia

[MIT](LICENSE).
