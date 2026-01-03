// Chrome Extension Popup Script
const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const explainBtn = document.getElementById('explain-btn');
    const reportBtn = document.getElementById('report-btn');
    
    // Analyze button click
    analyzeBtn.addEventListener('click', analyzeCurrentPage);
    
    // Explain button click
    explainBtn.addEventListener('click', showFullExplanation);
    
    // Report button click
    reportBtn.addEventListener('click', reportScam);
});

async function analyzeCurrentPage() {
    showLoading();
    
    try {
        // Get current tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        // Extract text from page
        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: extractPageText
        });
        
        const pageText = results[0].result;
        
        if (!pageText || pageText.trim().length < 50) {
            showError('Not enough text found on this page. Try a different page or paste text manually.');
            return;
        }
        
        // Call API
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: pageText,
                url: tab.url
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        displayResults(result);
        
        // Save to storage for later
        chrome.storage.local.set({ 
            lastAnalysis: result,
            lastUrl: tab.url,
            lastText: pageText
        });
        
    } catch (error) {
        showError(`Analysis failed: ${error.message}. Make sure the API server is running on ${API_URL}`);
    }
}

function extractPageText() {
    // Extract visible text from page
    const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, td, span, div');
    let text = '';
    
    textElements.forEach(el => {
        const elementText = el.innerText || el.textContent;
        if (elementText && elementText.trim()) {
            text += elementText.trim() + ' ';
        }
    });
    
    // Limit to first 5000 characters
    return text.substring(0, 5000);
}

function displayResults(result) {
    hideLoading();
    hideError();
    document.getElementById('initial').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    
    // Status banner
    const statusDiv = document.getElementById('status');
    const prediction = result.prediction;
    
    if (prediction === 'High Risk Scam') {
        statusDiv.className = 'status danger';
        statusDiv.textContent = '🚨 ' + prediction;
    } else if (prediction === 'Suspicious') {
        statusDiv.className = 'status warning';
        statusDiv.textContent = '⚠️ ' + prediction;
    } else {
        statusDiv.className = 'status safe';
        statusDiv.textContent = '✅ ' + prediction;
    }
    
    // Trust score
    const scoreDiv = document.getElementById('score');
    const score = result.score;
    
    if (score >= 70) {
        scoreDiv.className = 'score safe';
        scoreDiv.textContent = '🟢 ' + score;
    } else if (score >= 40) {
        scoreDiv.className = 'score warning';
        scoreDiv.textContent = '🟡 ' + score;
    } else {
        scoreDiv.className = 'score danger';
        scoreDiv.textContent = '🔴 ' + score;
    }
    
    // Explanation
    document.getElementById('explanation').textContent = result.explanation;
    
    // Flags
    if (result.flags && result.flags.length > 0) {
        document.getElementById('flags-section').style.display = 'block';
        const flagsList = document.getElementById('flags');
        flagsList.innerHTML = '';
        
        result.flags.slice(0, 5).forEach(flag => {
            const li = document.createElement('li');
            li.textContent = flag;
            flagsList.appendChild(li);
        });
    }
    
    // Show report button if suspicious
    if (score < 70) {
        document.getElementById('report-btn').style.display = 'block';
    }
}

function showFullExplanation() {
    chrome.storage.local.get(['lastAnalysis'], function(data) {
        if (data.lastAnalysis) {
            const advice = data.lastAnalysis.advice.join('\n\n');
            alert('Safety Recommendations:\n\n' + advice);
        }
    });
}

async function reportScam() {
    try {
        const data = await chrome.storage.local.get(['lastText', 'lastUrl']);
        
        const response = await fetch(`${API_URL}/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: data.lastText,
                url: data.lastUrl,
                user_feedback: 'Reported from extension'
            })
        });
        
        if (response.ok) {
            alert('Thank you for reporting! This helps improve our detection system.');
        }
    } catch (error) {
        alert('Failed to submit report: ' + error.message);
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('initial').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    hideError();
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    document.getElementById('initial').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    hideLoading();
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}
