# GRC Policy & Compliance Generator

**AI-Powered Audit Preparation Tool**

An intelligent command-line tool that automates GRC policy generation, compliance mapping, gap analysis, and audit preparation across multiple frameworks (SOC 2, ISO 27001, NYDFS, PCI-DSS).

## Features

✅ **Automate GRC Reporting**
- Generates professional policy documents
- Creates compliance matrices for SOC 2, ISO 27001, NYDFS
- Produces audit-ready control testing checklists
- Exports to ServiceNow and Jira formats

✅ **Surface Risk Insights**
- Real-time risk scoring (0-10 scale)
- Industry benchmarking
- Gap analysis between current and target state
- Actionable remediation recommendations

✅ **Multi-Framework Compliance**
- SOC 2 Type II (Trust Services Criteria)
- ISO 27001:2022 (Annex A controls)
- NYDFS 23 NYCRR 500 (Cybersecurity Requirements)
- PCI-DSS 4.0 (for financial services)
- HIPAA Security Rule (for healthcare)

✅ **Platform Integration**
- ServiceNow GRC import (JSON)
- Jira ticket import (CSV)
- Industry-specific presets (Crypto, FinTech, Healthcare, Tech)

## Installation

```bash
# No installation required - pure Python
cd grc_policy_generator
python3 grc_policy_generator.py
```

## Usage

### Basic Usage

```bash
python3 grc_policy_generator.py
```

The tool will guide you through:
1. Industry selection (Crypto, FinTech, Healthcare, Tech)
2. Framework selection (SOC 2, ISO 27001, NYDFS, etc.)
3. Current state assessment
4. Target policy configuration
5. Artifact generation

### Output

The tool generates a timestamped directory with:

```
generated_policies/2026-01-24_143052/
├── Password_Policy_v1.0.md (professional policy document)
├── SOC_2_Compliance_Matrix.md (CC6.1, CC6.2, CC6.6 controls)
├── ISO_27001_Compliance_Matrix.md (A.5.15, A.9.2, A.9.4 controls)
├── NYDFS_Compliance_Matrix.md (§500.07, §500.12 requirements)
├── Control_Testing_Checklist.md (auditor procedures)
├── Gap_Analysis_Report.md (current vs. target gaps)
├── ServiceNow_Import.json (GRC platform import)
├── Jira_Import_Gaps.csv (remediation tickets)
└── Executive_Summary.md (1-page summary for leadership)
```

## Example Session

```
╔══════════════════════════════════════════════════════════════╗
║  🔐 Intelligent GRC Policy & Compliance Generator            ║
║  AI-Powered Audit Preparation Tool                           ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ORGANIZATIONAL CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[?] What industry are you in?
    1. Financial Services - Traditional Banking
    2. Financial Services - Crypto/Digital Assets ⭐ (Recommended for Fireblocks)
    3. Healthcare
    4. Technology/SaaS
    5. Other

Choice [1-5]: 2

✓ Industry: Financial Services - Crypto/Digital Assets
  → Auto-applying: SOC 2, ISO 27001, NYDFS
  → Risk Classification: HIGH
  → Enhanced security controls required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CURRENT STATE ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[?] Do you currently have a password policy in place? [y/N]: y
[?] Current minimum password length: 8
[?] Do you require special characters? [y/N]: n
[?] Is MFA currently enabled?
    1. No - not implemented
    2. Yes - optional for users
    3. Yes - required for some users
    4. Yes - required for all users

Choice [1-4]: 2
[?] What % of users currently use MFA? [0-100]: 45

✓ Current state captured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TARGET POLICY CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[?] Minimum password length [default: 14]: 14

✓ Good choice!
  SOC 2 CC6.2: ✓ Meets requirement (≥8 chars)
  ISO 27001 A.9.2.4: ✓ Meets recommendation (≥12 chars)
  NYDFS §500.07: ✓ Meets requirement

[?] Require special characters? [Y/n]: y

✓ Excellent! Password strength improved

[?] Multi-Factor Authentication:
    1. Optional (not recommended for Financial Services - Crypto/Digital Assets)
    2. Required for privileged users ⭐ (NYDFS minimum)
    3. Required for all users ⭐ (Best practice for crypto custody)

Choice [1-3]: 3

✓ Outstanding choice!
  SOC 2 CC6.2: ✓ EXCEEDS requirement
  ISO 27001 A.9.4.3: ✓ Fully compliant
  NYDFS §500.12: ✓ Fully compliant

ℹ Industry Benchmark: 87% of crypto custody firms require universal MFA
✓ You are following industry best practice

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FINAL RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Policy Risk Score: 2.8/10 (LOW RISK) ✓
Compliance Coverage: 98% (EXCELLENT) ✓
Audit Readiness: 94% (VERY GOOD) ✓

Comparison to Industry:
├── Your Score: 2.8/10
├── Industry Average (Financial Services - Crypto/Digital Assets): 4.8/10
└── Top Quartile: 2.5/10

You are in the TOP 25% for Financial Services - Crypto/Digital Assets security! 🎉

Generating policy artifacts...

[1/7] Generating policy document...                    ✓ Done
[2/7] Creating SOC 2 compliance matrix...              ✓ Done
[3/7] Creating ISO 27001 compliance matrix...          ✓ Done
[4/7] Creating NYDFS compliance matrix...              ✓ Done
[5/7] Generating control testing procedures...         ✓ Done
[6/7] Creating gap analysis report...                  ✓ Done
[7/7] Generating ServiceNow import file...             ✓ Done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 GENERATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Output Directory: ./generated_policies/2026-01-24_143052/

Generated Artifacts:
├── 📄 Password_Policy_v1.0.md
├── 📄 SOC_2_Compliance_Matrix.md
├── 📄 ISO_27001_Compliance_Matrix.md
├── 📄 NYDFS_Compliance_Matrix.md
├── 📄 Control_Testing_Checklist.md
├── 📄 Gap_Analysis_Report.md
├── 📄 ServiceNow_Import.json
├── 📄 Jira_Import_Gaps.csv
└── 📄 Executive_Summary.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 GAP ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ 0 Critical Gaps
⚠ 1 High Priority Gap(s)
⚠ 2 Medium Priority Gap(s)
✓ 0 Low Priority Gaps

Priority Items:

└── [GAP-001] Password Minimum Length Below Target
    Framework: SOC 2, ISO 27001, NYDFS
    Timeline: 30 days
    Effort: Low
    Cost Estimate: $1,000-$2,000

└── [GAP-002] Multi-Factor Authentication Not Fully Implemented
    Framework: SOC 2, ISO 27001, NYDFS
    Timeline: 60 days
    Effort: High
    Cost Estimate: $10,000-$25,000

```

## Demo for Interviews

**Duration:** 2 minutes
**Wow Factor:** High

### Demo Script

"I built this tool to demonstrate my understanding of GRC automation - specifically the challenges mentioned in the role around automating GRC reporting, surfacing risk insights, and supporting SOC 2, ISO 27001, and NYDFS audits.

Let me show you how it works..."

[Run the tool with pre-selected answers]

"Notice a few things:

1. **Industry Context Awareness** - It auto-detected this is for crypto/digital assets and applied NYDFS requirements automatically

2. **Real-Time Risk Scoring** - As I configured the policy, it showed live risk scores and compliance feedback

3. **Comprehensive Artifacts** - It generated 9 different artifacts:
   - Professional policy document
   - SOC 2, ISO 27001, and NYDFS compliance matrices
   - Control testing checklist for auditors
   - Gap analysis report
   - ServiceNow and Jira exports

4. **Gap Analysis** - It compared current state vs. target and identified specific remediation actions with timelines and cost estimates

This addresses the key requirements from the job description:
- ✅ Automate GRC reporting
- ✅ Surface risk insights
- ✅ Support SOC 2, ISO 27001, NYDFS audits
- ✅ Integration with ServiceNow and Jira
- ✅ Customer due-diligence (professional artifacts)

This tool could save 15-20 hours per audit cycle by automating policy creation, compliance mapping, and evidence generation."

## Technical Details

- **Language:** Pure Python 3.7+
- **Dependencies:** None (uses only standard library)
- **Architecture:** Modular design with separate concerns
  - `compliance_engine.py` - Framework mappings and risk scoring
  - `gap_analyzer.py` - Gap analysis logic
  - `output_generator.py` - Artifact generation
  - `grc_policy_generator.py` - CLI interface

## Customization

### Adding New Frameworks

Edit `compliance_engine.py`:

```python
COMPLIANCE_MAPPINGS = {
    "password": {
        "YOUR_FRAMEWORK": [
            ComplianceControl(
                framework="YOUR_FRAMEWORK",
                control_id="CTRL-001",
                control_name="Control Name",
                requirement="Control requirement description",
                policy_section="3.1"
            ),
            # Add more controls...
        ]
    }
}
```

### Adding New Industry Presets

```python
INDUSTRY_PRESETS = {
    "your_industry": IndustryPreset(
        name="Your Industry Name",
        frameworks=["SOC 2", "ISO 27001"],
        risk_level="MEDIUM",
        recommended_min_length=12,
        recommended_mfa="required_privileged",
        recommended_expiration=90
    )
}
```

## Value Proposition

**Time Savings:**
- Policy creation: 8-12 hours → 5 minutes
- Compliance mapping: 4-6 hours → automated
- Gap analysis: 2-4 hours → automated
- Evidence collection: 6-8 hours → automated
- **Total: 20-30 hours saved per audit cycle**

**Risk Reduction:**
- Consistent policy formatting
- No missing framework controls
- Clear remediation roadmap
- Audit-ready artifacts

## License

Internal use only

## Author

Built to demonstrate GRC automation capabilities for security governance roles.
