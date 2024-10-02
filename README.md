# Filmskripte-Bewertung FSK und Genre

„only_fsk_rate.py“ verwendet nun die Skala, um einem neuen Drehbuch eine 
FSK-Bewertung zu geben. Die vorbereitende Wortfrequenzanalyse funktioniert genauso wie 
in „wortfrequenz_untersuchung.py“. Der Text wird tokenisiert, lemmatisiert, Stoppwörter 
werden entfernt und alle Wörter werden in Kleinbuchstaben umgewandelt. Dann wird 
wieder die relative Häufigkeit der Begriffe aus den Listen berechnet und mit der Skala 
abgeglichen. Nach der Einordnung in die Skala wird so schließlich die FSK-Bewertung für 
den Film ausgegeben.

„load_data.py“ lädt die Texte und ihre jeweiligen Genres aus der Ordnerstruktur.

„preprocess.py“ ist für die Vorverarbeitung der Texte zuständig. Hier werden die Texte 
tokenisiert, Stoppwörter werden entfernt und es kann wahlweise Stemming oder 
Lemmatization angewendet werden. Im Zuge dieses Projektes wurde Stemming verwendet, 
Lemmatization kann aber verwendet werden, indem die entsprechenden Werte für 
„use_stemming“ und „use_lemmatization“ angepasst werden.
Schließlich führt „preprocess.py“ eine TF-IDF Vektorisierung durch. 

„training.py“ teilt die 
Datenmenge in Trainings- und Testdaten, standartmäßig ist hier eine Verteilung von 80 zu 
20 eingestellt. Zuerst wird ein Modell basierend auf den vektorisierten Trainingsdaten 
erstellt, dann wird dieses Modell auf den Testdaten angewendet und es wird geprüft, wie 
viele Genres korrekt hervorgesagt wurden. Darauf basierend wird eine Evaluation mit 
Aussagen zu Precision, Recall und F1-Score erstellt.

„evaluate.py“ gibt eine erste Evaluierung in der Konsole aus.

„classify.py“ verarbeitet neue Texte wie auch bei den Trainingsdaten vor. Anschließend 
werden das trainierte Modell und der Vektorisierer geladen, um diese auf den neuen Texten 
anzuwenden und seine Genres vorherzusagen. 

„fsk.py“ beinhaltet die Funktionen von „only_fsk_rate.py“. 

„main_train.py“ ruft die Funktionen von „load_data.py“, „preprocess.py“ und „training.py“ 
auf, um anhand der Trainingsdaten ein Modell und einen Vektorisierer zu erstellen und zu 
speichern. 

„main_classify.py“ ruft Funktionen von „classify.py“ auf, um das Modell und den 
Vektorisierer auf einen neuen Text anzuwenden und so seine Genres zu bestimmen. Zudem 
ruft es die Funktionen von „fsk.py“ auf um wie bereits beschrieben eine 
Wortfrequenzanalyse durchzuführen und anhand der Skala die FSK-Bewertung für 
denselben Text zu erstellen. 

Für das Training zur Genre-Bestimmung muss dank dem 
modularen Aufbau nur „main_train.py“ ausgeführt werden und für die Bewertung von Genre 
und FSK eines neuen Textes ist nur die Ausführung von „main_classify.py“ nötig. Beides 
wird in der Konsole ausgegeben.
