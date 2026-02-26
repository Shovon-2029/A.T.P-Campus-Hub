from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime

# Initialize the Flask server
server = Flask(__name__)

# This is the magic line that fixes the error in your screenshot. 
# It allows your HTML file to send data here without being blocked.
CORS(server)

DATA_FILE = 'reviews_data.json'

# Setup initial mock data if the JSON file doesn't exist yet
def init_db():
    if not os.path.exists(DATA_FILE):
        default_reviews = [
            {
                "name": "Ayan Naskar",
                "rating": 4,
                "comment": "Great faculty and good placements. Hostel life is fun, but mess food can be improved. The central library is huge.",
                "date": "15 Feb 2026"
            },
            {
                "name": "Shovon Roy",
                "rating": 5,
                "comment": "The campus is breathtaking — literally on the beach! Labs are world-class and the library is 24/7. Highly recommend CSE, and IT departments.",
                "date": "02 Feb 2026"
            },
            {
                "name": "Anik Sarkar",
                "rating": 5,
                "comment": "I loved the innovation center and the open-air auditorium. The institute takes research seriously. Lots of fests and student clubs.",
                "date": "12 Jan 2026"
            }
        ]
        with open(DATA_FILE, 'w') as f:
            json.dump(default_reviews, f, indent=4)

init_db()

# Route to serve your exact HTML file
@server.route('/')
def home():
    return send_file('campus.html')

# API Route to GET all reviews
@server.route('/api/reviews', methods=['GET'])
def get_reviews():
    with open(DATA_FILE, 'r') as f:
        reviews = json.load(f)
    return jsonify(reviews)

# API Route to POST a new review
@server.route('/api/reviews', methods=['POST'])
def add_review():
    new_data = request.json
    
    # Generate today's date
    date_str = datetime.now().strftime("%d %b %Y")
    
    review_entry = {
        "name": new_data.get("name", "").strip(),
        "rating": int(new_data.get("rating", 5)),
        "comment": new_data.get("comment", "").strip(),
        "date": date_str
    }

    # Load existing, insert new at the top, and save
    with open(DATA_FILE, 'r') as f:
        reviews = json.load(f)
        
    reviews.insert(0, review_entry)

    with open(DATA_FILE, 'w') as f:
        json.dump(reviews, f, indent=4)
        
    return jsonify({"status": "success", "review": review_entry}), 201

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    server.run(debug=True, port=5000)