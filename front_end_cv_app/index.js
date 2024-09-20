
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

    // Send an AJAX request to the Flask backend
    fetch('/compare_cv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display results from the backend
        document.getElementById('matchScore').querySelector('p').innerText = data.match_score + '%';
        document.getElementById('missingKeywords').querySelector('ul').innerHTML = data.missing_keywords.map(keyword => `<li>${keyword}</li>`).join('');
        document.getElementById('improvementSuggestions').querySelector('p').innerText = data.suggestions;
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error processing the request.");
    });
});