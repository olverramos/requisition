# Análisis del proyecto y lista de mejoras

**Proyecto:** ARVII Requisition App (Django + MongoDB/MongoEngine)
**Fecha del análisis:** 2026-11-13
**Alcance:** código de `core/`, `home/`, `modules/`, configuración, dependencias, scripts y datos versionados.

---

## 1. Resumen ejecutivo

La aplicación es funcional y tiene una estructura modular clara, pero presenta **riesgos críticos de seguridad**, una **arquitectura con lógica de negocio concentrada en vistas muy grandes**, un **modelo de datos con comparaciones frágiles de estados**, y **ausencia total de pruebas automatizadas y CI**.

Hallazgos más graves:

1. **Credenciales de producción expuestas en el repositorio** (MongoDB, SendGrid, `DJANGO_SECRET_KEY`, contraseña de correo, contraseñas de usuarios semilla).
2. **El endpoint `/devtools/appspecific/com.chrome.devtools.json` publica el `SECRET_KEY`**.
3. **Vistas sin autenticación** que permiten crear/leer/eliminar solicitudes y documentos de terceros (IDOR).
4. **`AccountSetPasswordView` permite cambiar la contraseña de cualquier cuenta sin iniciar sesión**.
5. **Tareas sensibles sin verificación de rol en el backend** (solo se oculta en la UI).
6. **DEBUG=TRUE y `ALLOWED_HOSTS=['*']`** en configuración de producción.
7. **Django 3.2 (EOL) y `django-mongoengine` sin mantenimiento**.
8. **Cero pruebas automatizadas**.

Se recomienda atender primero los puntos de la sección 2 antes de cualquier nueva funcionalidad.

---

## 2. Seguridad (prioridad CRÍTICA)

### 2.1 Secretos y credenciales expuestas

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C1 | Contraseña de MongoDB en claro en scripts versionados | `heroku_config.sh:3`, `connect_db.sh:11`, `connect_local_db.sh:1`, `init_mongodb.mongo:3` | **Rotar credenciales** y eliminar del historial (`git filter-repo`/BFG). Usar variables de entorno. |
| C2 | `SENDGRID_API_KEY`, `DJANGO_SECRET_KEY`, `EMAIL_HOST_PASSWORD` en claro | `heroku_config.sh:19-24` (versionado) | Rotar todas las claves. Nunca versionar secretos. |
| C3 | Archivo `.env` con credenciales reales de producción en el árbol de trabajo | `core/.env` | Está en `.gitignore`, pero confirmar que nunca se subió. Rotar por precaución. Mover a `BASE_DIR/.env`. |
| C4 | Contraseñas de usuarios semilla en texto plano | `modules/authentication/scripts/data/accounts.json:7,21,35,...` | Eliminar el archivo del repo, usar variables/secret manager y obligar cambio de contraseña. |
| C5 | Credenciales por defecto en código | `core/settings.py:290` (`EMAIL_HOST_PASSWORD`), `core/settings.py:46-49` (`SECRET_KEY` aleatorio por proceso) | Sin valores por defecto: fallar al iniciar si falta la variable. |
| C6 | Volcado completo de la base con datos personales en el repo | `export/dump_requisitiondb_20261113/` (no versionado aún, sin ignorar) | Añadir `export/` a `.gitignore`, borrar el dump del disco/repo y tratarlo como dato sensible. |

> **Acción inmediata:** rotar MongoDB, SendGrid, Gmail app password y `DJANGO_SECRET_KEY`; asumir que todas están comprometidas.

### 2.2 Exposición directa de información

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C7 | Endpoint público devuelve el `SECRET_KEY` y la ruta del proyecto | `home/views.py:40-46`, `core/urls.py:18` | **Eliminar** la vista y la ruta. |
| C8 | Archivo de verificación servido con ruta absoluta de Heroku | `home/views.py:37-38` | Servir desde `STATIC_ROOT`/`.well-known` configurable. |
| C9 | `SECRET_KEY` aleatorio en cada arranque si falta la variable | `core/settings.py:46-49` | Fallo explícito (`ImproperlyConfigured`) si no está definido. Invalidaría sesiones y enlaces. |

### 2.3 Control de acceso / autenticación

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C10 | `AccountSetPasswordView` **sin `login_required`** permite fijar la contraseña de cualquier `account_id` | `modules/authentication/views.py:175-207`, `urls.py:16` | Exigir autenticación + rol ADMIN o ser la propia cuenta; validar con `validate_password`. |
| C11 | `AccountGenerateConfirmView` sin autenticación: reenvía correo de activación para cualquier cuenta | `modules/authentication/views.py:682-690` | Exigir autenticación y rol. |
| C12 | Registro público asigna rol `ASSISTANT` | `modules/authentication/views.py:70-125` | Rol por defecto `APPLICANT`/sin privilegios; activación manual o por invitación. |
| C13 | `create_account_view` crea usuario con contraseña vacía y `is_active=True` | `modules/authentication/views.py:405-413` | Generar token de activación y forzar establecimiento de contraseña. Verificar login con contraseña vacía. |
| C14 | Vistas sin `login_required` que leen/crean/borran datos: búsquedas, creación de solicitud, consulta, pago, documentos | `modules/operative/views.py:155,257,350,500,713,911,1010,1111,1177,1195` | Aplicar `login_required` y autorización por rol/propietario. |
| C15 | Eliminación y edición de documentos/solicitudes sin verificar propietario ni rol | `modules/operative/views.py:673,813,850,1195` | Autorización a nivel de objeto (solicitud pertenece al solicitante o al asistente asignado). |
| C16 | `get_account_view` expone datos de cualquier cuenta a cualquier usuario autenticado | `modules/authentication/views.py:564-597` | Limitar a ADMIN o a la propia cuenta. |
| C17 | `activate/delete/edit` de cuentas sin verificación de rol | `modules/authentication/views.py:441,517,538` | Comprobar `role == ADMIN` en backend, no solo ocultar botones. |
| C18 | Transiciones de estado sin validar rol ni estado actual | `modules/operative/views.py:673-707,813-848` | Máquina de estados + permisos por rol. |

### 2.4 Configuración de producción

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C19 | `DEBUG=TRUE` en configuración de producción | `core/.env`, `heroku_config.sh:17` | `DEBUG=False` obligatorio en producción. |
| C20 | `ALLOWED_HOSTS = ['*']` en ambas ramas | `core/settings.py:51-55` | Lista explícita desde variable de entorno. |
| C21 | `CSRF_TRUSTED_ORIGINS` solo local | `core/settings.py:58` | Incluir dominio de producción desde entorno. |
| C22 | Faltan flags de seguridad | `core/settings.py` | Añadir `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SECURE_HSTS_*`, `SECURE_PROXY_SSL_HEADER`, `SECURE_CONTENT_TYPE_NOSNIFF`, CSP. |
| C23 | `load_dotenv()` sin ruta: no encuentra `core/.env` si se ejecuta desde la raíz | `core/settings.py:21`, `core/.env` | `load_dotenv(BASE_DIR / '.env')` y definir `BASE_DIR` antes. |
| C24 | Carga silenciosa de `settings_debug.py` dentro de `try/except` | `core/settings.py:37-40` | Usar variables de entorno; no ocultar errores de importación. |

### 2.5 Tokens y correo

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C25 | Tokens de reseteo/confirmación son base64 reversible de `id|expiración`, sin firma ni hash en BD | `modules/authentication/models.py:313-363` | Usar `default_token_generator` de Django o tokens firmados (`signing.dumps`) con hash en BD y un solo uso real. |
| C26 | `max_times` no se aplica | `modules/authentication/models.py:322-327` | Validar y decrementar/invalidar de forma atómica. |
| C27 | Enlaces de reseteo/confirmación se acortan con TinyURL (el token se comparte con un tercero) | `modules/authentication/models.py:162-168,190-196` | **No usar acortadores externos**; usar el dominio propio. |
| C28 | Sin rate limiting en login, reseteo ni registro | `modules/authentication/views.py` | Añadir `django-axes`/throttling y bloqueo por intentos. |
| C29 | Enumeración de cuentas en el mensaje de reseteo | `modules/authentication/views.py:53` | Mensaje genérico siempre. |
| C30 | Envío de correo síncrono dentro de la petición HTTP | `core/utils.py:37-62` | Mover a tarea en segundo plano con timeout y reintentos. |

### 2.6 Subida de archivos

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| C31 | `FileField` sin límite de tamaño ni tipo MIME; contenido se guarda en base64 dentro de Mongo | `modules/operative/forms.py:336-403,586-653,1001-1046,1167-1190,1454,1483`; `views.py:744,1132` | Validar tamaño (p. ej. 5–10 MB), extensión/MIME real y almacenar en GridFS/S3, no en el documento. |
| C32 | Límite de 16 MB por documento de MongoDB | `modules/operative/models.py:60-68,93-100` | Igual que C31. |
| C33 | Documentos completos (base64) se cargan en listados | `modules/operative/views.py:1010-1046` | Excluir `content` en consultas de listado (`.exclude('content')`/proyección). |
| C34 | XSS almacenado potencial al inyectar datos del servidor con `innerHTML`/`.html()` | `modules/operative/static/js/requests/*.js`, `requestdocuments/index.js`, `authentication/static/js/*.js` | Construir DOM con `textContent` o escapar HTML; validar/sanitizar entradas. |

---

## 3. Prioridad ALTA (correctitud y negocio)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| A1 | Estados comparados como texto (`'4'`, `'9'`, `id < id`), se rompe con IDs de 2 dígitos | `modules/operative/views.py:37,167,268,516,866,1027,1031,1155`; `models.py:282` | Enum/`TextChoices`, campo `code` entero o comparación por orden explícito. |
| A2 | Números de solicitud consecutivos con `max + 1` sin atomicidad: duplicados en concurrencia | `modules/operative/models.py:253-260`, `views.py:440` | Secuencia atómica (`find_one_and_update` con `$inc`) + índice único en `number`. |
| A3 | `payment_register_request_view` devuelve una URL (no redirige) y `request_status` puede quedar sin definir | `modules/operative/views.py:713-810` | Usar `redirect()`; inicializar/validar estado; cubrir casos con un solo comprobante. |
| A4 | `create_request_view` puede acceder a `applicant.email` con `applicant=None` | `modules/operative/views.py:380-410` | Validar solicitante obligatorio antes de usar. |
| A5 | `edit_request_view` guarda el tomador aunque falle la validación del valor; `ramo` puede ser `None` | `modules/operative/views.py:600-660` | Validar todo antes de cualquier escritura; usar transacción. |
| A6 | Escrituras multi-documento sin transacción (solicitud + evento + documento) | `modules/operative/views.py` (varios) | Sesiones/transacciones de MongoDB o patrón outbox. |
| A7 | `update_status` reutiliza `operative_request_status` entre iteraciones (fuga de estado) | `modules/operative/models.py:262-285` | Reiniciar por solicitud; tests de regresión. |
| A8 | `OperativeRequest.init_table` puede lanzar `UnboundLocalError` (`field`) | `modules/operative/models.py:355-370` | Inicializar y validar antes de `append`. |
| A9 | `RamoField.init_table` usa `datetime.now()` sobre el módulo `datetime` y asigna `options` inexistente | `modules/parameters/models.py:114,122-124` | Corregir a `datetime.datetime.now()` y eliminar `options`. |
| A10 | Archivo de semilla `documentclasses.json` no existe | `modules/parameters/models.py:193`, `parameters/scripts/data/` | Añadir el archivo o manejar el error explícitamente. |
| A11 | Typos de modelo: `dafault=False` y `null=-True` | `modules/parameters/models.py:69,226`; `localization/models.py:47` | Corregir a `default` y `null=True`. |
| A12 | Rol con typo `assitant` usado en código y filtros | `modules/authentication/models.py:44` | Unificar constante; migrar datos existentes. |
| A13 | `date/time` con `datetime.datetime.now()` (naive) y `USE_TZ=True` | Todo el proyecto | Usar `django.utils.timezone.now()` (aware) o `timezone.localtime`. |
| A14 | Validación de contraseñas omitida (`set_password` directo) | `modules/authentication/views.py:194,362,658`; `models.py:140` | Llamar `validate_password` antes de guardar. |
| A15 | Campos de auditoría mal escritos (`update_at`, `update_by`) no se guardan | `modules/authentication/views.py:195-196,553` | Corregir a `updated_at`/`updated_by`. |
| A16 | Validación de formularios incompleta (`required=False` en campos clave) | `modules/operative/forms.py:190-260` | Hacer obligatorios `ramo`, `status`, tipos de documento, etc. |
| A17 | Paginación: `int(page)` sin control puede devolver 500; página 0 produce offset negativo; no se limita a `total_pages` | `core/utils.py:6-31`; múltiples vistas | Validar y normalizar `page`; helper reutilizable. |
| A18 | `ITEMS_PER_PAGE=10` pero las vistas usan 20 | `core/settings.py:238`; `views.py:114,233,336` | Unificar. |
| A19 | Filtro de fecha y búsqueda capturan `Exception` genérica y muestran el error al usuario | `modules/operative/views.py:107-121` | Manejar errores específicos y registrar el detalle. |
| A20 | `delete_request_view`: si `error` es `None` en GET, muestra mensaje "None" | `modules/operative/views.py:890` | Corregir flujo de mensajes. |

---

## 4. Arquitectura y mantenibilidad (prioridad MEDIA-ALTA)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| M1 | Vistas gigantes con lógica de negocio, validación y acceso a datos | `modules/operative/views.py` (1211 líneas), `authentication/views.py` (691) | Separar en `services/`, `selectors/`, formularios y vistas delgadas. |
| M2 | Formularios duplicados (mismos campos repetidos en varios forms) | `modules/operative/forms.py` (1499 líneas) | Herencia/base Mixin de formularios; reutilizar widgets. |
| M3 | Duplicación masiva de `try/except DoesNotExist` y mapeo de IDs | Varias vistas | Helpers (`get_or_none`) y servicios centralizados. |
| M4 | Lógica de datos y semillas/migraciones dentro de los modelos | `init_table`, `fix_*`, `migrate_documents` en `modules/*/models.py` | Mover a `management/commands/` y borrar migraciones ad-hoc ya aplicadas. |
| M5 | Código muerto/duplicado entre `get_request_view` y `OperativeRequest.query()` | `operative/views.py:911-1008`, `models.py:395-483` | Un solo serializador. |
| M6 | Módulo `auths` solo existe como `.pyc` y está referenciado (`'auths.Account'`) | `modules/auths/`, `modules/operative/models.py:105` | Eliminar y corregir la referencia a `authentication.Account` (o restaurar el módulo). |
| M7 | Lógica de autorización replicada con condicionales de rol en cada vista | `operative/views.py`, `authentication/views.py` | Decoradores/mixins de permisos reutilizables. |
| M8 | `context_processor` consulta `Account` en cada request y define el menú en código | `core/template_processor.py:1-57` | Cachear la cuenta en sesión/request y mover el menú a configuración/BD. |
| M9 | Mezcla de español/inglés en nombres, comentarios y textos | Todo el proyecto | Convención única (p. ej. dominio en español, código en inglés) documentada. |
| M10 | Sin tipado estático ni linter configurado (solo caché de Ruff) | Raíz | Añadir `pyproject.toml` con Ruff, mypy/pyright opcional y pre-commit. |
| M11 | Sin documentación funcional/técnica ni README real | `README.md` (vacío de contenido útil) | Documentar arquitectura, variables de entorno, despliegue y flujos. |
| M12 | `core/project.py` y `settings.py` definen `APP_URL` de forma contradictoria | `core/project.py:5`, `core/settings.py:27-29` | Fuente única desde entorno. |
| M13 | Código de depuración/scratch versionado (`test.py`) y scripts con credenciales | `test.py`, `connect_*.sh`, `heroku_config.sh` | Eliminar o mover a `scripts/` sin secretos. |

---

## 5. Modelo de datos y rendimiento (prioridad MEDIA-ALTA)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| P1 | Dinero como `IntField` (sin decimales, riesgo de desbordamiento) | `modules/operative/models.py:103` | `DecimalField` o entero de centavos; validar rango. |
| P2 | Índices insuficientes para los filtros reales | `modules/operative/models.py:133-137` | Añadir compuestos: `(status, created_at)`, `applicant`, `taker`, `assigned_to`, `number` único. |
| P3 | Búsqueda con `values_fields__icontains` sobre texto concatenado (escaneo completo, sin índice de texto) | `modules/operative/views.py:87,205,293` | Índice de texto de MongoDB o colección de búsqueda dedicada. |
| P4 | Posible N+1 al desreferenciar `applicant`, `taker`, `ramo`, `status`, `assigned_to` por fila | Plantillas de `requests/index_table*.html` | `.select_related()` y proyecciones; evaluar denormalización de nombres. |
| P5 | Se cargan documentos con `content` base64 en listados | `modules/operative/views.py:1010-1046` | Excluir `content` en listados y descargar bajo demanda. |
| P6 | Archivos dentro de documentos (límite 16 MB, memoria) | Modelos `RequestFile`, `OperativeRequestDocument` | GridFS/S3 con streaming. |
| P7 | Campos heredados duplicados (`request_receipt`, `request_police`… y `OperativeRequestDocument`) | `modules/operative/models.py:112-131` | Completar la migración y eliminar campos obsoletos. |
| P8 | `values_fields` con `max_length=50` para concatenar todos los campos | `modules/operative/models.py:111` | Aumentar/reemplazar por índice de búsqueda. |
| P9 | Sin caché para catálogos (ramos, estados, ciudades) | `modules/*/models.py`, formularios | Cachear catálogos poco cambiantes. |
| P10 | Consultas `Account.getAccount` repetidas en la misma petición | `core/template_processor.py`, vistas | Cachear en `request` (middleware/property). |
| P11 | Sin política de retención/anonimización de datos personales | `base_applicants`, `accounts`, documentos | Definir retención, borrado y cifrado en reposo. |
| P12 | Fechas naive mezcladas con `USE_TZ=True` | Modelos y vistas | Ver A13. |

---

## 6. Dependencias y despliegue (prioridad ALTA)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| D1 | Django `<4` (3.2 sin soporte) mientras el proyecto declara Django 5.0.4 | `requirements.txt`, `core/settings.py:1-6` | Planificar actualización a Django 4.2/5.2 LTS. |
| D2 | `django-mongoengine` 0.4.6 sin mantenimiento y condiciona la versión de Django | `requirements.txt` | Evaluar `django-mongodb-backend` oficial, migración a SQL/PostgreSQL o un fork mantenido. |
| D3 | Dependencias duplicadas y sin fijar entre `requirements*.txt` | `requirements.txt`, `requirements_dev.txt` | Única fuente + lock (`pip-tools`, Poetry o uv). |
| D4 | `requirements_dev.txt` no incluye linter/test runner | `requirements_dev.txt` | Añadir `ruff`, `pytest`, `pytest-django`, `mongomock`, `coverage`. |
| D5 | `.python-version` (3.10) difiere de entornos locales (3.12) y del runtime | `.python-version`, `__pycache__` | Fijar una versión y usarla en CI/Heroku. |
| D6 | `app.json` apunta a `./app/manage.py` (ruta inexistente) | `app.json:18` | Corregir a `./manage.py`. |
| D7 | `Procfile` sin workers/timeout/logging | `Procfile` | `gunicorn --workers 3 --timeout 60 --access-logfile -` desde entorno. |
| D8 | Sin Dockerfile/docker-compose pese a depender de MongoDB local | Raíz | Contenerizar app + Mongo para desarrollo reproducible. |
| D9 | Sin endpoint de salud ni monitoreo (Sentry/APM) | Raíz | Añadir `/health/` y Sentry con scrubbing de PII. |
| D10 | Sin CI/CD (GitHub Actions u otro) | Raíz | Pipeline: lint + tests + build + deploy. |
| D11 | Sin estrategia de backups/restauración documentada | `export/` | Automatizar `mongodump` cifrado y probar restauración. |
| D12 | `staticfiles/` presente pero ignorado; correcto, pero no hay pipeline de `collectstatic` documentado | `staticfiles/` | Documentar y automatizar en despliegue. |
| D13 | `README.md` sin instrucciones de instalación/despliegue | `README.md` | Completar. |

---

## 7. Pruebas y calidad (prioridad ALTA)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| T1 | Todos los `tests.py` están vacíos | `modules/*/tests.py` | Priorizar tests de permisos, estados, numeración y documentos. |
| T2 | Sin base de datos de prueba aislada | — | `mongomock`/contenedor Mongo efímero en CI. |
| T3 | Sin cobertura ni umbral mínimo | — | `coverage` + objetivo gradual (40% → 70%). |
| T4 | Sin pruebas de seguridad (IDOR, CSRF, XSS, uploads) | — | Añadir tests explícitos de autorización por rol/propietario. |
| T5 | Sin validación automatizada de lint/formato | `.ruff_cache` indica uso manual | Configurar Ruff + pre-commit + CI. |
| T6 | Sin pruebas de regresión para migraciones de datos (`fix_*`, `migrate_documents`) | `modules/*/models.py` | Tests con fixtures representativos. |

---

## 8. UX / Frontend (prioridad MEDIA)

| # | Hallazgo | Ubicación | Acción |
|---|---|---|---|
| U1 | HTML construido por concatenación de strings en JS (riesgo XSS y difícil mantenimiento) | `static/js/**` | Plantillas/`<template>` o framework ligero; escapar datos. |
| U2 | Código JS duplicado entre `index.js`, `search.js`, `query.js`, `form.js` | `modules/operative/static/js/requests/` | Extraer módulos compartidos. |
| U3 | Mensajes de error concatenados de forma poco legible | `modules/operative/views.py:483-491` | Renderizar errores de formulario en plantilla. |
| U4 | Formularios con django-crispy/bootstrap pero estilos repetidos manualmente | Templates y forms | Componentes reutilizables. |
| U5 | Sin internacionalización efectiva pese a `gettext` | `forms.py` | Definir idioma único o completar traducciones. |
| U6 | Accesibilidad (labels, foco, contraste) no verificada | Templates | Auditoría con Lighthouse/axe. |
| U7 | Logout por GET (CSRF logout) | `modules/authentication/urls.py:6` | Logout por POST. |
| U8 | Pantallas de error personalizadas ausentes (404/500) | `core/urls.py` | Añadir plantillas. |

---

## 9. Observabilidad y operación (prioridad MEDIA)

| # | Hallazgo | Acción |
|---|---|---|
| O1 | Uso de `print()` en semillas y modelos en lugar de `logging` | Configurar logging estructurado y reemplazar `print`. |
| O2 | `LOGGING` solo envía errores por correo (sin handler a consola/archivo) | Añadir handlers a stdout y Sentry. |
| O3 | Excepciones silenciadas con `except:`/`except Exception` | Registrar con contexto y no ocultar fallos. |
| O4 | Sin métricas de negocio (solicitudes creadas, tiempos de atención) | Instrumentar métricas/dashboards. |
| O5 | Sin alertas de errores ni salud de Mongo | Añadir healthcheck y alertas. |
| O6 | Sin auditoría centralizada de accesos a documentos | Registrar descargas/cambios. |

---

## 10. Plan de acción sugerido

### Fase 0 — Inmediata (1–2 días)
1. Rotar **todos** los secretos y credenciales (C1–C5).
2. Eliminar `devtools_json` y la ruta (C7).
3. Añadir `login_required`/roles a `AccountSetPasswordView`, `AccountGenerateConfirmView` y vistas de `operative` (C10–C18).
4. Poner `DEBUG=False`, `ALLOWED_HOSTS` explícito y flags de seguridad (C19–C22).
5. Añadir `export/` a `.gitignore` y retirar el dump (C6).

### Fase 1 — Corto plazo (1–2 semanas)
1. Corregir bugs de negocio A1–A8 y validaciones A13–A20.
2. Sustituir tokens por generador firmado y quitar TinyURL (C25–C27).
3. Validación de subidas y almacenamiento en GridFS/S3 (C31–C33).
4. Añadir índices y proyecciones; eliminar N+1 (P2–P5).
5. Primeros tests de permisos y flujos críticos + CI con lint/test (T1–T5).

### Fase 2 — Medio plazo (1–2 meses)
1. Refactor de vistas/formularios a servicios y permisos reutilizables (M1–M7).
2. Unificar el modelo de documentos y migrar datos (P7).
3. Actualizar Django y evaluar el backend de MongoDB (D1–D2).
4. Observabilidad, healthcheck y backups automatizados (O1–O5, D9–D11).
5. Mejoras frontend, accesibilidad y eliminación de XSS (U1–U8).

### Fase 3 — Largo plazo
1. API REST si se requieren integraciones o app móvil.
2. Endurecimiento de seguridad (MFA para administradores, auditoría, cifrado de campos).
3. Revisión de arquitectura y posible migración de MongoDB a un modelo relacional si el dominio lo justifica.

---

## 11. Checklist rápido de verificación

- [ ] Secretos rotados y fuera del historial de Git.
- [ ] Ningún endpoint público devuelve `SECRET_KEY` ni datos de terceros.
- [ ] Todas las vistas que tocan datos exigen autenticación y autorización por rol/objeto.
- [ ] `DEBUG=False`, hosts y cookies seguras configuradas en producción.
- [ ] Tokens de un solo uso, firmados y sin acortadores externos.
- [ ] Validación de tamaño/tipo de archivos y almacenamiento fuera de MongoDB.
- [ ] Estados y números de solicitud con tipos seguros y generación atómica.
- [ ] Índices y proyecciones para las consultas de listado.
- [ ] Tests de permisos, estados, numeración y documentos en CI.
- [ ] Linter/formato, CI, healthcheck, Sentry y backups automatizados.
- [ ] Dependencias fijadas y plan de actualización de Django/MongoEngine.
