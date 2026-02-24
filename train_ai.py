import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
import random

# 1. THE DATASET: Campus Problems and Solutions
# You can add as many patterns and responses here as you want!
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

# 2. PREPARING THE DATA FOR THE MACHINE LEARNING MODEL
X_train = []
y_train = []
responses_dict = {}

for intent in intents:
    responses_dict[intent["tag"]] = intent["responses"]
    for pattern in intent["patterns"]:
        X_train.append(pattern)
        y_train.append(intent["tag"])

# 3. TEXT VECTORIZATION (Converting words into numbers)
print("Converting text to numbers using TF-IDF...")
vectorizer = TfidfVectorizer(lowercase=True)
X_train_vectorized = vectorizer.fit_transform(X_train)

# 4. NEURAL NETWORK TRAINING (Multi-Layer Perceptron)
print("Training the Indigenous Neural Network Model...")
model = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=2000, random_state=42)
model.fit(X_train_vectorized, y_train)

# 5. SAVING THE TRAINED MODEL TO YOUR LOCAL MACHINE
print("Saving the AI model locally...")
joblib.dump(vectorizer, "ai_vectorizer.pkl")
joblib.dump(model, "ai_model.pkl")
joblib.dump(responses_dict, "ai_responses.pkl")

print("✅ AI Training Complete! Your indigenous model is saved and ready to use.")