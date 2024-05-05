document.getElementById('fetchIssue').addEventListener('click', function() {
    // Fetch the issue task from the correct endpoint
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/fetch-issue')
    .then(response => response.json())  // assuming the response is also in JSON format
    .then(data => {
        console.log(data); // Log the issue task
        let issueDisplay = document.getElementById('issueDisplay');
        issueDisplay.textContent = data.issue_statement; // Display the fetched issue task
        // Store the thread_id for later use when submitting the essay
        sessionStorage.setItem("currentThreadID", data.thread_id);
    })
    .catch(error => console.error('Error fetching issue:', error));
});

document.getElementById('essayForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    let essayText = document.getElementById('essayText').value;
    let responseArea = document.getElementById('responseArea');

    // Assuming you have a way to store and retrieve the current thread_id
    let thread_id = sessionStorage.getItem("currentThreadID");

    // Send a request to the Flask server to process the essay
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/submit-essay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({essay: essayText, thread_id: thread_id})
    })
    .then(response => response.json())  // Handle response as JSON
    .then(data => {
        console.log(data); // Log and process the response data here
        responseArea.style.display = 'block';
        // Display the evaluation response in the response area
        responseArea.textContent = `Evaluation: ${data.evaluation_message}`;
    })
    .catch(error => console.error('Error:', error));
};


