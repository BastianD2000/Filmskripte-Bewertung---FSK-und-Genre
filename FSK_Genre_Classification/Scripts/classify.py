import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# notwendige nltk-resourcen downloaden
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess(text, use_stemming=True, use_lemmatization=False):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    # tokenisierung
    tokens = word_tokenize(text)
    
    # stoppwörter entfernen
    tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # stemming oder lemmatization
    if use_stemming:
        tokens = [stemmer.stem(word) for word in tokens]
    elif use_lemmatization:
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return ' '.join(tokens)

def classify_text(model_path, vectorizer_path, mlb_path, text):
    # modell, vektorisierer, multiLabelbinarizer laden
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    mlb = joblib.load(mlb_path)
    
    # text vorverarbeiten
    preprocessed_text = preprocess(text)
    
    # text vektorisieren
    text_vectorized = vectorizer.transform([preprocessed_text])
    
    # vorhersage
    predicted_labels_binary = model.predict(text_vectorized)
    
    # vorhersagen in label-namen umwandeln
    predicted_labels = mlb.inverse_transform(predicted_labels_binary)
    
    # inverse_transform gibt liste, daraus erstes element wählen
    return predicted_labels[0]
