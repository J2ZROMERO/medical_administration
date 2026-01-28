import pytest
from datetime import datetime
from src.domain.clinical_history import ClinicalHistory, DocumentStatus, DomainException

def test_create_clinical_history_draft():
    history = ClinicalHistory(patient_id="123", content={"diagnosticos": "HTA"})
    assert history.status == DocumentStatus.DRAFT
    assert history.patient_id == "123"

def test_sign_clinical_history_success():
    history = ClinicalHistory(patient_id="123", content={"diagnosticos": "HTA"})
    now = datetime.now()
    history.sign(author_id="doc1", signed_at=now)
    
    assert history.status == DocumentStatus.SIGNED
    assert history.signed_by == "doc1"
    assert history.signed_at == now

def test_cannot_sign_without_diagnosis():
    history = ClinicalHistory(patient_id="123", content={})
    now = datetime.now()
    with pytest.raises(DomainException, match="Missing required field"):
        history.sign(author_id="doc1", signed_at=now)

def test_cannot_sign_already_signed():
    history = ClinicalHistory(patient_id="123", content={"diagnosticos": "HTA"})
    now = datetime.now()
    history.sign(author_id="doc1", signed_at=now)
    
    with pytest.raises(DomainException, match="Document is already signed"):
        history.sign(author_id="doc1", signed_at=now)
