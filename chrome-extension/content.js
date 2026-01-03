// Content Script - Runs on all web pages
// Highlights risky phrases directly on the page

let analysisResult = null;

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'highlight') {
        highlightRiskyPhrases(request.phrases);
        sendResponse({ success: true });
    }
});

function highlightRiskyPhrases(phrases) {
    if (!phrases || phrases.length === 0) return;
    
    // Create highlight styles
    injectHighlightStyles();
    
    // Get all text nodes
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    // Highlight each phrase
    phrases.forEach(phrase => {
        const searchText = phrase.text.toLowerCase();
        const riskLevel = phrase.risk_level;
        
        textNodes.forEach(textNode => {
            const text = textNode.textContent;
            const lowerText = text.toLowerCase();
            const index = lowerText.indexOf(searchText);
            
            if (index !== -1) {
                highlightText(textNode, index, searchText.length, riskLevel);
            }
        });
    });
}

function highlightText(textNode, start, length, riskLevel) {
    const text = textNode.textContent;
    const parent = textNode.parentNode;
    
    // Create highlighted span
    const span = document.createElement('span');
    span.className = `job-scam-highlight job-scam-${riskLevel}`;
    span.textContent = text.substring(start, start + length);
    span.title = `Scam indicator (${riskLevel} risk)`;
    
    // Split text node
    const before = document.createTextNode(text.substring(0, start));
    const after = document.createTextNode(text.substring(start + length));
    
    parent.insertBefore(before, textNode);
    parent.insertBefore(span, textNode);
    parent.insertBefore(after, textNode);
    parent.removeChild(textNode);
}

function injectHighlightStyles() {
    if (document.getElementById('job-scam-detector-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'job-scam-detector-styles';
    style.textContent = `
        .job-scam-highlight {
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: bold;
            cursor: help;
        }
        
        .job-scam-high {
            background-color: rgba(220, 53, 69, 0.3);
            border-bottom: 2px solid #dc3545;
        }
        
        .job-scam-medium {
            background-color: rgba(255, 193, 7, 0.3);
            border-bottom: 2px solid #ffc107;
        }
        
        .job-scam-low {
            background-color: rgba(108, 117, 125, 0.2);
            border-bottom: 1px solid #6c757d;
        }
    `;
    
    document.head.appendChild(style);
}
