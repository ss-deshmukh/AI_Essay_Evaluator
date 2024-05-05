document.getElementById('fetchIssue').addEventListener('click', function() {
    // Fetch the issue task from the correct endpoint
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/fetch-issue')
    .then(response => response.text())  // Handle response as plain text
    .then(data => {
        console.log(data); // Log the issue task
        // Display the plain text response in the issue display area
        document.getElementById('issueDisplay').textContent = data;
    })
    .catch(error => console.error('Error fetching issue:', error));
});

document.getElementById('essayForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    let essayText = document.getElementById('essayText').value;
    let responseArea = document.getElementById('responseArea');

    // Send a request to the Flask server to process the essay
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/submit-essay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({essay: essayText})
    })
    .then(response => response.text())  // Handle response as plain text
    .then(data => {
        console.log(data); // Log and process the response data here
        responseArea.style.display = 'block';
        // Display the plain text response in the response area
        responseArea.textContent = data; 
    })
    .catch(error => console.error('Error:', error));
};