from typing import Dict, Any
from datetime import datetime
import uuid
from ..domain.patient import Patient
from ..domain.consultation import Consultation
from ..domain.clinical_history import ClinicalHistory
from ..domain.evolution_note import EvolutionNote
from ..domain.repositories import PatientRepository, ConsultationRepository, DocumentRepository
from ..domain.unit_of_work import UnitOfWork

class MedicalService:
    def __init__(self, 
                 patient_repo: PatientRepository, 
                 consultation_repo: ConsultationRepository, 
                 doc_repo: DocumentRepository,
                 uow: UnitOfWork):
        self.patient_repo = patient_repo
        self.consultation_repo = consultation_repo
        self.doc_repo = doc_repo
        self.uow = uow

    def register_patient(self, name: str, gender: str, age: int, address: str) -> str:
        patient_id = str(uuid.uuid4())
        patient = Patient(patient_id, name, gender, age, address)
        self.patient_repo.save(patient)
        self.uow.commit() # Simple commit for MVP
        return patient_id

    def create_consultation(self, patient_id: str) -> str:
        consultation_id = str(uuid.uuid4())
        consultation = Consultation(consultation_id, patient_id, datetime.now())
        self.consultation_repo.save(consultation)
        self.uow.commit()
        return consultation_id

    def create_history_draft(self, patient_id: str, content: Dict[str, Any]) -> None:
        history = ClinicalHistory(patient_id, content)
        self.doc_repo.save_history(history)
        self.uow.commit()

    def sign_history(self, patient_id: str, author_id: str) -> None:
        history = self.doc_repo.get_history(patient_id)
        if not history:
            raise Exception("History not found")
        history.sign(author_id, datetime.now())
        self.doc_repo.save_history(history)
        self.uow.commit()

    def create_note_draft(self, consultation_id: str, content: Dict[str, Any]) -> str:
        note_id = str(uuid.uuid4())
        note = EvolutionNote(note_id, consultation_id, content)
        self.doc_repo.save_note(note)
        self.uow.commit()
        return note_id

    def sign_note(self, note_id: str, author_id: str) -> None:
        note = self.doc_repo.get_note(note_id)
        if not note:
            raise Exception("Note not found")
        note.sign(author_id, datetime.now())
        self.doc_repo.save_note(note)
        self.uow.commit()

    def correct_note(self, note_id: str, new_content: Dict[str, Any]) -> str:
        note = self.doc_repo.get_note(note_id)
        if not note:
            raise Exception("Note not found")
        
        new_id = str(uuid.uuid4())
        correction = note.create_correction(new_id, new_content)
        self.doc_repo.save_note(correction)
        self.uow.commit()
        return new_id
