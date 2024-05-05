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
    .then(response => response.json())
    .then(data => {
        console.log(data); // Log and process the response data here
        responseArea.style.display = 'block';
        responseArea.innerHTML = `<p>Score: ${data.score}</p><p>Feedback: ${data.feedback}</p>`;
    })
    .catch(error => console.error('Error:', error));
};

document.getElementById('fetchIssue').addEventListener('click', function() {
    // Fetch the issue task from the correct endpoint
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/fetch-issue')
    .then(response => response.json())  // assuming the response is also in JSON format
    .then(data => {
        console.log(data); // Log the issue task
        document.getElementById('issueDisplay').textContent = data.issue_task; // Display the fetched issue task
        startTimer();
    })
    .catch(error => console.error('Error fetching issue:', error));
});

function startTimer() {
    let duration = 30 * 60; // 30 minutes
    let timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById('timer').textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;  // Reset the timer after 30 minutes
        }
    }, 1000);
}
