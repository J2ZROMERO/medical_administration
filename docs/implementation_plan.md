# Medical Administration MVP Implementation Plan

The goal is to build an ambulatory clinical record management system using Python, FastAPI, and SQLAlchemy, following Hexagonal Architecture and SOLID principles.

## User Review Required
> [!IMPORTANT]
> The specification requires strict immutability for signed documents. The implementation will enforce this at the domain level.
> The architecture will be strictly separated into Domain, Application, and Infrastructure layers.

## Proposed Changes

### Directory Structure
```
src/
├── domain/           # Pure business logic (Entities, Value Objects, Repository Interfaces)
├── application/      # Use Cases / Interactors
├── infrastructure/   # Frameworks & Drivers (FastAPI, SQLAlchemy)
└── main.py           # Application Entry Point
tests/                # Unit and Integration Tests
```

### 1. Domain Layer (`src/domain/`)
Pure Python code, no dependencies on frameworks.
-   **Entities**: `Patient`, `MedicalRecord` (Expediente), `Consultation`, `ClinicalDocument` (Abstract), `ClinicalHistory`, `EvolutionNote`.
-   **Value Objects**: `DocumentStatus` (Draft, Signed), `DocumentContent`.
-   **Ports (Interfaces)**: `PatientRepository`, `ConsultationRepository`, `DocumentRepository`, `UnitOfWork`.
-   **Exceptions**: `DomainException`, `InvalidStateError`.

### 2. Application Layer (`src/application/`)
Orchestrates domain objects to fulfill use cases.
-   **Use Cases**:
    -   `RegisterPatient`
    -   `CreateConsultation`
    -   `SaveClinicalHistoryDraft`
    -   `SignClinicalHistory`
    -   `CreateEvolutionNoteDraft`
    -   `SignEvolutionNote`
    -   `CorrectSignedDocument`

### 3. Infrastructure Layer (`src/infrastructure/`)
Implementation of ports and external interfaces.
-   **Persistence**: SQLAlchemy models (mapped to domain entities or separate models), Repositories implementations.
-   **API**: FastAPI routers, Controllers, DTOs (Pydantic models for request/response).
-   **Configuration**: Database connection, settings.

### 4. Setup
-   `requirements.txt`: FastAPI, Uvicorn, SQLAlchemy, Pydantic, Pytest.

## Verification Plan

### Automated Tests
We will use `pytest` for testing.
1.  **Domain Unit Tests**: Verify business rules (e.g., cannot sign incomplete document, cannot edit signed document).
    -   `pytest tests/unit/domain`
2.  **Application Unit Tests**: Verify use cases using mock repositories.
    -   `pytest tests/unit/application`
3.  **Infrastructure/Integration Tests**: Verify database persistence and API endpoints (using SQLite for MVP).
    -   `pytest tests/integration`

### Manual Verification
1.  Start the API: `uvicorn src.main:app --reload`
2.  Use Swagger UI (`/docs`) to simulate the workflow:
    -   Register a patient.
    -   Start a consultation.
    -   Create a drafted Clinical History.
    -   Sign the Clinical History.
    -   Attempt to edit the signed history (should fail).
    -   Create a correction (new version).
