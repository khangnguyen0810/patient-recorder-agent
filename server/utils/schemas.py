# utils/schemas.py
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# ==========================================
# DEFINITIONS (Reusable Schema Objects)
# ==========================================

class Evidence(BaseModel):
    transcript_segment_ids: Optional[List[str]] = Field(default=None, description="Liên kết về đoạn audio/transcript làm căn cứ")
    start_time_sec: Optional[float] = Field(default=None)
    end_time_sec: Optional[float] = Field(default=None)
    quote: Optional[str] = Field(default=None, description="Trích lời nói gốc (nguyên văn từ transcript)")

class ExtractedItem(BaseModel):
    confidence: Optional[float] = Field(default=None, ge=0, le=1)
    evidence: Optional[List[Evidence]] = Field(default=None)
    needs_review: Optional[bool] = Field(default=None, description="True nếu confidence thấp hoặc thông tin mâu thuẫn")

class CodedConcept(BaseModel):
    text: str = Field(description="Tên hiển thị")
    code: Optional[str] = Field(default=None)
    system: Optional[Literal["ICD-10", "SNOMED-CT", "RxNorm", "LOINC", "CPT", "local"]] = Field(default=None, description="Hệ mã hóa")

# ==========================================
# METADATA SUB-SCHEMAS
# ==========================================

class Encounter(BaseModel):
    encounter_id: Optional[str] = None
    encounter_type: Optional[Literal["outpatient", "inpatient", "telemedicine", "emergency", "follow_up"]] = None
    encounter_datetime: Optional[str] = None
    specialty: Optional[str] = None

class Patient(BaseModel):
    patient_ref: Optional[str] = Field(default=None, description="ID tham chiếu sang hệ thống EMR")
    age: Optional[int] = None
    sex: Optional[Literal["male", "female", "other", "unknown"]] = None

class Provider(BaseModel):
    provider_ref: Optional[str] = None
    role: Optional[str] = None

class AudioMetadata(BaseModel):
    audio_file_ref: Optional[str] = None
    duration_sec: Optional[float] = None
    language: Optional[str] = None
    speaker_count: Optional[int] = None
    diarization_quality: Optional[float] = Field(default=None, ge=0, le=1)

class AiPipeline(BaseModel):
    asr_model: Optional[str] = None
    llm_model: Optional[str] = None
    pipeline_version: Optional[str] = None 

class NoteMetadata(BaseModel):
    note_id: str
    schema_version: str
    created_at: str
    encounter: Optional[Encounter] = None
    patient: Optional[Patient] = None
    provider: Optional[Provider] = None
    audio: Optional[AudioMetadata] = None
    ai_pipeline: Optional[AiPipeline] = None

# ==========================================
# SUBJECTIVE SUB-SCHEMAS
# ==========================================

class ChiefComplaint(ExtractedItem):
    text: str

class StructuredHPI(BaseModel):
    onset: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None
    character: Optional[str] = None
    aggravating_factors: Optional[str] = None
    relieving_factors: Optional[str] = None
    timing: Optional[str] = None
    severity: Optional[str] = None

class HPI(ExtractedItem):
    narrative: Optional[str] = Field(default=None, description="Đoạn văn HPI hoàn chỉnh")
    structured: Optional[StructuredHPI] = Field(default=None, description="Khung OLDCARTS")

class PastMedicalHistoryItem(ExtractedItem):
    condition: CodedConcept
    status: Optional[Literal["active", "resolved", "chronic"]] = None

class CurrentMedicationItem(ExtractedItem):
    drug: CodedConcept
    dose: Optional[str] = None
    frequency: Optional[str] = None
    adherence_note: Optional[str] = None

class AllergyItem(ExtractedItem):
    allergen: Optional[str] = None
    reaction: Optional[str] = None
    severity: Optional[Literal["mild", "moderate", "severe", "unknown"]] = None

class AllergiesSection(BaseModel):
    status: Optional[Literal["present", "denied", "not_mentioned"]] = None
    items: Optional[List[AllergyItem]] = None

class FamilyHistorySection(BaseModel):
    status: Optional[Literal["present", "denied", "not_mentioned"]] = None
    narrative: Optional[str] = None

class SocialHistoryHabit(BaseModel):
    status: Optional[Literal["present", "denied", "not_mentioned"]] = None
    detail: Optional[str] = None

class SocialHistorySection(BaseModel):
    smoking: Optional[SocialHistoryHabit] = None
    alcohol: Optional[SocialHistoryHabit] = None
    occupation: Optional[str] = None
    other: Optional[str] = None

class ReviewOfSystemsFinding(BaseModel):
    symptom: Optional[str] = None
    status: Optional[Literal["present", "denied", "not_mentioned"]] = None

class ReviewOfSystemsItem(BaseModel):
    system: Optional[str] = None
    findings: Optional[List[ReviewOfSystemsFinding]] = None

class SubjectiveSection(BaseModel):
    chief_complaint: ChiefComplaint
    history_of_present_illness: Optional[HPI] = None
    past_medical_history: Optional[List[PastMedicalHistoryItem]] = None
    current_medications: Optional[List[CurrentMedicationItem]] = None
    allergies: Optional[AllergiesSection] = None
    family_history: Optional[FamilyHistorySection] = None
    social_history: Optional[SocialHistorySection] = None
    review_of_systems: Optional[List[ReviewOfSystemsItem]] = None

# ==========================================
# OBJECTIVE SUB-SCHEMAS
# ==========================================

class VitalSignItem(ExtractedItem):
    type: Literal["blood_pressure", "heart_rate", "respiratory_rate", "temperature", "spo2", "weight", "height", "bmi", "pain_score"]
    value: str
    unit: Optional[str] = None
    loinc_code: Optional[str] = None

class PhysicalExamItem(ExtractedItem):
    system: str
    finding: str
    is_abnormal: Optional[bool] = None

class LabResultItem(ExtractedItem):
    test: Optional[CodedConcept] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    interpretation: Optional[Literal["normal", "high", "low", "critical", "unknown"]] = None

class ImagingItem(ExtractedItem):
    modality: Optional[str] = None
    body_site: Optional[str] = None
    impression: Optional[str] = None

class ObjectiveSection(BaseModel):
    vital_signs: Optional[List[VitalSignItem]] = None
    physical_exam: Optional[List[PhysicalExamItem]] = None
    lab_results: Optional[List[LabResultItem]] = None
    imaging_and_diagnostics: Optional[List[ImagingItem]] = None

# ==========================================
# ASSESSMENT SUB-SCHEMAS
# ==========================================

class ProblemItem(ExtractedItem):
    problem_id: str
    diagnosis: CodedConcept
    certainty: Optional[Literal["confirmed", "provisional", "rule_out", "differential"]] = None
    clinical_reasoning: Optional[str] = None
    differential_diagnoses: Optional[List[CodedConcept]] = None

class AssessmentSection(BaseModel):
    summary_statement: Optional[str] = None
    problems: List[ProblemItem]

# ==========================================
# PLAN SUB-SCHEMAS
# ==========================================

class MedicationDetail(BaseModel):
    drug: Optional[CodedConcept] = None
    dose: Optional[str] = None
    route: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

class PlanItem(ExtractedItem):
    problem_id: Optional[str] = None
    category: Literal["medication", "lab_order", "imaging_order", "procedure", "referral", "patient_education", "lifestyle", "follow_up", "other"]
    description: str
    medication_detail: Optional[MedicationDetail] = None

class FollowUpPlan(BaseModel):
    timeframe: Optional[str] = None
    return_precautions: Optional[str] = None

class PlanSection(BaseModel):
    items: Optional[List[PlanItem]] = None
    follow_up: Optional[FollowUpPlan] = None

# ==========================================
# QUALITY SUB-SCHEMAS
# ==========================================

class FlagItem(BaseModel):
    type: Literal["low_asr_confidence", "contradictory_information", "missing_critical_info", "possible_hallucination", "ambiguous_speaker", "medication_safety_concern"]
    detail: Optional[str] = None
    location: Optional[str] = None

class QualitySection(BaseModel):
    overall_confidence: float
    review_status: Literal["draft_unreviewed", "in_review", "approved", "amended"]
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    flags: Optional[List[FlagItem]] = None
    unprocessed_segments: Optional[List[Evidence]] = None

# ==========================================
# ROOT SCHEMA
# ==========================================

class SOAPNoteSchema(BaseModel):
    metadata: NoteMetadata
    subjective: SubjectiveSection
    objective: ObjectiveSection
    assessment: AssessmentSection
    plan: PlanSection
    quality: QualitySection