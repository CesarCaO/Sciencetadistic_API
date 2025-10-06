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
    
    createBoxplot(data);
    
    document.getElementById('metrics-results').classList.add('active');
}

function createBoxplot(data) {
    console.log('Creating chart with data:', data);
    
    const acceptedData = data.Accepted || data.accepted || [];
    const rejectedData = data.Rejected || data.rejected || [];
    
    if (!acceptedData || !rejectedData || acceptedData.length === 0 || rejectedData.length === 0) {
        console.error('Missing accepted or rejected papers data');
        alert('Error: No accepted or rejected papers data found in response');
        return;
    }
    
    const ctx = document.getElementById('boxplot');
    
    // Destroy previous chart if exists
    if (myChart) {
        myChart.destroy();
        myChart = null;
    }

    myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Accepted Papers',
                    data: acceptedData.map(v => ({x: 0, y: v})),
                    backgroundColor: 'rgba(17, 153, 142, 0.6)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointStyle: 'circle'
                },
                {
                    label: 'Rejected Papers',
                    data: rejectedData.map(v => ({x: 1, y: v})),
                    backgroundColor: 'rgba(235, 51, 73, 0.6)',
                    borderColor: 'rgba(235, 51, 73, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointStyle: 'circle'
                },
                {
                    label: 'Your Document',
                    data: [{x: 0.5, y: data.current_document}],
                    backgroundColor: '#0077b6',
                    borderColor: '#023e8a',
                    borderWidth: 2,
                    pointRadius: 10,
                    pointHoverRadius: 12,
                    pointStyle: 'star'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                x: {
                    type: 'linear',
                    min: -0.5,
                    max: 1.5,
                    ticks: {
                        stepSize: 0.5,
                        callback: function(value) {
                            if (value === 0) return 'Accepted';
                            if (value === 0.5) return 'Your Doc';
                            if (value === 1) return 'Rejected';
                            return '';
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Metric value',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    enabled: true,
                    mode: 'nearest',
                    intersect: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 10,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(3);
                        }
                    }
                }
            }
        }
    });
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
        const response = await fetch('/model/', {
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