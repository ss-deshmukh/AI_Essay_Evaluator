from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

application = Flask(__name__)
CORS(application)
# Define your OpenAI API key here. Ensure this key is kept secure and not exposed.
openai.api_key = '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'

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    """Fetch a new issue task from the GPT model."""
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Use an appropriate model; adjust according to your API plan
        prompt="Give me an issue task with instructions.",
        max_tokens=150
    )
    issue_task = response.choices[0].text.strip()
    return issue_task

@application.route('/submit-essay', methods=['POST'])
def submit_essay():
    """Receive an essay and process it."""
    data = request.get_json()
    essay = data['essay']
    score, feedback = process_essay(essay)
    return jsonify({'score': score, 'feedback': feedback})

def process_essay(essay):
    """Placeholder function to simulate processing an essay.
       Replace this with your actual method to evaluate essays."""
    # Simulate processing by making another API call (not implemented here)
    # This is where you would integrate with the API for actual essay scoring
    return "Score Placeholder", "Feedback Placeholder"

if __name__ == '__main__':
    # Run the Flask application
    application.run(debug=True, port=5000)
