from playwright.sync_api import sync_playwright
import time
import json
import random
from datetime import datetime
import os

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def map_model_name(short_name):
    model_map = {
        "m3": "Model 3",
        "my": "Model Y",
        "mx": "Model X",
        "ms": "Model S"
    }
    return model_map.get(short_name, "Unknown Model")

def compute_price_stats(data):
    model_price_stats = {
        "Model 3": {"min": float('inf'), "max": float('-inf'), "total": 0, "count": 0},
        "Model Y": {"min": float('inf'), "max": float('-inf'), "total": 0, "count": 0},
        "Model X": {"min": float('inf'), "max": float('-inf'), "total": 0, "count": 0},
        "Model S": {"min": float('inf'), "max": float('-inf'), "total": 0, "count": 0}
    }

    for car in data:
        model = map_model_name(car.get("Model", ""))
        price = car.get("Price", 0)
        
        if model in model_price_stats:
            model_price_stats[model]["min"] = min(model_price_stats[model]["min"], price)
            model_price_stats[model]["max"] = max(model_price_stats[model]["max"], price)
            model_price_stats[model]["total"] += price
            model_price_stats[model]["count"] += 1
    
    # Calculate the average prices
    for model, stats in model_price_stats.items():
        if stats["count"] > 0:
            stats["avg"] = stats["total"] / stats["count"]
        else:
            stats["avg"] = 0
    
    return model_price_stats


def count_models(data):
    model_count = {
        "Model 3": 0,
        "Model Y": 0,
        "Model X": 0,
        "Model S": 0
    }
    
    for car in data:
        model = map_model_name(car.get("Model", ""))
        if model in model_count:
            model_count[model] += 1
    
    return model_count

def save_data_to_json(data, used_api_urls, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # directory = "/Users/konstantinos/dev/teslafocus/fast-tesla/data/de"
        directory = "/home/srv516119.hstgr.cloud/public_html/teslafocus/tesla-scraper/data/de"  # VPS-Pfad
        os.makedirs(directory, exist_ok=True)
        # filename = f"data/de/tesla_inventory_{timestamp}.json"
        filename = os.path.join(directory, f"tesla_inventory_{timestamp}.json")


    model_counts = count_models(data)
    model_price_stats = compute_price_stats(data)
    
    output_data = {
        "results": data,
        "total_count": len(data),
        "model_counts": model_counts, 
        "model_price_stats": model_price_stats,
        "used_api_urls": used_api_urls
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
    colors = ["BLACK", "RED", "WHITE", "BLUE", "GREY"]  # Liste der Farboptionen für Model 3
    trims = ["M3RWD", "LRAWD", "PAWD"]  # TRIM Optionen, die bei WHITE für Model 3 verwendet werden
    models = [("my", None), ("ms", None), ("mx", None), ("m3", trims)]  # Modell-Liste mit zugehörigen Trim-Optionen
    color_index = 0
    trim_index = 0
    model_index = 0
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
                selected_model, selected_trims = models[model_index]
                if selected_model == "m3":
                    selected_color = colors[color_index]
                    if selected_color == "WHITE":
                        selected_trim = selected_trims[trim_index]
                        options = f'{{"TRIM":["{selected_trim}"], "PAINT":["{selected_color}"], "INTERIOR":["PREMIUM_BLACK","PREMIUM_WHITE"]}}'
                    else:
                        options = f'{{"PAINT":["{selected_color}"]}}'

                else:
                    options = "{}"

                params = f'{{"query":{{"model":"{selected_model}","condition":"used","options":{options},"arrangeby":"Price","order":"asc","market":"DE","language":"de","super_region":"north america","lng":8.6842,"lat":50.1187,"zip":"60313","range":0,"region":"HE"}}, "offset":{offset},"count":{batch_size},"outsideOffset":0,"outsideSearch":false,"isFalconDeliverySelectionEnabled":false,"version":null}}'

                
                the_api_url = f"{api_url}?query={params}"
                response = page.request.get(the_api_url)

                used_api_urls.append(the_api_url)  # Die verwendete API-URL speichern

                if response.ok:
                    data = response.json().get("results", [])
                    if not data:
                        print(f"Keine weiteren Daten verfügbar für Model {selected_model}, Farbe {selected_color if selected_model == 'm3' else 'N/A'} und Trim {selected_trim if selected_model == 'm3' and selected_color == 'WHITE' else 'N/A'}.")
                        
                        if selected_model == "m3":
                            if selected_color == "WHITE" and selected_trims and trim_index < len(selected_trims) - 1:
                                trim_index += 1  # Nächste Trim-Option für Weiß durchlaufen
                            else:
                                color_index += 1
                                trim_index = 0  # Trim-Index zurücksetzen, wenn die Farbe gewechselt wird

                            if color_index >= len(colors):
                                model_index += 1
                                color_index = 0  # Farben zurücksetzen, wenn das Modell gewechselt wird
                        else:
                            model_index += 1

                        offset = 0  # Offset zurücksetzen

                        if model_index >= len(models):
                            print("Alle Modelle, Farb- und Trimkombinationen durchlaufen, keine weiteren Daten verfügbar.")
                            break

                        if selected_model == "m3":
                            print(f"Wechsel zu Model: {models[model_index][0]}, Farbe: {colors[color_index]} und Trim: {trims[0] if selected_color == 'WHITE' else 'N/A'}")
                        else:
                            print(f"Wechsel zu Model: {models[model_index][0]}")
                        continue

                    all_data.extend(data)
                    print(f"API-Antwort mit offset={offset}, Model={selected_model}, Farbe={selected_color if selected_model == 'm3' else 'N/A'} und Trim={selected_trim if selected_model == 'm3' and selected_color == 'WHITE' else 'N/A'}: {len(data)} Einträge abgerufen.")
                    offset += batch_size  # Erhöhe den Offset für den nächsten Aufruf

                    if offset >= 100:  # Wenn Offset-Limit erreicht wird
                        print(f"Offset-Limit für Model {selected_model}, Farbe {selected_color if selected_model == 'm3' else 'N/A'} und Trim {selected_trim if selected_model == 'm3' and selected_color == 'WHITE' else 'N/A'} erreicht.")
                        
                        if selected_model == "m3":
                            if selected_color == "WHITE" and selected_trims and trim_index < len(selected_trims) - 1:
                                trim_index += 1  # Zur nächsten Trim-Option wechseln
                            else:
                                color_index += 1
                                trim_index = 0  # Trim-Index zurücksetzen, wenn die Farbe gewechselt wird

                            if color_index >= len(colors):
                                model_index += 1
                                color_index = 0  # Farben zurücksetzen, wenn das Modell gewechselt wird
                        else:
                            model_index += 1

                        offset = 0  # Offset zurücksetzen

                        if model_index >= len(models):
                            print("Alle Modelle, Farb- und Trimkombinationen durchlaufen, keine weiteren Daten verfügbar.")
                            break
                else:
                    print(f"HTTP-Fehler (API mit offset={offset}, Model={selected_model}, Farbe={selected_color if selected_model == 'm3' else 'N/A'} und Trim {selected_trim if selected_model == 'm3' and selected_color == 'WHITE' else 'N/A'}): {response.status} - {response.status_text}")
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
