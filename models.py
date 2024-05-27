from pydantic import BaseModel
from datetime import datetime, time
from typing import List, Optional


class ActivityBase(BaseModel):
    user_id: int
    activity_type: str
    duration: float
    steps_taken: Optional[int]
    calories_burned: Optional[float]
    avg_heart_rate: Optional[float]
    created_at: datetime


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True


class MedicationBase(BaseModel):
    user_id: int
    medication_name: str
    dosage: float
    measurement: str
    frequency_hours: float
    time_of_intake: time
    start_date: datetime
    end_date: datetime
    created_at: datetime
    treatment_adherence: bool


class MedicationCreate(MedicationBase):
    pass


class Medication(MedicationBase):
    id: int

    class Config:
        orm_mode = True


class SleepBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    sleep_quality: int
    interruptions: int
    created_at: datetime


class SleepCreate(SleepBase):
    pass


class Sleep(SleepBase):
    id: int

    class Config:
        orm_mode = True


class TreatmentAdherenceBase(BaseModel):
    user_id: int
    medication_id: int
    intake_confirmed: bool
    notes: Optional[str]
    created_at: datetime


class TreatmentAdherenceCreate(TreatmentAdherenceBase):
    pass


class TreatmentAdherence(TreatmentAdherenceBase):
    id: int

    class Config:
        orm_mode = True


class SymptomDetailBase(BaseModel):
    symptom_type: str
    severity: float
    duration: float
    notes: Optional[str]
    created_at: datetime


class SymptomDetailCreate(SymptomDetailBase):
    log_id: int


class SymptomDetail(SymptomDetailBase):
    id: int

    class Config:
        orm_mode = True


class SymptomLogBase(BaseModel):
    user_id: int
    created_at: datetime


class SymptomLogCreate(SymptomLogBase):
    symptoms: List[SymptomDetailCreate]


class SymptomLog(SymptomLogBase):
    id: int
    symptoms: List[SymptomDetail]

    class Config:
        orm_mode = True


class ConversationBase(BaseModel):
    user_id: int
    message: str
    response: Optional[str] = None
    timestamp: datetime

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int

    class Config:
        orm_mode = True