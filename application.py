from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

application = Flask(__name__)
CORS(application)  # Enable CORS for all domains and routes

# Setting the OpenAI API key and project ID from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
# openai.organization = os.getenv('OPENAI_ORG')  # Optional, set this if you have an organization ID

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    """Fetch a new issue task from the 'Essay-Eval' assistant."""
    try:
        response = openai.assistants.create(
            project_id="proj_EgViVREljr0o5yENJbmxrtdF" , # Project ID associated with the assistant,
            assistant_id="asst_xjUrpr5oEdoZZ2ay3d2MtEsM", # Essay-Eval assistant ID
            #model="gpt-3.5-turbo",  # assistant model selected
            messages=[{"role": "user", "content": "Give me an issue task with instructions."}],
            max_tokens=150
        )
        # Correctly parsing the response
        issue_task = response.choices[0].messages.content.strip()
        return jsonify({'issue_task': issue_task}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@application.route('/submit-essay', methods=['POST'])
def submit_essay():
    """Receive an essay and process it using the 'Essay-Eval' assistant."""
    data = request.get_json()
    if not data or 'essay' not in data:
        return jsonify({'error': 'No essay provided'}), 400
    essay = data['essay']
    try:
        response = openai.assistants.create(
            project_id="proj_EgViVREljr0o5yENJbmxrtdF",
            assistant_id="asst_xjUrpr5oEdoZZ2ay3d2MtEsM",
            model="gpt-3.5-turbo",  # Confirm this
            messages=[{"role": "user", "content": essay}],
            max_tokens=500
        )
        feedback = response.choices[0].messages.content.strip()
        score = "Score calculated from feedback"  # Define how you calculate the score based on feedback
        return jsonify({'score': score, 'feedback': feedback}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    application.run(debug=False)  # It is recommended to turn off debug mode in production environments
