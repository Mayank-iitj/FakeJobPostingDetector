"""
Standalone Job Scam Detector App
Streamlit app that works without external API
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.detector import JobScamDetector
from backend.utils.text_processor import TextProcessor

# Page configuration
st.set_page_config(
    page_title="Job Scam Detector",
    page_icon="🔍",
    layout="wide"
)

# Initialize detector and processor
@st.cache_resource
def load_detector():
    """Load detector (cached for performance)"""
    return JobScamDetector(), TextProcessor()

detector, text_processor = load_detector()


def get_score_color(score: int) -> str:
    """Get color based on trust score"""
    if score >= 70:
        return "🟢"
    elif score >= 40:
        return "🟡"
    else:
        return "🔴"


def main():
    """Main app"""
    
    # Header
    st.title("🔍 Job Scam Detector")
    st.markdown("**AI-powered system to detect fake and scam job postings**")
    st.caption("🟢 Running in Standalone Mode (No API Required)")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "This tool uses AI and rule-based analysis to identify "
            "potential job scams.\n\n"
            "✅ Works completely standalone\n\n"
            "⚠️ AI assistant only - verify independently"
        )
        
        st.header("Examples")
        if st.button("Load Legitimate Example"):
            st.session_state.example_text = (
                "Software Engineer at Microsoft\n\n"
                "Requirements:\n"
                "- 3+ years Python/Java experience\n"
                "- BS in Computer Science\n\n"
                "Competitive salary, health benefits, remote work.\n"
                "Apply at: careers@microsoft.com"
            )
        
        if st.button("Load Scam Example"):
            st.session_state.example_text = (
                "🚨 URGENT HIRING!!! 🚨\n\n"
                "Earn $500 PER DAY from home!\n"
                "NO EXPERIENCE! NO INTERVIEW!\n\n"
                "Just pay $99 registration fee!\n"
                "WhatsApp ONLY: +1-555-0123\n"
                "GUARANTEED INCOME!!!"
            )
    
    # Main content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("📝 Enter Job Posting")
        
        job_text = st.text_area(
            "Paste job posting text here:",
            value=st.session_state.get('example_text', ''),
            height=300,
            placeholder="Paste the job description..."
        )
        
        job_url = st.text_input(
            "Job URL (optional):",
            placeholder="https://example.com/job/123"
        )
        
        analyze_button = st.button("🔍 Analyze Job Posting", type="primary", use_container_width=True)
    
    with col2:
        st.header("📊 Analysis Results")
        results_container = st.container()
    
    # Process analysis
    if analyze_button and job_text.strip():
        with st.spinner("Analyzing..."):
            try:
                # Clean and analyze
                cleaned_text = text_processor.clean_text(job_text)
                result = detector.analyze(cleaned_text, job_url if job_url else None)
                
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
                    
                    # Flags
                    if result['flags']:
                        st.subheader("⚠️ Warning Signs")
                        for flag in result['flags']:
                            st.markdown(f"• {flag}")
                    
                    # Highlighted Phrases
                    if result['highlighted_phrases']:
                        st.subheader("🔍 Risky Phrases")
                        for phrase in result['highlighted_phrases'][:5]:
                            risk_icon = "🔴" if phrase['risk_level'] == "high" else "🟡"
                            st.markdown(f"{risk_icon} **\"{phrase['text']}\"** - {phrase['reason']}")
                    
                    st.markdown("---")
                    
                    # Safety Advice
                    st.subheader("💡 Safety Recommendations")
                    for advice in result['advice']:
                        st.markdown(f"{advice}")
                        
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
    
    elif analyze_button:
        st.warning("Please enter job posting text to analyze.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "🔒 Privacy Protected | AI Assistant Only - Verify Independently"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
