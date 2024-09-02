#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field


####
class MedicalRecord(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name_patient: str = Field(...)
    mail_patient: str = Field(...)
    number_patient: str = Field(...)
    name_doctor: str = Field(...)
    mail_doctor: str = Field(...)
    number_doctor: str = Field(...)
    diagnosis: str = Field(...)
    date: str = Field(...)

    class Config:
        #allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "name_patient": "Juan Perez",
                "mail_patient": "juan.perez@example.com",
                "number_patient": "555-0101",
                "name_doctor": "Dr. Ana Torres",
                "mail_doctor": "ana.torres@hospital.com",
                "number_doctor": "555-1001",
                "diagnosis": "Diabetes tipo 2",
                "date": "2022-03-15T14:00:00Z"
            }
        }



class MedicalRecordUpdate(BaseModel):
    name_patient: Optional[str]
    mail_patient: Optional[str]
    number_patient: Optional[str]
    name_doctor: Optional[str]
    mail_doctor: Optional[str]
    number_doctor: Optional[str]
    diagnosis: Optional[str]
    date: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "name_patient": "Juan Perez",
                "mail_patient": "juan.update@example.com",
                "number_patient": "555-0102",
                "name_doctor": "Dr. Ana Torres",
                "mail_doctor": "ana.update@hospital.com",
                "number_doctor": "555-1002",
                "diagnosis": "Diabetes tipo 1",
                "date": "2023-03-15T14:00:00Z"
            }
        }