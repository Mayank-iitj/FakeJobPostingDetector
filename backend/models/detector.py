"""
Job Scam Detector - Core ML Model
Hybrid system combining ML models with rule-based detection
"""
import re
import pickle
import os
from typing import Dict, List, Tuple
import logging
from backend.models.feature_extractor import FeatureExtractor
from backend.models.rules import ScamRuleEngine
from backend.config import settings

logger = logging.getLogger(__name__)


class JobScamDetector:
    """Main detector class combining ML and rule-based approaches"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.rule_engine = ScamRuleEngine()
        self.model = None
        self.vectorizer = None
        self._load_model()
    
    def _load_model(self):
        """Load trained ML model if available"""
        model_path = settings.MODEL_PATH
        
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data.get('model')
                    self.vectorizer = model_data.get('vectorizer')
                logger.info(f"Model loaded from {model_path}")
            except Exception as e:
                logger.warning(f"Could not load model: {e}. Using rule-based system only.")
        else:
            logger.warning(f"Model not found at {model_path}. Using rule-based system only.")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    def analyze(self, text: str, url: str = None) -> Dict:
        """
        Analyze job posting text for scam indicators
        
        Returns:
            Dict with prediction, score, flags, explanation, etc.
        """
        # Extract features
        features = self.feature_extractor.extract(text, url)
        
        # Apply rule-based detection
        rule_results = self.rule_engine.evaluate(text, features)
        
        # Get ML prediction if model is loaded
        ml_score = 0.5  # Default neutral score
        if self.model and self.vectorizer:
            try:
                text_vector = self.vectorizer.transform([text])
                ml_proba = self.model.predict_proba(text_vector)[0]
                ml_score = ml_proba[1]  # Probability of scam
            except Exception as e:
                logger.error(f"ML prediction error: {e}")
        
        # Combine ML and rule-based scores
        combined_score = self._combine_scores(ml_score, rule_results['score'])
        
        # Convert to trust score (0-100, higher is safer)
        trust_score = int((1 - combined_score) * 100)
        
        # Determine prediction category
        prediction = self._get_prediction_label(combined_score)
        
        # Generate highlighted phrases
        highlighted = self._highlight_risky_phrases(text, rule_results['matched_patterns'])
        
        # Generate explanation
        explanation = self._generate_explanation(
            combined_score, 
            rule_results['flags'],
            features
        )
        
        # Generate advice
        advice = self._generate_advice(combined_score, features)
        
        return {
            "prediction": prediction,
            "score": trust_score,
            "flags": rule_results['flags'],
            "highlighted_phrases": highlighted,
            "explanation": explanation,
            "advice": advice,
            "confidence": abs(combined_score - 0.5) * 2  # 0 to 1
        }
    
    def _combine_scores(self, ml_score: float, rule_score: float) -> float:
        """Combine ML and rule-based scores"""
        # Weight: 60% ML, 40% rules if model exists, otherwise 100% rules
        if self.model:
            return 0.6 * ml_score + 0.4 * rule_score
        return rule_score
    
    def _get_prediction_label(self, score: float) -> str:
        """Convert score to prediction label"""
        if score >= settings.SCAM_THRESHOLD_HIGH:
            return "High Risk Scam"
        elif score >= settings.SCAM_THRESHOLD_MEDIUM:
            return "Suspicious"
        else:
            return "Likely Legitimate"
    
    def _highlight_risky_phrases(self, text: str, matched_patterns: List[Dict]) -> List[Dict]:
        """Extract and highlight risky phrases from text"""
        highlighted = []
        
        for pattern in matched_patterns:
            highlighted.append({
                "text": pattern['match'],
                "risk_level": pattern['risk_level'],
                "reason": pattern['reason']
            })
        
        return highlighted[:10]  # Limit to top 10
    
    def _generate_explanation(self, score: float, flags: List[str], features: Dict) -> str:
        """Generate natural language explanation"""
        if score >= settings.SCAM_THRESHOLD_HIGH:
            explanation = "This posting shows multiple red flags typical of job scams. "
        elif score >= settings.SCAM_THRESHOLD_MEDIUM:
            explanation = "This posting has some concerning characteristics. "
        else:
            explanation = "This posting appears mostly legitimate, but always verify independently. "
        
        if flags:
            top_flags = flags[:3]
            explanation += f"Key concerns: {', '.join(top_flags)}. "
        
        if features.get('requires_payment'):
            explanation += "Legitimate employers never ask for upfront fees. "
        
        if features.get('unrealistic_salary'):
            explanation += "The salary claims appear unrealistically high. "
        
        return explanation
    
    def _generate_advice(self, score: float, features: Dict) -> List[str]:
        """Generate actionable safety advice"""
        advice = []
        
        if score >= settings.SCAM_THRESHOLD_MEDIUM:
            advice.extend([
                "🔍 Research the company on LinkedIn and Google",
                "❌ Never pay any fees or send money",
                "📧 Verify the email domain matches the company website",
                "🚩 Report this posting to the job platform",
                "👥 Check company reviews on Glassdoor"
            ])
        else:
            advice.extend([
                "✅ Still verify company legitimacy independently",
                "🔗 Check the official company website",
                "📞 Confirm contact details are genuine",
                "❓ Ask detailed questions in the interview"
            ])
        
        if features.get('whatsapp_only'):
            advice.append("⚠️ Avoid jobs that only communicate via WhatsApp")
        
        if features.get('requires_payment'):
            advice.insert(0, "🚨 NEVER pay any fees - this is a major scam indicator")
        
        return advice
