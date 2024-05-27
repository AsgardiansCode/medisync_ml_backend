import os

from dotenv import load_dotenv
from supabase import create_client, Client
from models import *
from datetime import datetime
from typing import List

load_dotenv()

supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)


def create_activity(activity: ActivityCreate) -> Activity:
    response = supabase.table("data_activity").insert(activity.dict()).execute()
    return Activity(**response.data[0])


def get_activity(activity_id: int) -> Activity:
    response = supabase.table("data_activity").select("*").eq("id", activity_id).execute()
    return Activity(**response.data[0])


def get_user_activities(user_id: int) -> List[Activity]:
    response = supabase.table("data_activity").select("*").eq("user_id", user_id).execute()
    return [Activity(**activity) for activity in response.data]


def create_medication(medication: MedicationCreate) -> Medication:
    response = supabase.table("data_medications").insert(medication.dict()).execute()
    return Medication(**response.data[0])


def get_medication(medication_id: int) -> Medication:
    response = supabase.table("data_medications").select("*").eq("id", medication_id).execute()
    return Medication(**response.data[0])


def get_user_medications(user_id: int) -> List[Medication]:
    response = supabase.table("data_medications").select("*").eq("user_id", user_id).execute()
    return [Medication(**medication) for medication in response.data]


def create_sleep(sleep: SleepCreate) -> Sleep:
    response = supabase.table("data_sleep").insert(sleep.dict()).execute()
    return Sleep(**response.data[0])


def get_sleep(sleep_id: int) -> Sleep:
    response = supabase.table("data_sleep").select("*").eq("id", sleep_id).execute()
    return Sleep(**response.data[0])


def get_user_sleep(user_id: int) -> List[Sleep]:
    response = supabase.table("data_sleep").select("*").eq("user_id", user_id).execute()
    return [Sleep(**sleep) for sleep in response.data]


def create_treatment_adherence(treatment_adherence: TreatmentAdherenceCreate) -> TreatmentAdherence:
    response = supabase.table("data_treatment_adherence").insert(treatment_adherence.dict()).execute()
    return TreatmentAdherence(**response.data[0])


def get_treatment_adherence(treatment_adherence_id: int) -> TreatmentAdherence:
    response = supabase.table("data_treatment_adherence").select("*").eq("id", treatment_adherence_id).execute()
    return TreatmentAdherence(**response.data[0])


def get_user_treatment_adherence(user_id: int) -> List[TreatmentAdherence]:
    response = supabase.table("data_treatment_adherence").select("*").eq("user_id", user_id).execute()
    return [TreatmentAdherence(**treatment_adherence) for treatment_adherence in response.data]


def create_symptom_log(symptom_log: SymptomLogCreate) -> SymptomLog:
    symptom_log_data = {k: v for k, v in symptom_log.dict().items() if k != "symptoms"}
    response = supabase.table("symptom_log").insert(symptom_log_data).execute()
    log_id = response.data[0]["id"]

    symptoms = [dict(log_id=log_id, **symptom.dict()) for symptom in symptom_log.symptoms]
    supabase.table("symptom_details").insert(symptoms).execute()

    return get_symptom_log(log_id)


def get_symptom_log(log_id: int) -> SymptomLog:
    response = supabase.table("symptom_log").select("*").eq("id", log_id).execute()
    log_data = response.data[0]

    symptoms_response = supabase.table("symptom_details").select("*").eq("log_id", log_id).execute()
    log_data["symptoms"] = symptoms_response.data

    return SymptomLog(**log_data)


def get_user_symptom_logs(user_id: int) -> List[SymptomLog]:
    response = supabase.table("symptom_log").select("*").eq("user_id", user_id).execute()
    logs = response.data

    for log in logs:
        symptoms_response = supabase.table("symptom_details").select("*").eq("log_id", log["id"]).execute()
        log["symptoms"] = symptoms_response.data

    return [SymptomLog(**log) for log in logs]


def create_conversation(conversation: ConversationCreate) -> Conversation:
    response = supabase.table("conversations").insert(conversation.dict()).execute()
    return Conversation(**response.data[0])


def get_user_conversations(user_id: int) -> List[Conversation]:
    response = supabase.table("conversations").select("*").eq("user_id", user_id).execute()
    return [Conversation(**conversation) for conversation in response.data]
