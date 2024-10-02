from Scripts.load_data import load_data
from Scripts.preprocess import preprocess_texts
from Scripts.training import train_and_save_model
import joblib
import os

base_path = 'trainingdata'
model_path = 'models/genre_model.pkl'
vectorizer_path = 'models/vectorizer.pkl'
mlb_path = 'models/mlb.pkl'
evaluation_path = 'evaluation.txt'

# daten laden
texts, labels = load_data(base_path)

# prüfen ob daten geladen wurden
if not texts or not labels:
    print("Keine Daten gefunden.")
else:
    # daten vorverarbeiten
    X, vectorizer = preprocess_texts(texts)

    # modell trainieren, evaluieren, speichern
    model, report, mlb = train_and_save_model(X, labels, model_path, vectorizer_path, vectorizer, mlb_path, evaluation_path)

    print(f"Modell gespeichert bei {model_path}")
    print(f"Vectorizer gespeichert bei {vectorizer_path}")
    print(f"MultiLabelBinarizer gespeichert bei {mlb_path}")
    print(f"Evaluation:\n{report}")
