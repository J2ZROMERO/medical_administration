import pytest
from datetime import datetime, timezone
from src.domain.evolution_note import EvolutionNote, DocumentStatus, MissingRequiredField, DocumentNotEditable

def test_sign_missing_required_fields():
    created_at = datetime(2026, 1, 27, 10, 0, tzinfo=timezone.utc)
    # Missing plan
    content = {"evolution": "Stable", "diagnoses": "Flu"}
    note = EvolutionNote.create_draft("note1", "cons1", created_at, content)
    
    with pytest.raises(MissingRequiredField) as excinfo:
        note.sign("doctor1", datetime.now(timezone.utc))
    
    assert "plan" in excinfo.value.fields

def test_sign_sets_fields_correctly():
    created_at = datetime(2026, 1, 27, 10, 0, tzinfo=timezone.utc)
    content = {"evolution": "Stable", "diagnoses": "Flu", "plan": "Rest"}
    note = EvolutionNote.create_draft("note1", "cons1", created_at, content)
    
    signed_at = datetime(2026, 1, 27, 10, 30, tzinfo=timezone.utc)
    note.sign("doctor1", signed_at)
    
    assert note.status == DocumentStatus.SIGNED
    assert note.signed_by == "doctor1"
    assert note.signed_at == signed_at

def test_signed_document_not_editable():
    created_at = datetime(2026, 1, 27, 10, 0, tzinfo=timezone.utc)
    content = {"evolution": "Stable", "diagnoses": "Flu", "plan": "Rest"}
    note = EvolutionNote.create_draft("note1", "cons1", created_at, content)
    
    note.sign("doctor1", datetime.now(timezone.utc))
    
    with pytest.raises(DocumentNotEditable):
        note.update_content({"evolution": "Changed"})

def test_correction_creates_new_draft_linked_to_original():
    created_at = datetime(2026, 1, 27, 10, 0, tzinfo=timezone.utc)
    content = {"evolution": "Stable", "diagnoses": "Flu", "plan": "Rest"}
    original_note = EvolutionNote.create_draft("note1", "cons1", created_at, content)
    original_note.sign("doctor1", datetime.now(timezone.utc))
    
    correction_at = datetime(2026, 1, 27, 11, 0, tzinfo=timezone.utc)
    new_content = {"evolution": "Worsened", "diagnoses": "Flu", "plan": "Hospital"}
    
    correction_note = original_note.create_correction("note2", correction_at, new_content)
    
    # Check correction properties
    assert correction_note.id == "note2"
    assert correction_note.status == DocumentStatus.DRAFT
    assert correction_note.previous_version_id == "note1"
    assert correction_note.content == new_content
    assert correction_note.created_at == correction_at
    
    # Check original is untouched (immutable in logic)
    assert original_note.id == "note1"
    assert original_note.status == DocumentStatus.SIGNED
