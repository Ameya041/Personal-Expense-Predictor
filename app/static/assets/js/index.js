/**
 * INDEX PAGE JS
 * Specific functionality for the main prediction page
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Index page scripts loaded');
    
    // Initialize charts if they exist
    initExpenseCharts();
    
    // Setup prediction form
    setupPredictionForm();
});

// Initialize Chart.js charts
function initExpenseCharts() {
    const chartElements = document.querySelectorAll('.expense-chart');
    
    chartElements.forEach(chartEl => {
        const ctx = chartEl.getContext('2d');
        const chartType = chartEl.dataset.chartType || 'doughnut';
        const chartData = JSON.parse(chartEl.dataset.chartData || '{}');
        
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: Object.keys(chartData),
                datasets: [{
                    data: Object.values(chartData),
                    backgroundColor: [
                        '#4361ee', '#3f37c9', '#4cc9f0',
                        '#4895ef', '#560bad', '#f72585'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ₹${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    });
}

// Prediction form handling
function setupPredictionForm() {
    const form = document.getElementById('prediction-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        // Client-side validation
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showAlert('danger', 'Please fill all required fields.');
        }
    });
}
