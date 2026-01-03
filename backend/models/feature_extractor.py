"""
Feature Extractor for Job Scam Detection
Extracts numerical and categorical features from job posting text
"""
import re
from typing import Dict
import validators


class FeatureExtractor:
    """Extract features from job posting text"""
    
    # Scam indicator patterns
    PAYMENT_KEYWORDS = [
        r'registration fee', r'processing fee', r'training fee',
        r'pay.*\$\d+', r'deposit required', r'payment.*required',
        r'administrative.*fee', r'security deposit'
    ]
    
    UNREALISTIC_SALARY = [
        r'\$\d{4,}.*per day', r'\$\d{5,}.*per week',
        r'₹\s*[5-9]\d{4,}.*per day', r'earn.*\$\d{4,}.*daily',
        r'\d{5,}.*per hour', r'make.*\$\d{4,}.*week'
    ]
    
    URGENCY_KEYWORDS = [
        r'urgent', r'immediate', r'limited slots?', r'hurry',
        r'act now', r'limited time', r'offer expires', r'only \d+ positions?',
        r'first come first serve', r'apply immediately'
    ]
    
    NO_INTERVIEW = [
        r'no interview', r'without interview', r'guaranteed.*selection',
        r'direct.*joining', r'immediate joining', r'automatic.*selection'
    ]
    
    POOR_GRAMMAR_INDICATORS = [
        r'\b[A-Z]{5,}\b',  # Excessive caps
        r'!!!+',  # Multiple exclamation marks
        r'\?\?\?+',  # Multiple question marks
    ]
    
    WHATSAPP_ONLY = [
        r'whatsapp.*only', r'contact.*whatsapp',
        r'telegram.*only', r'dm.*(?:whatsapp|telegram)',
        r'message.*(?:whatsapp|telegram)'
    ]
    
    CRYPTO_KEYWORDS = [
        r'crypto', r'bitcoin', r'cryptocurrency',
        r'NFT', r'blockchain', r'web3'
    ]
    
    GIFT_CARD_KEYWORDS = [
        r'gift card', r'amazon.*card', r'google play.*card',
        r'itunes.*card', r'prepaid card'
    ]
    
    def __init__(self):
        self.patterns = {
            'requires_payment': self.PAYMENT_KEYWORDS,
            'unrealistic_salary': self.UNREALISTIC_SALARY,
            'urgency': self.URGENCY_KEYWORDS,
            'no_interview': self.NO_INTERVIEW,
            'poor_grammar': self.POOR_GRAMMAR_INDICATORS,
            'whatsapp_only': self.WHATSAPP_ONLY,
            'crypto_mention': self.CRYPTO_KEYWORDS,
            'gift_cards': self.GIFT_CARD_KEYWORDS
        }
    
    def extract(self, text: str, url: str = None) -> Dict:
        """
        Extract all features from job posting text
        
        Returns:
            Dict of boolean and numerical features
        """
        text_lower = text.lower()
        
        features = {
            # Pattern-based boolean features
            'requires_payment': self._check_patterns(text_lower, self.PAYMENT_KEYWORDS),
            'unrealistic_salary': self._check_patterns(text_lower, self.UNREALISTIC_SALARY),
            'urgency': self._check_patterns(text_lower, self.URGENCY_KEYWORDS),
            'no_interview': self._check_patterns(text_lower, self.NO_INTERVIEW),
            'poor_grammar': self._check_patterns(text, self.POOR_GRAMMAR_INDICATORS),
            'whatsapp_only': self._check_patterns(text_lower, self.WHATSAPP_ONLY),
            'crypto_mention': self._check_patterns(text_lower, self.CRYPTO_KEYWORDS),
            'gift_cards': self._check_patterns(text_lower, self.GIFT_CARD_KEYWORDS),
            
            # Text statistics
            'text_length': len(text),
            'word_count': len(text.split()),
            'has_email': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'has_phone': bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)),
            'generic_email': self._has_generic_email(text),
            'missing_company_name': not self._has_company_name(text),
            'excessive_caps': self._count_caps_words(text) > 3,
            
            # URL-based features
            'url_suspicious': self._check_url_suspicious(url) if url else False,
        }
        
        return features
    
    def _check_patterns(self, text: str, patterns: list) -> bool:
        """Check if any pattern matches in text"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _has_generic_email(self, text: str) -> bool:
        """Check for generic email domains"""
        generic_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
        for domain in generic_domains:
            if domain in text.lower():
                return True
        return False
    
    def _has_company_name(self, text: str) -> bool:
        """Simple check for company name presence"""
        company_indicators = ['company', 'inc', 'ltd', 'llc', 'corp', 'pvt']
        for indicator in company_indicators:
            if indicator in text.lower():
                return True
        return False
    
    def _count_caps_words(self, text: str) -> int:
        """Count words in all caps"""
        words = text.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        return len(caps_words)
    
    def _check_url_suspicious(self, url: str) -> bool:
        """Check if URL looks suspicious"""
        if not url:
            return False
        
        # Check if valid URL
        if not validators.url(url):
            return True
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz']
        for tld in suspicious_tlds:
            if url.endswith(tld):
                return True
        
        return False
