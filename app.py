import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv

import crud
import schemas
import requests

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")
supa: Client = create_client(url, key)

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

eureka_server = "http://localhost:8761/eureka/apps/"
app_name = "ml_backend"
instance_id = f"{app_name}:{'localhost'}"

#
# class Context(BaseModel):
#     location: str = Field(..., example="Home")
#     time_of_day: str = Field(..., example="Morning")
#     social_context: str = Field(..., example="Alone")
#     mood: str = Field(..., example="Happy")
#     device: str = Field(..., example="Smartphone")
#
#
# # Function modified to accept a Context instance and convert it
# def get_user_context(context: Context):
#     user_context = {
#         'time_of_day': context.time_of_day,
#         'location': context.location,
#         'social_context': context.social_context,
#         'mood': context.mood,
#         'device': context.device
#     }
#     return user_context


def register_service():
    instance_info = {
        "instance": {
            "instanceId": instance_id,
            "hostName": "localhost",
            "app": app_name.upper(),
            "ipAddr": "127.0.0.1",
            "vipAddress": app_name,
            "secureVipAddress": app_name,
            "statusPageUrl": "http://localhost:8000",
            "port": {"$": 8000, "@enabled": "true"},
            "dataCenterInfo": {
                "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
                "name": "MyOwn"
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(eureka_server + app_name, json=instance_info, headers=headers)
    print(f"Registered with Eureka: {response.status_code}")

@app.on_event("startup")
def on_startup():
    register_service()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI service!"}

@app.post("/activities/", response_model=schemas.Activity)
def create_activity(activity: schemas.ActivityCreate):
    return crud.create_activity(activity)


@app.get("/activities/{id}", response_model=schemas.Activity)
def get_activity(id: int):
    activity = crud.get_activity(id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.get("/users/{user_id}/activities/", response_model=List[schemas.Activity])
def get_user_activities(user_id: int):
    return crud.get_user_activities(user_id)


@app.post("/medications/", response_model=schemas.Medication)
def create_medication(medication: schemas.MedicationCreate):
    return crud.create_medication(medication)


@app.get("/medications/{id}", response_model=schemas.Medication)
def get_medication(id: int):
    medication = crud.get_medication(id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


@app.get("/users/{user_id}/medications/", response_model=List[schemas.Medication])
def get_user_medications(user_id: int):
    return crud.get_user_medications(user_id)


@app.post("/sleep/", response_model=schemas.Sleep)
def create_sleep(sleep: schemas.SleepCreate):
    return crud.create_sleep(sleep)


@app.get("/sleep/{id}", response_model=schemas.Sleep)
def get_sleep(id: int):
    sleep = crud.get_sleep(id)
    if not sleep:
        raise HTTPException(status_code=404, detail="Sleep data not found")
    return sleep


@app.get("/users/{user_id}/sleep/", response_model=List[schemas.Sleep])
def get_user_sleep(user_id: int):
    return crud.get_user_sleep(user_id)


@app.post("/treatment_adherence/", response_model=schemas.TreatmentAdherence)
def create_treatment_adherence(treatment_adherence: schemas.TreatmentAdherenceCreate):
    return crud.create_treatment_adherence(treatment_adherence)


@app.get("/treatment_adherence/{id}", response_model=schemas.TreatmentAdherence)
def get_treatment_adherence(id: int):
    treatment_adherence = crud.get_treatment_adherence(id)
    if not treatment_adherence:
        raise HTTPException(status_code=404, detail="Treatment adherence not found")
    return treatment_adherence


@app.get("/users/{user_id}/treatment_adherence/", response_model=List[schemas.TreatmentAdherence])
def get_user_treatment_adherence(user_id: int):
    return crud.get_user_treatment_adherence(user_id)


@app.post("/symptom_logs/", response_model=schemas.SymptomLog)
def create_symptom_log(symptom_log: schemas.SymptomLogCreate):
    return crud.create_symptom_log(symptom_log)

@app.get("/users/{user_id}/symptom_logs/", response_model=List[schemas.SymptomLog])
def get_user_symptom_logs(user_id: int):
    return crud.get_user_symptom_logs(user_id)


@app.post("/conversations/", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate):
    conversation.timestamp = datetime.utcnow()
    conversation.response = "This is a dummy response for your symptom: " + conversation.message
    return crud.create_conversation(conversation)


@app.get("/users/{user_id}/conversations/", response_model=List[schemas.Conversation])
def get_user_conversations(user_id: int):
    return crud.get_user_conversations(user_id)


#
# curl -i -X POST http://localhost:8001/services/ --data name=fastapi-service --data url=http://localhost:8000
#
# curl -i -X POST http://localhost:8001/services/fastapi-service/routes --data 'paths[]=/fastapi'