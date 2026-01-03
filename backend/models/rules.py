"""
Rule-Based Scam Detection Engine
Pattern matching and heuristic rules for job scam detection
"""
import re
from typing import Dict, List


class ScamRuleEngine:
    """Rule-based detection system"""
    
    def __init__(self):
        # Define rule patterns with risk levels and descriptions
        self.rules = [
            {
                'pattern': r'(?:registration|processing|training|administrative)\s+fee',
                'risk_level': 'high',
                'reason': 'Requests upfront payment',
                'weight': 0.3
            },
            {
                'pattern': r'(?:no|without)\s+interview',
                'risk_level': 'high',
                'reason': 'No interview required',
                'weight': 0.25
            },
            {
                'pattern': r'(?:\$|₹)\s*\d{4,}.*(?:per day|daily|/day)',
                'risk_level': 'high',
                'reason': 'Unrealistic daily salary',
                'weight': 0.25
            },
            {
                'pattern': r'guaranteed\s+(?:selection|job|income)',
                'risk_level': 'high',
                'reason': 'Guaranteed selection claims',
                'weight': 0.2
            },
            {
                'pattern': r'(?:whatsapp|telegram)\s+only',
                'risk_level': 'medium',
                'reason': 'WhatsApp/Telegram-only communication',
                'weight': 0.15
            },
            {
                'pattern': r'(?:urgent|immediate|hurry|act now)',
                'risk_level': 'medium',
                'reason': 'Urgency pressure tactics',
                'weight': 0.1
            },
            {
                'pattern': r'work\s+from\s+home.*\$\d{3,}',
                'risk_level': 'medium',
                'reason': 'Work-from-home with high pay',
                'weight': 0.15
            },
            {
                'pattern': r'limited\s+(?:slots?|positions?|time)',
                'risk_level': 'medium',
                'reason': 'Artificial scarcity',
                'weight': 0.1
            },
            {
                'pattern': r'(?:bitcoin|crypto|cryptocurrency|NFT)',
                'risk_level': 'medium',
                'reason': 'Cryptocurrency mention in job',
                'weight': 0.15
            },
            {
                'pattern': r'gift\s+card',
                'risk_level': 'high',
                'reason': 'Gift card payment method',
                'weight': 0.25
            },
            {
                'pattern': r'!!!+',
                'risk_level': 'low',
                'reason': 'Excessive punctuation',
                'weight': 0.05
            },
            {
                'pattern': r'\b[A-Z]{6,}\b',
                'risk_level': 'low',
                'reason': 'Excessive capitalization',
                'weight': 0.05
            },
            {
                'pattern': r'(?:gmail|yahoo|hotmail)\.com',
                'risk_level': 'low',
                'reason': 'Generic email domain',
                'weight': 0.08
            },
            {
                'pattern': r'(?:earn|make)\s+\$\d{3,}.*(?:week|daily)',
                'risk_level': 'high',
                'reason': 'Unrealistic earnings promise',
                'weight': 0.2
            },
            {
                'pattern': r'no\s+(?:experience|skills?)\s+(?:needed|required)',
                'risk_level': 'medium',
                'reason': 'No experience needed with high pay',
                'weight': 0.12
            },
        ]
    
    def evaluate(self, text: str, features: Dict) -> Dict:
        """
        Evaluate text against rule patterns
        
        Returns:
            Dict with score, flags, and matched patterns
        """
        text_lower = text.lower()
        matched_patterns = []
        flags = []
        total_score = 0.0
        
        # Check each rule
        for rule in self.rules:
            matches = list(re.finditer(rule['pattern'], text_lower, re.IGNORECASE))
            
            if matches:
                # Record match
                for match in matches[:1]:  # Take first match only per rule
                    matched_patterns.append({
                        'match': match.group(),
                        'risk_level': rule['risk_level'],
                        'reason': rule['reason']
                    })
                
                # Add flag
                flags.append(rule['reason'])
                
                # Add to score
                total_score += rule['weight']
        
        # Additional feature-based flags
        if features.get('missing_company_name'):
            flags.append("Missing company information")
            total_score += 0.1
        
        if features.get('url_suspicious'):
            flags.append("Suspicious URL or domain")
            total_score += 0.15
        
        # Normalize score to 0-1 range
        normalized_score = min(total_score, 1.0)
        
        return {
            'score': normalized_score,
            'flags': flags,
            'matched_patterns': matched_patterns
        }
