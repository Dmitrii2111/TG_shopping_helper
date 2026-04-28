from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)

# Initialize Natasha components (loaded into memory once)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)

def extract_products(text: str) -> list[str]:
    """
    Extracts nouns from text and lemmatizes them.
    Example: "Купить молоко, свежий хлеб и бананы" -> ["молоко", "хлеб", "банан"]
    """
    doc = Doc(text)
    
    # Run NLP pipeline
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    
    products = []
    
    for token in doc.tokens:
        # We are only interested in Nouns (Существительные)
        if token.pos == 'NOUN':
            # Convert to dictionary form (lemmatization)
            token.lemmatize(morph_vocab)
            # Capitalize the first letter for neatness
            products.append(token.lemma.capitalize())
            
    # Fallback: if the user sends something Natasha doesn't recognize as a noun 
    # (e.g., a completely unknown slang word), we just return the original text.
    if not products:
        return [text.capitalize()]
        
    return products