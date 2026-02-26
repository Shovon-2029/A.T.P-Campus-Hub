import uvicorn
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import random
import json
import os
import shutil
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = 'complaints_data.json'
UPLOAD_DIR = 'uploads'

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Self-healing database loader
def load_db():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except:
        return {}

def save_db(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generate_tracking_id():
    return f"CW-2026-{random.randint(1000, 9999)}"

@app.get("/")
async def serve_home():
    return FileResponse('complaint.html')

@app.post("/api/complaints")
async def submit_complaint(
    category: str = Form(...),
    incident_date: str = Form(...),
    description: str = Form(...),
    evidence: Optional[UploadFile] = File(None) # Bulletproof file typing
):
    try:
        db = load_db()
        
        tracking_id = generate_tracking_id()
        while tracking_id in db:
            tracking_id = generate_tracking_id()
            
        saved_filename = "No file attached"
        
        # If the user uploaded a file, save it safely
        if evidence and evidence.filename:
            file_extension = evidence.filename.split('.')[-1]
            saved_filename = f"{tracking_id}_evidence.{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, saved_filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(evidence.file, buffer)
        
        # Save all data to JSON
        db[tracking_id] = {
            "category": category,
            "incident_date": incident_date,
            "description": description,
            "evidence_file": saved_filename,
            "status": "Investigation in Progress",
            "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_db(db)
        return {"message": "Success", "tracking_id": tracking_id}
        
    except Exception as e:
        # If it crashes, print the EXACT reason to the terminal!
        print(f"\n❌ CRASH REPORT: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/complaints/{tracking_id}")
async def track_complaint(tracking_id: str):
    db = load_db()
    complaint = db.get(tracking_id.upper())
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Invalid tracking ID or complaint not found.")
    return complaint

if __name__ == "__main__":
    print("SERVER RUNNING! Open http://127.0.0.1:9000 in your browser.")
    uvicorn.run(app, host="127.0.0.1", port=9000)