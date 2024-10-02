import os
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# dateien lesen
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().lower()

# csv lesen und wörter mit severity ratings extrahieren
def read_profanity_csv(file_path):
    profanity_dict = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            word = row['text'].lower()
            severity_rating = float(row['severity_rating'])
            profanity_dict[word] = severity_rating
    return profanity_dict

# tokenisierung und lemmatisierung
def preprocess_text(text):
    tokens = word_tokenize(text)

    # nur wörter aus buchstaben behalten
    words = [word for word in tokens if word.isalpha()]

    # stopwörter entfernen
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # lemmatisierung
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    return lemmatized_words

# berechnung der relativen häufigkeit und anzahl der kritischen wörter
def calculate_combined_relative_frequency(text_tokens, combined_word_list, profanity_dict):
    word_count = 0
    for word in text_tokens:
        if word in combined_word_list:
            word_count += 1
        if word in profanity_dict:
            word_count += int(profanity_dict[word])

    total_words = len(text_tokens)
    if total_words == 0:
        return 0, 0

    return word_count / total_words, word_count

# bestimmung der fsk-bewertung
def determine_fsk_based_on_relative_frequency(relative_frequency):
    if relative_frequency <= 0.0189:
        return 'FSK 0'
    elif relative_frequency <= 0.0250:
        return 'FSK 6'
    elif relative_frequency <= 0.0300:
        return 'FSK 12'
    elif relative_frequency <= 0.0350:
        return 'FSK 16'
    else:
        return 'FSK 18'

# berechnung der fsk für einzelnen film
def calculate_fsk_for_movie(movie_file, combined_word_list, profanity_dict):
    text = read_file(movie_file)
    tokens = preprocess_text(text)

    # relative häufigkeit der wörter aus listen und csv berechnen
    rel_freq, word_count = calculate_combined_relative_frequency(tokens, combined_word_list, profanity_dict)

    # fsk-bewertung basierend auf relative häufigkeit bestimmen
    fsk_rating = determine_fsk_based_on_relative_frequency(rel_freq)

    return fsk_rating
