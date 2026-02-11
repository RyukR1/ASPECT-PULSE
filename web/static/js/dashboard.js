// ============================================
// ASPECT-PULSE - DASHBOARD JAVASCRIPT
// ============================================

let overallChart = null;
let performanceChart = null;

// Load dashboard data
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
});

function loadDashboardData() {
    // This would normally load from a backend API
    // For now, we'll initialize with sample data structures
    
    // Get data from localStorage if available
    const savedData = localStorage.getItem('aspectPulseData');
    
    if (savedData) {
        const data = JSON.parse(savedData);
        updateDashboard(data);
    } else {
        initializeDashboard();
    }
}

function initializeDashboard() {
    // Initialize empty dashboard
    updateMetrics({
        totalAnalyses: 0,
        totalSentences: 0,
        positivePercent: 0,
        negativePercent: 0
    });
    
    initializeCharts({});
}

function updateDashboard(data) {
    // Update metrics
    const totalSentences = data.total_sentences || 0;
    const overall = data.overall_sentiment || {};
    
    const positivePercent = totalSentences > 0 
        ? Math.round((overall.positive || 0) / totalSentences * 100) 
        : 0;
    const negativePercent = totalSentences > 0 
        ? Math.round((overall.negative || 0) / totalSentences * 100) 
        : 0;
    
    updateMetrics({
        totalAnalyses: data.totalAnalyses || 0,
        totalSentences: totalSentences,
        positivePercent: positivePercent,
        negativePercent: negativePercent
    });
    
    // Update aspects list
    if (data.by_aspect) {
        updateAspectsList(data.by_aspect);
    }
    
    // Update charts
    initializeCharts(data);
}

function updateMetrics(metrics) {
    const elements = {
        'Total Analyses': metrics.totalAnalyses,
        'Sentences Analyzed': metrics.totalSentences,
        'Positive Sentiment': metrics.positivePercent + '%',
        'Negative Sentiment': metrics.negativePercent + '%'
    };
    
    const metricDivs = document.querySelectorAll('.metric');
    let index = 0;
    
    for (let [label, value] of Object.entries(elements)) {
        if (index < metricDivs.length) {
            metricDivs[index].querySelector('.metric-value').textContent = value;
            index++;
        }
    }
}

function updateAspectsList(byAspect) {
    const container = document.getElementById('topAspectsList');
    
    if (Object.keys(byAspect).length === 0) {
        container.innerHTML = '<p class="no-data">No data available yet</p>';
        return;
    }
    
    container.innerHTML = '';
    
    // Sort aspects by total mentions
    const sortedAspects = Object.entries(byAspect)
        .sort((a, b) => b[1].total - a[1].total)
        .slice(0, 5);
    
    sortedAspects.forEach(([aspect, data]) => {
        const element = document.createElement('div');
        element.className = 'aspect-badge';
        element.innerHTML = `
            <span class="aspect-badge-title">${aspect}</span>
            <span class="aspect-badge-count">${data.total} mentions</span>
        `;
        container.appendChild(element);
    });
}

function initializeCharts(data) {
    const overall = data.overall_sentiment || { positive: 0, negative: 0, neutral: 0 };
    const byAspect = data.by_aspect || {};
    
    // Overall Sentiment Chart
    const overallCtx = document.getElementById('overallSentimentChart');
    if (overallCtx) {
        if (overallChart) {
            overallChart.destroy();
        }
        
        overallChart = new Chart(overallCtx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [
                        overall.positive || 0,
                        overall.negative || 0,
                        overall.neutral || 0
                    ],
                    backgroundColor: [
                        '#10b981',
                        '#ef4444',
                        '#f59e0b'
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Aspect Performance Chart
    const performanceCtx = document.getElementById('aspectPerformanceChart');
    if (performanceCtx && Object.keys(byAspect).length > 0) {
        if (performanceChart) {
            performanceChart.destroy();
        }
        
        const aspects = Object.keys(byAspect);
        const positiveData = aspects.map(a => byAspect[a].positive);
        const negativeData = aspects.map(a => byAspect[a].negative);
        const neutralData = aspects.map(a => byAspect[a].neutral);
        
        performanceChart = new Chart(performanceCtx, {
            type: 'bar',
            data: {
                labels: aspects,
                datasets: [
                    {
                        label: 'Positive',
                        data: positiveData,
                        backgroundColor: '#10b981'
                    },
                    {
                        label: 'Negative',
                        data: negativeData,
                        backgroundColor: '#ef4444'
                    },
                    {
                        label: 'Neutral',
                        data: neutralData,
                        backgroundColor: '#f59e0b'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: true
                    },
                    y: {
                        stacked: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Listen for storage changes (when analysis is done on home page)
window.addEventListener('storage', function(e) {
    if (e.key === 'aspectPulseData') {
        loadDashboardData();
    }
});
