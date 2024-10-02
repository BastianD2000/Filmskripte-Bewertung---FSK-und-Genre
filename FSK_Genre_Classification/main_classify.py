import joblib
from Scripts.classify import classify_text, preprocess
from Scripts.fsk import calculate_fsk_for_movie, read_file, read_profanity_csv


def classify_text_from_file(model_path, vectorizer_path, mlb_path, file_path):
    # text lesen
    with open(file_path, 'r', encoding='utf-8') as file:
        new_text = file.read()

    # text vorverarbeiten
    preprocessed_text = preprocess(new_text)

    # klassifizierung
    labels = classify_text(model_path, vectorizer_path, mlb_path, preprocessed_text)
    return labels


# fsk-bewertung bestimmen
def fsk_rating_from_file(file_path, combined_word_list, profanity_dict):
    return calculate_fsk_for_movie(file_path, combined_word_list, profanity_dict)


# pfade zu den modellen und zu untersuchenden txt datei
model_path = 'models/genre_model.pkl'
vectorizer_path = 'models/vectorizer.pkl'
mlb_path = 'models/mlb.pkl'
file_path = 'saving_private_ryan.txt'  # hier angeben, auf welche klassifiziert+fsk bestimmt werden soll

# wortlisten laden
drugs_list = [word.lower() for word in read_file('word_lists/drugs_words.txt').splitlines()]
violence_list = [word.lower() for word in read_file('word_lists/violence_words.txt').splitlines()]
sexual_list = [word.lower() for word in read_file('word_lists/sexual_words.txt').splitlines()]

# csv laden
profanity_dict = read_profanity_csv('word_lists/profanity_words.csv')

# kombinierte wortliste erstellen
combined_word_list = drugs_list + violence_list + sexual_list

# klassifizierung
labels = classify_text_from_file(model_path, vectorizer_path, mlb_path, file_path)
print(f'Die vorhergesagten Kategorien sind: {labels}')

# fsk-bewertung
fsk_rating = fsk_rating_from_file(file_path, combined_word_list, profanity_dict)
print(f'Die FSK-Bewertung des Films lautet: {fsk_rating}')
