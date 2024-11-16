const API_URL_PATTERN = "https://www.tesla.com/inventory/api/v4/inventory-results?query=*";
const REQUEST_STORAGE_KEY = 'apiRequests';
const ID_STORAGE_KEY = 'extractedIds';
const REQUEST_STORAGE_DATA = '';

// Funktion, die die Daten der IDs vom Server anfragt
function fetchCarData(ids) {
    fetch(`https://example.com/api/cars?ids=${ids.join(',')}`)
        .then(response => response.json())
        .then(carData => {
            console.log('Car data fetched:', carData);
            chrome.storage.local.set({ [ID_STORAGE_KEY]: carData });
        })
        .catch(error => console.error('Error fetching car data:', error));
}

// Listener für Nachrichten vom Content Script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message received in background:", message);
    if (message.type === 'EXTRACTED_IDS') {
        const ids = message.ids;

        fetch('http://127.0.0.1:8000/ids/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ids: ids }),
        })
        .then(response => response.json())
        .then(data => {
            chrome.storage.local.set({ [REQUEST_STORAGE_DATA]: data }, function() {
                console.log('Data appended for:', data);
            });

            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) { 
                if (tabs.length > 0 && tabs[0].id && tabs[0].url.includes('tesla.com')) {
                    chrome.tabs.sendMessage(tabs[0].id, {type: 'RETURNED_CAR_DATA', data: data});
                } else {
                    console.error('No active tab found or tab id is undefined.');
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            sendResponse({ success: false, error: error.message });
        });
        
        // Richtig: Die Funktion wird aufgerufen, nachdem die IDs extrahiert wurden
        fetchCarData(ids);
        return true;  // Send response asynchronously
    }
    else if (message.type === 'REQUEST_CAR_DATA') {
        fetchCarData(message.ids);
    }
});

// Store metadata of the request
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        chrome.storage.local.get([REQUEST_STORAGE_KEY], function(result) {
            const requests = result[REQUEST_STORAGE_KEY] || {};
            if (!requests[details.url]) {
                requests[details.url] = {
                    url: details.url,
                    timestamp: Date.now(),
                    data: []
                };
                chrome.storage.local.set({ [REQUEST_STORAGE_KEY]: requests }, function() {
                    console.log('Request metadata saved:', details.url);
                });
            }
        });
        return { cancel: false };
    },
    { urls: [API_URL_PATTERN] }
);

// Capture the response body
chrome.webRequest.onCompleted.addListener(
    function(details) {
        if (details.statusCode === 200 && details.url.includes("inventory-results")) {
            fetch(details.url)
                .then(response => response.json())
                .then(data => {
                    chrome.storage.local.get([REQUEST_STORAGE_KEY], function(result) {
                        const requests = result[REQUEST_STORAGE_KEY] || {};
                        if (requests[details.url]) {
                            requests[details.url].data = data;
                            chrome.storage.local.set({ [REQUEST_STORAGE_KEY]: requests }, function() {
                                console.log('Data for request updated:', details.url);
                            });
                        }
                    });
                })
                .catch(error => {
                    console.error('Error fetching API response:', error);
                });
        }
    },
    { urls: [API_URL_PATTERN] }
);
