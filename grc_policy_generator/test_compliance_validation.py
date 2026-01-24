#!/usr/bin/env python3
"""
Test that compliance matrices are now dynamic
"""

import sys
import os
sys.path.insert(0, '/home/user/Policy-and-Compliance-Template-Generator/grc_policy_generator')

from compliance_engine import get_framework_controls
from output_generator import OutputGenerator
import shutil

# Test Weak Configuration (should show non-compliant)
weak_config = {
    'min_length': 5,
    'require_special': False,
    'mfa_required': 'optional',
    'expiration': 365
}

# Test Strong Configuration (should show compliant)
strong_config = {
    'min_length': 14,
    'require_special': True,
    'mfa_required': 'required_all',
    'expiration': 60
}

test_dir = "/tmp/test_compliance_matrices"
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

print("Testing Compliance Matrix Validation...\n")

# Test 1: Weak Config
print("1. WEAK CONFIG (5 chars, no MFA, no special chars)")
print("   Expected: Many ✗ Non-Compliant statuses\n")

os.makedirs(f"{test_dir}/weak", exist_ok=True)
generator_weak = OutputGenerator(f"{test_dir}/weak")

controls_soc2 = get_framework_controls('password', ['SOC 2'])
soc2_controls = [c for c in controls_soc2 if c.framework == 'SOC 2']

matrix_file = generator_weak.generate_compliance_matrix(soc2_controls, 'SOC 2', weak_config)

with open(matrix_file, 'r') as f:
    content = f.read()

print("   SOC 2 Compliance Matrix (Weak Config):")
print("   " + "─" * 60)
for line in content.split('\n')[5:15]:  # Show control rows
    if '|' in line and not line.startswith('|---'):
        print(f"   {line}")

# Check for non-compliant markers
non_compliant_count = content.count('✗ Non-Compliant')
partial_count = content.count('⚠ Partial')
compliant_count = content.count('✓ Compliant')

print(f"\n   Results: ✓ {compliant_count} Compliant, ⚠ {partial_count} Partial, ✗ {non_compliant_count} Non-Compliant")

assert non_compliant_count > 0, "Weak config should have non-compliant controls!"
print(f"   ✓ Validation working - found non-compliant controls\n")

# Test 2: Strong Config
print("2. STRONG CONFIG (14 chars, universal MFA, special chars)")
print("   Expected: All ✓ Compliant statuses\n")

os.makedirs(f"{test_dir}/strong", exist_ok=True)
generator_strong = OutputGenerator(f"{test_dir}/strong")

matrix_file_strong = generator_strong.generate_compliance_matrix(soc2_controls, 'SOC 2', strong_config)

with open(matrix_file_strong, 'r') as f:
    content_strong = f.read()

print("   SOC 2 Compliance Matrix (Strong Config):")
print("   " + "─" * 60)
for line in content_strong.split('\n')[5:15]:  # Show control rows
    if '|' in line and not line.startswith('|---'):
        print(f"   {line}")

# Check for compliant markers
non_compliant_count_strong = content_strong.count('✗ Non-Compliant')
compliant_count_strong = content_strong.count('✓ Compliant')

print(f"\n   Results: ✓ {compliant_count_strong} Compliant, ✗ {non_compliant_count_strong} Non-Compliant")

assert compliant_count_strong > compliant_count, "Strong config should have more compliant controls!"
print(f"   ✓ Validation working - strong config more compliant\n")

# Test 3: Verify they're different
print("3. VERIFICATION")
assert content != content_strong, "Matrices should be different for different configs!"
print(f"   ✓ Matrices are different based on configuration")

print("\n" + "="*60)
print("✅ COMPLIANCE MATRIX VALIDATION IS WORKING!")
print("="*60)
print("\nKey findings:")
print(f"  - Weak config: {compliant_count} compliant, {non_compliant_count} non-compliant")
print(f"  - Strong config: {compliant_count_strong} compliant, {non_compliant_count_strong} non-compliant")
print(f"  - Matrices are now dynamic and reflect actual policy configuration")

# Cleanup
shutil.rmtree(test_dir)
print(f"\n✓ Test artifacts cleaned up")
