from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
import joblib
import os

def train_and_save_model(X, y, model_path, vectorizer_path, vectorizer, mlb_path, evaluation_path):
    # multi-label binarizer für mehrere genres
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(y)

    # train-test-split 80 zu 20
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # modelltraining mit OneVsRestClassifier
    model = OneVsRestClassifier(SVC())
    model.fit(X_train, y_train)

    # vorhersage auf testdaten
    y_pred = model.predict(X_test)

    # ergebnisse ausgeben
    report = classification_report(y_test, y_pred, target_names=mlb.classes_, output_dict=True)

    # evaluierung formatieren
    formatted_report = format_classification_report(report)

    # evaluierung in datei schreiben
    with open(evaluation_path, 'w') as f:
        f.write(formatted_report)

    # modell speichern
    joblib.dump(model, model_path)

    # vektorisierer speichern
    joblib.dump(vectorizer, vectorizer_path)

    # multilabelbinarizer speichern
    joblib.dump(mlb, mlb_path)
    
    return model, formatted_report, mlb

def format_classification_report(report):
    lines = []
    for label, metrics in report.items():
        if isinstance(metrics, dict):
            lines.append(f"Label: {label}")
            for metric, value in metrics.items():
                lines.append(f"  {metric}: {value:.2f}")
            lines.append("")
        else:
            lines.append(f"{label}: {metrics:.2f}")
    return "\n".join(lines)
