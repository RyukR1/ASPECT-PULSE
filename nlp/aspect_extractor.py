import spacy
from .preprocessing import nlp # Import the loaded SpaCy model

# --- Define Aspect Keywords ---
# This dictionary maps aspects to a list of related keywords.
ASPECT_KEYWORDS = {
    'Battery': ['battery', 'charging', 'power', 'mah', 'charger', 'lasts', 'charge'],
    'Camera': ['camera', 'photo', 'picture', 'video', 'lens', 'zoom', 'selfie', 'portraits'],
    'Display': ['display', 'screen', 'oled', 'amoled', 'refresh rate', 'brightness', 'pixels'],
    'Performance': ['performance', 'speed', 'fast', 'slow', 'lag', 'smooth', 'processor', 'ram', 'gaming'],
    'Value': ['price', 'value', 'cheap', 'expensive', 'cost', 'worth', 'budget']
}
# -----------------------------

def extract_aspect(sentence):
    """
    Extracts the primary aspect from a sentence using a rule-based approach.
    
    Args:
        sentence (str): The input sentence to analyze.
        
    Returns:
        str: The identified aspect, or 'Unclassified' if no aspect is found.
    """
    sentence_lower = sentence.lower()
    doc = nlp(sentence_lower)
    
    found_aspects = set()
    
    # 1. Direct Keyword Matching
    for aspect, keywords in ASPECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in sentence_lower:
                found_aspects.add(aspect)

    # 2. Dependency Parsing for Refinement
    # If multiple aspects are found, we try to find the most likely one.
    # We prioritize nouns that are subjects of the sentence.
    if len(found_aspects) > 1:
        for token in doc:
            # Check if the token is a noun subject (nsubj)
            if token.dep_ == 'nsubj':
                for aspect, keywords in ASPECT_KEYWORDS.items():
                    if token.lemma_ in keywords:
                        # If a subject matches a keyword, we consider it the primary aspect
                        return aspect

    # If only one aspect was found, or refinement didn't work, return the first one found.
    if found_aspects:
        return list(found_aspects)[0]
        
    return 'Unclassified'

if __name__ == '__main__':
    test_sentences = [
        "The battery life is incredible, lasting me two full days.",
        "I'm really disappointed with the camera quality in low light.",
        "The screen is bright and vibrant, perfect for watching movies.",
        "Gaming performance is super smooth with no lag at all.",
        "For the price, this phone is an absolute steal.",
        "The phone feels fast, but the battery could be better.", # Should be 'Performance' or 'Battery'
        "This is a great device overall." # Should be 'Unclassified'
    ]
    
    print("--- Aspect Extraction Examples ---")
    for sentence in test_sentences:
        aspect = extract_aspect(sentence)
        print(f"Sentence: '{sentence}'")
        print(f"-> Aspect: {aspect}\n")
