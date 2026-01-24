"""
Gap Analyzer - Compare current state vs target state
Surfaces risk insights and generates actionable recommendations
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Gap:
    """Represents a compliance gap."""
    gap_id: str
    title: str
    description: str
    current_state: str
    target_state: str
    risk_level: str  # CRITICAL, HIGH, MEDIUM, LOW
    framework: str
    remediation: str
    timeline_days: int
    effort: str  # Low, Medium, High
    cost_estimate: str


class GapAnalyzer:
    """Analyze gaps between current and target state."""

    def __init__(self, current_state: Dict[str, Any], target_state: Dict[str, Any], frameworks: List[str]):
        self.current_state = current_state
        self.target_state = target_state
        self.frameworks = frameworks
        self.gaps: List[Gap] = []

    def analyze(self) -> List[Gap]:
        """Perform gap analysis and return list of gaps."""
        self.gaps = []

        # Analyze password length
        self._analyze_password_length()

        # Analyze MFA
        self._analyze_mfa()

        # Analyze password complexity
        self._analyze_complexity()

        # Analyze expiration
        self._analyze_expiration()

        # Analyze hardware tokens
        self._analyze_hardware_tokens()

        return self.gaps

    def _analyze_password_length(self):
        """Analyze password length gap."""
        current_length = self.current_state.get('min_length', 0)
        target_length = self.target_state.get('min_length', 8)

        if current_length < target_length:
            gap_size = target_length - current_length

            if gap_size >= 6:
                risk = "HIGH"
                timeline = 30
            elif gap_size >= 4:
                risk = "MEDIUM"
                timeline = 60
            else:
                risk = "LOW"
                timeline = 90

            frameworks_text = ", ".join(self.frameworks)

            self.gaps.append(Gap(
                gap_id=f"GAP-{len(self.gaps)+1:03d}",
                title="Password Minimum Length Below Target",
                description=f"Current password length ({current_length} chars) is below target ({target_length} chars)",
                current_state=f"{current_length} characters minimum",
                target_state=f"{target_length} characters minimum",
                risk_level=risk,
                framework=frameworks_text,
                remediation=f"Update password policy in Active Directory/authentication system to enforce {target_length} character minimum. Communicate change to users 14 days in advance.",
                timeline_days=timeline,
                effort="Low",
                cost_estimate="$1,000-$2,000 (primarily communication and user support)"
            ))

    def _analyze_mfa(self):
        """Analyze MFA gap."""
        current_mfa = self.current_state.get('mfa_status', 'none')
        target_mfa = self.target_state.get('mfa_required', 'optional')
        current_adoption = self.current_state.get('mfa_adoption_pct', 0)

        # Check if there's a gap
        gap_exists = False
        risk = "LOW"
        timeline = 90

        if target_mfa == 'required_all' and current_mfa != 'required_all':
            gap_exists = True
            risk = "CRITICAL" if "NYDFS" in self.frameworks else "HIGH"
            timeline = 60 if risk == "CRITICAL" else 90
            current_desc = f"MFA {current_mfa.replace('_', ' ')} ({current_adoption}% adoption)"
            target_desc = "MFA required for all users (100% adoption)"

        elif target_mfa == 'required_privileged' and current_mfa in ['none', 'optional']:
            gap_exists = True
            risk = "HIGH"
            timeline = 60
            current_desc = f"MFA {current_mfa.replace('_', ' ')}"
            target_desc = "MFA required for privileged users"

        if gap_exists:
            frameworks_text = ", ".join(self.frameworks)

            self.gaps.append(Gap(
                gap_id=f"GAP-{len(self.gaps)+1:03d}",
                title="Multi-Factor Authentication Not Fully Implemented",
                description=f"MFA implementation does not meet target requirements for {frameworks_text}",
                current_state=current_desc,
                target_state=target_desc,
                risk_level=risk,
                framework=frameworks_text,
                remediation="Deploy MFA solution (e.g., Okta, Duo, Microsoft Authenticator). Enroll users in phases. Provide training and support. Monitor adoption rates.",
                timeline_days=timeline,
                effort="Medium" if target_mfa == 'required_privileged' else "High",
                cost_estimate="$10,000-$25,000 (MFA licenses + deployment)" if target_mfa == 'required_all' else "$5,000-$10,000"
            ))

    def _analyze_complexity(self):
        """Analyze password complexity gap."""
        current_complexity = self.current_state.get('has_complexity', False)
        target_complexity = self.target_state.get('require_special', False)

        if target_complexity and not current_complexity:
            self.gaps.append(Gap(
                gap_id=f"GAP-{len(self.gaps)+1:03d}",
                title="Password Complexity Requirements Not Enforced",
                description="Current policy does not enforce special character requirements",
                current_state="No complexity requirements",
                target_state="Special characters required",
                risk_level="MEDIUM",
                framework=", ".join(self.frameworks),
                remediation="Enable password complexity rules in authentication system. Require users to update passwords at next login.",
                timeline_days=30,
                effort="Low",
                cost_estimate="$500-$1,000 (configuration + communication)"
            ))

    def _analyze_expiration(self):
        """Analyze password expiration gap."""
        current_exp = self.current_state.get('expiration_days', 999)
        target_exp = self.target_state.get('expiration', 90)

        # Only flag if current is significantly longer than target
        if current_exp > target_exp + 30:
            self.gaps.append(Gap(
                gap_id=f"GAP-{len(self.gaps)+1:03d}",
                title="Password Expiration Period Too Long",
                description=f"Current expiration ({current_exp} days) exceeds target ({target_exp} days)",
                current_state=f"{current_exp} days" if current_exp < 900 else "No expiration",
                target_state=f"{target_exp} days",
                risk_level="LOW",
                framework=", ".join(self.frameworks),
                remediation=f"Update password expiration policy to {target_exp} days. Consider implementing password breach detection as compensating control.",
                timeline_days=60,
                effort="Low",
                cost_estimate="$500-$1,000"
            ))

    def _analyze_hardware_tokens(self):
        """Analyze hardware token gap for privileged users."""
        has_hardware_tokens = self.current_state.get('has_hardware_tokens', False)
        target_mfa = self.target_state.get('mfa_required', 'optional')

        # For crypto/high-risk, recommend hardware tokens for admins
        if target_mfa in ['required_all', 'required_privileged'] and not has_hardware_tokens:
            if "NYDFS" in self.frameworks or "crypto" in self.current_state.get('industry', '').lower():
                self.gaps.append(Gap(
                    gap_id=f"GAP-{len(self.gaps)+1:03d}",
                    title="Hardware Security Keys for Privileged Users",
                    description="Best practice for crypto/digital asset custody: hardware tokens for admins",
                    current_state="Software-based MFA only",
                    target_state="Hardware security keys (YubiKey/Titan) for privileged users",
                    risk_level="MEDIUM",
                    framework="NYDFS Best Practice, ISO 27001 A.9.4.3",
                    remediation="Procure hardware security keys (YubiKey 5 or Google Titan). Deploy to all privileged users (admins, developers with production access). Require enrollment within 30 days.",
                    timeline_days=90,
                    effort="Medium",
                    cost_estimate="$5,000-$10,000 (50-100 keys @ $50-100 each + deployment)"
                ))

    def get_summary(self) -> Dict[str, Any]:
        """Get gap analysis summary."""
        critical = sum(1 for g in self.gaps if g.risk_level == "CRITICAL")
        high = sum(1 for g in self.gaps if g.risk_level == "HIGH")
        medium = sum(1 for g in self.gaps if g.risk_level == "MEDIUM")
        low = sum(1 for g in self.gaps if g.risk_level == "LOW")

        return {
            "total_gaps": len(self.gaps),
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "has_critical": critical > 0,
            "has_high": high > 0
        }

    def generate_jira_export(self) -> List[Dict[str, str]]:
        """Generate Jira-compatible CSV data."""
        jira_items = []

        for gap in self.gaps:
            due_date = (datetime.now() + timedelta(days=gap.timeline_days)).strftime("%Y-%m-%d")

            jira_items.append({
                "Summary": gap.title,
                "Description": f"{gap.description}\n\nCurrent State: {gap.current_state}\nTarget State: {gap.target_state}\n\nRemediation:\n{gap.remediation}",
                "Issue Type": "Compliance Gap",
                "Priority": self._map_risk_to_priority(gap.risk_level),
                "Labels": f"GRC,Audit,{gap.framework.replace(' ', '-').replace(',', '')}",
                "Due Date": due_date,
                "Custom Field (Effort)": gap.effort,
                "Custom Field (Cost Estimate)": gap.cost_estimate
            })

        return jira_items

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
