import requests
from bs4 import BeautifulSoup
import time
import re
import os
import logging


base_url = 'https://imsdb.com'


# Zum Abrufen und Parsen
def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err} - URL: {url}')
    except Exception as err:
        print(f'Other error occurred: {err} - URL: {url}')
    return None


# Mit der base url erstellte Urls zum abrufen aller Skripte
def get_script_list():
    url = f'{base_url}/all-scripts.html'
    soup = get_soup(url)
    if soup:
        script_links = []
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/Movie Scripts/'):
                script_links.append(link['href'])
        return script_links
    else:
        print('Failed to retrieve the script list.')
    return []


# FÜr den Machine Learning Teil zum Auslesen der Skripte, um diese dann einlesen zu können
def get_genres(movie_url):
    full_url = f'{base_url}{movie_url}'
    print(f'Full url: {full_url}')
    soup = get_soup(full_url)
    if soup:
        genre_tags = soup.find_all('a', href=re.compile(r'/genre/'))
        if genre_tags:
            return [genre_tag.get_text() for genre_tag in genre_tags[18:]]
            # Übersprint die ersten 18 Genre-Einträge, da dort immer alle existierenden Genres aufgelistet sind
        else:
            print(f'Genres not found in: {full_url}')
    else:
        print(f'Failed to fetch genres from: {full_url}')
    return ['Unknown']


# Abrufen des Skript-Inhaltes und alle Bedingungen die für verschiedene Titel Formen notwendig sind
def get_script_content(script_url):
    # Neuen Link aufbauen
    print(f'Script url: {script_url}')

    # Doppelpunkte werden durch Bindestriche ersetzt und das Leerzeichen nach einem Doppelpunkt entfernt
    script_name = script_url.split('/')[-1].replace(' Script.html', '').replace('%20', ' ')
    script_name = script_name.replace(':', '-')

    # Entfernt Leerzeichen nach einem neuen Bindestrich entstehen
    script_name = re.sub(r'-\s+', '-', script_name)

    # Ersetzt alle Leerzeichen eines Filmtitels durch Bindestriche, da diese so in der URl des Skriptes stehen
    script_name = script_name.replace(' ', '-')

    new_url = f'{base_url}/scripts/{script_name}.html'

    soup = get_soup(new_url)
    if soup:
        script_text_div = soup.find('td', {'class': 'scrtext'}) or soup.find('pre', {'class': 'scrtext'}) or soup.find(
            'div', {'class': 'scrtext'})
        if script_text_div:
            return script_text_div.get_text()
        else:
            print(f'Script content not found in: {new_url}')
    else:
        print(f'Failed to fetch script content from: {new_url}')

    return ''


# Logging-Konfiguration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Erstellen eines sicheren Titels der abgespeichert werden kann
def get_safe_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)


# Abspeichern der Skripte und Testen, ob Skript schon vorhanden ist
def save_file(path, content, description):
    if os.path.exists(path):
        logging.info(f'The {description} "{os.path.basename(path)}" already exists in the folder "'
                     f'{os.path.dirname(path)}".')
        return
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
        logging.info(f'Successfully saved {description}: {path}')
    except Exception as e:
        logging.error(f'Error saving {description} {os.path.basename(path)}: {e}')


# Genaues abspeichern der Skripte, um spezielle Ordnerstruktur zu erhalten, die für die Machine Learning Anwendung gebraucht wird
def save_script(title, content, genres=None):
    if genres is None:
        genres = ["Genre"]
    safe_title = get_safe_title(title)
    base_directory = os.path.join("Scripts", safe_title)

    # Falls es noch nicht existiert, Verzeichnis erstellen
    os.makedirs(base_directory, exist_ok=True)

    # Pfade zur Skript- und Genres-Datei erstellen
    script_path = os.path.join(base_directory, "Script.txt")
    genres_path = os.path.join(base_directory, "Genres.txt")

    # Dateien unter den Pfaden abspeichern
    save_file(script_path, content, "script")
    save_file(genres_path, '\n'.join(genres), "genres")


# Hauptfunktion zum Scrapen und Speichern der Skripte
def main(specific_title=None, specific_genre=None):
    script_list = get_script_list()
    if not script_list:
        logging.error('No scripts found to scrape.')
        return

    for script in script_list:
        script_title = script.split('/')[-1].replace('%20', ' ').replace(' Script.html', '').replace('.html', '')

        # Bei spezifisch angegebenem Titel nach diesem Filtern
        if specific_title and specific_title.lower() != script_title.lower():
            continue

        logging.info(f'Scraping script: {script_title}')

        # Genres abrufen
        genres = get_genres(script)

        # Bei spezifisch angegebenem Genre nach diesem Filtern
        if specific_genre and specific_genre.lower() not in [genre.lower() for genre in genres]:
            continue

        # Inhalt vom Skript abrufen
        script_content = get_script_content(script)
        if script_content:
            save_script(script_title, script_content, genres)
        else:
            logging.error(f'Failed to get script content for: {script_title}')

        # Pause um Server nicht zu stark zu belasten
        time.sleep(2)


if __name__ == '__main__':
    main(specific_title='Interstellar')
    # main(specific_genre='Drama')
