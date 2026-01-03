# Sample job postings for testing

## Legitimate Job Example 1
Software Engineer at Microsoft
We are seeking a talented Software Engineer to join our Cloud Services team.

Requirements:
- Bachelor's degree in Computer Science or related field
- 3+ years of experience with Python, Java, or C#
- Experience with cloud platforms (Azure, AWS, GCP)
- Strong problem-solving and communication skills

Responsibilities:
- Design and develop scalable cloud services
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews

We offer competitive salary, comprehensive benefits, stock options, and a great work environment.

Apply at: careers.microsoft.com

---

## Legitimate Job Example 2
Marketing Manager - Remote Position
ABC Tech Inc. is hiring a Marketing Manager to lead our digital marketing initiatives.

Qualifications:
- 5+ years in digital marketing
- MBA or equivalent experience
- Proven track record in B2B marketing
- Experience with marketing automation tools

Compensation: $80,000 - $100,000 annually, plus benefits

Contact: hr@abctech.com
Company website: www.abctech.com

---

## SCAM Example 1
🚨 URGENT HIRING - LIMITED SLOTS!!! 🚨

Earn $500 PER DAY working from home!!!
NO EXPERIENCE NEEDED!
NO INTERVIEW REQUIRED!
GUARANTEED INCOME!

Just pay a small registration fee of $99 to get started!
This is a LIMITED TIME offer - only 10 positions available!

Work your own hours!
Be your own boss!
Make money while you sleep!

Contact us on WhatsApp ONLY: +1-555-0123
ACT NOW before slots fill up!!!

---

## SCAM Example 2
Personal Assistant Needed - URGENT

We need someone to help process payments and handle packages.

Requirements:
- Must have bank account
- Must be available to receive packages at home
- Must be able to purchase gift cards

Pay: $300/day GUARANTEED

Training fee: $75 (refunded after first week)
Payment processing fee: $50

Contact via Telegram: @fastmoney123

No interview needed - start today!

---

## SCAM Example 3
Cryptocurrency Trading Assistant

Make $10,000+ monthly with our proven Bitcoin trading system!

No experience required - we provide training!
Work from anywhere in the world!
Guaranteed returns!

Investment required: $199 startup package

Our system has a 99% success rate!
Don't miss this life-changing opportunity!

WhatsApp: +1-555-SCAM
Email: easymoney@gmail.com

HURRY - Limited enrollment period!

---

## Suspicious Example (Borderline)
Data Entry Clerk - Work From Home

Looking for data entry specialists to work remotely.

Requirements:
- Computer and internet connection
- Basic typing skills
- No experience necessary

Pay: $150 per day

Note: There is a small admin fee of $35 for background check and software setup.

Contact: jobs@workonline.tk

Immediate start available.

---

## How to Use These Examples

### Testing the Web UI:
1. Start the API: `python backend/main.py`
2. Start the UI: `streamlit run frontend/streamlit_app.py`
3. Copy and paste examples into the text area
4. Click "Analyze Job Posting"

### Testing the CLI:
```bash
# Direct text
python cli.py "URGENT HIRING! Pay $99 fee to start!"

# From file
echo "Your job text" > test_job.txt
python cli.py --file test_job.txt
```

### Testing the API:
```bash
# Using curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Your job posting text here"}'
```

### Expected Results:

**Legitimate jobs should get:**
- Trust Score: 70-95
- Prediction: "Likely Legitimate"
- Few or no warning flags

**Scam jobs should get:**
- Trust Score: 0-40
- Prediction: "High Risk Scam"
- Multiple warning flags

**Suspicious jobs should get:**
- Trust Score: 40-70
- Prediction: "Suspicious"
- Some warning flags
