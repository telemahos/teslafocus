# ToDo:

18.11.24
- Update the DB, with new daily data
- Make options page to login in the extension
- Automate the scraping and the update of invetory data
- Google Login Auth2
- Auth login to SQLite
- 






# TODO
####################### SOS #######################


###################################################
- Calculate the BC for the other Models and Variations
- Add Weight and Power kW/PS of any car
- ADD Photos as Modal window
- Show Min, Avg, Max Price of each car
- add security oath2 to the API calls


# DONE
+ These numbers (all Models and all cars) should be saved in a Table in DB
+ The scrapers should calculate all the Models seperately and all cars too.
+ The data should load automaticaly, when the site is loading, and if more cars are loading or with filters, the data should be updated.
+ Try to make it look nice in the html
+ If a car is new make the container greenish
+ Show the difference of the new price - vs - old price od the car 
+ Transfer the code for the battary capacity in another file, because it will be more and more calculations


de_CH, sv_SE, da_DK, da_DK, en_IE, it_IT, de_LU, no_NO, de_AT, 



# Tesla Invetory App - Extension

# IDEAS
- When click on "more Info" of the car, we can drop down a list with all the extras of the car (20 wheels, back heating seats ...), the price history, extra photos if available
- When two or more cars are to compare, we can show all the extras that it has, alongside with the technical information and price history
- The scrapers should record the numbers of each model, each day. I should track this information for analytics purposeses.
- Favoriten und Markierungen: Benutzer können ihre bevorzugten Fahrzeuge markieren oder speichern.
- Benachrichtigungen: Sende Benachrichtigungen an Benutzer über relevante Updates oder Änderungen.
- Push-Benachrichtigungen: Implementiere Benachrichtigungen, die Benutzer bei bestimmten Ereignissen informieren, z. B. wenn neue Fahrzeuge in die Datenbank aufgenommen werden oder wenn sich der Preis eines zuvor gespeicherten Fahrzeugs ändert.
- Echtzeit-Updates: Verwende Technologien wie WebSockets oder Server-Sent Events (SSE), um den Benutzern sofortige Updates anzuzeigen, ohne dass sie die Seite neu laden müssen.
- Preisalarme: Erlaube den Benutzern, Preisalarme für bestimmte Fahrzeuge zu setzen. Sie können benachrichtigt werden, wenn der Preis eines Fahrzeugs unter einen festgelegten Schwellenwert fällt.
- Wunschlisten: Biete eine Funktion an, mit der Benutzer Fahrzeuge zu einer Wunschliste hinzufügen können, damit sie diese später leicht finden und überwachen können.
- Suchanfragen speichern: Benutzer können ihre bevorzugten Suchanfragen (z. B. nach Modell, Preis, Baujahr) speichern und beim nächsten Mal schnell darauf zugreifen.
- Automatische Suchläufe: Automatisiere regelmäßige Suchanfragen, bei denen die Benutzer benachrichtigt werden, wenn ein neues Fahrzeug erscheint, das ihren gespeicherten Suchkriterien entspricht.
- Fahrzeuge vergleichen: Erlaube den Benutzern, mehrere Fahrzeuge auszuwählen und sie Seite an Seite zu vergleichen. Zeige wichtige Unterschiede wie Preis, Kilometerstand, Zustand und verfügbare Extras an.
- Bewertungen und Kommentare: Implementiere ein Bewertungssystem, bei dem Benutzer Fahrzeuge basierend auf ihren Erfahrungen oder Meinungen bewerten und kommentieren können.
- Soziale Medien und Fahrzeug-Sharing: Biete den Benutzern die Möglichkeit, Fahrzeuge direkt über soziale Medien (z. B. Twitter, Facebook, WhatsApp) oder E-Mail zu teilen.
- Preisbewertungsdienste: Integriere Preisbewertungsdienste (wie z. B. Autotrader, Kelley Blue Book), damit Benutzer erfahren können, ob der angezeigte Preis marktgerecht ist.
- Versicherungs- und Finanzierungsangebote: Füge eine Funktion hinzu, die Versicherungs- oder Finanzierungsoptionen anzeigt, wenn Benutzer ein Fahrzeug finden, das sie interessiert.
- Fahrzeughistorie: Biete den Benutzern die Möglichkeit, eine detaillierte Historie jedes Fahrzeugs zu sehen, z. B. Vorbesitzer, Unfälle, Wartungen usw. Dies kann über externe API-Integrationen mit Diensten wie Carfax erfolgen.
- Statistiken über den Fahrzeugmarkt: Zeige aggregierte Statistiken an, z. B. die durchschnittliche Verweildauer eines Fahrzeugtyps auf dem Markt, die durchschnittlichen Preisänderungen im Laufe der Zeit oder wie sich die Verfügbarkeit bestimmter Modelle ändert.
- Personalisierte Fahrzeugempfehlungen: Basierend auf den Suchverläufen und den Fahrzeugen, die ein Benutzer betrachtet, kannst du personalisierte Fahrzeugempfehlungen geben.
- Analyse des Benutzerverhaltens: Nutze Analysetools, um herauszufinden, welche Fahrzeuge und Modelle am beliebtesten sind, und optimiere die Benutzeroberfläche oder Angebote entsprechend.
- Benutzerbewertungen für Fahrzeuge: Ermögliche es den Benutzern, bestimmte Modelle oder Fahrzeuge zu bewerten und ihre Erfahrungen mit anderen zu teilen.
- Diskussionsforen oder Q&A-Bereich: Implementiere einen Bereich, in dem Benutzer Fragen zu bestimmten Modellen stellen oder Tipps und Ratschläge zum Kauf von Gebrauchtwagen austauschen können.
- Datenexport: Erlaube den Benutzern, die Fahrzeugdaten in verschiedene Formate (z. B. CSV, PDF) zu exportieren, damit sie ihre Daten offline oder für andere Zwecke weiterverwenden können.
- Berichte generieren: Biete die Möglichkeit, Berichte über den Fahrzeugmarkt, Preisentwicklungen oder den Zustand bestimmter Modelle zu erstellen.
- Fahrzeuge auf einer Karte anzeigen: Verwende Karten, um Fahrzeuge nach Standort zu präsentieren. Benutzer können schnell Fahrzeuge in ihrer Nähe finden.
- Route zum Fahrzeug planen: Füge eine Funktion hinzu, die den Benutzer direkt zu dem Ort des Fahrzeugs navigiert (z. B. mit Google Maps oder Apple Maps).
- Reparaturempfehlungen: Basierend auf dem Kilometerstand und dem Alter des Fahrzeugs kannst du Wartungs- oder Reparaturempfehlungen anzeigen.
- Erweiterte Filter: Erlaube den Benutzern, ihre Suche mit detaillierten Filtern zu verfeinern, z. B. nach Extras, Farbe, Motorleistung, Kraftstoffverbrauch usw.
- Volltextsuche: Implementiere eine Volltextsuche, damit Benutzer nach spezifischen Merkmalen oder Fahrzeugtypen suchen können.
- Synchronisierung zwischen Geräten: Wenn du ein Benutzerkonto mit Login implementierst, kannst du eine Cross-Plattform-Synchronisation einführen, sodass gespeicherte Daten und Präferenzen auf allen Geräten verfügbar sind, auf denen der Benutzer die Erweiterung verwendet.
- Öffentliche API: Erstelle eine API für Drittanbieter, um den Zugriff auf die Fahrzeugdaten zu ermöglichen. Andere Entwickler könnten damit neue Apps oder Dienste aufbauen, die auf den von dir gesammelten Daten basieren.
- Affiliate-Links: Biete Links zu Versicherungen, Finanzierungsanbietern oder Autohändlern an, um zusätzliche Einnahmequellen zu erschließen.
- Partnerprogramme: Du könntest mit Autohändlern zusammenarbeiten und den Verkauf fördern, indem du spezielle Angebote oder Rabatte für Benutzer deiner Erweiterung anbietest.
- Preisentwicklungsanalyse: Füge Tools hinzu, die den Benutzern helfen, den Preistrend eines Fahrzeugs über einen bestimmten Zeitraum zu verfolgen.
- Empfohlener Kaufzeitpunkt: Basierend auf Preisschwankungen kannst du Empfehlungen geben, wann der beste Zeitpunkt für den Kauf eines bestimmten Fahrzeugs ist.
- KI-basierte Preisvorhersagen: Nutze Machine Learning, um zukünftige Preisentwicklungen für Fahrzeuge vorherzusagen.
- Archivierte Fahrzeuge anzeigen: Biete eine Funktion, bei der Benutzer auf historische Daten von Fahrzeugen zugreifen können, die nicht mehr verfügbar sind, um Trends und Preise über die Zeit zu analysieren.
- Benutzeroberfläche im Dark Mode: Füge einen Dark Mode hinzu, der insbesondere bei längerer Nutzung die Augen schont und die Benutzererfahrung verbessert.
- Premium-Abonnement: Biete erweiterte Funktionen wie detaillierte Fahrzeuganalysen, erweiterte Filtermöglichkeiten oder Prioritätsbenachrichtigungen als Teil eines Premium-Abonnements an.