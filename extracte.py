from faker import Faker
import pandas as pd 
import hashlib 
import random 
import csv
from google.cloud import storage  

fake =Faker()

NUM_EMPLOYEES = 1000
BUCKET_NAME = "bkt-employee-dat4"




def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
def generate_employee_data(n):
    employees = []

    for i  in range(n):
        raw_password = fake.password()
        employee = { 
            "employee_id": f"E{i+1000}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),                      # PII
            "phone_number": fake.phone_number(),        # PII
            "date_of_birth": fake.date_of_birth(minimum_age=22, maximum_age=60),
            "address": fake.address().replace("\n", ", "),  # PII
            "job_title": fake.job(),
            "department": random.choice(
                ["IT", "HR", "Finance", "Sales", "Operations"]
            ),
            "salary": random.randint(30000, 90000),     # Sensitive
            "password_hash": hash_password(raw_password),  # 🔐 Hashed password
            "hire_date": fake.date_between(start_date="-10y", end_date="today"),
            "country": fake.country()
                    }
        employees.append(employee)
    return pd.DataFrame(employees)


def upload_to_gcs(bucket_name, local_file, gcs_path):
    client =storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    blob.upload_from_filename(local_file)
    print(f" upload file terminée gs://{bucket_name}/{gcs_path}")


if __name__ == "__main__":
    df = generate_employee_data(NUM_EMPLOYEES) # 1️⃣ Génération des données
    # 2️⃣ Sauvegarde locale 
    df.to_csv("employee_data.csv",index=False)
    print("Fichier csv creer localement : ")
    print(df.head())


    # 3️⃣ Upload vers GCS
    upload_to_gcs(
        bucket_name = "bkt-employee-dat4",
        local_file = "employee_data.csv",
        gcs_path = "raw/employee_data.csv"
     )


   







