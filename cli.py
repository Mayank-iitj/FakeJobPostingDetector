"""
Quick CLI tool for testing job scam detection
Usage: python cli.py "Job posting text here"
"""
import sys
import argparse
import requests
import json
from typing import Dict


def analyze_job(text: str, url: str = None, api_url: str = "http://localhost:8000") -> Dict:
    """Call API to analyze job posting"""
    try:
        response = requests.post(
            f"{api_url}/analyze",
            json={"text": text, "url": url},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        print(f"   Make sure the API server is running: python backend/main.py")
        sys.exit(1)


def display_result(result: Dict):
    """Display analysis result in terminal"""
    # Header
    print("\n" + "="*60)
    print("JOB SCAM ANALYSIS RESULT")
    print("="*60 + "\n")
    
    # Trust Score
    score = result['score']
    if score >= 70:
        emoji = "🟢"
        color = "\033[92m"  # Green
    elif score >= 40:
        emoji = "🟡"
        color = "\033[93m"  # Yellow
    else:
        emoji = "🔴"
        color = "\033[91m"  # Red
    
    print(f"{color}Trust Score: {emoji} {score}/100\033[0m")
    
    # Prediction
    prediction = result['prediction']
    print(f"Classification: {prediction}")
    print(f"Confidence: {int(result['confidence'] * 100)}%\n")
    
    # Explanation
    print("Explanation:")
    print(f"  {result['explanation']}\n")
    
    # Flags
    if result['flags']:
        print("⚠️  Warning Signs Detected:")
        for i, flag in enumerate(result['flags'], 1):
            print(f"  {i}. {flag}")
        print()
    
    # Highlighted Phrases
    if result['highlighted_phrases']:
        print("🔍 Risky Phrases Found:")
        for phrase in result['highlighted_phrases'][:5]:
            risk_emoji = "🔴" if phrase['risk_level'] == "high" else "🟡" if phrase['risk_level'] == "medium" else "⚪"
            print(f'  {risk_emoji} "{phrase["text"]}" - {phrase["reason"]}')
        print()
    
    # Advice
    print("💡 Safety Recommendations:")
    for advice in result['advice']:
        # Remove emojis from advice for cleaner terminal output
        clean_advice = advice.encode('ascii', 'ignore').decode('ascii').strip()
        print(f"  • {clean_advice}")
    
    print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Job Scam Detector CLI - Analyze job postings for scam indicators"
    )
    
    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        help="Job posting text to analyze"
    )
    
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Read job text from file"
    )
    
    parser.add_argument(
        "-u", "--url",
        type=str,
        help="Job posting URL (optional)"
    )
    
    parser.add_argument(
        "--api",
        type=str,
        default="http://localhost:8000",
        help="API endpoint URL (default: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response"
    )
    
    args = parser.parse_args()
    
    # Get text from argument or file
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        print("Error: Please provide text or use --file option")
        parser.print_help()
        sys.exit(1)
    
    if not text.strip():
        print("❌ Error: Empty text provided")
        sys.exit(1)
    
    # Analyze
    print("🔍 Analyzing job posting...")
    result = analyze_job(text, args.url, args.api)
    
    # Display result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        display_result(result)


if __name__ == "__main__":
    main()
