from sqlalchemy.orm import Session
from typing import Optional
from ..domain.patient import Patient
from ..domain.consultation import Consultation
from ..domain.clinical_history import ClinicalHistory, DocumentStatus
from ..domain.evolution_note import EvolutionNote
from ..domain.repositories import PatientRepository, ConsultationRepository, DocumentRepository, UnitOfWork
from .models import PatientModel, ConsultationModel, ClinicalHistoryModel, EvolutionNoteModel

class SqlAlchemyPatientRepository(PatientRepository):
    def __init__(self, session: Session):
        self.session = session
    def save(self, patient: Patient):
        model = PatientModel(id=patient.id, name=patient.name, gender=patient.gender, age=patient.age, address=patient.address)
        self.session.add(model)
    def get_by_id(self, id: str) -> Optional[Patient]:
        m = self.session.query(PatientModel).filter_by(id=id).first()
        return Patient(m.id, m.name, m.gender, m.age, m.address) if m else None

class SqlAlchemyConsultationRepository(ConsultationRepository):
    def __init__(self, session: Session):
        self.session = session
    def save(self, consultation: Consultation):
        model = ConsultationModel(id=consultation.id, patient_id=consultation.patient_id, date_time=consultation.date_time)
        self.session.add(model)
    def get_by_id(self, id: str) -> Optional[Consultation]:
        m = self.session.query(ConsultationModel).filter_by(id=id).first()
        return Consultation(m.id, m.patient_id, m.date_time) if m else None

class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: Session):
        self.session = session
    def save_history(self, history: ClinicalHistory):
        # Simplification: merge/upsert manually
        existing = self.session.query(ClinicalHistoryModel).filter_by(patient_id=history.patient_id).first()
        if existing:
            existing.content = history.content
            existing.status = history.status.value
            existing.signed_by = history.signed_by
            existing.signed_at = history.signed_at
        else:
            model = ClinicalHistoryModel(
                patient_id=history.patient_id, content=history.content, 
                status=history.status.value, signed_by=history.signed_by, signed_at=history.signed_at
            )
            self.session.add(model)

    def get_history(self, patient_id: str) -> Optional[ClinicalHistory]:
        m = self.session.query(ClinicalHistoryModel).filter_by(patient_id=patient_id).first()
        if not m: return None
        h = ClinicalHistory(m.patient_id, m.content, DocumentStatus(m.status))
        h.signed_by = m.signed_by
        h.signed_at = m.signed_at
        return h

    def save_note(self, note: EvolutionNote):
        existing = self.session.query(EvolutionNoteModel).filter_by(id=note.id).first()
        if existing:
            existing.content = note.content
            existing.status = note.status.value
            existing.signed_by = note.signed_by
            existing.signed_at = note.signed_at
        else:
            model = EvolutionNoteModel(
                id=note.id, consultation_id=note.consultation_id, content=note.content,
                status=note.status.value, signed_by=note.signed_by, signed_at=note.signed_at,
                correction_of=note.correction_of
            )
            self.session.add(model)

    def get_note(self, id: str) -> Optional[EvolutionNote]:
        m = self.session.query(EvolutionNoteModel).filter_by(id=id).first()
        if not m: return None
        n = EvolutionNote(m.id, m.consultation_id, m.content, DocumentStatus(m.status))
        n.signed_by = m.signed_by
        n.signed_at = m.signed_at
        n.correction_of = m.correction_of
        return n

class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        self.session = session
    def commit(self):
        self.session.commit()
    def rollback(self):
        self.session.rollback()
