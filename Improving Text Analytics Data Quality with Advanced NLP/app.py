# Backend - Flask API (app.py)
from flask import Flask, request, jsonify, render_template
import spacy
import re
from textblob import TextBlob
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text.lower()

def analyze_text(text):
    cleaned_text = clean_text(text)
    doc = nlp(cleaned_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    sentiment = TextBlob(cleaned_text).sentiment.polarity
    
    return {
        "cleaned_text": cleaned_text,
        "entities": entities,
        "sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = analyze_text(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

