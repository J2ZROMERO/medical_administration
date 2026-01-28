Documento de trabajo: Expediente clínico (MVP) — Dominio → SPEC → BDD → TDD (con Hexagonal)
0) Objetivo del curso/proyecto

Construir una aplicación web para gestión de expediente clínico ambulatorio (consulta), siguiendo un flujo disciplinado:

Dominio entendido

SPEC (qué debe hacer)

BDD (cómo debe comportarse: escenarios)

TDD (cómo implementarlo: tests primero)

Arquitectura Hexagonal (consolidada en el paso de TDD)

1) Dominio entendido (qué estamos modelando)
1.1 Qué es el expediente clínico en la práctica

El expediente clínico es el conjunto único de documentos e información clínica del paciente dentro de un establecimiento. En la vida real, el médico lo usa para:

continuidad clínica,

seguridad del paciente (indicaciones claras),

evidencia clínica (lo que se hizo y por qué).

1.2 Reglas troncales del dominio (las que mandan el diseño)

Un expediente único por paciente (dentro del establecimiento).

El expediente se compone de documentos clínicos (notas y formatos).

Toda nota/documento debe tener:

paciente asociado,

fecha/hora,

autor,

firma (electrónica/digital en sistema).

Confidencialidad: acceso restringido por roles; no exponer datos identificables sin permiso.

Conservación: retención mínima (como política del sistema).

La atención ambulatoria mínima para arrancar: Historia Clínica y Nota de Evolución.

Interpretación práctica: si el sistema no protege firma/inmutabilidad y no asegura mínimos, el expediente “no sirve” ni clínica ni legalmente.

2) SPEC (MVP ambulatorio — lo mínimo para arrancar)
2.1 Alcance del MVP

Atención ambulatoria (consulta) con:

Historia clínica

Nota de evolución

2.2 Entidades mínimas

Paciente

Expediente (único por paciente)

Consulta (visita con fecha/hora)

Documento clínico:

Historia clínica

Nota de evolución

Estado del documento:

Borrador

Firmado

2.3 Flujo funcional mínimo

Registrar paciente (datos mínimos).

Crear consulta para un paciente.

Capturar Historia clínica (borrador).

Capturar Nota de evolución (borrador).

Firmar documentos (pasan a “Firmado”).

Documentos firmados no se editan:

correcciones se hacen como nueva versión ligada a la anterior.

2.4 Campos mínimos por documento (MVP)

Historia clínica

Interrogatorio

Exploración física (incluye signos vitales, peso, talla)

Resultados de estudios (si existen)

Diagnósticos / problemas

Pronóstico

Indicación terapéutica

Nota de evolución

Evolución / actualización del cuadro

Diagnósticos / problemas actuales

Plan / indicaciones terapéuticas

2.5 Reglas de validación para “Firmar”

No se puede firmar si falta:

paciente asociado

fecha/hora

autor

campos mínimos del contenido (según tipo)

2.6 Reglas no funcionales mínimas

Control de acceso por rol (médico/admin/recepción…)

Auditoría (quién creó/firmó)

Retención y confidencialidad (política de sistema)

Inmutabilidad lógica de documentos firmados (sin “editar” lo firmado)

3) BDD (escenarios Gherkin del MVP)
Feature: Registro de paciente
Feature: Registro de paciente
  As a médico o asistente
  I want to registrar un paciente
  So that pueda crear su expediente y consultas

  Scenario: Registrar paciente con datos mínimos
    Given no existe un paciente con nombre "Juan Pérez" y domicilio "CDMX"
    When registro un paciente con:
      | nombre     | sexo | edad | domicilio |
      | Juan Pérez | M    | 35   | CDMX      |
    Then el paciente queda creado
    And el expediente del paciente existe (único en el establecimiento)

Feature: Crear consulta
Feature: Crear consulta
  As a médico
  I want to crear una consulta para un paciente
  So that pueda documentar la atención

  Scenario: Crear consulta para un paciente existente
    Given existe el paciente "Juan Pérez"
    When creo una consulta para "Juan Pérez" en fecha_hora "2026-01-27T10:00:00"
    Then la consulta queda creada y asociada a "Juan Pérez"

Feature: Historia clínica
Feature: Historia clínica
  As a médico
  I want to capturar y firmar la historia clínica
  So that quede documentado el estado basal del paciente

  Scenario: Guardar historia clínica en borrador
    Given existe una consulta activa para "Juan Pérez"
    When capturo una historia clínica con:
      | interrogatorio | exploracion_fisica | signos_vitales        | peso | talla | resultados_estudios | diagnosticos | pronostico | indicacion_terapeutica |
      | texto         | texto              | TA:120/80 FC:70       | 80   | 1.75  | N/A                 | "HTA"        | "Bueno"    | "Ajuste dieta"         |
    Then la historia clínica queda en estado "Borrador"

  Scenario: Firmar historia clínica con mínimos completos
    Given existe una historia clínica en estado "Borrador" para "Juan Pérez"
    And el autor es "Dra. López"
    When firmo la historia clínica en "2026-01-27T10:20:00"
    Then la historia clínica cambia a estado "Firmado"
    And se registra firmado_por "Dra. López"
    And se registra firmado_en "2026-01-27T10:20:00"

  Scenario: Bloquear firmado de historia clínica si faltan mínimos
    Given existe una historia clínica en estado "Borrador" para "Juan Pérez"
    And falta "diagnosticos"
    When intento firmar la historia clínica
    Then el sistema rechaza el firmado
    And muestra el error "Faltan campos mínimos: diagnosticos"

Feature: Nota de evolución
Feature: Nota de evolución
  As a médico
  I want to capturar y firmar notas de evolución por consulta
  So that quede la trazabilidad de la evolución del paciente

  Scenario: Crear nota de evolución en borrador
    Given existe una consulta activa para "Juan Pérez"
    When creo una nota de evolución con:
      | evolucion         | diagnosticos      | plan_indicaciones          |
      | "Mejoría parcial" | "HTA controlada"  | "Continuar medicamento X"  |
    Then la nota de evolución queda en estado "Borrador"

  Scenario: Firmar nota de evolución con mínimos completos
    Given existe una nota de evolución en estado "Borrador" para "Juan Pérez"
    And el autor es "Dra. López"
    When firmo la nota de evolución en "2026-01-27T10:40:00"
    Then la nota de evolución cambia a estado "Firmado"
    And se registra firmado_por "Dra. López"
    And se registra firmado_en "2026-01-27T10:40:00"

  Scenario: Bloquear firmado de nota de evolución si faltan mínimos
    Given existe una nota de evolución en estado "Borrador" para "Juan Pérez"
    And falta "plan_indicaciones"
    When intento firmar la nota de evolución
    Then el sistema rechaza el firmado
    And muestra el error "Faltan campos mínimos: plan_indicaciones"

Feature: Inmutabilidad y correcciones
Feature: Inmutabilidad y correcciones
  As a médico
  I want que las notas firmadas no se editen
  So that exista trazabilidad y no haya alteraciones

  Scenario: No permitir editar documento firmado
    Given existe una nota de evolución en estado "Firmado" para "Juan Pérez"
    When intento editar el campo "evolucion"
    Then el sistema rechaza la edición
    And muestra el error "Documento firmado: no editable"

  Scenario: Crear corrección como nueva versión
    Given existe una nota de evolución en estado "Firmado" para "Juan Pérez"
    When creo una "corrección" vinculada a la nota firmada con:
      | evolucion                       | diagnosticos | plan_indicaciones        |
      | "Corrección: se ajusta dosis"   | "HTA"        | "Aumentar dosis a ..."   |
    Then se crea un nuevo documento en estado "Borrador"
    And queda vinculado como "versión corregida de" la nota original

4) Siguiente paso: TDD + consolidación Hexagonal (recomendación)
4.1 Por qué aquí consolidamos hexagonal

Porque TDD te obliga a separar:

Dominio puro (reglas)

Aplicación (casos de uso)

Infra (DB/web)

4.2 Mapa BDD → Use Cases (Application Layer)

De los escenarios salen estos casos de uso:

RegisterPatient

CreateConsultation

SaveClinicalHistoryDraft

SignClinicalHistory

CreateEvolutionNoteDraft

SignEvolutionNote

CorrectSignedDocument

EditDraftDocument

4.3 Puertos (interfaces) típicos

PatientRepository

ConsultationRepository

DocumentRepository

Clock (control de tiempo en tests)

IdGenerator

(opcional) AuditLog

4.4 Orden recomendado de tests (TDD)

Unit tests de Dominio (sin DB, sin web):

firmar OK / firmar falla por mínimos

firmado no editable

corrección crea nueva versión

Tests de Aplicación (use cases) con repos in-memory/fakes

Integración Infra (SQLAlchemy + Postgres en docker)

(Opcional) E2E que ejecute Gherkin (pytest-bdd/behave)

5) Checklist para empezar a construir (día 1)

 Carpeta domain/ con entidades y reglas (sin SQLAlchemy).

 Carpeta application/ con use cases + puertos.

 Carpeta infrastructure/ con repos SQLAlchemy y API.

 tests/unit/ con primeros tests de sign() y validaciones.

 Inyección de Clock + IdGenerator para tests deterministas.

 Pipeline mínimo (pytest).

6) Cómo sabemos que el MVP está “hecho”

Puedes:

crear paciente,

crear consulta,

guardar historia clínica en borrador,

firmarla (si cumple mínimos),

guardar nota de evolución en borrador,

firmarla,

intentar editar firmada y el sistema lo bloquea,

crear corrección como documento nuevo ligado.