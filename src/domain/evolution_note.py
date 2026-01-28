from enum import Enum
from datetime import datetime
from typing import Dict, Any, Optional, List
import copy

class DocumentStatus(str, Enum):
    DRAFT = "DRAFT"
    SIGNED = "SIGNED"

class DomainException(Exception):
    pass

class MissingRequiredField(DomainException):
    def __init__(self, fields: List[str]):
        self.message = f"Missing required fields: {', '.join(fields)}"
        self.fields = fields
        super().__init__(self.message)

class DocumentNotEditable(DomainException):
    def __init__(self):
        super().__init__("Document is signed and cannot be edited")

class EvolutionNote:
    def __init__(
        self, 
        id: str, 
        consultation_id: str, 
        created_at: datetime, 
        content: Dict[str, Any], 
        status: DocumentStatus = DocumentStatus.DRAFT,
        previous_version_id: Optional[str] = None
    ):
        self.id = id
        self.consultation_id = consultation_id
        self.created_at = created_at
        self.content = content
        self.status = status
        self.previous_version_id = previous_version_id
        self.signed_by: Optional[str] = None
        self.signed_at: Optional[datetime] = None

    @classmethod
    def create_draft(cls, id: str, consultation_id: str, created_at: datetime, content: Dict[str, Any]) -> 'EvolutionNote':
        return cls(id, consultation_id, created_at, content, DocumentStatus.DRAFT)

    def update_content(self, new_content: Dict[str, Any]) -> None:
        if self.status == DocumentStatus.SIGNED:
            raise DocumentNotEditable()
        self.content = new_content

    def sign(self, author_id: str, signed_at: datetime) -> None:
        if self.status == DocumentStatus.SIGNED:
            # Idempotent or raise? Usually raise if trying to resign or modify. 
            # Prompt implies checking fields first.
            pass

        required = ["evolution", "diagnoses", "plan"]
        missing = [field for field in required if not self.content.get(field)]
        
        if missing:
            raise MissingRequiredField(missing)

        self.status = DocumentStatus.SIGNED
        self.signed_by = author_id
        self.signed_at = signed_at

    def create_correction(self, new_id: str, created_at: datetime, new_content: Dict[str, Any]) -> 'EvolutionNote':
        if self.status != DocumentStatus.SIGNED:
            # Only signed documents usually need a formal "correction" version, 
            # otherwise you just update the draft. 
            # But the prompt says "corrección de documento firmado crea nueva..."
            raise DomainException("Can only correct signed documents")

        return EvolutionNote(
            id=new_id,
            consultation_id=self.consultation_id,
            created_at=created_at,
            content=new_content,
            status=DocumentStatus.DRAFT,
            previous_version_id=self.id
        )
