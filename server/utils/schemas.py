from pydantic import BaseModel, Field
from typing import Literal, Optional

class SubjectiveSchema(BaseModel):
    reasonForVisit: str | None
    symptoms: list[str]
    historyOfPresentIllness: str | None
    pastHistory: str | None

class VitalSignSchema(BaseModel):
    name: str
    value: str
    unit: str | None

class ClinicalTestSchema(BaseModel):
    name: str
    result: str

class ObjectiveSchema(BaseModel):
    vitalSigns: list[VitalSignSchema]
    physicalExam: str | None
    clinicalTests: list[ClinicalTestSchema]

class DiagnosisSchema(BaseModel):
    name: str
    icd10Code: str | None
    type: Literal['primary', 'secondary', 'differential']
    originalText: str | None

class AssessmentSchema(BaseModel):
    diagnoses: list[DiagnosisSchema]
    evaluation: str | None

class MedicationSchema(BaseModel):
    name: str
    dosage: str | None
    instruction: str | None

class PlanSchema(BaseModel):
    medications: list[MedicationSchema]
    orders: list[str]
    monitoring: str | None
    followUp: str | None

# --- New Metadata Sub-schemas ---

class Patient(BaseModel):
    patient_ref: Optional[str] = Field(default=None, description="ID tham chiếu sang hệ thống EMR")
    age: Optional[int] = None
    sex: Optional[Literal["male", "female", "other", "unknown"]] = None

class AudioMetadata(BaseModel):
    audio_file_ref: Optional[str] = None
    duration_sec: Optional[float] = None
    language: Optional[str] = None
    speaker_count: Optional[int] = None
    diarization_quality: Optional[float] = Field(default=None, ge=0, le=1)

class MetadataSchema(BaseModel):
    patient: Optional[Patient] = None
    audio: Optional[AudioMetadata] = None

# --- Main Schema ---

class SOAPNoteSchema(BaseModel):
    metadata: Optional[MetadataSchema] = None
    subjective: SubjectiveSchema
    objective: ObjectiveSchema
    assessment: AssessmentSchema
    plan: PlanSchema