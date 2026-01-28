from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class PatientModel(Base):
    __tablename__ = 'patients'
    id = Column(String, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    address = Column(String)

class ConsultationModel(Base):
    __tablename__ = 'consultations'
    id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey('patients.id'))
    date_time = Column(DateTime)

class ClinicalHistoryModel(Base):
    __tablename__ = 'clinical_histories'
    patient_id = Column(String, ForeignKey('patients.id'), primary_key=True)
    content = Column(JSON)
    status = Column(String)
    signed_by = Column(String, nullable=True)
    signed_at = Column(DateTime, nullable=True)

class EvolutionNoteModel(Base):
    __tablename__ = 'evolution_notes'
    id = Column(String, primary_key=True)
    consultation_id = Column(String, ForeignKey('consultations.id'))
    content = Column(JSON)
    status = Column(String)
    signed_by = Column(String, nullable=True)
    signed_at = Column(DateTime, nullable=True)
    correction_of = Column(String, nullable=True)

# DB Setup
engine = create_engine('sqlite:///medical.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
