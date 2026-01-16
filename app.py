from flask import Flask, request, jsonify, render_template
from collections import Counter
import json
import os

app = Flask(__name__)

# Data Persistence
DATA_FILE = 'feedback_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Load initial data
feedback_store = load_data()

# Constants for Analysis
POSITIVE_WORDS = {
    "shiny", "elegant", "comfortable", "premium", "beautiful", "good", "great", 
    "amazing", "love", "perfect", "nice", "smooth", "light"
}

NEGATIVE_WORDS = {
    "tarnish", "dull", "broke", "uncomfortable", "heavy", "fragile", "bad", 
    "poor", "hate", "worst", "rough", "cheap"
}

THEMES = {
    "Comfort": {"light", "heavy", "fit", "wearable", "comfortable", "uncomfortable", "smooth", "rough"},
    "Durability": {"broke", "strong", "quality", "fragile", "tarnish", "lasting", "sturdy"},
    "Appearance": {"shiny", "dull", "design", "polish", "elegant", "beautiful", "looks", "style"}
}

def analyze_sentiment(text):
    """
    Simple rule-based sentiment analysis.
    Returns 'Positive', 'Negative', or 'Neutral'.
    """
    text_lower = text.lower()
    words = text_lower.split()
    
    pos_count = sum(1 for word in words if word in POSITIVE_WORDS)
    neg_count = sum(1 for word in words if word in NEGATIVE_WORDS)
    
    if pos_count >= neg_count:
        return "Positive"
    else:
        return "Negative"

def detect_themes(text):
    """
    Detects themes present in the text based on keywords.
    Returns a list of detected themes.
    """
    text_lower = text.lower()
    detected = []
    
    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected.append(theme)
                break # Avoid adding same theme multiple times for one review
    
    return detected

# Note: generate_insights is now handled in frontend (Task B3), but keeping backend route if needed for future or legacy support.
# The user explicitly asked to move logic to frontend, but didn't ask to delete the backend endpoint. 
# However, the frontend no longer calls /api/insights. We can leave it or remove it. 
# Given the instruction "move logic", leaving it is harmless but unused.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    
    product_id = data.get('product_id')
    rating = data.get('rating')
    text = data.get('text', '')
    
    if not product_id or not rating:
        return jsonify({"error": "Missing product_id or rating"}), 400
        
    sentiment = analyze_sentiment(text)
    themes = detect_themes(text)
    
    feedback_entry = {
        "product_id": product_id,
        "rating": int(rating),
        "text": text,
        "sentiment": sentiment,
        "themes": themes
    }
    
    feedback_store.append(feedback_entry)
    save_data(feedback_store) # Save to file
    
    return jsonify({"message": "Feedback received", "analysis": {"sentiment": sentiment, "themes": themes}}), 201

@app.route('/api/feedback/<product_id>', methods=['GET'])
def get_feedback(product_id):
    # Reload data to ensure we have the latest if modified externally (optional but good for dev)
    # feedback_store = load_data() 
    # For simplicity and performance, we trust the in-memory store is in sync via save_data
    
    product_reviews = [f for f in feedback_store if f['product_id'] == product_id]
    
    # Aggregate stats
    sentiment_counts = Counter(r['sentiment'] for r in product_reviews)
    theme_counts = Counter()
    for r in product_reviews:
        theme_counts.update(r['themes'])
        
    return jsonify({
        "reviews": product_reviews,
        "stats": {
            "sentiment": dict(sentiment_counts),
            "themes": dict(theme_counts)
        }
    })

@app.route('/api/insights/<product_id>', methods=['GET'])
def get_insights(product_id):
    # This endpoint is likely unused now as logic moved to frontend, but keeping for compatibility
    return jsonify({"insights": []}) 


if __name__ == '__main__':
    app.run(debug=True)
