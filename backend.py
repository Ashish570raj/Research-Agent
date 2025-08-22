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
    
    try:
        response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15
        )

        if response.status_code != 200:
            print("⚠️ IBM IAM token request failed")
            print("Status:", response.status_code)
            print("Response:", response.text)
            response.raise_for_status()

        last_token = response.json().get("access_token")
        last_time = time.time()
        return last_token

    except Exception as e:
        print("❌ Exception while getting IAM token:", str(e))
        raise

@app.post("/predict/")
async def predict(request: ResearchRequest):
    try:
        mltoken = get_ibm_token()
    except Exception as e:
        return {"error": f"Failed to get IBM Cloud IAM token: {e}"}

    if not DEPLOYMENT_URL:
        return {"error": "DEPLOYMENT_URL is not set. Please check your Render environment variables."}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mltoken}"
    }

    research_prompt = (
        f"You are an academic research assistant in the field of {request.field}. "
        f"Provide a concise summary of the following query, suggest references if possible, "
        f"and give actionable suggestions. \n\nQuery: {request.prompt}"
    )

    payload = {"messages": [{"role": "user", "content": research_prompt}]}

    def generate_stream():
        try:
            print("➡️ Sending request to IBM Deployment:", DEPLOYMENT_URL)
            with requests.post(DEPLOYMENT_URL, headers=headers, json=payload, stream=True, timeout=60) as response:
                print("✅ Response Status:", response.status_code)
                if response.status_code != 200:
                    yield f"Error: Deployment request failed. Status: {response.status_code}, Response: {response.text}"
                    return

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
