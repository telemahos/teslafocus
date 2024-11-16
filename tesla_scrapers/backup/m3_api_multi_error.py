from playwright.sync_api import sync_playwright
import time
import json
import random
from datetime import datetime

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def save_data_to_json(data, used_api_urls, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tesla_inventory_{timestamp}.json"
    
    output_data = {
        "results": data,
        "total_count": len(data),
        "used_api_urls": used_api_urls  # Fügen Sie die verwendeten API-URLs hinzu
    }
    
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
    used_api_urls = []  # Liste zum Speichern der verwendeten API-URLs
    colors = ["BLACK", "RED", "WHITE", "BLUE", "GREY"]  # Liste der Farboptionen
    trims = ["M3RWD", "LRAWD", "PAWD"]  # TRIM Optionen, die bei WHITE verwendet werden
    color_index = 0
    trim_index = 0
    offset = 0
    batch_size = 50

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

            api_url = "https://www.tesla.com/inventory/api/v4/inventory-results"

            while True:
                selected_color = colors[color_index]
                if selected_color == "WHITE":
                    selected_trim = trims[trim_index]
                    options = f'{{"TRIM":["{selected_trim}"], "PAINT":["{selected_color}"], "INTERIOR":["PREMIUM_BLACK","PREMIUM_WHITE"]}}'
                else:
                    options = f'{{"PAINT":["{selected_color}"]}}'

                params = f'{{"query":{{"model":"m3","condition":"used","options":{options},"arrangeby":"Price","order":"asc","market":"DE","language":"de","super_region":"north america","lng":8.6842,"lat":50.1187,"zip":"60313","range":0,"region":"HE"}}, "offset":{offset},"count":{batch_size},"outsideOffset":0,"outsideSearch":false,"isFalconDeliverySelectionEnabled":false,"version":null}}'
                
                the_api_url = f"{api_url}?query={params}"
                response = page.request.get(the_api_url)

                used_api_urls.append(the_api_url)  # Die verwendete API-URL speichern

                if response.ok:
                    data = response.json().get("results", [])
                    if not data:
                        print(f"Keine weiteren Daten verfügbar für Farbe {selected_color} und Trim {selected_trim if selected_color == 'WHITE' else 'N/A'}.")
                        
                        if selected_color == "WHITE" and trim_index < len(trims) - 1:
                            trim_index += 1  # Nächste Trim-Option für Weiß durchlaufen
                        else:
                            color_index += 1
                            trim_index = 0  # Trim-Index zurücksetzen, wenn die Farbe gewechselt wird

                        offset = 0  # Offset zurücksetzen

                        if color_index >= len(colors):
                            print("Alle Farb- und Trimkombinationen durchlaufen, keine weiteren Daten verfügbar.")
                            break

                        print(f"Wechsel zu Farbe: {colors[color_index]} und Trim: {trims[trim_index] if colors[color_index] == 'WHITE' else 'N/A'}")
                        continue

                    all_data.extend(data)
                    print(f"API-Antwort mit offset={offset}, Farbe={selected_color} und Trim={selected_trim if selected_color == 'WHITE' else 'N/A'}: {len(data)} Einträge abgerufen.")
                    offset += batch_size  # Erhöhe den Offset für den nächsten Aufruf

                    if offset >= 100:  # Wenn Offset-Limit erreicht wird
                        print(f"Offset-Limit für Farbe {selected_color} und Trim {selected_trim if selected_color == 'WHITE' else 'N/A'} erreicht.")
                        
                        if selected_color == "WHITE" and trim_index < len(trims) - 1:
                            trim_index += 1  # Zur nächsten Trim-Option wechseln
                        else:
                            color_index += 1
                            trim_index = 0  # Trim-Index zurücksetzen, wenn die Farbe gewechselt wird

                        offset = 0  # Offset zurücksetzen

                        if color_index >= len(colors):
                            print("Alle Farb- und Trimkombinationen durchlaufen, keine weiteren Daten verfügbar.")
                            break
                else:
                    print(f"HTTP-Fehler (API mit offset={offset}, Farbe={selected_color} und Trim={selected_trim if selected_color == 'WHITE' else 'N/A'}): {response.status} - {response.status_text}")
                    break

            return all_data if all_data else None, used_api_urls

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None, used_api_urls
        finally:
            browser.close()

max_attempts = 3

for attempt in range(1, max_attempts + 1):
    print(f"Versuch {attempt} von {max_attempts}")
    data, used_api_urls = get_inventory_data()
    if data:
        print("Daten erfolgreich abgerufen:")
        save_data_to_json(data, used_api_urls)
        break
    else:
        print(f"Fehler beim Abrufen der Daten. Versuch {attempt} von {max_attempts}.")
        if attempt < max_attempts:
            wait_time = random.uniform(20, 30)
            print(f"Warte {wait_time:.2f} Sekunden vor dem nächsten Versuch...")
            time.sleep(wait_time)
        else:
            print("Konnte die Daten nach mehreren Versuchen nicht abrufen.")