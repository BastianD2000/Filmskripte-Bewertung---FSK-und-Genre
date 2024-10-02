import os

def load_data(base_path):
    texts = []
    labels = []
    
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            text_file = os.path.join(folder_path, 'script.txt')
            label_file = os.path.join(folder_path, 'genre.txt')
            
            # prüfen, ob script.txt existiert
            if not os.path.exists(text_file):
                print(f"Warning: {text_file} does not exist, skipping this folder.")
                continue
            
            # prüfen, ob genre.txt existiert
            if not os.path.exists(label_file):
                print(f"Warning: {label_file} does not exist, skipping this folder.")
                continue

            # prüfen, ob genre.txt leer ist
            if os.path.getsize(label_file) == 0:
                print(f"Warning: {label_file} is empty, skipping this folder.")
                continue
            
            # script.txt mit utf-8 öffnen
            with open(text_file, 'r', encoding='utf-8') as tf:
                text = tf.read()
                
            # genre.txt mit UTF-8 Kodierung öffnen
            with open(label_file, 'r', encoding='utf-8') as lf:
                label_lines = lf.read().strip().split('\n')
                labels_list = [label.strip() for label in label_lines if label.strip()]
            
            texts.append(text)
            labels.append(labels_list)
    
    return texts, labels
