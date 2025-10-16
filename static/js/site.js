let myChart = null;

// Navigation between pages
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = e.target.dataset.page;
        
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        
        e.target.classList.add('active');
        document.getElementById(`${page}-page`).classList.add('active');
    });
});

// Show selected file name
document.getElementById('metrics-file').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    document.getElementById('metrics-filename').textContent = fileName ? `✓ ${fileName}` : '';
});

document.getElementById('prediction-file').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    document.getElementById('prediction-filename').textContent = fileName ? `✓ ${fileName}` : '';
});

// Metrics form submission
document.getElementById('metrics-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('metric', document.getElementById('metric-select').value);
    formData.append('file', document.getElementById('metrics-file').files[0]);

    document.getElementById('metrics-loading').classList.add('active');
    document.getElementById('metrics-results').classList.remove('active');
    document.getElementById('analyze-btn').disabled = true;

    try {
        const response = await fetch('/metrics', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }

        const data = await response.json();
        console.log('Data received:', data);
        displayMetricResults(data);
    } catch (error) {
        console.error('Complete error:', error);
        alert('Error analyzing document: ' + error.message);
    } finally {
        document.getElementById('metrics-loading').classList.remove('active');
        document.getElementById('analyze-btn').disabled = false;
    }
});

function displayMetricResults(data) {
    console.log('Displaying results:', data);
    
    if (!data || data.current_document === undefined) {
        alert('Error: The server response does not contain the expected data');
        console.error('Data received:', data);
        return;
    }
    
    const metricNameEl = document.getElementById('metric-name');
    const metricValueEl = document.getElementById('metric-value');
    
    if (!metricNameEl || !metricValueEl) {
        console.error('Error: DOM elements not found');
        alert('Internal error: DOM elements not found');
        return;
    }
    
    metricNameEl.textContent = data.metric || 'Metric';
    metricValueEl.textContent = parseFloat(data.current_document).toFixed(3);

    document.getElementById('metrics-results').classList.add('active');
}



// Prediction form submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', document.getElementById('prediction-file').files[0]);

    document.getElementById('prediction-loading').classList.add('active');
    document.getElementById('prediction-results').innerHTML = '';
    document.getElementById('prediction-results').classList.remove('active');
    document.getElementById('predict-btn').disabled = true;

    try {
        const response = await fetch('/prediction', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Request error');

        const data = await response.json();
        displayPredictionResult(data);
    } catch (error) {
        alert('Error analyzing document: ' + error.message);
    } finally {
        document.getElementById('prediction-loading').classList.remove('active');
        document.getElementById('predict-btn').disabled = false;
    }
});

function displayPredictionResult(data) {
    const isAccepted = data.prediction === 1;
    const resultClass = isAccepted ? 'accepted' : 'rejected';
    const resultText = isAccepted ? 'ACCEPTED' : 'REJECTED';
    const resultEmoji = isAccepted ? '✅' : '❌';
    const resultMessage = isAccepted 
        ? 'Your article has a high probability of being accepted'
        : 'Your article needs improvements before submission';

    document.getElementById('prediction-results').innerHTML = `
        <div class="prediction-result ${resultClass}">
            <h2>${resultEmoji} ${resultText}</h2>
            <p>${resultMessage}</p>
        </div>
    `;
    
    document.getElementById('prediction-results').classList.add('active');
}