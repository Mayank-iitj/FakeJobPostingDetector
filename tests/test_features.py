"""
Unit tests for Feature Extractor
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.feature_extractor import FeatureExtractor


@pytest.fixture
def extractor():
    return FeatureExtractor()


def test_payment_detection(extractor):
    """Test detection of payment requirements"""
    text = "Pay $99 registration fee to start this amazing opportunity"
    features = extractor.extract(text)
    assert features['requires_payment'] == True


def test_unrealistic_salary(extractor):
    """Test detection of unrealistic salary claims"""
    text = "Earn $5000 per day working from home"
    features = extractor.extract(text)
    assert features['unrealistic_salary'] == True


def test_urgency_keywords(extractor):
    """Test detection of urgency tactics"""
    text = "URGENT! Limited slots available! Apply immediately!"
    features = extractor.extract(text)
    assert features['urgency'] == True


def test_no_interview_flag(extractor):
    """Test detection of 'no interview' claims"""
    text = "No interview required, guaranteed selection"
    features = extractor.extract(text)
    assert features['no_interview'] == True


def test_whatsapp_only(extractor):
    """Test detection of WhatsApp-only communication"""
    text = "Contact via WhatsApp only: +1234567890"
    features = extractor.extract(text)
    assert features['whatsapp_only'] == True


def test_crypto_mention(extractor):
    """Test detection of cryptocurrency mentions"""
    text = "Bitcoin trading job opportunity"
    features = extractor.extract(text)
    assert features['crypto_mention'] == True


def test_gift_card_mention(extractor):
    """Test detection of gift card payments"""
    text = "Process payments via Amazon gift cards"
    features = extractor.extract(text)
    assert features['gift_cards'] == True


def test_generic_email(extractor):
    """Test detection of generic email domains"""
    text = "Contact us at joboffers@gmail.com"
    features = extractor.extract(text)
    assert features['generic_email'] == True


def test_legitimate_job(extractor):
    """Test that legitimate job has fewer flags"""
    text = """
    Software Engineer at TechCorp Inc.
    Requirements: 3+ years experience in Python
    Salary: $80,000 - $100,000
    Apply at careers@techcorp.com
    """
    features = extractor.extract(text)
    
    # Should not trigger major scam indicators
    assert features['requires_payment'] == False
    assert features['unrealistic_salary'] == False
    assert features['no_interview'] == False


def test_url_validation(extractor):
    """Test URL validation"""
    # Suspicious TLD
    features = extractor.extract("Job posting", "http://scam-site.tk")
    assert features['url_suspicious'] == True
    
    # Normal URL
    features = extractor.extract("Job posting", "https://linkedin.com/jobs/123")
    assert features['url_suspicious'] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
