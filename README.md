# ETL Data Pipeline on GCP (Cloud Composer + Data Fusion + BigQuery + Looker)

This project is a small end-to-end **ETL pipeline on Google Cloud**.  
I generate **fake employee data**, **hash passwords**, upload the file to **Cloud Storage**, then use **Cloud Data Fusion** to transform and load it into **BigQuery**. Finally, the data is ready to be explored in **Looker / Looker Studio**.

The goal is to show a *realistic* pipeline (even with the real problems you hit on GCP: quotas, Dataproc cluster configs, compute profiles, etc.).

---

## Architecture
<img width="808" height="345" alt="ETL Pipeline drawio" src="https://github.com/user-attachments/assets/5299a928-bc4d-49f2-bdd7-af89bc4aa65f" />



**Flow**
1. **Cloud Composer (Airflow)** runs the workflow (or you can run it manually).
2. **Python extraction script** generates fake data + hashes passwords.
3. The CSV lands in **Cloud Storage**.
4. **Cloud Data Fusion** reads from GCS, transforms with Wrangler, and loads into **BigQuery**.
5. **Looker / Looker Studio** visualizes the BigQuery table.

---

## What I built 

I started with a simple idea: “Let’s create a small employee dataset and move it through a real cloud pipeline.”

### 1) Generate fake data (Python)
I used a Python script (`extracte.py`) to generate a CSV file like:

- employee_id  
- first_name / last_name  
- email  
- department  
- salary  
- hire_date  
- **password_hash** (important: not plain text)

Why fake data? Because it’s the safest way to build and demo a pipeline without touching real personal data.

### 2) Hash the passwords (security step)
Instead of storing passwords as text (never do that), I hash them before writing the CSV.

- Hashing is **one-way**
- I used **salted hashing** (ex: bcrypt style) so the same password doesn’t always produce the same hash
- Result: even if someone sees the CSV, they can’t “read” the original passwords

## Important!! The output contains only: `password_hash`, never the real password.

### 3) Upload to Cloud Storage
Once the CSV is generated locally, I push it to a **GCS bucket** (landing zone).  
That bucket is the “handoff point” between extraction and transformation.

### 4) Transform + Load with Cloud Data Fusion
In **Cloud Data Fusion**, I built a pipeline with:

- **GCSFile** (source)
- **Wrangler** (transformations)
  - set correct column types
  - rename columns if needed
  - clean nulls / bad values
- **BigQuery** (sink)

So the final dataset ends up inside BigQuery as a clean table.

### 5) Analytics with Looker
Once it’s in BigQuery, it’s super easy to connect Looker (or Looker Studio) and build dashboards.

---

## What I did on GCP (step-by-step)

### Services used
- **Cloud Storage**: store the raw CSV
- **Cloud Data Fusion**: ETL transformations + BigQuery load
- **Cloud Dataproc** (behind Data Fusion): execution engine for the pipeline
- **BigQuery**: final warehouse
- **Cloud Composer (Airflow)**: orchestration (optional but recommended)
- **Looker / Looker Studio**: visualization

### Setup (high level)
1. Created a **GCS bucket** (example: `gs://<your-bucket>/raw/employee_data.csv`)
2. Created a **BigQuery dataset** + table destination
3. Created a **Cloud Data Fusion instance**
4. Built the pipeline in Data Fusion (GCSFile → Wrangler → BigQuery)
5. (Optional) Created a **Composer environment** and triggered the pipeline from Airflow

---

## How to run it (local → GCS)

### 1) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
