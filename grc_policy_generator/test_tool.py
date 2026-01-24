#!/usr/bin/env python3
"""
Quick test to verify the tool works end-to-end
"""

from compliance_engine import (
    INDUSTRY_PRESETS, RiskScorer, get_framework_controls,
    calculate_compliance_coverage
)
from gap_analyzer import GapAnalyzer
from output_generator import OutputGenerator
from datetime import datetime, timedelta
import os
import shutil


def test_compliance_engine():
    """Test compliance engine."""
    print("Testing compliance engine...")

    # Test industry presets
    assert 'crypto' in INDUSTRY_PRESETS
    preset = INDUSTRY_PRESETS['crypto']
    assert preset.name == "Financial Services - Crypto/Digital Assets"
    assert "NYDFS" in preset.frameworks
    print("✓ Industry presets working")

    # Test risk scorer
    scorer = RiskScorer()
    config = {
        'min_length': 14,
        'require_special': True,
        'mfa_required': 'required_all',
        'expiration': 60
    }
    result = scorer.calculate_password_risk(config)
    assert result['score'] >= 0 and result['score'] <= 10
    assert result['risk_level'] in ['LOW', 'MEDIUM-LOW', 'MEDIUM', 'MEDIUM-HIGH', 'HIGH']
    print(f"✓ Risk scorer working (score: {result['score']}/10, level: {result['risk_level']})")

    # Test framework controls
    controls = get_framework_controls('password', ['SOC 2', 'ISO 27001', 'NYDFS'])
    assert len(controls) > 0
    assert any(c.framework == 'SOC 2' for c in controls)
    assert any(c.framework == 'ISO 27001' for c in controls)
    assert any(c.framework == 'NYDFS' for c in controls)
    print(f"✓ Framework controls working ({len(controls)} controls loaded)")

    return result


def test_gap_analyzer():
    """Test gap analyzer."""
    print("\nTesting gap analyzer...")

    current_state = {
        'min_length': 8,
        'has_complexity': False,
        'mfa_status': 'optional',
        'mfa_adoption_pct': 45,
        'has_hardware_tokens': False,
        'expiration_days': 90,
        'industry': 'crypto'
    }

    target_state = {
        'min_length': 14,
        'require_special': True,
        'mfa_required': 'required_all',
        'expiration': 60
    }

    analyzer = GapAnalyzer(current_state, target_state, ['SOC 2', 'ISO 27001', 'NYDFS'])
    gaps = analyzer.analyze()
    summary = analyzer.get_summary()

    assert isinstance(gaps, list)
    assert summary['total_gaps'] >= 0
    print(f"✓ Gap analyzer working ({summary['total_gaps']} gaps found)")
    print(f"  - Critical: {summary['critical']}, High: {summary['high']}, Medium: {summary['medium']}, Low: {summary['low']}")

    # Test Jira export
    jira_data = analyzer.generate_jira_export()
    assert isinstance(jira_data, list)
    print(f"✓ Jira export working ({len(jira_data)} tickets)")

    return gaps, summary


def test_output_generator(risk_result, gaps, gap_summary):
    """Test output generator."""
    print("\nTesting output generator...")

    test_output_dir = "/tmp/grc_test_output"
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    generator = OutputGenerator(test_output_dir)

    config = {
        'min_length': 14,
        'require_special': True,
        'mfa_required': 'required_all',
        'expiration': 60
    }

    metadata = {
        'effective_date': datetime.now().strftime('%Y-%m-%d'),
        'next_review_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'frameworks': ['SOC 2', 'ISO 27001', 'NYDFS']
    }

    # Test policy document generation
    policy_file = generator.generate_policy_document('password', config, metadata)
    assert os.path.exists(policy_file)
    print(f"✓ Policy document generated: {os.path.basename(policy_file)}")

    # Test compliance matrix
    controls = get_framework_controls('password', ['SOC 2', 'ISO 27001', 'NYDFS'])
    soc2_controls = [c for c in controls if c.framework == 'SOC 2']
    matrix_file = generator.generate_compliance_matrix(soc2_controls, 'SOC 2')
    assert os.path.exists(matrix_file)
    print(f"✓ Compliance matrix generated: {os.path.basename(matrix_file)}")

    # Test control testing checklist
    checklist_file = generator.generate_control_testing_checklist(controls, ['SOC 2', 'ISO 27001', 'NYDFS'])
    assert os.path.exists(checklist_file)
    print(f"✓ Control testing checklist generated: {os.path.basename(checklist_file)}")

    # Test gap analysis report
    gap_file = generator.generate_gap_analysis_report(gaps, gap_summary)
    assert os.path.exists(gap_file)
    print(f"✓ Gap analysis report generated: {os.path.basename(gap_file)}")

    # Test ServiceNow export
    sn_file = generator.generate_servicenow_export('password', controls, metadata)
    assert os.path.exists(sn_file)
    print(f"✓ ServiceNow export generated: {os.path.basename(sn_file)}")

    # Test Jira export
    jira_file = generator.generate_jira_export(gaps)
    assert os.path.exists(jira_file)
    print(f"✓ Jira export generated: {os.path.basename(jira_file)}")

    # Test executive summary
    exec_file = generator.generate_executive_summary('password', risk_result, gap_summary, metadata)
    assert os.path.exists(exec_file)
    print(f"✓ Executive summary generated: {os.path.basename(exec_file)}")

    print(f"\n✓ All artifacts generated successfully in: {test_output_dir}")

    # Cleanup
    # shutil.rmtree(test_output_dir)
    print(f"ℹ Test output kept for inspection: {test_output_dir}")


def main():
    """Run all tests."""
    print("="*60)
    print("GRC Policy Generator - Component Tests")
    print("="*60)

    try:
        # Test compliance engine
        risk_result = test_compliance_engine()

        # Test gap analyzer
        gaps, gap_summary = test_gap_analyzer()

        # Test output generator
        test_output_generator(risk_result, gaps, gap_summary)

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe tool is ready to use. Run:")
        print("  python3 grc_policy_generator.py")
        print()

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
