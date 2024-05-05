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
THREAD_ID = ""
#FILE_ID = "file-0WJRwD4tDJVdyQwOseNw8Dbz"  # This should be the actual file ID of 'issue-pool.pdf' uploaded to OpenAI

@application.route('/')
def home():
    return "Welcome to the Essay Scoring Service!"

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    try:

        # Retrieving Essay_Eval assistant GPT
        assistant = openai.beta.assistants.retrieve(ASSISTANT_ID)

        # Create a Thread with an opening message to initate conversation
        thread = openai.beta.threads.create(
        # Create the initial message asking for an issue statement
            messages = [
                {
                    "role":"user", 
                    "content" : "Give me any random issue statement with instructions from the Issue pool document."
                }
            ]
        )

        # Storing thread id as local variable for next message in same conversation thread
        THREAD_ID = thread.id

        # Starting the run (this is where asistant computes a response)
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id = assistant.id
        )

        # crude way to give enought time for assistant to complete the run, research on polling to change this method 
        while run.status == "queued" or run.status == "in_progress":
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
    
        # Checking if the run is complete
        status = run.status

        # Fetch the messages after the run is complete
        list_messages = openai.beta.threads.messages.list(thread_id=thread.id)
        
        response_message = list_messages.data[0].content[0].text.value #[-1].content[-1].text.value

        return jsonify({"issue_statement": response_message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#changes pending for Submit Essay -----------

@application.route('/submit-essay', methods=['POST'])
def submit_essay():
    data = request.json
    essay = data['essay']
    thread_id = data['thread_id']

    try:
        
        assistant = openai.beta.assistants.retrieve(ASSISTANT_ID)

        thread = openai.beta.threads.retrieve(THREAD_ID)

        # Add the user's essay to the pre existing thread
        messages = openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=essay
        )

        # Continue the run to evaluate the essay
        run = openai.beta.threads.runs.create(
            thread_id = thread.id,
            assistant_id= assistant.id
        )

        while run.status == "queued" or run.status == "in_progress":
            run = openai.beta.threads.runs.retrieve(
                thread_id = thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)

        # Fetch the messages for evaluation
        evaluation = openai.beta.threads.messages.list(thread_id = thread.id)
        evaluation_message = evaluation.data[0].content[0].text.value

        return jsonify({"evaluation": evaluation_message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    application.run(debug=True)
