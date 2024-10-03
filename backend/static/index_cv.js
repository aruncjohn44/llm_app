
const loadingIndicator = document.getElementById('loadingIndicator'); 

// Show the loading indicator before sending the request
loadingIndicator.style.display = 'none';

document.getElementById('submitBtn').addEventListener('click', function() {
    // Get the file input and job description
    let cvFile = document.getElementById('cvUpload').files[0];
    let jobDescription = document.getElementById('jobDescription').value;

    if (!cvFile || !jobDescription) {
        alert("Please upload a CV and enter a job description.");
        return;
    }

    // Create FormData object to hold the file and text data
    let formData = new FormData();
    formData.append('cv', cvFile);
    formData.append('jobDescription', jobDescription);

    // Show the loading indicator before sending the request
    loadingIndicator.style.display = 'block'; // Show the loading indicator

    // Send an AJAX request to the Flask backend
    fetch('/compare_cv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        // Hide the loading indicator when the response is received
        loadingIndicator.style.display = 'none';
        // Display results from the backend
        document.getElementById('matchScore').querySelector('p').innerText = data.match_score + '%';
        // Assuming `data.matching_keywords` and `data.missing_keywords` contain arrays of skills
        document.getElementById('matchingSkills').querySelector('.skills-grid').innerHTML = 
        data.matching_keywords.map(keyword => `<div class="skill-tile">${keyword}</div>`).join('');

        document.getElementById('missingSkills').querySelector('.skills-grid').innerHTML = 
        data.missing_keywords.map(keyword => `<div class="skill-tile">${keyword}</div>`).join('');

        document.getElementById('improvementSuggestions').querySelector('p').innerText = data.suggestions;
    })
    .catch(error => {

        // Hide the loading indicator when the response is received
        loadingIndicator.style.display = 'none';

        console.error('Error:', error);
        alert("There was an error processing the request.");
    });
});