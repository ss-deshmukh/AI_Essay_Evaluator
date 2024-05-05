import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

application = Flask(__name__)
CORS(application)  # Enable CORS for all domains and routes

# Set the OpenAI API key from environment variables or secure storage
openai.api_key = os.getenv('gre_gpt_api_key')

# Define constants for the assistant and the file
ASSISTANT_ID = "asst_xjUrpr5oEdoZZ2ay3d2MtEsM"
#FILE_ID = "file-0WJRwD4tDJVdyQwOseNw8Dbz"  # This should be the actual file ID of 'issue-pool.pdf' uploaded to OpenAI

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    try:

        assistant = openai.beta.assistants.retrieve(ASSISTANT_ID)


        # Create a Thread for the assistant to use
        thread = openai.beta.threads.create(
        # Create the initial message asking for an issue statement
            fetch_issue_messages = [
                {
                    "role":"user",
                    "content" : "Give me any random issue statement with instructions from the Issue pool document."
                }
            ]
        )

        # Start the run using the file for document retrieval
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id = assistant.id
        )


        time.sleep(5)

        if run.status == "completed":
            # Fetch the messages after the run is complete
                messages = openai.beta.threads.messages.retrieve(
                    thread_id="thread_id"
                )
        
        response_message = messages.data.content.text.value

        return jsonify({"issue_statement": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#changes pending for Submit Essay -----------

@application.route('/submit-essay', methods=['POST'])
def submit_essay():
    data = request.json
    essay = data['essay']
    thread_id = data['thread_id']

    try:
        # Add the user's essay to the thread
        message = openai.Message.create(
            thread_id=thread_id,
            role="user",
            content=essay
        )

        # Continue the run to evaluate the essay
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Fetch the messages for evaluation
        messages = openai.Message.list(thread_id=thread_id)
        evaluation_message = next((m['content'] for m in messages['data'] if m['role'] == 'assistant'), None)

        return jsonify({"evaluation": evaluation_message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    application.run(debug=True)
