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
    
    // Calculate statistics instead of plotting all points
    function calculateStats(arr) {
        const sorted = arr.slice().sort((a, b) => a - b);
        const min = sorted[0];
        const max = sorted[sorted.length - 1];
        const q1 = sorted[Math.floor(sorted.length * 0.25)];
        const median = sorted[Math.floor(sorted.length * 0.5)];
        const q3 = sorted[Math.floor(sorted.length * 0.75)];
        const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
        return { min, q1, median, q3, max, mean };
    }
    
    const acceptedStats = calculateStats(acceptedData);
    const rejectedStats = calculateStats(rejectedData);
    
    console.log('Accepted stats:', acceptedStats);
    console.log('Rejected stats:', rejectedStats);
    
    const ctx = document.getElementById('boxplot');
    
    // Destroy previous chart if exists
    if (myChart) {
        myChart.destroy();
        myChart = null;
    }

    // Create box plot visualization
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Accepted Papers', 'Your Document', 'Rejected Papers'],
            datasets: [
                {
                    label: 'Min',
                    data: [acceptedStats.min, null, rejectedStats.min],
                    backgroundColor: 'transparent',
                    borderColor: 'transparent',
                    borderWidth: 0
                },
                {
                    label: 'Q1-Min',
                    data: [
                        acceptedStats.q1 - acceptedStats.min,
                        null,
                        rejectedStats.q1 - rejectedStats.min
                    ],
                    backgroundColor: 'rgba(17, 153, 142, 0.3)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Q3-Q1 (IQR)',
                    data: [
                        acceptedStats.q3 - acceptedStats.q1,
                        null,
                        rejectedStats.q3 - rejectedStats.q1
                    ],
                    backgroundColor: 'rgba(17, 153, 142, 0.6)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Max-Q3',
                    data: [
                        acceptedStats.max - acceptedStats.q3,
                        null,
                        rejectedStats.max - rejectedStats.q3
                    ],
                    backgroundColor: 'rgba(17, 153, 142, 0.3)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Your Document',
                    data: [null, data.current_document, null],
                    backgroundColor: '#0077b6',
                    borderColor: '#023e8a',
                    borderWidth: 3,
                    type: 'scatter',
                    pointStyle: 'star',
                    pointRadius: 15,
                    pointHoverRadius: 17
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                x: {
                    stacked: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    stacked: true,
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
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        title: function(context) {
                            return context[0].label;
                        },
                        afterTitle: function(context) {
                            const label = context[0].label;
                            if (label === 'Accepted Papers') {
                                return `\nStatistics (n=${acceptedData.length}):\nMin: ${acceptedStats.min.toFixed(3)}\nQ1: ${acceptedStats.q1.toFixed(3)}\nMedian: ${acceptedStats.median.toFixed(3)}\nMean: ${acceptedStats.mean.toFixed(3)}\nQ3: ${acceptedStats.q3.toFixed(3)}\nMax: ${acceptedStats.max.toFixed(3)}`;
                            } else if (label === 'Rejected Papers') {
                                return `\nStatistics (n=${rejectedData.length}):\nMin: ${rejectedStats.min.toFixed(3)}\nQ1: ${rejectedStats.q1.toFixed(3)}\nMedian: ${rejectedStats.median.toFixed(3)}\nMean: ${rejectedStats.mean.toFixed(3)}\nQ3: ${rejectedStats.q3.toFixed(3)}\nMax: ${rejectedStats.max.toFixed(3)}`;
                            } else if (label === 'Your Document') {
                                return `\nValue: ${data.current_document.toFixed(3)}`;
                            }
                        },
                        label: function() {
                            return null; // Hide individual dataset labels
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