from playwright.sync_api import sync_playwright
import time
import json
import random
from datetime import datetime

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def save_data_to_json(data, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tesla_mY_{timestamp}.json"
    
    # Fügen Sie die Anzahl der Autos zum Daten-Dictionary hinzu
    output_data = {"results": data, "total_count": len(data)}
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    print(f"Daten in {filename} gespeichert.")

def scroll_to_bottom(page):
    previous_height = None
    while True:
        current_height = page.evaluate("(window.innerHeight + window.scrollY)")
        if previous_height == current_height:
            break
        previous_height = current_height
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        random_sleep(2, 4)  # Wartezeit, um das Laden der Inhalte zu ermöglichen

def get_inventory_data():
    all_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True
        )
        page = context.new_page()
        try:
            page.goto("https://www.tesla.com/de_de", timeout=120000)
            random_sleep(5, 10)

            try:
                cookie_accept_button = page.locator('button:has-text("Alle Cookies akzeptieren")')
                if cookie_accept_button.is_visible(timeout=5000):
                    cookie_accept_button.click()
                    print("Cookie-Zustimmung akzeptiert.")
                    random_sleep(2, 5)
            except:
                print("Kein Cookie-Zustimmungs-Dialog gefunden oder bereits akzeptiert.")

            if page.locator("text=Ich bin kein Roboter").is_visible():
                print("CAPTCHA erkannt. Versuche manuell zu lösen...")
                input("Drücken Sie Enter, wenn Sie das CAPTCHA gelöst haben...")

            scroll_to_bottom(page)
            print("Seite vollständig gescrollt.")

            # API URLs mit Offset-Werten
            api_url = "https://www.tesla.com/inventory/api/v4/inventory-results"

            # Nutzung einer Schleife für die API-Aufrufe
            for offset in [0, 50]:
                params = f'{{"query":{{"model":"my","condition":"used","options":{{}},"arrangeby":"Price","order":"asc","market":"DE","language":"de","super_region":"north america","lng":8.6842,"lat":50.1187,"zip":"60313","range":0,"region":"HE"}}, "offset":{offset},"count":50,"outsideOffset":0,"outsideSearch":false,"isFalconDeliverySelectionEnabled":false,"version":null}}'
                response = page.request.get(f"{api_url}?query={params}")

                if response.ok:
                    data = response.json().get("results", [])
                    all_data.extend(data)
                    print(f"API-Antwort mit offset={offset}: {len(data)} Einträge abgerufen.")
                else:
                    print(f"HTTP-Fehler (API mit offset={offset}): {response.status} - {response.status_text}")

            return all_data if all_data else None

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None
        finally:
            browser.close()

max_attempts = 3
for attempt in range(1, max_attempts + 1):
    print(f"Versuch {attempt} von {max_attempts}")
    data = get_inventory_data()
    if data:
        print("Daten erfolgreich abgerufen:")
        print(json.dumps(data, indent=2))
        save_data_to_json(data)
        break
    else:
        print(f"Fehler beim Abrufen der Daten. Versuch {attempt} von {max_attempts}.")
        if attempt < max_attempts:
            wait_time = random.uniform(20, 30)
            print(f"Warte {wait_time:.2f} Sekunden vor dem nächsten Versuch...")
            time.sleep(wait_time)
        else:
            print("Konnte die Daten nach mehreren Versuchen nicht abrufen.")