# Chrome Extension User Guide

## Installation

### From Source (Developer Mode)

1. **Open Chrome Extensions Page**
   - Navigate to `chrome://extensions/`
   - Or: Menu → More Tools → Extensions

2. **Enable Developer Mode**
   - Toggle "Developer mode" in the top right

3. **Load Extension**
   - Click "Load unpacked"
   - Select the `chrome-extension` folder
   - Extension should appear in your toolbar

4. **Pin Extension** (Optional)
   - Click the puzzle icon in Chrome toolbar
   - Find "Job Scam Detector"
   - Click the pin icon

---

## Usage

### Analyzing a Job Page

1. **Navigate to any job posting** (LinkedIn, Indeed, etc.)

2. **Click the extension icon** in your toolbar

3. **Click "Analyze This Page"**
   - Extension extracts text from the page
   - Sends to API for analysis
   - Results appear in popup

4. **Review Results:**
   - 🟢 Green (70-100): Likely safe
   - 🟡 Yellow (40-69): Be cautious
   - 🔴 Red (0-39): High risk

### Understanding Results

**Trust Score**: 0-100 rating
- Higher = Safer
- Based on ML model + rules

**Warning Signs**: List of detected scam indicators
- Example: "Requests upfront payment"
- Example: "Unrealistic salary claims"

**Explanation**: Why the score was given

**Buttons:**
- "📖 Why This Score?" - Shows full recommendations
- "🚩 Report as Scam" - Submit feedback

---

## Supported Job Sites

The extension works on ANY website, including:

✅ **Major Job Boards:**
- LinkedIn
- Indeed
- Glassdoor
- Monster
- ZipRecruiter
- CareerBuilder

✅ **Company Career Pages:**
- Google Careers
- Microsoft Jobs
- Any company website

✅ **Email/Messages:**
- Copy job text
- Paste into web UI for analysis

✅ **Social Media:**
- Facebook job groups
- Reddit posts
- Twitter DMs

---

## Troubleshooting

### "API Error: Network request failed"

**Problem**: Can't reach the backend server

**Solutions:**
1. Make sure the API is running:
   ```bash
   python backend/main.py
   ```

2. Check API is at `http://localhost:8000`

3. Try the health check:
   ```bash
   curl http://localhost:8000/health
   ```

### "Not enough text found on this page"

**Problem**: Page doesn't have enough content

**Solutions:**
1. Make sure you're on the full job posting page
2. Some sites load content dynamically - wait for page to fully load
3. Try refreshing the page
4. Copy text manually and use web UI instead

### Extension Not Appearing

**Problem**: Extension icon not visible

**Solutions:**
1. Check `chrome://extensions/` - should show "Job Scam Detector"
2. Make sure it's enabled (toggle should be blue)
3. Try reloading the extension
4. Pin it to toolbar (puzzle icon → pin)

### Analysis Takes Too Long

**Problem**: Stuck on "Analyzing..."

**Solutions:**
1. Check if API server is running
2. Page might have too much text - extraction takes time
3. Refresh popup and try again
4. Check browser console for errors (F12 → Console)

---

## Privacy & Security

### What Data Is Collected?

**We DO NOT:**
- ❌ Store your browsing history
- ❌ Track which sites you visit
- ❌ Send personal information
- ❌ Share data with third parties

**We DO:**
- ✅ Send job posting text to local API (localhost only)
- ✅ Store last analysis result locally in browser
- ✅ Allow you to report scams (optional)

### Permissions Explained

**activeTab**: Read content from current tab when you click the icon
- Used to: Extract job posting text for analysis
- Only activates: When you click "Analyze This Page"

**storage**: Store your last analysis result
- Used to: Cache results so you can review them
- Stored: Only in your browser (not sent anywhere)

---

## Tips for Best Results

### ✅ Do:
- Use on complete job descriptions
- Check the full posting, not just snippets
- Read the explanation, not just the score
- Verify independently even if score is high
- Report incorrect predictions

### ❌ Don't:
- Trust the score 100% - it's an AI assistant
- Use as only verification method
- Ignore common sense indicators
- Share sensitive info before verifying company

---

## Advanced Usage

### Keyboard Shortcuts
You can add custom shortcuts:
1. Go to `chrome://extensions/shortcuts`
2. Find "Job Scam Detector"
3. Set a shortcut (e.g., `Ctrl+Shift+S`)

### Batch Analysis
For multiple jobs:
1. Copy each job text
2. Use the Web UI (`http://localhost:8501`)
3. Paste and analyze multiple times

### Integration with Other Tools
The extension uses the API, so you can:
- Build custom integrations
- Use API directly from other apps
- Create automated workflows

---

## Updating the Extension

When new versions are released:

1. **Pull latest code**
   ```bash
   git pull origin main
   ```

2. **Go to** `chrome://extensions/`

3. **Click the reload icon** on "Job Scam Detector"

4. **Refresh any open tabs**

---

## Uninstalling

To remove the extension:

1. Go to `chrome://extensions/`
2. Find "Job Scam Detector"
3. Click "Remove"
4. Confirm removal

All stored data will be deleted automatically.

---

## Known Limitations

1. **Requires API Server**: Extension needs backend running
2. **English Only**: Currently supports English text only
3. **Text-Only**: Can't analyze images or videos
4. **Dynamic Content**: Some sites load content via JavaScript - may miss text
5. **Rate Limiting**: No built-in rate limiting (analyze responsibly)

---

## Feature Requests

Want a new feature? Please:
1. Check existing issues on GitHub
2. Open a new issue with your idea
3. Describe the use case
4. We'll review and prioritize

---

## Support

Need help?
- 📖 Check this guide first
- 🐛 Report bugs on GitHub Issues
- 💬 Ask questions in GitHub Discussions
- 📧 Contact maintainers

---

## Example Workflow

**Scenario**: Job seeker reviewing LinkedIn posting

1. Find job on LinkedIn
2. Click extension icon
3. Click "Analyze This Page"
4. See: 🟡 Score 45 - "Suspicious"
5. Review warnings:
   - "WhatsApp-only communication"
   - "Unrealistic salary claims"
6. Read advice:
   - "Research company on LinkedIn"
   - "Verify official website"
7. Decide: Investigate further before applying
8. Report if confirmed scam

**Result**: Protected from potential scam!

---

Stay safe while job hunting! 🛡️
