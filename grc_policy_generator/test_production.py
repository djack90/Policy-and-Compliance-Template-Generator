#!/usr/bin/env python3
"""
Quick test of production-ready tool with different configurations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, '/home/user/Policy-and-Compliance-Template-Generator/grc_policy_generator')

from compliance_engine import RiskScorer, get_framework_controls
from gap_analyzer import GapAnalyzer
from output_generator import OutputGenerator
from datetime import datetime, timedelta
import shutil


def test_dynamic_outputs():
    """Test that outputs actually change based on configuration."""
    print("Testing dynamic outputs...")

    test_dir = "/tmp/grc_production_test"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    os.makedirs(test_dir)

    # Test Configuration 1: Weak security
    print("\n1. Testing WEAK configuration (8 chars, no MFA)...")
    weak_config = {
        'min_length': 8,
        'require_special': False,
        'mfa_required': 'optional',
        'expiration': 90
    }

    current_state_weak = {
        'min_length': 8,
        'has_complexity': False,
        'mfa_status': 'none',
        'mfa_adoption_pct': 0,
        'has_hardware_tokens': False,
        'expiration_days': 999,
        'industry': 'crypto'
    }

    scorer = RiskScorer()
    weak_risk = scorer.calculate_password_risk(weak_config)
    print(f"   Risk Score: {weak_risk['score']}/10 ({weak_risk['risk_level']})")

    analyzer_weak = GapAnalyzer(current_state_weak, weak_config, ['SOC 2', 'ISO 27001', 'NYDFS'])
    weak_gaps = analyzer_weak.analyze()
    print(f"   Gaps Found: {len(weak_gaps)}")

    # Test Configuration 2: Strong security
    print("\n2. Testing STRONG configuration (14 chars, universal MFA)...")
    strong_config = {
        'min_length': 14,
        'require_special': True,
        'mfa_required': 'required_all',
        'expiration': 60
    }

    current_state_strong = {
        'min_length': 8,
        'has_complexity': False,
        'mfa_status': 'optional',
        'mfa_adoption_pct': 45,
        'has_hardware_tokens': False,
        'expiration_days': 90,
        'industry': 'crypto'
    }

    strong_risk = scorer.calculate_password_risk(strong_config)
    print(f"   Risk Score: {strong_risk['score']}/10 ({strong_risk['risk_level']})")

    analyzer_strong = GapAnalyzer(current_state_strong, strong_config, ['SOC 2', 'ISO 27001', 'NYDFS'])
    strong_gaps = analyzer_strong.analyze()
    print(f"   Gaps Found: {len(strong_gaps)}")

    # Verify outputs are different
    assert weak_risk['score'] != strong_risk['score'], "Risk scores should be different!"
    assert len(weak_gaps) != len(strong_gaps), "Gap counts should be different!"

    print(f"\n✓ Outputs are dynamic - risk scores and gap counts vary with configuration")

    # Test Executive Insights generation
    print("\n3. Testing Executive Insights generation...")

    generator = OutputGenerator(os.path.join(test_dir, "test1"))

    metadata = {
        'effective_date': datetime.now().strftime('%Y-%m-%d'),
        'next_review_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'frameworks': ['SOC 2', 'ISO 27001', 'NYDFS']
    }

    # Generate weak config insights
    gap_summary_weak = analyzer_weak.get_summary()
    insights_weak = generator.generate_executive_insights(
        'password', weak_risk, weak_gaps, gap_summary_weak, weak_config, ['SOC 2', 'ISO 27001', 'NYDFS']
    )

    assert os.path.exists(insights_weak), "Executive insights file should be created"
    print(f"   ✓ Executive insights created: {insights_weak}")

    # Verify content is dynamic
    with open(insights_weak, 'r') as f:
        content_weak = f.read()
        assert str(weak_config['min_length']) in content_weak, "Should include actual password length"
        assert "8 chars" in content_weak or "8 characters" in content_weak, "Should mention 8 character length"

    # Generate strong config insights
    generator2 = OutputGenerator(os.path.join(test_dir, "test2"))
    gap_summary_strong = analyzer_strong.get_summary()
    insights_strong = generator2.generate_executive_insights(
        'password', strong_risk, strong_gaps, gap_summary_strong, strong_config, ['SOC 2', 'ISO 27001', 'NYDFS']
    )

    with open(insights_strong, 'r') as f:
        content_strong = f.read()
        assert str(strong_config['min_length']) in content_strong, "Should include actual password length"
        assert "14" in content_strong, "Should mention 14 character length"

    # Verify they're different
    assert content_weak != content_strong, "Insights should be different for different configs!"
    print(f"   ✓ Insights content is dynamic and reflects configuration")

    # Show sample of insights
    print(f"\n4. Sample Executive Insights (Strong Config):")
    print("   " + "─" * 60)
    lines = content_strong.split('\n')
    for line in lines[:25]:
        print(f"   {line}")
    print("   " + "─" * 60)

    print(f"\n✅ ALL PRODUCTION TESTS PASSED!")
    print(f"\nKey findings:")
    print(f"  - Weak config: Risk {weak_risk['score']}/10, {len(weak_gaps)} gaps")
    print(f"  - Strong config: Risk {strong_risk['score']}/10, {len(strong_gaps)} gaps")
    print(f"  - Outputs are fully dynamic")
    print(f"  - Executive insights provide clear prioritization")

    # Cleanup
    shutil.rmtree(test_dir)
    print(f"\n✓ Test artifacts cleaned up")


if __name__ == "__main__":
    try:
        test_dynamic_outputs()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
