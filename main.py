from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string
from datetime import datetime

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for demonstration (resets when server restarts)
complaints_db = {}

# Define the expected data format from the frontend
class Complaint(BaseModel):
    title: str
    category: str
    description: str
    is_anonymous: bool

def generate_tracking_id():
    """Generate a random 12-character alphanumeric tracking ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

@app.post("/api/complaints")
async def submit_complaint(complaint: Complaint):
    tracking_id = generate_tracking_id()
    
    # Save to mock database
    complaints_db[tracking_id] = {
        "title": complaint.title,
        "category": complaint.category,
        "description": complaint.description,
        "is_anonymous": complaint.is_anonymous,
        "status": "Pending Investigation",
        "date_submitted": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return {"message": "Success", "tracking_id": tracking_id}

@app.get("/api/complaints/{tracking_id}")
async def track_complaint(tracking_id: str):
    # Lookup complaint by ID
    complaint = complaints_db.get(tracking_id.upper())
    
    if not complaint:
        raise HTTPException(status_code=404, detail="Invalid tracking ID or complaint not found.")
        
    return complaint

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
