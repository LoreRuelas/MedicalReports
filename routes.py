#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from model import MedicalRecord, MedicalRecordUpdate
from bson import ObjectId
import json 
from bson.json_util import dumps

router = APIRouter()

def get_medical_record_by_id(db, id: str):
    return db.find_one({"_id": id})

def get_patients_by_doctor(db, name_doctor: str):
    #print("NAME DOCTOR: ", name_doctor)
    return db.find({"name_doctor": name_doctor})

def get_certain_patient(db, name_patient: str):
    return db.find({"name_patient": name_patient})

@router.post("/", response_description="Add a new medical record", status_code=status.HTTP_201_CREATED, response_model=MedicalRecord)
def create_medical_record(request: Request, record: MedicalRecord = Body(...)):
    print("Hola on post")
    record_dict = jsonable_encoder(record)
    new_record = request.app.database["medical_db"].insert_one(record_dict)
    created_record = get_medical_record_by_id(request.app.database["medical_db"], new_record.inserted_id)
    return created_record

@router.get("/", response_description="List all medical records", response_model=List[MedicalRecord])
def list_medical_records(request: Request):
    print("Hola on get")
    records = list(request.app.database["medical_db"].find())
    print("Hola dsp records ", records)
    return records

@router.get("/{id}", response_description="Get a single medical record by id", response_model=MedicalRecord)
def find_medical_record(id: str, request: Request):
    #print("Hola on get")
    record = get_medical_record_by_id(request.app.database["medical_db"], id)
    #print("Hol", record)
    if record:
        print(record)
        return record

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")

@router.get("/doctor/{name_doctor}", response_description="Get patients from a doctor", response_model=List[MedicalRecord])
def find_medical_record(name_doctor: str, request: Request):
    #print("Hola on get_by_doctor")
    record = get_patients_by_doctor(request.app.database["medical_db"], name_doctor)
    #print("1: ", record)
    if record:
        x = []
        for i in record:
            x.append(i)
        #print("AAAA: ", x)
        return x

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical records not found")

@router.get("/patient/{name_patient}", response_description="Get info of a certain patient", response_model=List[MedicalRecord])
def find_medical_record(name_patient: str, request: Request):
    #print("Hola on get_by_doctor")
    record = get_certain_patient(request.app.database["medical_db"], name_patient)
    #print("1: ", record)
    if record:
        x = []
        for i in record:
            x.append(i)
        #print("AAAA: ", x)
        return x

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical records not found")

@router.get("/diagnosis/{name_patient}", response_description="Get diagnosis of a certain patient", response_model=List)
def find_medical_record(name_patient: str, request: Request):
    group = [{"$match": {"name_patient": name_patient}},{"$project": {"_id": 0,name_patient: 1, name_patient: 1, "diagnosis": 1}}]
    pipeline = list(request.app.database["medical_db"].aggregate(group))
    print(pipeline)
    if pipeline:
        return pipeline

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical records not found")

@router.get("/patientsDoctor/{name_doctor}", response_description="Get patients number from a doctor", response_model=List)
def find_medical_record(name_doctor: str, request: Request):
    group = [{"$match": {"name_doctor": name_doctor}},{"$group": {"_id": "$name_patient","number_patient": { "$first": "$number_patient" }}}, {"$project": {"_id": 0,"name_patient": "$_id","number_patient": 1}}]
    pipeline = list(request.app.database["medical_db"].aggregate(group))
    print(pipeline)
    if pipeline:
        return pipeline

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical records not found")

@router.put("/{id}", response_description="Update a medical record by id", response_model=MedicalRecord)
def update_medical_record(id: str, request: Request, update: MedicalRecordUpdate = Body(...)):
    update_data = jsonable_encoder(update)
    request.app.database["medical_db"].update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_record = get_medical_record_by_id(request.app.database["medical_db"], id)
    if updated_record:
        return updated_record
    raise HTTPException(status_code=404, detail="Medical record not found")

@router.delete("/{id}", response_description="Delete a medical record")
def delete_medical_record(id: str, request: Request):
    delete_result = request.app.database["medical_db"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Medical record not found")


