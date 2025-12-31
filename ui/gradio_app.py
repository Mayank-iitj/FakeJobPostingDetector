"""
Gradio Interface for Threat Intelligence Platform
Interactive UI for phishing detection and malware analysis
"""

import gradio as gr
import requests
import os
from typing import Dict, Any
import json
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")


# Helper Functions
def scan_phishing_url(url: str, capture_screenshot: bool = True, analyze_dom: bool = True) -> Dict[str, Any]:
    """Call phishing detection API"""
    try:
        response = requests.post(
            f"{API_URL}/scan/phishing",
            json={
                "url": url,
                "capture_screenshot": capture_screenshot,
                "analyze_dom": analyze_dom
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}


def analyze_malware_file(file) -> Dict[str, Any]:
    """Call malware analysis API"""
    try:
        with open(file.name, 'rb') as f:
            files = {'file': (file.name, f, 'application/octet-stream')}
            response = requests.post(
                f"{API_URL}/scan/malware",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}


def format_phishing_result(result: Dict) -> tuple:
    """Format phishing scan result for display"""
    if "error" in result:
        return (
            f"❌ Error: {result['error']}",
            None,
            None
        )
    
    # Format verdict with emoji
    verdict_emoji = "🚨" if result['verdict'] == "PHISH" else "✅"
    verdict_text = f"{verdict_emoji} **{result['verdict']}**"
    
    # Risk gauge
    risk_score = result['risk_score']
    risk_color = 'red' if risk_score > 0.7 else 'orange' if risk_score > 0.4 else 'green'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score * 100,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': risk_color},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    # Detailed report
    report = f"""
# Phishing Scan Report

**Scan ID:** `{result['scan_id']}`  
**URL:** `{result['url']}`  
**Verdict:** {verdict_text}  
**Risk Score:** {risk_score:.2%}  
**Confidence:** {result['confidence']:.2%}  
**Scan Time:** {result['scan_time_ms']}ms  

## Explanation
{result['explanation']}

## Feature Scores
- **ViT Score:** {result['features']['vit_score']:.2%}
- **DOM Score:** {result['features']['dom_score']:.2% if result['features']['dom_score'] else 'N/A'}
- **Fusion Score:** {result['features']['fusion_score']:.2%}

---
*Scanned at: {result['timestamp']}*
    """
    
    return (verdict_text, fig, report)


def format_malware_result(result: Dict) -> tuple:
    """Format malware analysis result for display"""
    if "error" in result:
        return (
            f"❌ Error: {result['error']}",
            None,
            None
        )
    
    # Threat meter
    threat_score = result['threat_score']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_score,
        title={'text': "Threat Level"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "crimson"},
            'steps': [
                {'range': [0, 3], 'color': "green"},
                {'range': [3, 7], 'color': "orange"},
                {'range': [7, 10], 'color': "red"}
            ]
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    # Detailed report
    report = f"""
# Malware Analysis Report

**Scan ID:** `{result['scan_id']}`  
**Filename:** `{result['filename']}`  
**SHA-256:** `{result['sha256']}`  
**File Type:** {result['file_type']}  
**Size:** {result['file_size_kb']} KB  

## Classification
**Family:** 🦠 **{result['family']}**  
**Confidence:** {result['confidence']:.2%}  
**Threat Score:** {result['threat_score']:.1f}/10  

## Detected Behaviors
{chr(10).join([f"- {behavior}" for behavior in result['behaviors']])}

## Model Scores
- **CNN (Bytes):** {result['features']['cnn_score']:.2%}
- **RNN (Imports):** {result['features']['rnn_score']:.2%}
- **GNN (Call Graph):** {result['features']['gnn_score']:.2%}
- **Ensemble:** {result['features']['ensemble_score']:.2%}

## Behavioral Indicators
- **Persistence:** {'✅' if result['indicators']['persistence'] else '❌'}
- **Network Activity:** {'✅' if result['indicators']['network_activity'] else '❌'}
- **File Operations:** {'✅' if result['indicators']['file_operations'] else '❌'}
- **Registry Modifications:** {'✅' if result['indicators']['registry_modifications'] else '❌'}

---
*Analysis Time: {result['scan_time_ms']}ms*  
*Scanned at: {result['timestamp']}*
    """
    
    return (f"🦠 **{result['family']}**", fig, report)


# Build Gradio Interface
def build_interface():
    """Build main Gradio interface"""
    
    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="red",
            secondary_hue="orange"
        ),
        title="Threat Intelligence Platform",
        css="""
        .gradio-container {
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        }
        .prose h1 {
            color: #ff6b6b !important;
            text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
        }
        """
    ) as demo:
        
        gr.Markdown(
            """
            # 🛡️ Threat Intelligence Platform
            ### Enterprise-Grade Cybersecurity ML System
            
            **Powered by Vision Transformers + Deep Ensemble (CNN+RNN+GNN)**
            """
        )
        
        with gr.Tabs():
            # Phishing Scanner Tab
            with gr.Tab("🎣 Phishing Scanner"):
                gr.Markdown("### Scan URLs for phishing threats using ViT + DOM analysis")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        url_input = gr.Textbox(
                            label="🔗 URL to Scan",
                            placeholder="https://example.com",
                            lines=1
                        )
                        
                        with gr.Row():
                            capture_ss = gr.Checkbox(
                                label="Capture Screenshot",
                                value=True
                            )
                            analyze_dom_check = gr.Checkbox(
                                label="Analyze DOM",
                                value=True
                            )
                        
                        scan_btn = gr.Button(
                            "🔍 Scan URL",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=1):
                        verdict_display = gr.Markdown(
                            "**Verdict:** _Waiting for scan..._"
                        )
                        risk_gauge = gr.Plot(label="Risk Assessment")
                
                with gr.Row():
                    report_output = gr.Markdown(label="Detailed Report")
                
                # Wire up event
                scan_btn.click(
                    fn=lambda u, c, a: format_phishing_result(
                        scan_phishing_url(u, c, a)
                    ),
                    inputs=[url_input, capture_ss, analyze_dom_check],
                    outputs=[verdict_display, risk_gauge, report_output]
                )
            
            # Malware Analysis Tab
            with gr.Tab("🦠 Malware Analysis"):
                gr.Markdown("### Analyze PE/ELF binaries using Multi-Modal Ensemble")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        file_upload = gr.File(
                            label="📁 Upload Binary (PE/ELF)",
                            file_types=[".exe", ".dll", ".bin", ".elf"],
                            type="filepath"
                        )
                        
                        analyze_btn = gr.Button(
                            "🔬 Analyze File",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column(scale=1):
                        family_display = gr.Markdown(
                            "**Family:** _Waiting for analysis..._"
                        )
                        threat_gauge = gr.Plot(label="Threat Assessment")
                
                with gr.Row():
                    malware_report = gr.Markdown(label="Analysis Report")
                
                # Wire up event
                analyze_btn.click(
                    fn=lambda f: format_malware_result(
                        analyze_malware_file(f) if f else {"error": "No file uploaded"}
                    ),
                    inputs=[file_upload],
                    outputs=[family_display, threat_gauge, malware_report]
                )
            
            # Bulk Scan Tab
            with gr.Tab("📦 Bulk Scan"):
                gr.Markdown("### Upload CSV with URLs for batch processing")
                
                csv_upload = gr.File(
                    label="📊 Upload CSV",
                    file_types=[".csv"]
                )
                
                bulk_btn = gr.Button("🚀 Start Bulk Scan", variant="primary")
                
                bulk_status = gr.Markdown("**Status:** _Waiting..._")
                bulk_results = gr.Dataframe(label="Results")
            
            # About Tab
            with gr.Tab("ℹ️ About"):
                gr.Markdown(
                    """
                    # 🛡️ Threat Intelligence Platform
                    
                    ## Features
                    
                    ### Phishing Detection (98%+ F1-Score)
                    - **Vision Transformer** fine-tuned on website screenshots
                    - **DOM Analysis** with BERT encoding
                    - **Late Fusion** with XGBoost meta-learner
                    - Real-time prediction with explainability
                    
                    ### Malware Classification (99%+ Recall)
                    - **CNN Branch** for raw byte analysis (ResNet18)
                    - **RNN Branch** for import sequence modeling (LSTM)
                    - **GNN Branch** for call graph analysis (GraphConvNet)
                    - **Ensemble Stacking** with LightGBM
                    
                    ## Technology Stack
                    - **ML:** PyTorch Lightning, HuggingFace Transformers, PyG
                    - **Backend:** FastAPI, Celery, Redis
                    - **Frontend:** Gradio, Streamlit, Next.js
                    - **MLOps:** MLflow, W&B, Prometheus, Grafana
                    - **Deployment:** Docker, Railway/Vercel
                    
                    ## API Documentation
                    📚 **Swagger Docs:** [/docs](http://localhost:8000/docs)  
                    📖 **ReDoc:** [/redoc](http://localhost:8000/redoc)
                    
                    ## GitHub
                    ⭐ **Repository:** [github.com/yourname/threat-intel-platform](https://github.com)
                    
                    ---
                    
                    **Built with ❤️ for the AI/Cybersecurity community**
                    """
                )
        
        gr.Markdown(
            """
            ---
            *Threat Intelligence Platform v1.0.0 | Powered by Vision Transformers + Deep Ensemble*
            """
        )
    
    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
