from transformers import pipeline

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

def get_sentiment_pipeline():
    """
    Initializes and returns a Hugging Face sentiment analysis pipeline.
    The model is downloaded and cached on the first run.
    
    Returns:
        transformers.Pipeline: An initialized sentiment analysis pipeline.
    """
    try:
        print(f"Loading sentiment analysis model: '{MODEL_NAME}'...")
        sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME)
        print("Model loaded successfully.")
        return sentiment_pipeline
    except Exception as e:
        print(f"Error loading sentiment model: {e}")
        return None

def get_sentiment(sentence, sentiment_pipeline):
    """
    Analyzes a sentence and returns its sentiment polarity score.
    
    Args:
        sentence (str): The sentence to analyze.
        sentiment_pipeline (transformers.Pipeline): The sentiment analysis pipeline.
        
    Returns:
        float: A polarity score between -1.0 (very negative) and 1.0 (very positive).
               Returns 0.0 if the pipeline is not available.
    """
    if not sentiment_pipeline:
        print("Sentiment pipeline is not available.")
        return 0.0
        
    try:
        result = sentiment_pipeline(sentence)[0]
        score = result['score']
        label = result['label']
        
        # Convert the result to a single polarity score from -1 to 1
        if label == 'NEGATIVE':
            return -score
        else: # POSITIVE
            return score
            
    except Exception as e:
        print(f"Error analyzing sentiment for sentence '{sentence}': {e}")
        return 0.0

if __name__ == '__main__':
    # Initialize the pipeline
    sentiment_analyzer = get_sentiment_pipeline()
    
    if sentiment_analyzer:
        test_sentences = [
            "The battery life is incredible, lasting me two full days.", # Positive
            "I'm really disappointed with the camera quality in low light.", # Negative
            "The screen is bright and vibrant.", # Positive
            "This phone is okay, I guess.", # Neutral-ish, but model will lean one way
            "What a terrible waste of money." # Very Negative
        ]
        
        print("\n--- Sentiment Analysis Examples ---")
        for sentence in test_sentences:
            polarity = get_sentiment(sentence, sentiment_analyzer)
            print(f"Sentence: '{sentence}'")
            print(f"-> Polarity: {polarity:.4f}\n")
