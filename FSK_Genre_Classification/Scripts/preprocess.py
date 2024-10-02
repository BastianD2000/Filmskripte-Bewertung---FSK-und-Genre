import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# notwendige nltk-resourcen herunterladen
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_texts(texts, use_stemming=True, use_lemmatization=False):
    """
    vorverarbeitung:
    -tokenisierung
    -Stoppwörter entfernen
    -stemming oder lemmatization
    -vektorisierung mit TF-IDF
    """
    
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    def preprocess(text):
        # tokenisierung
        tokens = word_tokenize(text)
        
        # entfernen von stoppwörtern
        tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # stemming oder lemmatization
        if use_stemming:
            tokens = [stemmer.stem(word) for word in tokens]
        elif use_lemmatization:
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        return ' '.join(tokens)
    
    # texte vorverarbeiten
    preprocessed_texts = [preprocess(text) for text in texts]
    
    # TF-IDF vektorisierung
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(preprocessed_texts)
    
    return X, vectorizer
