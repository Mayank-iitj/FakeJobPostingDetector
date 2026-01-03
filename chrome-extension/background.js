// Background Service Worker
// Handles extension lifecycle events

chrome.runtime.onInstalled.addListener(() => {
    console.log('Job Scam Detector extension installed');
});

// Handle messages from content scripts or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyze') {
        // Could add background analysis logic here
        sendResponse({ status: 'received' });
    }
});
