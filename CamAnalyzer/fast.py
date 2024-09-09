# Filename: main.py

from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from pydantic import BaseModel
import pandas as pd
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize BigQuery Client

@app.get("/get_beach_data")
def get_beach(beach_code):
    """
    Endpoint to retrieve beach data from BigQuery based on beach_name.
    """
    client = bigquery.Client()

    # Define your query with a placeholder for beach_name
    query = """SELECT * FROM `lewagon-data-428814.SQM_Dataset.SQM` ORDER BY Finish_Date DESC LIMIT 1"""



    # Execute the query
    query_job = client.query(query)
    results = query_job.result()
    df = results.to_dataframe()
    return df.to_json()

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

# To run the server, use the command: uvicorn main:app --reload
