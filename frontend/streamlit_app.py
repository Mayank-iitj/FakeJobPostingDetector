"""
Streamlit Web UI for Job Scam Detection
User-friendly interface for testing job postings
Works standalone or with API backend
"""
import streamlit as st
import requests
import json
import sys
import os
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page configuration
st.set_page_config(
    page_title="Job Scam Detector",
    page_icon="🔍",
    layout="wide"
)

# API Configuration - check environment variable for deployment
API_URL = os.getenv("API_URL", "http://localhost:8000")
USE_STANDALONE = os.getenv("STANDALONE_MODE", "true").lower() == "true"

# Import standalone detector if available
try:
    from backend.models.detector import JobScamDetector
    from backend.utils.text_processor import TextProcessor
    STANDALONE_AVAILABLE = True
except ImportError:
    STANDALONE_AVAILABLE = False


def analyze_job_api(text: str, url: str = None) -> Optional[Dict]:
    """Call API to analyze job posting"""
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"text": text, "url": url},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def analyze_job_standalone(text: str, url: str = None) -> Optional[Dict]:
    """Analyze job posting using standalone detector"""
    try:
        if 'detector' not in st.session_state:
            st.session_state.detector = JobScamDetector()
            st.session_state.text_processor = TextProcessor()
        
        detector = st.session_state.detector
        text_processor = st.session_state.text_processor
        
        cleaned_text = text_processor.clean_text(text)
        result = detector.analyze(cleaned_text, url)
        return result
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None


def analyze_job(text: str, url: str = None) -> Optional[Dict]:
    """Analyze job posting - tries API first, falls back to standalone"""
    # Try API first if not in forced standalone mode
    if not USE_STANDALONE:
        result = analyze_job_api(text, url)
        if result:
            return result
    
    # Use standalone mode if API unavailable or forced
    if STANDALONE_AVAILABLE:
        return analyze_job_standalone(text, url)
    
    st.error(
        "❌ Unable to analyze job posting.\n\n"
        "API is unavailable and standalone mode is not configured.\n\n"
        "Please ensure backend dependencies are installed or start the API server."
    )
    return None


def report_scam(text: str, url: str = None, feedback: str = None):
    """Report a scam job posting"""
    try:
        response = requests.post(
            f"{API_URL}/report",
            json={"text": text, "url": url, "user_feedback": feedback},
            timeout=5
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Report Error: {str(e)}")
        return None


def get_score_color(score: int) -> str:
    """Get color based on trust score"""
    if score >= 70:
        return "🟢"
    elif score >= 40:
        return "🟡"
    else:
        return "🔴"


def main():
    """Main Streamlit app"""
    
    # Header
    st.title("🔍 Job Scam Detector")
    st.markdown("**AI-powered system to detect fake and scam job postings**")
    
    # Show mode indicator
    mode = "Standalone Mode" if (USE_STANDALONE or not API_URL.startswith("http://localhost")) else "API Mode"
    mode_color = "🟢" if STANDALONE_AVAILABLE or mode == "API Mode" else "🟡"
    st.caption(f"{mode_color} Running in: {mode}")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This tool uses AI and rule-based analysis to identify "
            "potential job scams. Enter a job posting to get:\n\n"
            "✅ Trust Score (0-100)\n\n"
            "⚠️ Scam Indicators\n\n"
            "💡 Safety Recommendations"
        )
        
        st.header("⚠️ Disclaimer")
        st.warning(
            "This is an AI assistant only. Always verify job postings "
            "independently. Never pay fees or share sensitive information "
            "before thorough verification."
        )
        
        st.header("Examples")
        if st.button("Load Legitimate Example"):
            st.session_state.example_text = (
                "Software Engineer position at TechCorp Inc.\n\n"
                "Requirements:\n"
                "- 3+ years Python/Java experience\n"
                "- BS in Computer Science\n"
                "- Strong problem-solving skills\n\n"
                "We offer competitive salary, health benefits, and remote work options.\n"
                "Apply at: careers@techcorp.com"
            )
        
        if st.button("Load Scam Example"):
            st.session_state.example_text = (
                "🚨 URGENT HIRING!!! 🚨\n\n"
                "Earn $500 PER DAY working from home!!!\n"
                "NO EXPERIENCE NEEDED! NO INTERVIEW!\n\n"
                "Just pay small $99 registration fee to start!\n"
                "Limited slots available - ACT NOW!\n\n"
                "Contact WhatsApp ONLY: +1-555-0123\n"
                "GUARANTEED INCOME! Don't miss this opportunity!!!"
            )
    
    # Main content area
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("📝 Enter Job Posting")
        
        # Text input
        job_text = st.text_area(
            "Paste job posting text here:",
            value=st.session_state.get('example_text', ''),
            height=300,
            placeholder="Paste the job description, email, or message here..."
        )
        
        # URL input (optional)
        job_url = st.text_input(
            "Job posting URL (optional):",
            placeholder="https://example.com/jobs/12345"
        )
        
        # Analyze button
        analyze_button = st.button("🔍 Analyze Job Posting", type="primary", use_container_width=True)
    
    with col2:
        st.header("📊 Analysis Results")
        results_container = st.container()
    
    # Process analysis
    if analyze_button and job_text.strip():
        with st.spinner("Analyzing job posting..."):
            result = analyze_job(job_text, job_url if job_url else None)
        
        if result:
            with results_container:
                # Trust Score
                score_emoji = get_score_color(result['score'])
                st.metric(
                    label="Trust Score",
                    value=f"{score_emoji} {result['score']}/100"
                )
                
                # Prediction
                prediction = result['prediction']
                if prediction == "High Risk Scam":
                    st.error(f"🚨 **{prediction}**")
                elif prediction == "Suspicious":
                    st.warning(f"⚠️ **{prediction}**")
                else:
                    st.success(f"✅ **{prediction}**")
                
                # Confidence
                confidence_pct = int(result['confidence'] * 100)
                st.progress(result['confidence'])
                st.caption(f"Confidence: {confidence_pct}%")
                
                st.markdown("---")
                
                # Explanation
                st.subheader("📖 Explanation")
                st.write(result['explanation'])
                
                # Scam Indicators
                if result['flags']:
                    st.subheader("⚠️ Scam Indicators Found")
                    for flag in result['flags']:
                        st.markdown(f"• {flag}")
                
                # Highlighted Phrases
                if result['highlighted_phrases']:
                    st.subheader("🔍 Risky Phrases Detected")
                    for phrase in result['highlighted_phrases'][:5]:
                        risk_icon = "🔴" if phrase['risk_level'] == "high" else "🟡" if phrase['risk_level'] == "medium" else "⚪"
                        st.markdown(f"{risk_icon} **\"{phrase['text']}\"** - {phrase['reason']}")
                
                st.markdown("---")
                
                # Safety Advice
                st.subheader("💡 Safety Recommendations")
                for advice in result['advice']:
                    st.markdown(f"{advice}")
                
                st.markdown("---")
                
                # Report option
                if result['score'] < 70:
                    st.subheader("🚩 Report This Job")
                    if st.button("Report as Scam", use_container_width=True):
                        report_result = report_scam(job_text, job_url)
                        if report_result:
                            st.success("Thank you for reporting! This helps improve our system.")
    
    elif analyze_button:
        st.warning("Please enter job posting text to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "🔒 Your privacy is protected. We don't store personal information. | "
        "Built with ❤️ using Streamlit & FastAPI"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
