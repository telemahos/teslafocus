// Constants
const API_URL_PATTERN = "https://www.tesla.com/inventory/api/v4/inventory-results?query=*";
const REQUEST_STORAGE_KEY = 'apiRequests';
const ID_STORAGE_KEY = 'extractedIds'; 
const API_ENDPOINT = 'http://127.0.0.1:8000/api/cars/ids/';
// const API_ENDPOINT = 'http://127.0.0.1:8000/ids/';
// const API_ENDPOINT = 'http://93.127.202.194:8000/ids/';

// Cache for managing request data
let requestCache = new Map();

// Helper function to handle storage operations
async function updateStorage(key, data) {
    try {
        await chrome.storage.local.set({ [key]: data });
        console.log(`Storage updated for key: ${key}`);
    } catch (error) {
        console.error(`Error updating storage for key ${key}:`, error);
    }
}

// Helper function to fetch data from the API
async function fetchFromAPI(ids, maxRetries = 3) {
    let attempt = 0;
    
    while (attempt < maxRetries) {
        try {
            console.log(`Attempt ${attempt + 1} to fetch data for ${ids.length} VINs`);
            
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ ids: ids })
            });

            if (response.status === 500) {
                console.log(`Server error (500) on attempt ${attempt + 1}`);
                // Wait before retry with exponential backoff
                await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
                attempt++;
                continue;
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log(`Successfully fetched data for ${ids.length} VINs`);
            return data;

        } catch (error) {
            console.error(`API fetch error on attempt ${attempt + 1}:`, error);
            
            if (attempt === maxRetries - 1) {
                // On last attempt, return partial data or empty result
                return {
                    cars: [],
                    error: error.message,
                    failedIds: ids
                };
            }
            
            // Wait before retry with exponential backoff
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
            attempt++;
        }
    }

    return {
        cars: [],
        error: 'Max retries reached',
        failedIds: ids
    };
}

// Helper function to send message to active tab
// In Background.js, modifizieren Sie die sendMessageToActiveTab Funktion:
async function sendMessageToActiveTab(message) {
    try {
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        console.log('Found tabs:', tabs); // Debug-Log
        
        if (!tabs || tabs.length === 0) {
            throw new Error('No active tab found');
        }

        const activeTab = tabs[0];
        console.log('Active tab:', activeTab); // Debug-Log

        // Weniger strenge URL-Überprüfung
        if (!activeTab?.id) {
            throw new Error('No valid tab ID found');
        }

        // Optional: Überprüfen Sie die URL weniger streng
        if (!activeTab.url?.includes('tesla.com')) {
            console.warn('Warning: Active tab is not a Tesla.com page');
            // Trotzdem fortfahren
        }

        return await chrome.tabs.sendMessage(activeTab.id, message);
    } catch (error) {
        console.error('Error sending message to tab:', error);
        // Fügen Sie eine Verzögerung hinzu und versuchen Sie es erneut
        await new Promise(resolve => setTimeout(resolve, 1000));
        return await chrome.tabs.sendMessage(tabs[0].id, message);
    }
}

// Main message handler
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    const handleMessage = async () => {
        try {
            switch (message.type) {
                case 'EXTRACTED_IDS':
                    if (!Array.isArray(message.ids) || message.ids.length === 0) {
                        return { success: false, error: 'No valid IDs to process' };
                    }

                    // Split IDs into smaller chunks to avoid overwhelming the server
                    const chunkSize = 10; // Adjust based on your server's capacity
                    const chunks = [];
                    for (let i = 0; i < message.ids.length; i += chunkSize) {
                        chunks.push(message.ids.slice(i, i + chunkSize));
                    }

                    let allData = { cars: [] };
                    let failedIds = [];

                    for (const chunk of chunks) {
                        const result = await fetchFromAPI(chunk);
                        if (result.cars) {
                            allData.cars = [...allData.cars, ...result.cars];
                        }
                        if (result.failedIds) {
                            failedIds = [...failedIds, ...result.failedIds];
                        }
                    }

                    if (allData.cars.length > 0) {
                        await updateStorage(REQUEST_STORAGE_KEY, allData);
                        
                        await sendMessageToActiveTab({
                            type: 'RETURNED_CAR_DATA',
                            data: allData,
                            failedIds: failedIds
                        });

                        return { 
                            success: true, 
                            data: allData,
                            failedIds: failedIds
                        };
                    } else {
                        return { 
                            success: false, 
                            error: 'No data retrieved',
                            failedIds: failedIds
                        };
                    }

                case 'REQUEST_CAR_DATA':
                    await fetchCarData(message.ids);
                    return { success: true };

                default:
                    throw new Error(`Unknown message type: ${message.type}`);
            }
        } catch (error) {
            console.error('Message handling error:', error.message);
            return { success: false, error: error.message };
        }
    };

    // Execute async handler and send response
    handleMessage().then(sendResponse);
    return true; // Keep message channel open for async response
});

// Web request monitoring
chrome.webRequest.onBeforeRequest.addListener(
    async (details) => {
        try {
            const requests = (await chrome.storage.local.get(REQUEST_STORAGE_KEY))[REQUEST_STORAGE_KEY] || {};
            
            if (!requests[details.url]) {
                requests[details.url] = {
                    url: details.url,
                    timestamp: Date.now(),
                    data: []
                };
                await updateStorage(REQUEST_STORAGE_KEY, requests);
            }
        } catch (error) {
            console.error('Error in onBeforeRequest:', error);
        }
        return { cancel: false };
    },
    { urls: [API_URL_PATTERN] }
);

// Response capture
chrome.webRequest.onCompleted.addListener(
    async (details) => {
        try {
            if (details.statusCode === 200 && details.url.includes(API_URL_PATTERN)) {
                const response = await fetch(details.url);
                const data = await response.json();
                
                const requests = (await chrome.storage.local.get(REQUEST_STORAGE_KEY))[REQUEST_STORAGE_KEY] || {};
                
                if (requests[details.url]) {
                    requests[details.url].data = data;
                    await updateStorage(REQUEST_STORAGE_KEY, requests);
                }

                // Cache the response
                requestCache.set(details.url, {
                    timestamp: Date.now(),
                    data: data
                });
            }
        } catch (error) {
            console.error('Error in onCompleted:', error);
        }
    },
    { urls: [API_URL_PATTERN] }
);

// Helper function to fetch car data
async function fetchCarData(ids) {
    try {
        console.log('Received IDs:', ids); // Debug-Log

        // Verbesserte Validierung
        if (!ids) {
            console.warn('No IDs provided, waiting for data...');
            return null;
        }

        if (!Array.isArray(ids)) {
            ids = [ids]; // Konvertiere einzelne ID in Array
        }

        if (ids.length === 0) {
            console.warn('Empty IDs array, waiting for data...');
            return null;
        }

        const data = await fetchFromAPI(ids);
        
        if (data) {
            try {
                await sendMessageToActiveTab({
                    type: 'RETURNED_CAR_DATA',
                    data: data
                });
            } catch (sendError) {
                console.warn('Could not send message to tab, will retry:', sendError);
                // Optional: Implementieren Sie hier eine Retry-Logik
            }
        }

        return data;
    } catch (error) {
        console.error('Error fetching car data:', error);
        return null;
    }
}

// Clean up cache periodically (every 30 minutes)
setInterval(() => {
    const now = Date.now();
    for (const [url, data] of requestCache.entries()) {
        if (now - data.timestamp > 30 * 60 * 1000) { // 30 minutes
            requestCache.delete(url);
        }
    }
}, 30 * 60 * 1000); // Run every 30 minutes