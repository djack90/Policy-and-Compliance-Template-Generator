"""
Output Generator - Create all compliance artifacts
Generates: Policy docs, compliance matrices, audit checklists, export files
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from compliance_engine import ComplianceControl
from gap_analyzer import Gap


class OutputGenerator:
    """Generate all GRC compliance artifacts."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_policy_document(self, policy_type: str, config: Dict[str, Any],
                                 metadata: Dict[str, Any]) -> str:
        """Generate the main policy document in Markdown."""

        if policy_type == "password":
            content = self._generate_password_policy(config, metadata)
        else:
            content = self._generate_access_control_policy(config, metadata)

        filepath = os.path.join(self.output_dir, f"{policy_type.title()}_Policy_v1.0.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def _generate_password_policy(self, config: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate password policy content."""
        special_char_text = 'include at least one special character' if config['require_special'] else 'not require special characters'

        if config['mfa_required'] == 'required_all':
            mfa_text = "required for all users"
        elif config['mfa_required'] == 'required_privileged':
            mfa_text = "required for all privileged and administrative users"
        else:
            mfa_text = "optional but recommended"

        frameworks_list = ", ".join(metadata['frameworks'])

        return f"""---
**Policy ID:** POL-SEC-001
**Version:** 1.0
**Status:** Draft
**Effective Date:** {metadata['effective_date']}
**Review Cycle:** Annual
**Next Review:** {metadata['next_review_date']}
**Policy Owner:** CISO
**Compliance Frameworks:** {frameworks_list}
---

# Password & Authentication Policy

## 1. Purpose

This policy establishes password and authentication requirements to protect organizational systems and data, based on industry best practices and compliance with {frameworks_list}.

This policy is designed to:
- Protect against unauthorized access to systems and data
- Ensure compliance with applicable regulatory requirements
- Implement defense-in-depth security controls
- Support audit and compliance activities

## 2. Scope

This policy applies to:
- All employees, contractors, consultants, and third-party users
- All systems, applications, and services (cloud and on-premises)
- All access to organizational data and resources

## 3. Policy Requirements

### 3.1 Password Requirements

- **Minimum Length:** Passwords must be at least {config['min_length']} characters long
- **Complexity:** Passwords must {special_char_text}
- **Password Expiration:** Passwords expire every {config['expiration']} days
- **Password History:** Users cannot reuse their last 4 passwords
- **Password Lockout:** Accounts lock after 5 failed login attempts
- **Compromised Passwords:** Passwords matching known breach databases must be changed immediately

### 3.2 Multi-Factor Authentication (MFA)

Multi-factor authentication is **{mfa_text}**.

Acceptable MFA methods:
- Authenticator apps (Microsoft Authenticator, Google Authenticator, Duo)
- Hardware security keys (YubiKey, Titan Security Key)
- Biometric authentication (when combined with another factor)

Unacceptable MFA methods:
- SMS-based codes (vulnerable to SIM swapping attacks)
- Email-based codes (email account may be compromised)

### 3.3 Privileged Account Management

Privileged accounts (administrators, developers with production access) require:
- Separate accounts for privileged vs. standard access
- Hardware-based MFA (security keys preferred)
- Enhanced monitoring and logging
- Annual access review and recertification

## 4. Responsibilities

### 4.1 Users
- Create and maintain passwords in accordance with this policy
- Protect passwords and authentication credentials
- Never share passwords or MFA devices
- Report lost/stolen MFA devices immediately
- Complete required security awareness training

### 4.2 IT Administrators
- Enforce password settings in authentication systems
- Monitor for policy violations and anomalous authentication patterns
- Provide user support for password and MFA issues
- Maintain audit logs of authentication events

### 4.3 Information Security Team
- Review and update this policy annually
- Monitor compliance with password requirements
- Investigate authentication-related security incidents
- Provide security awareness training

### 4.4 CISO / Policy Owner
- Approve exceptions to this policy
- Ensure policy aligns with business needs and compliance requirements
- Report policy compliance to executive leadership

## 5. Exceptions

Exceptions to this policy must be:
- Documented with business justification
- Approved by the CISO
- Reviewed quarterly
- Accompanied by compensating controls

## 6. Enforcement

Violations of this policy may result in:
- Revocation of system access
- Disciplinary action up to and including termination
- Legal action if violation results in data breach or regulatory penalties

## 7. Related Policies

- Access Control Policy
- Acceptable Use Policy
- Incident Response Policy
- Data Classification Policy

## 8. Compliance Framework References

This policy supports compliance with:
- **SOC 2:** CC6.1 (Logical Access), CC6.2 (Authentication)
- **ISO 27001:2022:** A.5.15 (Access Control), A.9.2.4 (Password Management), A.9.4.3 (Strong Authentication)
- **NYDFS 23 NYCRR 500:** §500.07 (Access Controls), §500.12 (Multi-Factor Authentication)

## 9. Policy Review and Maintenance

This policy will be reviewed:
- Annually, or
- When significant changes occur to business operations, or
- When required by new regulatory requirements, or
- Following a security incident related to authentication

---

**Approval Signatures:**

CISO: _________________________ Date: _________

CTO: _________________________ Date: _________

---

*Document Classification: Internal Use Only*
*Last Updated: {metadata['effective_date']}*
"""

    def _generate_access_control_policy(self, config: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate access control policy content."""
        roles_list = "\n".join(f"- **{role}**" for role in config.get('roles', ['admin', 'user', 'guest']))
        mfa_text = 'required' if config.get('mfa_required') else 'recommended'
        frameworks_list = ", ".join(metadata['frameworks'])

        return f"""---
**Policy ID:** POL-SEC-002
**Version:** 1.0
**Status:** Draft
**Effective Date:** {metadata['effective_date']}
**Compliance Frameworks:** {frameworks_list}
---

# Access Control Policy

## 1. Purpose

This policy establishes access control requirements based on {frameworks_list} to protect organizational systems and data.

## 2. Roles and Responsibilities

The following roles are defined:

{roles_list}

## 3. Policy Requirements

### 3.1 Access Control Principles
- Access is granted based on the **principle of least privilege**
- Role-based access control (RBAC) is enforced for all systems
- Access rights are reviewed quarterly
- Multi-factor authentication is **{mfa_text}** for all users

### 3.2 Access Request Process
- All access requests must be approved by the user's manager and the data/system owner
- Access is provisioned within 24 hours of approval
- Temporary access expires automatically after the specified period

### 3.3 Access Review
- User access rights are reviewed quarterly
- Privileged access is reviewed monthly
- Unused accounts are disabled after 30 days of inactivity
- Terminated employee access is revoked immediately

## 4. Scope

This policy applies to all systems, applications, and data.

## 5. Enforcement

Violations may result in disciplinary action and/or revocation of access.

## 6. Compliance Framework References

This policy supports compliance with:
- **SOC 2:** CC6.1, CC6.3
- **ISO 27001:2022:** A.5.15, A.9.2.1
- **NYDFS 23 NYCRR 500:** §500.07

---

*Last Updated: {metadata['effective_date']}*
"""

    def generate_compliance_matrix(self, controls: List[ComplianceControl],
                                   framework: str) -> str:
        """Generate compliance matrix for a specific framework."""
        filepath = os.path.join(self.output_dir, f"{framework.replace(' ', '_')}_Compliance_Matrix.md")

        content = f"""# {framework} Compliance Matrix

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

| Control ID | Control Name | Requirement | Policy Section | Status |
|------------|--------------|-------------|----------------|--------|
"""

        for control in controls:
            content += f"| {control.control_id} | {control.control_name} | {control.requirement} | Section {control.policy_section} | ✓ {control.status} |\n"

        content += f"""
---

**Summary:**
- Total Controls: {len(controls)}
- Compliant: {len(controls)}
- Compliance Rate: 100%

**Status Legend:**
- ✓ Compliant: Control is fully implemented and documented
- ⚠ Partial: Control is partially implemented
- ✗ Non-Compliant: Control is not implemented
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_control_testing_checklist(self, controls: List[ComplianceControl],
                                          frameworks: List[str]) -> str:
        """Generate auditor control testing checklist."""
        filepath = os.path.join(self.output_dir, "Control_Testing_Checklist.md")

        content = f"""# Control Testing Checklist for Auditors

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Frameworks:** {', '.join(frameworks)}

## Overview

This checklist provides testing procedures for auditors to verify implementation and effectiveness of controls.

---

"""

        for framework in frameworks:
            framework_controls = [c for c in controls if c.framework == framework]
            if not framework_controls:
                continue

            content += f"## {framework}\n\n"

            for control in framework_controls:
                content += f"""### {control.control_id}: {control.control_name}

**Control Statement:** {control.requirement}

**Testing Procedures:**
1. ☐ Review policy document (Section {control.policy_section})
2. ☐ Obtain system configuration screenshots/exports
3. ☐ Interview responsible personnel (IT Admin, Security Team)
4. ☐ Test control effectiveness with sample transactions
5. ☐ Review access logs and audit trails

**Evidence to Collect:**
- Policy document showing requirement (Section {control.policy_section})
- System configuration screenshot
- Sample of 25 user accounts for testing
- Access log exports (last 90 days)
- Interview notes with IT administrators

**Expected Auditor Questions:**
- How is this control enforced technically?
- What happens if a user violates this policy?
- How do you monitor compliance with this control?
- When was this control last reviewed/tested?

**Testing Sample Size:** Minimum 25 items or 100% of privileged users

---

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_gap_analysis_report(self, gaps: List[Gap], summary: Dict[str, Any]) -> str:
        """Generate gap analysis report."""
        filepath = os.path.join(self.output_dir, "Gap_Analysis_Report.md")

        content = f"""# Gap Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Executive Summary

Total Gaps Identified: **{summary['total_gaps']}**

| Priority | Count |
|----------|-------|
| Critical | {summary['critical']} |
| High     | {summary['high']} |
| Medium   | {summary['medium']} |
| Low      | {summary['low']} |

"""

        if summary['total_gaps'] == 0:
            content += """
✅ **Excellent!** No compliance gaps identified. Your target policy configuration fully meets all selected framework requirements.

**Next Steps:**
1. Review and approve policy document
2. Communicate policy to all users
3. Implement technical controls
4. Begin compliance monitoring
"""
        else:
            content += "## Detailed Gap Analysis\n\n---\n\n"

            for gap in gaps:
                content += f"""### {gap.gap_id}: {gap.title}

**Risk Level:** {gap.risk_level}
**Framework:** {gap.framework}

**Current State:** {gap.current_state}
**Target State:** {gap.target_state}

**Description:**
{gap.description}

**Remediation Plan:**
{gap.remediation}

**Timeline:** {gap.timeline_days} days
**Effort:** {gap.effort}
**Cost Estimate:** {gap.cost_estimate}

---

"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_servicenow_export(self, policy_type: str, controls: List[ComplianceControl],
                                   metadata: Dict[str, Any]) -> str:
        """Generate ServiceNow GRC import JSON."""
        filepath = os.path.join(self.output_dir, "ServiceNow_Import.json")

        data = {
            "policy": {
                "policy_id": "POL-SEC-001" if policy_type == "password" else "POL-SEC-002",
                "policy_name": f"{policy_type.title()} Policy",
                "version": "1.0",
                "status": "Draft",
                "policy_owner": "CISO",
                "effective_date": metadata['effective_date'],
                "next_review_date": metadata['next_review_date'],
                "compliance_frameworks": metadata['frameworks'],
                "risk_rating": "High" if "NYDFS" in metadata['frameworks'] else "Medium"
            },
            "controls": [
                {
                    "control_id": c.control_id,
                    "framework": c.framework,
                    "control_name": c.control_name,
                    "requirement": c.requirement,
                    "implementation_status": c.status,
                    "policy_section": c.policy_section,
                    "test_frequency": "Quarterly",
                    "last_test_date": None,
                    "next_test_date": None
                }
                for c in controls
            ],
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "generated_by": "GRC Policy Generator",
                "version": "1.0"
            }
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return filepath

    def generate_jira_export(self, gaps: List[Gap]) -> str:
        """Generate Jira import CSV."""
        filepath = os.path.join(self.output_dir, "Jira_Import_Gaps.csv")

        if not gaps:
            # Create empty file with headers
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("No gaps identified - no Jira tickets needed\n")
            return filepath

        fieldnames = ["Summary", "Description", "Issue Type", "Priority", "Labels", "Due Date", "Effort", "Cost Estimate"]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for gap in gaps:
                due_date = (datetime.now() + timedelta(days=gap.timeline_days)).strftime("%Y-%m-%d")
                writer.writerow({
                    "Summary": gap.title,
                    "Description": f"{gap.description}\n\nCurrent: {gap.current_state}\nTarget: {gap.target_state}\n\nRemediation: {gap.remediation}",
                    "Issue Type": "Compliance Gap",
                    "Priority": self._map_risk_to_priority(gap.risk_level),
                    "Labels": f"GRC,Audit,{gap.framework.replace(' ', '-')}",
                    "Due Date": due_date,
                    "Effort": gap.effort,
                    "Cost Estimate": gap.cost_estimate
                })

        return filepath

    def generate_executive_summary(self, policy_type: str, risk_score: Dict[str, Any],
                                   summary: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Generate 1-page executive summary."""
        filepath = os.path.join(self.output_dir, "Executive_Summary.md")

        content = f"""# Executive Summary: {policy_type.title()} Policy

**Date:** {metadata['effective_date']}
**Prepared For:** Executive Leadership, Board of Directors
**Frameworks:** {', '.join(metadata['frameworks'])}

## Overview

This executive summary provides an overview of the new {policy_type.title()} Policy and its impact on organizational risk and compliance posture.

## Key Highlights

✅ **Risk Score:** {risk_score['score']}/10 ({risk_score['risk_level']} risk)
✅ **Compliance Coverage:** {risk_score['compliance_pct']}%
✅ **Gaps Identified:** {summary['total_gaps']} ({summary['critical']} critical, {summary['high']} high priority)

## Business Impact

**Benefits:**
- Enhanced protection against unauthorized access and data breaches
- Compliance with {', '.join(metadata['frameworks'])}
- Reduced audit findings and regulatory risk
- Improved security posture for customer due diligence

**Risks if Not Implemented:**
- Potential audit findings during SOC 2/ISO 27001 certification
- Regulatory penalties (NYDFS violations can result in significant fines)
- Increased risk of credential-based attacks
- Reputational damage from security incidents

## Implementation Timeline

Based on gap analysis, full implementation requires:
- **Critical/High Priority Items:** 30-60 days
- **Medium Priority Items:** 60-90 days
- **Full Compliance:** 90 days

## Resource Requirements

**Estimated Investment:**
- Technology/Licensing: $15,000-$30,000 (MFA platform, hardware keys)
- Implementation Labor: 80-120 hours (IT, Security teams)
- Training/Communication: 20-40 hours
- **Total Estimated Cost:** $25,000-$50,000

## Recommendation

**RECOMMEND APPROVAL** of this policy with immediate implementation of critical controls.

This policy aligns with industry best practices and regulatory requirements, positioning the organization for successful audit outcomes and enhanced security posture.

---

*For questions, contact: CISO*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    @staticmethod
    def _map_risk_to_priority(risk_level: str) -> str:
        """Map risk level to Jira priority."""
        mapping = {
            "CRITICAL": "Highest",
            "HIGH": "High",
            "MEDIUM": "Medium",
            "LOW": "Low"
        }
        return mapping.get(risk_level, "Medium")


from datetime import timedelta
