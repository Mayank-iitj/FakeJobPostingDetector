"""
Tests for the Rule Engine
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.rules import ScamRuleEngine
from backend.models.feature_extractor import FeatureExtractor


@pytest.fixture
def rule_engine():
    return ScamRuleEngine()


@pytest.fixture
def feature_extractor():
    return FeatureExtractor()


def test_high_risk_detection(rule_engine, feature_extractor):
    """Test detection of high-risk scam indicators"""
    text = "Pay $99 registration fee! No interview! Guaranteed job!"
    features = feature_extractor.extract(text)
    result = rule_engine.evaluate(text, features)
    
    assert result['score'] > 0.5  # Should be high risk
    assert len(result['flags']) > 0
    assert len(result['matched_patterns']) > 0


def test_medium_risk_detection(rule_engine, feature_extractor):
    """Test detection of medium-risk indicators"""
    text = "Work from home! WhatsApp only! Urgent hiring!"
    features = feature_extractor.extract(text)
    result = rule_engine.evaluate(text, features)
    
    assert result['score'] > 0.2
    assert len(result['flags']) > 0


def test_legitimate_job_low_score(rule_engine, feature_extractor):
    """Test that legitimate jobs get low scam scores"""
    text = """
    Senior Software Engineer at Microsoft
    Requirements: 5+ years experience, BS in Computer Science
    Apply through our careers portal
    """
    features = feature_extractor.extract(text)
    result = rule_engine.evaluate(text, features)
    
    assert result['score'] < 0.3  # Should be low risk


def test_pattern_matching(rule_engine, feature_extractor):
    """Test specific pattern matching"""
    text = "Guaranteed selection without any interview!!!"
    features = feature_extractor.extract(text)
    result = rule_engine.evaluate(text, features)
    
    # Check that specific patterns were matched
    matched_texts = [p['match'] for p in result['matched_patterns']]
    assert any('without' in match.lower() and 'interview' in match.lower() 
               for match in matched_texts)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
