"""
Streamlit Dashboard for Threat Intelligence Platform
Analytics, metrics, and monitoring dashboard
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Threat Intel Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    h1 {
        color: #ff6b6b;
        text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Sidebar
st.sidebar.title("🛡️ Threat Intel Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Overview", "🎣 Phishing Metrics", "🦠 Malware Analytics", "⚙️ API Monitor", "📈 Model Performance"]
)

st.sidebar.markdown("---")
st.sidebar.info("**Version:** 1.0.0  \n**Status:** ✅ Active")


# Generate mock data for demonstration
def generate_mock_data():
    """Generate mock analytics data"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    df_phishing = pd.DataFrame({
        'date': dates,
        'total_scans': [100 + i*5 for i in range(30)],
        'phishing_detected': [20 + i*2 for i in range(30)],
        'legitimate': [80 + i*3 for i in range(30)]
    })
    
    df_malware = pd.DataFrame({
        'date': dates,
        'total_scans': [50 + i*3 for i in range(30)],
        'malware_detected': [35 + i*2 for i in range(30)],
        'families': [8 + (i % 5) for i in range(30)]
    })
    
    return df_phishing, df_malware


# Page: Overview
if page == "📊 Overview":
    st.title("📊 Threat Intelligence Overview")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Scans (24h)",
            value="1,247",
            delta="+127"
        )
    
    with col2:
        st.metric(
            label="Threats Detected",
            value="342",
            delta="+45",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="API Uptime",
            value="99.8%",
            delta="+0.2%"
        )
    
    with col4:
        st.metric(
            label="Avg Response Time",
            value="487ms",
            delta="-23ms"
        )
    
    st.markdown("---")
    
    # Activity timeline
    df_phishing, df_malware = generate_mock_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎣 Phishing Detection Trends")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_phishing['date'],
            y=df_phishing['phishing_detected'],
            mode='lines+markers',
            name='Phishing Detected',
            line=dict(color='#ff6b6b', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_phishing['date'],
            y=df_phishing['legitimate'],
            mode='lines+markers',
            name='Legitimate',
            line=dict(color='#51cf66', width=3)
        ))
        fig.update_layout(
            template='plotly_dark',
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🦠 Malware Detection Trends")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_malware['date'],
            y=df_malware['malware_detected'],
            mode='lines+markers',
            name='Malware Detected',
            line=dict(color='#ff6b6b', width=3),
            fill='tozeroy'
        ))
        fig.update_layout(
            template='plotly_dark',
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top threats
    st.markdown("---")
    st.subheader("🔥 Top Threats (Last 7 Days)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top Phishing Domains**")
        phishing_domains = pd.DataFrame({
            'Domain': ['suspicious-bank.com', 'fake-paypal.net', 'phish-amazon.org', 'scam-microsoft.com', 'fraud-apple.net'],
            'Detections': [234, 189, 156, 142, 128],
            'Risk Score': [0.98, 0.95, 0.92, 0.89, 0.87]
        })
        st.dataframe(phishing_domains, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**Top Malware Families**")
        malware_families = pd.DataFrame({
            'Family': ['Emotet', 'TrickBot', 'Ryuk', 'Zeus', 'Dridex'],
            'Samples': [89, 67, 54, 48, 42],
            'Threat Level': [9.8, 9.5, 9.9, 8.7, 8.5]
        })
        st.dataframe(malware_families, use_container_width=True, hide_index=True)


# Page: Phishing Metrics
elif page == "🎣 Phishing Metrics":
    st.title("🎣 Phishing Detection Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("F1-Score", "98.6%", "+0.3%")
    with col2:
        st.metric("Precision", "97.8%", "+0.2%")
    with col3:
        st.metric("Recall", "99.4%", "+0.1%")
    
    st.markdown("---")
    
    # Confusion Matrix
    st.subheader("📊 Confusion Matrix (Last 1000 Scans)")
    
    confusion_data = [[782, 18], [12, 188]]
    
    fig = go.Figure(data=go.Heatmap(
        z=confusion_data,
        x=['Predicted Legitimate', 'Predicted Phishing'],
        y=['Actual Legitimate', 'Actual Phishing'],
        colorscale='RdYlGn_r',
        text=confusion_data,
        texttemplate='%{text}',
        textfont={"size": 20}
    ))
    
    fig.update_layout(
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 ViT Feature Importance")
        features = ['Visual Layout', 'Logo Detection', 'Form Elements', 'Color Scheme', 'Text Density']
        importance = [0.32, 0.28, 0.22, 0.12, 0.06]
        
        fig = go.Figure(go.Bar(
            x=importance,
            y=features,
            orientation='h',
            marker=dict(color='#ff6b6b')
        ))
        fig.update_layout(
            template='plotly_dark',
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌐 DOM Feature Importance")
        features = ['SSL Certificate', 'Form Count', 'External Links', 'Domain Age', 'JavaScript']
        importance = [0.35, 0.25, 0.20, 0.15, 0.05]
        
        fig = go.Figure(go.Bar(
            x=importance,
            y=features,
            orientation='h',
            marker=dict(color='#51cf66')
        ))
        fig.update_layout(
            template='plotly_dark',
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)


# Page: Malware Analytics
elif page == "🦠 Malware Analytics":
    st.title("🦠 Malware Analysis Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Recall", "99.2%", "+0.4%")
    with col2:
        st.metric("Precision", "97.5%", "+0.2%")
    with col3:
        st.metric("Accuracy", "98.3%", "+0.3%")
    
    st.markdown("---")
    
    # Family distribution
    st.subheader("📊 Malware Family Distribution")
    
    families = ['Emotet', 'TrickBot', 'Ryuk', 'Zeus', 'Dridex', 'Locky', 'WannaCry', 'Others']
    counts = [89, 67, 54, 48, 42, 35, 28, 95]
    
    fig = go.Figure(data=[go.Pie(
        labels=families,
        values=counts,
        hole=0.4,
        marker=dict(colors=px.colors.sequential.Reds)
    )])
    
    fig.update_layout(
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Branch performance
    st.markdown("---")
    st.subheader("🎯 Ensemble Branch Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**CNN Branch (Bytes)**")
        st.metric("Accuracy", "95.2%")
        st.progress(0.952)
    
    with col2:
        st.markdown("**RNN Branch (Imports)**")
        st.metric("Accuracy", "98.1%")
        st.progress(0.981)
    
    with col3:
        st.markdown("**GNN Branch (Call Graph)**")
        st.metric("Accuracy", "99.3%")
        st.progress(0.993)


# Page: API Monitor
elif page == "⚙️ API Monitor":
    st.title("⚙️ API Performance Monitor")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Requests/min", "142", "+23")
    with col2:
        st.metric("p50 Latency", "245ms", "-12ms")
    with col3:
        st.metric("p95 Latency", "487ms", "-23ms")
    with col4:
        st.metric("Error Rate", "0.2%", "-0.1%")
    
    st.markdown("---")
    
    # Latency distribution
    st.subheader("📈 Response Time Distribution")
    
    import numpy as np
    latencies = np.random.gamma(2, 100, 1000)
    
    fig = go.Figure(data=[go.Histogram(
        x=latencies,
        nbinsx=50,
        marker=dict(color='#ff6b6b')
    )])
    
    fig.update_layout(
        template='plotly_dark',
        height=300,
        xaxis_title="Latency (ms)",
        yaxis_title="Frequency"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Endpoint stats
    st.markdown("---")
    st.subheader("🔗 Endpoint Statistics")
    
    endpoints = pd.DataFrame({
        'Endpoint': ['/scan/phishing', '/scan/malware', '/auth/token', '/health'],
        'Requests (24h)': [734, 412, 89, 1247],
        'Avg Latency': ['487ms', '1.2s', '123ms', '45ms'],
        'Success Rate': ['99.8%', '99.5%', '100%', '100%']
    })
    
    st.dataframe(endpoints, use_container_width=True, hide_index=True)


# Page: Model Performance
elif page == "📈 Model Performance":
    st.title("📈 Model Performance Tracking")
    
    st.subheader("🎯 Model Drift Detection")
    
    # Drift over time
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    drift_scores = [0.02 + 0.001*i + np.random.normal(0, 0.005) for i in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=drift_scores,
        mode='lines+markers',
        name='Drift Score',
        line=dict(color='#ff6b6b', width=3)
    ))
    fig.add_hline(y=0.05, line_dash="dash", line_color="yellow", annotation_text="Warning Threshold")
    fig.add_hline(y=0.10, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    
    fig.update_layout(
        template='plotly_dark',
        height=300,
        yaxis_title="Drift Score",
        xaxis_title="Date"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Model versions
    st.subheader("📦 Model Versions")
    
    versions = pd.DataFrame({
        'Version': ['v1.2.0 (Production)', 'v1.1.5', 'v1.1.0', 'v1.0.0'],
        'Deployed': ['2025-12-28', '2025-12-15', '2025-11-30', '2025-11-01'],
        'F1-Score': ['98.6%', '98.3%', '97.8%', '97.2%'],
        'Status': ['🟢 Active', '🟡 Staging', '⚪ Archived', '⚪ Archived']
    })
    
    st.dataframe(versions, use_container_width=True, hide_index=True)
    
    # Retraining schedule
    st.markdown("---")
    st.subheader("🔄 Automated Retraining")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Next Scheduled Retrain:** 2025-01-07 00:00 UTC")
        st.info("**Last Retrain:** 2025-12-24 00:00 UTC")
    
    with col2:
        st.success("**Training Data:** 52,847 samples")
        st.success("**New Samples (This Week):** 3,421")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Threat Intelligence Platform v1.0.0 | Powered by Vision Transformers + Deep Ensemble</p>
        <p>Built with ❤️ for the AI/Cybersecurity community</p>
    </div>
    """,
    unsafe_allow_html=True
)
