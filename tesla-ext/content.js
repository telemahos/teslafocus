console.log("Content Script Loaded"); 

// The Dialog is closing after 5 sec.
window.addEventListener("load", () => {  // "load" verwenden
    // console.log("Page fully loaded");
    
    const checkIfLoaded = () => {
        const dialog = document.querySelector('#iso-container > div > dialog');

        if (dialog) {
            dialog.close(); // Schließe das Dialogfenster
            dialog.setAttribute("aria-hidden", "true");
            // console.log("Dialog geschlossen");
            // Calls the function to extract the Ids
            
        } else {
            console.log("Dialog not found");
            // Calls the function to extract the Ids
            extractIds();
        }
    };

    // Optional: Timeout anpassen oder entfernen
    setTimeout(checkIfLoaded, 2000); // 1000ms (1 Sekunde) als Beispiel
})

// Listener for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('LISTENER2');
    if (message.type === "RETURNED_CAR_DATA") {
        const cars = message.data;
        console.log("Message received from background, CARS:", cars);
        
        // Handle failed IDs if any
        if (message.failedIds && message.failedIds.length > 0) {
            console.warn(`Failed to fetch data for VINs:`, message.failedIds);
            // Optional: Display a user-friendly message for failed VINs
            message.failedIds.forEach(vin => {
                const article = document.querySelector(`article[data-id^="${vin}"]`);
                if (article) {
                    const dataContainer = article.querySelector('.result-federal-incentive');
                    if (dataContainer) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'tf-data-container tf-error';
                        errorDiv.innerHTML = `
                            <div class="tf-data-column">
                                <div><strong>VIN:</strong> ${vin}</div>
                                <div><strong>Status:</strong> Data temporarily unavailable</div>
                            </div>
                        `;
                        dataContainer.innerHTML = '';
                        dataContainer.appendChild(errorDiv);
                    }
                }
            });
        }

        // Process successful data
        if (cars && cars.cars && cars.cars.length > 0) {
            displayData(cars);
        }
    }
});

function formatPrice(price) {
    if (price === null || price === undefined) {
        return "0";
    }
    // Konvertiere den Preis in eine Zahl
    const numericPrice = parseFloat(price);
    // Prüfe auf gültige Zahl
    if (isNaN(numericPrice)) {
        return "Invalid Price"; // oder eine andere passende Zeichenfolge
    }
    // Formatiere den Preis mit Punkt als Tausendertrennzeichen und Euro-Zeichen
    return numericPrice.toLocaleString('de-DE', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + '€';
}

function formatDate(dateString) {
    const date = new Date(dateString); // Konvertiere den Datumsstring in ein Date-Objekt
    if (isNaN(date)) {
        console.error(`Invalid date string: ${dateString}`);
        return 'Invalid Date'; // oder eine andere passende Zeichenfolge
    }
    // Optionen für die Datumsformatierung
    const options = { day: '2-digit', month: 'short', year: 'numeric' };
    // Formatiere das Datum
    const formattedDate = date.toLocaleDateString('en-EN', options);
    return formattedDate; // Gibt das formatierte Datum zurück
}

let notFoundVINs = []; // Array für nicht gefundene VINs
let processedVINs = new Set(); // Set to keep track of processed VINs
let allExtractedIds = []; // Array to store all extracted IDs

// Function to display the retrieved data on the page
function displayData(data) {
    console.log("Received data:", data);
    
    if (!data || !data.cars || !Array.isArray(data.cars)) {
        console.error("Invalid data format received:", data);
        return;
    }

    // Reset notFoundVINs for each displayData call
    notFoundVINs = [];
    
    const articleElements = document.querySelectorAll('article[data-id]');
    if (articleElements.length === 0) {
        console.error("No article elements found with data-id attribute");
        return;
    }

    console.log("Article elements found: ", articleElements);
    
    articleElements.forEach((article) => {
        try {
            const dataId = article.getAttribute('data-id');
            const vinFromElement = dataId.split('-')[0];
            const carData = data.cars.find(car => car.vin === vinFromElement);
            const dataContainer = article.querySelector('.result-federal-incentive');

            if (!dataContainer) {
                console.error(`No .result-federal-incentive element found for VIN ${vinFromElement}`);
                if (!notFoundVINs.includes(vinFromElement)) {
                    notFoundVINs.push(vinFromElement);
                }
                return;
            }

            const customDataDiv = document.createElement('div');
            customDataDiv.className = 'tf-data-container';
            customDataDiv.style.padding = 'var(--tds-size-3x)';

            // Erstelle zwei Spalten
            const column1 = document.createElement('div');
            column1.className = 'tf-data-column';

            const column2 = document.createElement('div');
            column2.className = 'tf-data-column';

            if (carData) {
                // Set background color based on days in stock
                if(carData.days_in_stock === 0) {
                    customDataDiv.style.backgroundColor = '#e9fcf5'; // New car color
                } else if(carData.days_in_stock >= 20) {
                    customDataDiv.style.backgroundColor = '#f6edf5'; // Older inventory color
                } else {
                    customDataDiv.style.backgroundColor = '#eff6f9'; // Default color
                }

                // Column 1 content
                column1.innerHTML += `<div><strong>VIN:</strong> ${carData.vin}</div>`;
                const formatted = formatDate(carData.factory_gated_date);
                column1.innerHTML += `<div><strong>` + chrome.i18n.getMessage('manufactory_date') + `:</strong> ${formatted}</div>`;
                const daysInStockValue = carData.days_in_stock === 0 ? "New" : carData.days_in_stock;
                column1.innerHTML += `<div><strong>` + chrome.i18n.getMessage('days_in_stock') + `:</strong> ${daysInStockValue}</div>`;
                const priceDifference = formatPrice(carData.price_difference);
                const priceTrend = carData.price_trend;
                column1.innerHTML += `<div><strong>` + chrome.i18n.getMessage('price_variation') + `:</strong> ${priceTrend}${priceDifference}</div>`;

                // Column 2 content
                column2.innerHTML += `<div><strong>` + chrome.i18n.getMessage('facility') + `:</strong>  ${carData.factory || 'N/A'}</div>`;
                if (carData.battery_capacity) {
                    column2.innerHTML += `<div><strong>` + chrome.i18n.getMessage('battery_capacity') + `:</strong> ${carData.battery_capacity} kWh</div>`;
                } else {
                    column2.innerHTML += `<div><strong>` + chrome.i18n.getMessage('battery_capacity') + `:</strong> ${chrome.i18n.getMessage('not_available')}</div>`;
                }                              
                if(carData.model === "my" || carData.model === "m3") {
                    const heatpumpStatus = carData.heatpump ? chrome.i18n.getMessage('yes') : chrome.i18n.getMessage('no');
                    column2.innerHTML += `<div><strong>` + chrome.i18n.getMessage('heatpump') + `:</strong> ${heatpumpStatus}</div>`;
                }
                const vehiclePhotos = carData.photos_count === 0 ? chrome.i18n.getMessage('no')  : chrome.i18n.getMessage('yes');
                column2.innerHTML += `<div><strong>` + chrome.i18n.getMessage('vehicle_photos') + `:</strong> ${vehiclePhotos}</div>`;
                const donation = chrome.i18n.getMessage('titledonatebutton');

            } else {
                // Handle missing car data
                customDataDiv.classList.add('tf-no-data');
                customDataDiv.style.backgroundColor = '#fff3f3'; // Leicht rötlicher Hintergrund für fehlende Daten
                
                // Einfache Anzeige für fehlende Daten
                column1.innerHTML = `
                    <div><strong>VIN:</strong> ${vinFromElement}</div>
                    <div><strong>Status:</strong>` + chrome.i18n.getMessage('status') + `</div>
                    <div><small>` + chrome.i18n.getMessage('take_a_moment') + `</small></div>
                `;
                
                // column2.innerHTML = `
                //     <div><small>` + chrome.i18n.getMessage('retrieving_data') + `</small></div>
                    
                // `;

                console.log(`No matching car data found for VIN ${vinFromElement}`);
                if (!notFoundVINs.includes(vinFromElement)) {
                    notFoundVINs.push(vinFromElement);
                }
            }

            // Füge die Spalten zum Container hinzu
            customDataDiv.appendChild(column1);
            customDataDiv.appendChild(column2);

            // Leere den Container und füge den neuen Inhalt hinzu
            dataContainer.innerHTML = '';
            dataContainer.appendChild(customDataDiv);
            
            // Mark this VIN as processed
            processedVINs.add(vinFromElement);

        } catch (error) {
            console.error(`Error processing article with VIN ${vinFromElement}:`, error);
        }
    });

    // Nach der Bearbeitung aller Artikel, überprüfe, ob nicht gefundene VINs vorhanden sind
    if (notFoundVINs.length > 0) {
        console.log("VINs without data, scheduling retry:", notFoundVINs);
        // Retry with exponential backoff
        setTimeout(() => {
            console.log("Retrying to fetch data for VINs:", notFoundVINs);
            chrome.runtime.sendMessage({ 
                type: 'EXTRACTED_IDS', 
                ids: notFoundVINs,
                isRetry: true 
            });
        }, 5000); // 5 Sekunden Wartezeit vor dem Retry
    }
}


// ######## STYLES ##########
// CSS-Stile definieren
const styles = `
    .tf-data-container {
        display: flex;
        justify-content: space-between; /* Verteilt die Spalten gleichmäßig aliceblue*/
        background-color: #eff6f9;
    }
    .tf-data-column {
        flex: 1; /* Jeder Spalte nimmt den gleichen Platz ein */
        padding: 0 10px; /* Seitenabstand für die Spalten */
    }
`;

// Stylesheet erstellen und hinzufügen
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);

// ######## CALLBACK ##########
// Refresh Content after new API cals
let track = 0;
let lastProcessedArticleCount = 0;
// let allExtractedIds = []; // New array to store all extracted IDs

// Function to handle DOM changes
const handleDOMChanges = (mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            const currentArticleCount = document.querySelectorAll('article.result.card').length;
            
            if (currentArticleCount !== lastProcessedArticleCount) {
                console.log('Content changed, re-extracting IDs');
                track++;

                // Call extractIds() for all articles
                const newIds = extractIds(0);
                
                // Merge new IDs with existing IDs, removing duplicates
                allExtractedIds = [...new Set([...allExtractedIds, ...newIds])];

                // Send all IDs to the background script
                chrome.runtime.sendMessage({ type: 'EXTRACTED_IDS', ids: allExtractedIds });

                lastProcessedArticleCount = currentArticleCount;

                // Trigger a re-display of data
                chrome.runtime.sendMessage({ type: 'REQUEST_CAR_DATA', ids: allExtractedIds });
            }
        }
    }

    // Check for aria-busy changes
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'aria-busy') {
            const isBusy = mutation.target.getAttribute('aria-busy') === 'true';
            if (!isBusy) {
                console.log("Filter change detected, re-extracting IDs");
                // Extract all IDs
                const newIds = extractIds(0);
                // Merge new IDs with existing IDs, removing duplicates
                allExtractedIds = [...new Set([...allExtractedIds, ...newIds])];
                chrome.runtime.sendMessage({ type: 'EXTRACTED_IDS', ids: allExtractedIds });
                chrome.runtime.sendMessage({ type: 'REQUEST_CAR_DATA', ids: allExtractedIds });
            }
        }
    }
};

// Initialize the Mutation Observer
const observer = new MutationObserver(handleDOMChanges);

// Select the node (element) you want to observe
const targetNode = document.querySelector('#iso-container > div > div.tds-loader.tds-loader--fullscreen');


// Configure the observer
const config = { attributes: true, childList: true, subtree: true };

// Start observing the document body
observer.observe(document.body, { attributes: true, childList: true, subtree: true });

// Start observing the target node for configured mutations
if (targetNode) {
    observer.observe(targetNode, config);
    manualExtractAndSend(); // Rufe die Funktion hier auf
} else {
    console.error('Target node not found');
}

// Modified extractIds function to handle partial extraction
function extractIds(startIndex = 0) {
    console.log('extractIds() from Content.js');
    const articles = document.querySelectorAll('article.result.card');
    console.log("articles: ", articles);
    const ids = Array.from(articles).slice(startIndex).map(article => {
        const dataId = article.getAttribute('data-id');
        console.log("dataId: " + dataId.split('-')[0]);
        return dataId.split('-')[0];
    });

    return ids;
}

// Add this function to manually trigger data extraction and sending
function manualExtractAndSend() {
    const newIds = extractIds(0);
    allExtractedIds = [...new Set([...allExtractedIds, ...newIds])];
    chrome.runtime.sendMessage({ type: 'EXTRACTED_IDS', ids: allExtractedIds });
    console.log("Manually extracted and sent all IDs:", allExtractedIds);
}