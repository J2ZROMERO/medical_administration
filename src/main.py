from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from .domain.repositories import UnitOfWork
from .infrastructure.models import SessionLocal, init_db
from .infrastructure.repositories import SqlAlchemyPatientRepository, SqlAlchemyConsultationRepository, SqlAlchemyDocumentRepository, SqlAlchemyUnitOfWork
from .application.service import MedicalService

app = FastAPI(title="Medical Administration MVP")

# Init DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Dependency
def get_service():
    session = SessionLocal()
    try:
        patient_repo = SqlAlchemyPatientRepository(session)
        consultation_repo = SqlAlchemyConsultationRepository(session)
        doc_repo = SqlAlchemyDocumentRepository(session)
        uow = SqlAlchemyUnitOfWork(session)
        yield MedicalService(patient_repo, consultation_repo, doc_repo, uow)
    finally:
        session.close()

# DTOs
class PatientCreate(BaseModel):
    name: str
    gender: str
    age: int
    address: str

class ConsultationCreate(BaseModel):
    patient_id: str

class HistoryCreate(BaseModel):
    patient_id: str
    content: Dict[str, Any]

class NoteCreate(BaseModel):
    consultation_id: str
    content: Dict[str, Any]

class SignRequest(BaseModel):
    author_id: str

class CorrectionRequest(BaseModel):
    note_id: str
    new_content: Dict[str, Any]

# Endpoints
@app.post("/patients/")
def register_patient(patient: PatientCreate, service: MedicalService = Depends(get_service)):
    return {"id": service.register_patient(patient.name, patient.gender, patient.age, patient.address)}

@app.post("/consultations/")
def create_consultation(consultation: ConsultationCreate, service: MedicalService = Depends(get_service)):
    return {"id": service.create_consultation(consultation.patient_id)}

@app.post("/history/draft")
def draft_history(history: HistoryCreate, service: MedicalService = Depends(get_service)):
    service.create_history_draft(history.patient_id, history.content)
    return {"status": "created"}

@app.post("/history/sign")
def sign_history(history_id: str, req: SignRequest, service: MedicalService = Depends(get_service)): # patient_id as history_id for simplifiction in URL
    try:
        service.sign_history(history_id, req.author_id)
        return {"status": "signed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/notes/draft")
def draft_note(note: NoteCreate, service: MedicalService = Depends(get_service)):
    id = service.create_note_draft(note.consultation_id, note.content)
    return {"id": id}

@app.post("/notes/{note_id}/sign")
def sign_note(note_id: str, req: SignRequest, service: MedicalService = Depends(get_service)):
    try:
        service.sign_note(note_id, req.author_id)
        return {"status": "signed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/notes/correct")
def correct_note(req: CorrectionRequest, service: MedicalService = Depends(get_service)):
    try:
        id = service.correct_note(req.note_id, req.new_content)
        return {"id": id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
