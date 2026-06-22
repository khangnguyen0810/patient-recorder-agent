from pydantic import BaseModel
from typing import Literal

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

class SOAPNoteSchema(BaseModel):
    subjective: SubjectiveSchema
    objective: ObjectiveSchema
    assessment: AssessmentSchema
    plan: PlanSchema