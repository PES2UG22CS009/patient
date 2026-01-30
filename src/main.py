from fastapi import FastAPI
from src.api.patients import router as patients_router
from src.api.doctors import router as doctors_router
from src.api.appointments import router as appointments_router

app = FastAPI(title="Medical Encounter Management System (MEMS)")

app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(doctors_router, prefix="/doctors", tags=["doctors"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
