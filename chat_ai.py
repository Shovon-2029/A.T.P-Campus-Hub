import os
import joblib
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

# ==========================================
# 1. TRAINING FUNCTION (From your 2nd block)
# ==========================================
def train_and_save_model():
    print("Training data not found. Initiating AI training...")
    
    intents = [
        {
            "tag": "greeting",
            "patterns": ["hi", "hello", "hey", "good morning", "what's up", "hey ai"],
            "responses": ["Hello! I am your ATP Campus AI. How can I help you today?", "Hey mate! Need help with your schedule, food, or campus facilities?"]
        },
        {
            "tag": "food",
            "patterns": ["I am hungry", "where is the canteen", "food", "lunch", "cafeteria", "what is there to eat", "dinner", "snacks"],
            "responses": ["The main campus cafeteria is open from 8 AM to 8 PM. Today's special is Veg Thali!", "You can grab snacks at the Nescafe outlet near the Central Library."]
        },
        {
            "tag": "medical",
            "patterns": ["I am sick", "emergency", "doctor", "medical", "fever", "I hurt myself", "hospital", "ambulance"],
            "responses": ["The Campus Medical Center is located in Block B, Ground Floor. For extreme emergencies, call the campus ambulance at 102.", "Please visit the campus clinic! We have a doctor on duty 24/7."]
        },
        {
            "tag": "schedule",
            "patterns": ["where is my class", "timetable", "schedule", "lecture", "what class is next", "attendance"],
            "responses": ["You can view your real-time schedule by clicking the 'Schedule' tab on your dashboard.", "Please check the Schedule section above for your updated timetable and room numbers."]
        },
        {
            "tag": "stress",
            "patterns": ["I am stressed", "depressed", "anxious", "exams are hard", "pressure", "mental health", "sad"],
            "responses": ["College can be tough, but you are not alone! The campus counselor is available in the Student Center from 10 AM - 4 PM. Take a deep breath.", "Please don't stress too much. Reach out to our campus mental health support team at wellness@atp.edu."]
        },
        {
            "tag": "library",
            "patterns": ["books", "library", "where can I study", "quiet place", "issue a book"],
            "responses": ["The Central Library is open 24/7 during exam weeks. Don't forget your Student ID card to issue books!", "Looking for a quiet place? The 3rd floor of the Central Library is a silent study zone."]
        },
        {
            "tag": "lost_found",
            "patterns": ["I lost my wallet", "lost and found", "I found a phone", "missing ID card", "where is lost and found"],
            "responses": ["Lost something? Check with the main security desk at Gate 1. They maintain the official lost and found registry."]
        },
        {
            "tag": "hostel",
            "patterns": ["hostel", "dorm", "warden", "room cleaning", "hostel complaint"],
            "responses": ["For hostel-related issues, please contact your respective Block Warden or raise an issue in the 'Complaint' tab on the menu."]
        }
    ]

    X_train = []
    y_train = []
    responses_dict = {}

    for intent in intents:
        responses_dict[intent["tag"]] = intent["responses"]
        for pattern in intent["patterns"]:
            X_train.append(pattern)
            y_train.append(intent["tag"])

    print("Converting text to numbers using TF-IDF...")
    vectorizer = TfidfVectorizer(lowercase=True)
    X_train_vectorized = vectorizer.fit_transform(X_train)

    print("Training the Indigenous Neural Network Model...")
    model = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=2000, random_state=42)
    model.fit(X_train_vectorized, y_train)

    print("Saving the AI model locally...")
    joblib.dump(vectorizer, "ai_vectorizer.pkl")
    joblib.dump(model, "ai_model.pkl")
    joblib.dump(responses_dict, "ai_responses.pkl")
    print("✅ AI Training Complete! Your indigenous model is saved and ready to use.\n")

# ==========================================
# 2. FLASK APP SETUP (From your 1st block)
# ==========================================

# Check if models exist, if not, train them first
if not (os.path.exists("ai_vectorizer.pkl") and os.path.exists("ai_model.pkl") and os.path.exists("ai_responses.pkl")):
    train_and_save_model()

app = Flask(__name__)
CORS(app)

# Load the trained AI components into memory
print("Loading trained AI components into memory...")
vectorizer = joblib.load("ai_vectorizer.pkl")
model = joblib.load("ai_model.pkl")
responses_dict = joblib.load("ai_responses.pkl")
print("✅ Components loaded. Starting server...")

@app.route('/')
def home():
    # Make sure you have a templates folder with student.html inside it!
    return render_template('student.html') 

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat?"})

    # Transform the user input and Predict
    vectorized_input = vectorizer.transform([user_message.lower()])
    tag = model.predict(vectorized_input)[0]
    
    # Get a random response from the predicted tag
    response = random.choice(responses_dict.get(tag, ["I'm not sure about that, but I can look into it!"]))
    
    return jsonify({"response": response})

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=5001)