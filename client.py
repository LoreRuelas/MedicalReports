#!/usr/bin/env python3
import argparse
import logging
import os
import requests


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('medical_db.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
MED_API_URL = os.getenv("MED_API_URL", "http://localhost:8000")

def print_aggregation(aggregate):
    for k in aggregate.keys():
        print(f"{k}: {aggregate[k]}")
    print("="*50)

def print_data(report):
    for k in report.keys():
        print(f"{k}: {report[k]}")
    print("="*50)

def print_all(report):
    print(report)

def list_patients_by_doctor(name_doctor):

    # for the route
    suffix = f"/medical_records/doctor/{name_doctor}"
    endpoint = MED_API_URL + suffix
    
    # get response
    response = requests.get(endpoint)

    if response.ok:
        json_resp = response.json()
        # print if correct response
        for book in json_resp:
            print_data(book)
    else:
        # print if error
        print(f"Error: {response}")


def list_info_patient(name_patient):

    # for the route
    suffix = f"/medical_records/patient/{name_patient}"
    endpoint = MED_API_URL + suffix
    
    # get response
    response = requests.get(endpoint)

    if response.ok:
        json_resp = response.json()
        # print if correct response
        for book in json_resp:
            print_data(book)
    else:
        # print if error
        print(f"Error: {response}")

def list_diagnosis_patient(name_patient):
    # for the route
    suffix = f"/medical_records/diagnosis/{name_patient}"
    endpoint = MED_API_URL + suffix
    
    # get response
    response = requests.get(endpoint)

    if response.ok:
        json_resp = response.json()
        # print if correct response
        for book in json_resp:
            print_aggregation(book)
    else:
        # print if error
        print(f"Error: {response}")

def list_patients_doctor(name_doctor):
    # for the route
    suffix = f"/medical_records/patientsDoctor/{name_doctor}"
    endpoint = MED_API_URL + suffix
    
    # get response
    response = requests.get(endpoint)

    if response.ok:
        json_resp = response.json()
        # print if correct response
        for book in json_resp:
            print_aggregation(book)
    else:
        # print if error
        print(f"Error: {response}")

def get_patient_by_id(id):
    suffix = f"/medical_records/{id}"
    endpoint = MED_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_data(json_resp)
    else:
        print(f"Error: {response}")



def get_patients():
    suffix = f"/medical_records"
    endpoint = MED_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        for book in json_resp:
            print_data(book)
    else:
        print(f"Error: {response}")


def main():
    log.info(f"Welcome to medical report handler. App requests to: {MED_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search_patients_from_doctor","search_diagnosis_patient", "search_by_patient", "search_by_doctor", "get"]

    parser.add_argument("action", choices=list_of_actions, help="Action to be user of the medical reports")
    parser.add_argument("-i", "--id",help="Provide a book ID which related to the book action", default=None)
    # declaration of parameters
    parser.add_argument("-np", "--name_patient", help="Search parameter to look for reports of a certain patient", default=0)
    parser.add_argument("-nd", "--name_doctor", help="Search parameter to look for report made by a certain doctor", default=0)
    parser.add_argument("-nump", "--num_patient", help="Search parameter to look for a number of a certain patient", default=0)
    
    args = parser.parse_args()

    if args.id and not args.action in ["search_patients_from_doctor","search_diagnosis_patient", "search_by_patient", "search_by_doctor", "get"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)


    if args.action == "search_by_doctor" and args.name_doctor:
        list_patients_by_doctor(args.name_doctor)
    elif args.action == "search_diagnosis_patient" and args.name_patient:
        list_diagnosis_patient(args.name_patient)
    elif args.action == "search_patients_from_doctor" and args.name_doctor:
        list_patients_doctor(args.name_doctor)
    elif args.action == "search_by_patient" and args.name_patient:
        list_info_patient(args.name_patient)
    elif args.action == "get" and args.id:
        get_patient_by_id(args.id)
    elif args.action == "get" and not args.id:
        get_patients()

if __name__ == "__main__":
    main()