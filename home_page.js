document.getElementById('essayForm').onsubmit = function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    let essayText = document.getElementById('essayText').value;
    let responseArea = document.getElementById('responseArea');

    // Here you would normally send a request to your server
    // Example using Fetch API:
    fetch('https://essay-eval-heroku-4cb23fb0fd31.herokuapp.com/fetch-issue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({essay: essayText})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); //Processing data here
        responseArea.style.display = 'block';
        responseArea.innerHTML = `<p>Score: ${data.score}</p><p>Feedback: ${data.feedback}</p>`;
    })
    .catch(error => console.error('Error:', error));
};


document.getElementById('fetchIssue').addEventListener('click', function() {
    fetch('/fetch-issue')
    .then(response => response.text())
    .then(text => {
        document.getElementById('issueDisplay').textContent = text;
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
            timer = duration;
        }
    }, 1000);
}
