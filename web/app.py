"""
Flask web application for Aspect-Pulse
Aspect-Based Sentiment Analysis & Competitive Benchmarking Hub
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import json
from datetime import datetime

# --- Add project root to sys.path ---
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
# ------------------------------------

# --- Import from our project modules ---
from nlp.preprocessing import get_sentences
from nlp.aspect_extractor import extract_aspect, ASPECT_KEYWORDS
from sentiment.sentiment_model import get_sentiment_pipeline, get_sentiment
# ---------------------------------------

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Cache for sentiment model
sentiment_pipeline = None

def load_model():
    """Load sentiment model"""
    global sentiment_pipeline
    if sentiment_pipeline is None:
        sentiment_pipeline = get_sentiment_pipeline()
    return sentiment_pipeline

def run_analysis(raw_text):
    """
    Runs the full NLP pipeline on a block of raw text.
    Returns a list of analysis results with aspect and sentiment information.
    """
    try:
        sentences = get_sentences(raw_text)
        results = []
        
        model = load_model()
        if not model:
            return {"error": "Failed to load sentiment model"}

        for sentence in sentences:
            if len(sentence.strip()) < 3:
                continue
                
            aspect = extract_aspect(sentence)
            if aspect != 'Unclassified':
                polarity = get_sentiment(sentence, model)
                results.append({
                    'sentence': sentence,
                    'aspect': aspect,
                    'polarity': polarity,
                    'score': polarity.get('score', 0)
                })

        return results
    except Exception as e:
        return {"error": str(e)}

def aggregate_results(results):
    """
    Aggregate results by aspect for visualization.
    """
    if isinstance(results, dict) and 'error' in results:
        return results
    
    aggregated = {}
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for result in results:
        aspect = result['aspect']
        sentiment = result['polarity'].get('label', 'neutral').lower()
        
        if aspect not in aggregated:
            aggregated[aspect] = {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0}
        
        aggregated[aspect][sentiment] += 1
        aggregated[aspect]['total'] += 1
        sentiment_counts[sentiment] += 1
    
    return {
        'by_aspect': aggregated,
        'overall_sentiment': sentiment_counts,
        'total_sentences': len(results)
    }

# --- Routes ---

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for text analysis"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Please provide text to analyze'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text is too long (max 5000 characters)'}), 400
        
        results = run_analysis(text)
        
        if isinstance(results, dict) and 'error' in results:
            return jsonify(results), 400
        
        aggregated = aggregate_results(results)
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': aggregated,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/aspects')
def get_aspects():
    """API endpoint to get available aspects"""
    return jsonify({
        'aspects': list(ASPECT_KEYWORDS.keys()),
        'description': 'List of product aspects that can be analyzed'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
