// Change between pages
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


// Metrics form
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

        if (!response.ok) throw new Error('Error en la solicitud');

        const data = await response.json();
        displayMetricResults(data);
    } catch (error) {
        alert('Error al analizar el documento: ' + error.message);
    } finally {
        document.getElementById('metrics-loading').classList.remove('active');
        document.getElementById('analyze-btn').disabled = false;
    }
});

//Function for display the analysis file result
function displayMetricResults(data) {
    document.getElementById('metric-name').textContent = data.metric_name;
    document.getElementById('metric-value').textContent = data.user_result.toFixed(3);
    
    createBoxplot(data);
    
    document.getElementById('metrics-results').classList.add('active');
}

//Create boxplot
function createBoxplot(data) {
    const ctx = document.getElementById('boxplot');
    
    if (window.myChart) {
        window.myChart.destroy();
    }

    const allData = [
        ...data.accepted_papers.map(v => ({x: 'Accepted', y: v})),
        ...data.rejected_papers.map(v => ({x: 'Rejected', y: v})),
        {x: 'Tu documento', y: data.user_result}
    ];

    window.myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Accepted papers',
                    data: data.Accepted.map(v => ({x: 0, y: v})),
                    backgroundColor: 'rgba(17, 153, 142, 0.5)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    pointRadius: 6
                },
                {
                    label: 'Rejected papers',
                    data: data.Rejected.map(v => ({x: 1, y: v})),
                    backgroundColor: 'rgba(235, 51, 73, 0.5)',
                    borderColor: 'rgba(235, 51, 73, 1)',
                    pointRadius: 6
                },
                {
                    label: 'Your document',
                    data: [{x: 0.5, y: data.user_result}],
                    backgroundColor: '#0077b6',
                    borderColor: '#0077b6',
                    pointRadius: 12,
                    pointStyle: 'star'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    min: -0.5,
                    max: 1.5,
                    ticks: {
                        callback: function(value) {
                            if (value === 0) return 'Accepted';
                            if (value === 1) return 'Rejected';
                            if (value === 0.5) return 'Your doc';
                            return '';
                        }
                    }
                },
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Metric Value'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Value: ${context.parsed.y.toFixed(3)}`;
                        }
                    }
                }
            }
        }
    });
}
