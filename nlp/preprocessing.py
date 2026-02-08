import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
import spacy

# --- Download necessary NLTK data ---
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK WordNet...")
    nltk.download('wordnet')
# ------------------------------------

# --- Load SpaCy model ---
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading SpaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')
# --------------------------

def preprocess_text(text):
    """
    Cleans and preprocesses a single text string.
    
    Args:
        text (str): The input text to process.
        
    Returns:
        list of str: A list of lemmatized, non-stopword tokens.
    """
    if not isinstance(text, str):
        return []

    # 1. Lowercasing
    text = text.lower()
    
    # 2. Tokenization
    tokens = word_tokenize(text)
    
    # 3. Stop-word and punctuation removal
    stop_words = set(stopwords.words('english'))
    punct = set(string.punctuation)
    filtered_tokens = [word for word in tokens if word not in stop_words and word not in punct]
    
    # 4. Lemmatization (using NLTK)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    return lemmatized_tokens

def get_sentences(text):
    """
    Splits a block of text into individual sentences.
    
    Args:
        text (str): The input text.
        
    Returns:
        list of str: A list of sentences.
    """
    if not isinstance(text, str):
        return []
    return sent_tokenize(text)

if __name__ == '__main__':
    sample_review = """
    The battery life on this phone is amazing, it lasts for two days straight! 
    However, the camera is a bit of a letdown. Photos are grainy in low light. 
    Performance is top-notch, very snappy. But the display could be brighter.
    """
    
    print("--- Original Review ---")
    print(sample_review)
    
    # --- Sentence Splitting ---
    sentences = get_sentences(sample_review)
    print("\n--- Sentences ---")
    for i, sentence in enumerate(sentences):
        print(f"{i+1}: {sentence}")
        
    # --- Text Preprocessing (on the first sentence) ---
    first_sentence = sentences[0]
    processed_tokens = preprocess_text(first_sentence)
    print("\n--- Preprocessed First Sentence ---")
    print(f"Original: {first_sentence}")
    print(f"Tokens: {processed_tokens}")
    
    # --- Using SpaCy for more advanced processing (e.g., dependency parsing) ---
    print("\n--- SpaCy Dependency Parse (Second Sentence) ---")
    doc = nlp(sentences[1]) # "However, the camera is a bit of a letdown."
    for token in doc:
        print(f"{token.text:<12} {token.pos_:<8} {token.dep_:<10} {token.head.text}")
