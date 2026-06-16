from typing import List, Optional
from pydantic import BaseModel

class VitalSign(BaseModel):
    type: str
    value: str
    unit: Optional[str] = None

class Problem(BaseModel):
    diagnosis: str
    certainty: Optional[str] = None
    reasoning: Optional[str] = None

class PlanItem(BaseModel):
    category: str
    description: str

class SOAPNoteSchema(BaseModel):
    chief_complaint: str
    hpi_narrative: Optional[str] = None
    past_medical_history: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    vital_signs: Optional[List[VitalSign]] = None
    physical_exam: Optional[List[str]] = None
    problems: List[Problem]
    plan: Optional[List[PlanItem]] = None
    overall_confidence_note: Optional[str] = None