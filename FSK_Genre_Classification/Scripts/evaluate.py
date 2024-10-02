from sklearn.metrics import classification_report
import joblib

def evaluate_model(model_path, vectorizer_path, mlb_path, X_test, y_test):
    # modell, vektorisierer, multiLabelbinarizer laden
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    mlb = joblib.load(mlb_path)
    
    # testdaten vektorisieren
    X_test_vectorized = vectorizer.transform(X_test)
    
    # vorhersage
    y_pred = model.predict(X_test_vectorized)
    
    # auswertung
    print(classification_report(y_test, y_pred, target_names=mlb.classes_))
