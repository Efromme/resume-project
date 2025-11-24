// Your API endpoint
const API_URL = 'https://dha8uvgm1f.execute-api.us-east-1.amazonaws.com/prod/costs';

// Fetch cost data when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Loading cost data...');
    fetchCostData();
});

async function fetchCostData() {
    try {
        // Call your API
        const response = await fetch(API_URL);
        
        // Check if successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Parse JSON
        const data = await response.json();
        console.log('📊 Data received:', data);
        
        // Update the stat cards
        document.getElementById('total-cost').textContent = `$${data.total.toFixed(4)}`;
        document.getElementById('avg-cost').textContent = `$${data.average.toFixed(4)}`;
        document.getElementById('days-tracked').textContent = data.count;
        document.getElementById('last-update').textContent = new Date().toLocaleString();
        
        // Create the chart
        createChart(data.dates, data.costs);
        
    } catch (error) {
        console.error('❌ Error fetching cost data:', error);
        document.getElementById('total-cost').textContent = 'Error';
        document.getElementById('avg-cost').textContent = 'Error';
        document.getElementById('days-tracked').textContent = 'Error';
    }
}

function createChart(dates, costs) {
    const ctx = document.getElementById('costChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Daily AWS Cost (USD)',
                data: costs,
                borderColor: '#bd5d38', // Matches your theme color
                backgroundColor: 'rgba(189, 93, 56, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Cost: $${context.parsed.y.toFixed(6)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(6);
                        }
                    }
                }
            }
        }
    });
}