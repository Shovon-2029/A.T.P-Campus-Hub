from flask import Flask, request, jsonify, render_template
import joblib
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Add this line to allow your HTML to talk to Flask

# 1. Load the trained AI components
vectorizer = joblib.load("ai_vectorizer.pkl")
model = joblib.load("ai_model.pkl")
responses_dict = joblib.load("ai_responses.pkl")

@app.route('/')
def home():
    # This serves your HTML file
    return render_template('student.html') 

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat?"})

    # 2. Transform the user input and Predict
    vectorized_input = vectorizer.transform([user_message.lower()])
    tag = model.predict(vectorized_input)[0]
    
    # 3. Get a random response from the predicted tag
    response = random.choice(responses_dict.get(tag, ["I'm not sure about that, but I can look into it!"]))
    
    return jsonify({"response": response})

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=5000)
    