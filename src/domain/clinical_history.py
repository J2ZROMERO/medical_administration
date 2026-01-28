from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any

class DocumentStatus(Enum):
    DRAFT = "draft"
    SIGNED = "signed"

class DomainException(Exception):
    pass

class ClinicalHistory:
    def __init__(self, patient_id: str, content: Dict[str, Any], status: DocumentStatus = DocumentStatus.DRAFT):
        self.patient_id = patient_id
        self.content = content
        self.status = status
        self.signed_by: Optional[str] = None
        self.signed_at: Optional[datetime] = None

    def sign(self, author_id: str, signed_at: datetime) -> None:
        if self.status == DocumentStatus.SIGNED:
            raise DomainException("Document is already signed")
        
        # Validation of minimum fields (mvp)
        required_fields = [
            "interrogatorio", 
            "exploracion_fisica", 
            "signos_vitales", 
            "diagnosticos", 
            "pronostico", 
            "indicacion_terapeutica"
        ]
        for field in required_fields:
            if field not in self.content:
                 raise DomainException(f"Missing required field: {field}")

        self.status = DocumentStatus.SIGNED
        self.signed_by = author_id
        self.signed_at = signed_at
