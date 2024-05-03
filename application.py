from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

application = Flask(__name__)
CORS(application)  # Enable CORS for all domains and routes

# Setting the OpenAI API key from environment variables
openai.api_key = os.getenv('gre_gpt_api_key')

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    """Fetch a new issue task from the GPT model using the updated API."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the gpt-3.5-turbo model
            messages=[{"role": "user", "content": "Give me an issue task with instructions."}],
            max_tokens=150
        )
        # Correctly parsing the response
        issue_task = response.choices[0].message.content.strip()
        
        return jsonify({'issue_task': issue_task}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@application.route('/submit-essay', methods=['POST'])
def submit_essay():
    """Receive an essay and process it."""
    data = request.get_json()
    if not data or 'essay' not in data:
        return jsonify({'error': 'No essay provided'}), 400
    essay = data['essay']
    score, feedback = process_essay(essay)
    return jsonify({'score': score, 'feedback': feedback})

def process_essay(essay):
    """Placeholder function to simulate processing an essay."""
    return "Score Placeholder", "Feedback Placeholder"

if __name__ == '__main__':
    application.run(debug=False)  # It is recommended to turn off debug mode in production environments
