from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# ==========================================
# 1. DATABASE SETUP (SQLAlchemy + SQLite)
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./campus_hub.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. DATABASE MODELS
# ==========================================
class ScheduleDB(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String, index=True)
    time = Column(String)
    subject = Column(String)
    room = Column(String)

class AnnouncementDB(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class EventDB(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    event_date = Column(DateTime)
    location = Column(String)

class CampusDetailDB(Base):
    __tablename__ = "campus_details"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)
    info = Column(Text)
    contact_email = Column(String)

class SMSAlertDB(Base):
    __tablename__ = "sms_alerts"
    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String)
    message = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. PYDANTIC SCHEMAS (For Data Validation)
# ==========================================
class ChatMessage(BaseModel):
    message: str

class ScheduleSchema(BaseModel):
    day: str
    time: str
    subject: str
    room: str

class AnnouncementSchema(BaseModel):
    title: str
    content: str

class EventSchema(BaseModel):
    name: str
    description: str
    event_date: datetime
    location: str

# ==========================================
# 4. FASTAPI APPLICATION & CORS
# ==========================================
app = FastAPI(title="ATP Campus Hub API")

# Configure CORS so your frontend HTML can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 5. API ENDPOINTS
# ==========================================

# --- AI CHATBOT FEATURE ---
import joblib
import random
import os

# --- LOAD LOCAL ML AI MODEL ---
# Check if the trained model exists
MODEL_EXISTS = os.path.exists("ai_model.pkl")

if MODEL_EXISTS:
    ai_vectorizer = joblib.load("ai_vectorizer.pkl")
    ai_model = joblib.load("ai_model.pkl")
    ai_responses = joblib.load("ai_responses.pkl")
    print("✅ Indigenous AI Model Loaded Successfully!")
else:
    print("⚠️ AI Model not found. Please run 'python train_ai.py' first.")

# --- AI CHATBOT ENDPOINT ---
@app.post("/api/ai/chat")
async def chat_with_ai(chat: ChatMessage):
    if not MODEL_EXISTS:
        return {"reply": "My AI brain is currently offline. The admin needs to run the training script!"}

    user_msg = chat.message
    
    try:
        # 1. Convert user's text to numbers using our vectorizer
        msg_vectorized = ai_vectorizer.transform([user_msg])
        
        # 2. AI predicts the probability of different intents
        probabilities = ai_model.predict_proba(msg_vectorized)[0]
        max_prob = max(probabilities)
        
        # 3. If the AI is confident enough (e.g., > 30% certainty)
        if max_prob > 0.3:
            # Get the predicted intent tag
            predicted_tag = ai_model.predict(msg_vectorized)[0]
            # Pick a random response from that tag's responses
            reply = random.choice(ai_responses[predicted_tag])
        else:
            # If the AI doesn't understand the question
            reply = "I'm still learning! Could you rephrase that? I can help with food, medical issues, classes, library, and mental health."
            
    except Exception as e:
        reply = "Oops! My neural network had a minor hiccup."
        
    return {"reply": reply}
# --- SCHEDULE FEATURES ---
@app.get("/api/schedule")
def get_schedule(db: Session = Depends(get_db)):
    return db.query(ScheduleDB).all()

@app.post("/api/schedule")
def create_schedule(schedule: ScheduleSchema, db: Session = Depends(get_db)):
    new_schedule = ScheduleDB(**schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

# --- ANNOUNCEMENT FEATURES ---
@app.get("/api/announcements")
def get_announcements(db: Session = Depends(get_db)):
    return db.query(AnnouncementDB).order_by(AnnouncementDB.created_at.desc()).all()

@app.post("/api/announcements")
def create_announcement(announcement: AnnouncementSchema, db: Session = Depends(get_db)):
    new_announcement = AnnouncementDB(**announcement.dict())
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

# --- EVENT FEATURES ---
@app.get("/api/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(EventDB).order_by(EventDB.event_date.asc()).all()

@app.post("/api/events")
def create_event(event: EventSchema, db: Session = Depends(get_db)):
    new_event = EventDB(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# --- CAMPUS DETAILS ---
@app.get("/api/campus-details")
def get_campus_details(db: Session = Depends(get_db)):
    return db.query(CampusDetailDB).all()

# --- SMS & ALERTS ---
@app.get("/api/sms")
def get_sms_alerts(db: Session = Depends(get_db)):
    return db.query(SMSAlertDB).order_by(SMSAlertDB.sent_at.desc()).all()

# ==========================================
# 6. POPULATE DUMMY DATA (For Testing)
# ==========================================
@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    # If no announcements exist, create a dummy one
    if not db.query(AnnouncementDB).first():
        db.add(AnnouncementDB(title="Welcome to ATP", content="Welcome to the new semester!"))
        db.add(EventDB(name="Tech Fest 2026", description="Annual tech festival", event_date=datetime(2026, 3, 15), location="Main Auditorium"))
        db.add(ScheduleDB(day="Monday", time="10:00 AM", subject="Data Structures", room="Room 101"))
        db.commit()
    db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)