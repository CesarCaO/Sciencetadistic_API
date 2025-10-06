 // Cambiar entre páginas
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

// Mostrar nombre de archivo seleccionado
document.getElementById('metrics-file').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    document.getElementById('metrics-filename').textContent = fileName ? `✓ ${fileName}` : '';
});

document.getElementById('prediction-file').addEventListener('change', (e) => {
    const fileName = e.target.files[0]?.name || '';
    document.getElementById('prediction-filename').textContent = fileName ? `✓ ${fileName}` : '';
});

// Formulario de métricas
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
        console.log('Datos recibidos:', data); // Para debugging
        displayMetricResults(data);
    } catch (error) {
        console.error('Error completo:', error);
        alert('Error al analizar el documento: ' + error.message);
    } finally {
        document.getElementById('metrics-loading').classList.remove('active');
        document.getElementById('analyze-btn').disabled = false;
    }
});

function displayMetricResults(data) {
    
    //console.log('Estructura completa de datos:', data);
    //console.log('Claves disponibles:', Object.keys(data));
    
    if (!data || data.current_document === undefined) {
        alert('Error: The server response does not contain de expected data\nKeys received: ' + Object.keys(data).join(', '));
        console.error('Data received:', data);
        return;
    }
    
    document.getElementById('metric-name').textContent = data.metric;
    document.getElementById('metric-value').textContent = parseFloat(data.current_document).toFixed(3);
    
    createBoxplot(data);
    
    document.getElementById('metrics-results').classList.add('active');
}

function createBoxplot(data) {
    //console.log('Creando gráfico con datos:', data);
    //console.log('Accepted:', data.Accepted);
    //console.log('Rejected:', data.Rejected);
    
    // API could sent the response on diferent formats
    const acceptedData = data.Accepted || data.accepted || data.Aceptados || [];
    const rejectedData = data.Rejected || data.rejected || data.Rechazados || [];
    
    
    if (!acceptedData || !rejectedData || acceptedData.length === 0 || rejectedData.length === 0) {
        console.error('Data of accepted and rejected papers is missing');
        console.error('Accepted:', acceptedData);
        console.error('Rejected:', rejectedData);
        alert('Error: Data of accepted and rejected papers was not found');
        return;
    }
    
    const ctx = document.getElementById('boxplot');
    
    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Accepted papers',
                    data: acceptedData.map(v => ({x: 0, y: v})),
                    backgroundColor: 'rgba(17, 153, 142, 0.5)',
                    borderColor: 'rgba(17, 153, 142, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Rejected papers',
                    data: rejectedData.map(v => ({x: 1, y: v})),
                    backgroundColor: 'rgba(235, 51, 73, 0.5)',
                    borderColor: 'rgba(235, 51, 73, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Your document',
                    data: [{x: 0.5, y: data.current_document}],
                    backgroundColor: '#0077b6',
                    borderColor: '#0077b6',
                    pointRadius: 12,
                    pointHoverRadius: 14,
                    pointStyle: 'star'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0,
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
                        text: 'Metric value'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    enabled: true,
                    mode: 'nearest',
                    intersect: true,
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
// Formulario de predicción
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', document.getElementById('prediction-file').files[0]);

    document.getElementById('prediction-loading').classList.add('active');
    document.getElementById('prediction-results').innerHTML = '';
    document.getElementById('predict-btn').disabled = true;

    try {
        const response = await fetch('/model/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Error en la solicitud');

        const data = await response.json();
        displayPredictionResult(data);
    } catch (error) {
        alert('Error al analizar el documento: ' + error.message);
    } finally {
        document.getElementById('prediction-loading').classList.remove('active');
        document.getElementById('predict-btn').disabled = false;
    }
});

function displayPredictionResult(data) {
    const isAccepted = data.prediction === 1;
    const resultClass = isAccepted ? 'accepted' : 'rejected';
    const resultText = isAccepted ? 'ACEPTADO' : 'RECHAZADO';
    const resultEmoji = isAccepted ? '✅' : '❌';
    const resultMessage = isAccepted 
        ? 'Tu artículo tiene alta probabilidad de ser aceptado'
        : 'Tu artículo necesita mejoras antes de ser sometido';

    document.getElementById('prediction-results').innerHTML = `
        <div class="prediction-result ${resultClass}">
            <h2>${resultEmoji} ${resultText}</h2>
            <p>${resultMessage}</p>
        </div>
    `;
    
    document.getElementById('prediction-results').classList.add('active');
}
