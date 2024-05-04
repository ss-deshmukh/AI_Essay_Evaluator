from flask import Flask, request, jsonify, render_template
import openai
import os

application = Flask(__name__)

# Set the OpenAI API key from environment variables or secure storage
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define constants for the assistant and the file
ASSISTANT_ID = "asst_xjUrpr5oEdoZZ2ay3d2MtEsM"
FILE_ID = "file-0WJRwD4tDJVdyQwOseNw8Dbz"  # This should be the actual file ID of 'issue-pool.pdf' uploaded to OpenAI

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/fetch-issue', methods=['GET'])
def fetch_issue():
    try:
        # Create a Thread for the assistant to use
        thread = openai.Thread.create(assistant_id=ASSISTANT_ID)
        thread_id = thread['id']

        # Create the initial message asking for an issue statement
        message = openai.Message.create(
            thread_id=thread_id,
            role="user",
            content="Give me the issue statement with instructions."
        )

        # Start the run using the file for document retrieval
        run = openai.Run.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            file_ids=[FILE_ID]
        )

        # Fetch the messages after the run is complete
        messages = openai.Message.list(thread_id=thread_id)
        response_message = next((m['content'] for m in messages['data'] if m['role'] == 'assistant'), None)

        return jsonify({"issue_statement": response_message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        run = openai.Run.create(
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
