#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"  # Asegúrate de que la URL sea correcta para tu API

def main():
    with open("medical_records.csv", 'r', encoding='utf-8') as fd:
        records_csv = csv.DictReader(fd)
        print(records_csv)
        for record in records_csv:
            
            # Enviar el registro a la API
            response = requests.post(BASE_URL+"/medical_records", json=record)
            if not response.ok:
                print(f"Failed to post medical record {response} - {record}")

if __name__ == "__main__":
    main()
