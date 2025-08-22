# backend.py
import os
import requests
import time
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL")  # Your Granite deployment endpoint

app = FastAPI()

class ResearchRequest(BaseModel):
    prompt: str
    field: str = "General"

# --- Token Caching ---
last_token = None
last_time = 0

def get_ibm_token():
    global last_token, last_time
    if last_token and time.time() - last_time < 3500:  # valid for ~1h
        return last_token
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token_response.raise_for_status()
    last_token = token_response.json().get("access_token")
    last_time = time.time()
    return last_token

@app.post("/predict/")
async def predict(request: ResearchRequest):
    try:
        mltoken = get_ibm_token()
    except Exception as e:
        return {"error": f"Failed to get IBM Cloud IAM token: {e}"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mltoken}"
    }

    research_prompt = (
        f"You are an academic research assistant in the field of {request.field}. "
        f"Provide a concise summary of the following query, suggest references if possible, "
        f"and give actionable suggestions. \n\nQuery: {request.prompt}"
    )

    payload = {
        "messages": [{"role": "user", "content": research_prompt}]
    }

    def generate_stream():
        try:
            with requests.post(DEPLOYMENT_URL, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith("data: "):
                        try:
                            data = json.loads(line.replace("data: ", "", 1))
                            delta = data["choices"][0]["delta"].get("content", "")
                            yield delta
                        except (json.JSONDecodeError, KeyError):
                            continue
        except requests.exceptions.RequestException as e:
            yield f"Error: Failed to connect to AI deployment. {e}"

    return StreamingResponse(generate_stream(), media_type="text/plain")
