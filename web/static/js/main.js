// ============================================
// ASPECT-PULSE - MAIN JAVASCRIPT
// ============================================

const API_ENDPOINT = '/analyze';
const textInput = document.getElementById('textInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const charCount = document.getElementById('charCount');

let sentimentChart = null;
let aspectChart = null;

// Character counter
if (textInput) {
    textInput.addEventListener('input', function() {
        charCount.textContent = this.value.length;
        analyzeBtn.disabled = this.value.trim().length === 0;
    });
}

// Analyze button
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeText);
}

async function analyzeText() {
    const text = textInput.value.trim();

    if (!text) {
        showError('Please enter some text to analyze.');
        return;
    }

    if (text.length > 5000) {
        showError('Text is too long. Maximum 5000 characters allowed.');
        return;
    }

    // Show loading, hide results
    loadingSpinner.style.display = 'flex';
    resultsSection.style.display = 'none';
    hideError();

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Analysis failed. Please try again.');
            loadingSpinner.style.display = 'none';
            return;
        }

        // Display results
        displayResults(data);
        loadingSpinner.style.display = 'none';
        resultsSection.style.display = 'block';

    } catch (error) {
        showError('Network error. Please check your connection and try again.');
        loadingSpinner.style.display = 'none';
        console.error('Error:', error);
    }
}

function displayResults(data) {
    const results = data.results;
    const summary = data.summary;

    // Display summary cards
    displaySummaryCards(summary);

    // Display charts
    displayCharts(results, summary);

    // Display detailed table
    displayResultsTable(results);
}

function displaySummaryCards(summary) {
    const container = document.getElementById('summaryCards');
    container.innerHTML = '';

    const overallSentiment = summary.overall_sentiment;
    const total = summary.total_sentences;

    const positivePercent = total > 0 ? Math.round((overallSentiment.positive / total) * 100) : 0;
    const negativePercent = total > 0 ? Math.round((overallSentiment.negative / total) * 100) : 0;
    const neutralPercent = total > 0 ? Math.round((overallSentiment.neutral / total) * 100) : 0;

    const cards = [
        { label: 'Positive', value: overallSentiment.positive, percent: positivePercent, class: 'positive' },
        { label: 'Negative', value: overallSentiment.negative, percent: negativePercent, class: 'negative' },
        { label: 'Neutral', value: overallSentiment.neutral, percent: neutralPercent, class: 'neutral' }
    ];

    cards.forEach(card => {
        const element = document.createElement('div');
        element.className = `summary-card ${card.class}`;
        element.innerHTML = `
            <div class="summary-value">${card.percent}%</div>
            <div class="summary-label">${card.label} (${card.value})</div>
        `;
        container.appendChild(element);
    });
}

function displayCharts(results, summary) {
    // Overall Sentiment Chart
    const sentimentCtx = document.getElementById('sentimentChart');
    if (sentimentCtx) {
        if (sentimentChart) {
            sentimentChart.destroy();
        }

        const overallSentiment = summary.overall_sentiment;
        sentimentChart = new Chart(sentimentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [
                        overallSentiment.positive,
                        overallSentiment.negative,
                        overallSentiment.neutral
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

    // Aspect Chart
    const aspectCtx = document.getElementById('aspectChart');
    if (aspectCtx && summary.by_aspect) {
        if (aspectChart) {
            aspectChart.destroy();
        }

        const aspects = Object.keys(summary.by_aspect);
        const positiveData = aspects.map(a => summary.by_aspect[a].positive);
        const negativeData = aspects.map(a => summary.by_aspect[a].negative);
        const neutralData = aspects.map(a => summary.by_aspect[a].neutral);

        aspectChart = new Chart(aspectCtx, {
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
                indexAxis: 'y',
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

function displayResultsTable(results) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';

    results.forEach(result => {
        const sentiment = result.polarity.label.toLowerCase();
        const score = (result.polarity.score * 100).toFixed(1);

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${escapeHtml(result.sentence.substring(0, 50))}${result.sentence.length > 50 ? '...' : ''}</td>
            <td><strong>${result.aspect}</strong></td>
            <td>
                <span class="sentiment-badge ${sentiment}">
                    ${sentiment}
                </span>
            </td>
            <td>${score}%</td>
        `;
        tbody.appendChild(row);
    });
}

function clearResults() {
    resultsSection.style.display = 'none';
    textInput.value = '';
    charCount.textContent = '0';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
