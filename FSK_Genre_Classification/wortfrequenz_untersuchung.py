import os
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# dateien lesen
def read_file(file_path):
    print(f"Lese Datei: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().lower()


# csv lesen und wörter mit severity rating extrahieren
def read_profanity_csv(file_path):
    print(f"Lese CSV Datei: {file_path}")
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
    print("Starte Tokenisierung und Lemmatisierung des Textes...")
    tokens = word_tokenize(text)

    # nur wörter aus buchstaben behalten
    words = [word for word in tokens if word.isalpha()]

    # stopwörter entfernen
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # lemmatisierung
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    print(f"Anzahl der Wörter nach Vorverarbeitung: {len(lemmatized_words)}")
    return lemmatized_words


# relative häufigkeit und anzahl sensibler wörter berechnen
def calculate_combined_relative_frequency(text_tokens, combined_word_list, profanity_dict):
    word_count = 0
    for word in text_tokens:
        if word in combined_word_list:
            word_count += 1
        if word in profanity_dict:
            word_count += int(profanity_dict[word])

    total_words = len(text_tokens)
    print(f"Anzahl der gefundenen Wörter aus der kombinierten Liste und CSV: {word_count}")
    print(f"Gesamtzahl der Wörter im Text: {total_words}")

    if total_words == 0:
        return 0, 0

    return word_count / total_words, word_count


# anzahl gefundener wörter pro liste
def calculate_word_list_counts(text_tokens, word_lists, profanity_dict):
    counts = {}
    for name, word_list in word_lists.items():
        counts[name] = sum(1 for word in text_tokens if word in word_list)
        print(f"Gefundene Wörter aus {name}-Liste: {counts[name]}")

    # profanity wörter zählen
    profanity_count = sum(int(profanity_dict.get(word, 0)) for word in text_tokens)
    counts['profanity'] = profanity_count
    print(f"Gefundene Wörter aus Profanity-Liste: {profanity_count}")

    return counts


# durchschnitt aller texte in einem fsk-ordner berechnen
def calculate_average_combined_frequency(fsk_folder, combined_word_list, word_lists, profanity_dict):
    total_frequency = 0
    total_word_counts = {name: 0 for name in word_lists.keys()}
    total_word_counts['profanity'] = 0
    num_texts = 0

    print(f"Durchlaufe Ordner: {fsk_folder}")
    for file_name in os.listdir(fsk_folder):
        file_path = os.path.join(fsk_folder, file_name)

        if file_name.endswith(".txt"):
            print(f"Verarbeite Datei: {file_name}")
            num_texts += 1
            text = read_file(file_path)
            tokens = preprocess_text(text)

            # relative häufigkeit für kombinierte wortliste berechnen
            rel_freq, word_count = calculate_combined_relative_frequency(tokens, combined_word_list, profanity_dict)
            total_frequency += rel_freq

            # anzahl gefundener wörter pro Liste berechnen
            word_list_counts = calculate_word_list_counts(tokens, word_lists, profanity_dict)
            for name, count in word_list_counts.items():
                total_word_counts[name] += count

            print(f"Relative Häufigkeit für diesen Text: {rel_freq:.4f}")

    avg_frequency = total_frequency / num_texts if num_texts > 0 else 0
    avg_word_counts = {name: total_word_counts[name] / num_texts if num_texts > 0 else 0 for name in
                       total_word_counts.keys()}

    print(f"Anzahl der verarbeiteten Texte: {num_texts}")
    return avg_frequency, avg_word_counts


# durchschnitt pro fsk-stufe berechnen
def calculate_average_per_fsk(fsk_folder, combined_word_list, word_lists, profanity_dict):
    fsk_levels = ['0', '6', '12', '16', '18']
    results = {}

    for fsk in fsk_levels:
        fsk_path = os.path.join(fsk_folder, fsk)
        if os.path.isdir(fsk_path):
            print(f"Starte Berechnungen für FSK-Stufe: {fsk}")
            avg_frequency, avg_word_counts = calculate_average_combined_frequency(fsk_path, combined_word_list,
                                                                                  word_lists, profanity_dict)
            results[fsk] = (avg_frequency, avg_word_counts)
        else:
            print(f"Ordner für FSK-Stufe {fsk} nicht gefunden!")

    return results


# wortlisten laden und in kleinbuchstaben umwandeln
print("Lade Wortlisten...")
drugs_list = [word.lower() for word in read_file('word_lists/drugs_words.txt').splitlines()]
violence_list = [word.lower() for word in read_file('word_lists/violence_words.txt').splitlines()]
sexual_list = [word.lower() for word in read_file('word_lists/sexual_words.txt').splitlines()]

# csv laden
print("Lade Wörter und Severity Ratings aus der CSV-Datei...")
profanity_dict = read_profanity_csv('word_lists/profanity_words.csv')

# kombinierte wortliste erstellen
print("Erstelle kombinierte Wortliste...")
combined_word_list = drugs_list + violence_list + sexual_list

# pfad zum ordner mit fsk-unterordnern
fsk_folder = 'movie_scripts'

# liste aus wortlisten
word_lists = {
    'drugs': drugs_list,
    'violence': violence_list,
    'sexual': sexual_list
}

# durchschnittliche relative häufigkeit und wortzählung pro fsk-stufe berechnen
print("Starte Berechnung der durchschnittlichen relativen Häufigkeit pro FSK-Stufe...")
average_frequencies = calculate_average_per_fsk(fsk_folder, combined_word_list, word_lists, profanity_dict)

# ergebnisse anzeigen
for fsk, (avg_frequency, avg_word_counts) in average_frequencies.items():
    print(f"Durchschnittliche relative Häufigkeit der Wörter für FSK {fsk}: {avg_frequency:.4f}")
    for name, avg_count in avg_word_counts.items():
        print(f"Durchschnittlich gefundene Wörter aus {name}-Liste für FSK {fsk}: {avg_count:.2f}")
