import os
import subprocess
from pathlib import Path
import shutil

# Verzeichnis mit den JSON-Dateien
JSON_DIR = Path("/Users/konstantinos/dev/teslafocus/fast-tesla/data/de")
# Unterverzeichnis für verarbeitete Dateien
PROCESSED_DIR = JSON_DIR / "processed"
# Pfad zur `add_cars_2db.py`
DB_SCRIPT = Path("/Users/konstantinos/dev/teslafocus/fast-tesla/add_cars_2db.py")
# Pfad zur Logdatei
LOG_FILE = Path("/Users/konstantinos/dev/teslafocus/fast-tesla/log_file.txt")

# Stelle sicher, dass das Unterverzeichnis existiert
PROCESSED_DIR.mkdir(exist_ok=True)

def load_logged_files(log_file):
    """
    Lädt die Namen der bereits verarbeiteten JSON-Dateien aus der Logdatei.
    """
    if not log_file.exists():
        return set()
    with log_file.open("r") as f:
        return set(line.strip() for line in f.readlines())

def log_file_as_processed(log_file, json_file):
    """
    Fügt den Namen der JSON-Datei zur Logdatei hinzu.
    """
    with log_file.open("a") as f:
        f.write(f"{json_file.name}\n")

def find_new_json_files(directory, logged_files):
    """
    Findet neue JSON-Dateien, die noch nicht verarbeitet wurden.
    Sortiert sie nach Zeitstempel im Dateinamen (älteste zuerst).
    """
    all_json_files = list(directory.glob("tesla_inventory_*.json"))
    new_files = [file for file in all_json_files if file.name not in logged_files]

    # Sortiere Dateien nach Zeitstempel aus dem Dateinamen
    new_files.sort(key=lambda f: f.name.split("_")[2].replace(".json", ""))
    return new_files

def insert_json_to_db(json_file):
    """
    Führt das Python-Skript aus, das die Daten in die SQLite-DB einfügt.
    """
    try:
        result = subprocess.run(
            ["python3", str(DB_SCRIPT), str(json_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Erfolgreich eingefügt: {json_file}")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Einfügen: {json_file}")
        print(e.stderr)
        return False

def move_to_processed(json_file):
    """
    Verschiebt die JSON-Datei in das `processed`-Unterverzeichnis.
    """
    try:
        shutil.move(str(json_file), str(PROCESSED_DIR / json_file.name))
        print(f"Datei verschoben nach: {PROCESSED_DIR / json_file.name}")
    except Exception as e:
        print(f"Fehler beim Verschieben von {json_file}: {e}")

def main():
    # Geloggte Dateien laden
    logged_files = load_logged_files(LOG_FILE)

    # Neue Dateien finden, sortiert nach ältesten zuerst
    new_files = find_new_json_files(JSON_DIR, logged_files)

    if not new_files:
        print("Keine neuen JSON-Dateien gefunden.")
        return

    for json_file in new_files:
        print(f"Verarbeite Datei: {json_file}")
        if insert_json_to_db(json_file):
            # Datei als verarbeitet markieren
            log_file_as_processed(LOG_FILE, json_file)
            # Datei verschieben
            move_to_processed(json_file)

if __name__ == "__main__":
    main()
