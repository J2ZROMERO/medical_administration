from abc import ABC, abstractmethod
from typing import Optional
from .patient import Patient
from .consultation import Consultation
from .clinical_history import ClinicalHistory
from .evolution_note import EvolutionNote

class PatientRepository(ABC):
    @abstractmethod
    def save(self, patient: Patient) -> None: pass
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Patient]: pass

class ConsultationRepository(ABC):
    @abstractmethod
    def save(self, consultation: Consultation) -> None: pass
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Consultation]: pass

class DocumentRepository(ABC):
    @abstractmethod
    def save_history(self, history: ClinicalHistory) -> None: pass
    @abstractmethod
    def get_history(self, patient_id: str) -> Optional[ClinicalHistory]: pass
    @abstractmethod
    def save_note(self, note: EvolutionNote) -> None: pass
    @abstractmethod
    def get_note(self, id: str) -> Optional[EvolutionNote]: pass
