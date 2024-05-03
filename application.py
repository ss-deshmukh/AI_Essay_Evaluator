from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

application = Flask(__name__)
CORS(application)  # This enables CORS for all routes, allowing requests from any origin

# Setting the OpenAI API key from environment variables
openai.api_key = os.getenv('gre_gpt_api_key')

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    """Fetch a new issue task from the GPT model."""
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Use an appropriate model; adjust according to your API plan
            prompt="Give me an issue task with instructions.",
            max_tokens=150
        )
        issue_task = response.choices[0].text.strip()
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
    """Placeholder function to simulate processing an essay.
       Replace this with your actual method to evaluate essays."""
    # Here, you would call the OpenAI API or another service to evaluate the essay
    # Returning placeholder values for demonstration
    return "Score Placeholder", "Feedback Placeholder"

if __name__ == '__main__':
    # Run the Flask application on the default host and port
    application.run(debug=False)  # It is recommended to turn off debug mode in production environments
