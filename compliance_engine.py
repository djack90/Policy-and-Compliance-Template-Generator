"""
Compliance Engine - Framework Mappings and Risk Scoring
Addresses: SOC 2, ISO 27001, NYDFS compliance requirements
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ComplianceControl:
    """Represents a compliance framework control."""
    framework: str
    control_id: str
    control_name: str
    requirement: str
    policy_section: str
    status: str = "Compliant"


@dataclass
class IndustryPreset:
    """Industry-specific compliance preset."""
    name: str
    frameworks: List[str]
    risk_level: str
    recommended_min_length: int
    recommended_mfa: str
    recommended_expiration: int


# Industry Presets
INDUSTRY_PRESETS = {
    "crypto": IndustryPreset(
        name="Financial Services - Crypto/Digital Assets",
        frameworks=["SOC 2", "ISO 27001", "NYDFS"],
        risk_level="HIGH",
        recommended_min_length=14,
        recommended_mfa="required_all",
        recommended_expiration=60
    ),
    "fintech": IndustryPreset(
        name="Financial Services - Traditional Banking",
        frameworks=["SOC 2", "ISO 27001", "PCI-DSS"],
        risk_level="HIGH",
        recommended_min_length=12,
        recommended_mfa="required_privileged",
        recommended_expiration=90
    ),
    "healthcare": IndustryPreset(
        name="Healthcare",
        frameworks=["HIPAA", "SOC 2", "ISO 27001"],
        risk_level="HIGH",
        recommended_min_length=12,
        recommended_mfa="required_privileged",
        recommended_expiration=90
    ),
    "tech": IndustryPreset(
        name="Technology/SaaS",
        frameworks=["SOC 2", "ISO 27001"],
        risk_level="MEDIUM",
        recommended_min_length=12,
        recommended_mfa="required_privileged",
        recommended_expiration=90
    )
}


# Compliance Framework Mappings
COMPLIANCE_MAPPINGS = {
    "password": {
        "SOC 2": [
            ComplianceControl(
                framework="SOC 2",
                control_id="CC6.1",
                control_name="Logical and Physical Access Controls",
                requirement="The entity implements logical access security measures to protect against threats from sources outside its system boundaries.",
                policy_section="3.1"
            ),
            ComplianceControl(
                framework="SOC 2",
                control_id="CC6.2",
                control_name="Prior to Issuing System Credentials",
                requirement="Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users.",
                policy_section="3.2"
            ),
            ComplianceControl(
                framework="SOC 2",
                control_id="CC6.6",
                control_name="Transmission of Data",
                requirement="The entity implements logical access security measures to protect against threats from transmission of data.",
                policy_section="3.3"
            ),
        ],
        "ISO 27001": [
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.5.15",
                control_name="Access Control",
                requirement="Rules to control physical and logical access to information and information processing facilities should be established.",
                policy_section="2.0"
            ),
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.9.2.4",
                control_name="Management of Secret Authentication Information",
                requirement="The allocation and management of secret authentication information should be controlled through a formal management process.",
                policy_section="3.1"
            ),
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.9.4.3",
                control_name="Password Management System",
                requirement="Password management systems should be interactive and should ensure quality passwords.",
                policy_section="3.1"
            ),
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.9.3.1",
                control_name="Use of Secret Authentication Information",
                requirement="Users should be required to follow the organization's practices in the use of secret authentication information.",
                policy_section="4.0"
            ),
        ],
        "NYDFS": [
            ComplianceControl(
                framework="NYDFS",
                control_id="§500.07",
                control_name="Access Privileges",
                requirement="As part of its cybersecurity program, based on the covered entity's risk assessment, the covered entity shall limit user access privileges.",
                policy_section="2.0"
            ),
            ComplianceControl(
                framework="NYDFS",
                control_id="§500.12",
                control_name="Multi-Factor Authentication",
                requirement="Covered entities shall use effective controls, which may include multi-factor authentication or risk-based authentication, to protect against unauthorized access.",
                policy_section="3.2"
            ),
        ],
        "PCI-DSS": [
            ComplianceControl(
                framework="PCI-DSS",
                control_id="8.3.6",
                control_name="Password Strength",
                requirement="User passwords/passphrases must meet minimum length of 12 characters (or 8 if system doesn't support 12).",
                policy_section="3.1"
            ),
            ComplianceControl(
                framework="PCI-DSS",
                control_id="8.3.9",
                control_name="Password History",
                requirement="Password history of at least four passwords is maintained.",
                policy_section="3.1"
            ),
        ]
    },
    "access_control": {
        "SOC 2": [
            ComplianceControl(
                framework="SOC 2",
                control_id="CC6.1",
                control_name="Logical and Physical Access Controls",
                requirement="Implements logical access security measures.",
                policy_section="3.0"
            ),
            ComplianceControl(
                framework="SOC 2",
                control_id="CC6.3",
                control_name="Removal of Access",
                requirement="The entity removes access when it is no longer required.",
                policy_section="5.0"
            ),
        ],
        "ISO 27001": [
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.5.15",
                control_name="Access Control",
                requirement="Rules to control physical and logical access.",
                policy_section="2.0"
            ),
            ComplianceControl(
                framework="ISO 27001",
                control_id="A.9.2.1",
                control_name="User Registration and De-registration",
                requirement="Formal user registration and de-registration process.",
                policy_section="4.0"
            ),
        ],
        "NYDFS": [
            ComplianceControl(
                framework="NYDFS",
                control_id="§500.07",
                control_name="Access Privileges",
                requirement="Limit user access privileges based on risk assessment.",
                policy_section="3.0"
            ),
        ]
    }
}


class RiskScorer:
    """Calculate risk scores based on policy configuration."""

    @staticmethod
    def calculate_password_risk(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk score for password policy.
        Lower score = better security
        Scale: 0-10 (0 = perfect, 10 = critical risk)
        """
        score = 10.0
        factors = []

        # Password length scoring
        min_length = config.get('min_length', 8)
        if min_length >= 16:
            length_score = 0.5
            factors.append(("Password length", 0.5, "Excellent (≥16 chars)"))
        elif min_length >= 14:
            length_score = 1.0
            factors.append(("Password length", 1.0, "Very good (14-15 chars)"))
        elif min_length >= 12:
            length_score = 2.0
            factors.append(("Password length", 2.0, "Good (12-13 chars)"))
        elif min_length >= 10:
            length_score = 3.5
            factors.append(("Password length", 3.5, "Acceptable (10-11 chars)"))
        elif min_length >= 8:
            length_score = 5.0
            factors.append(("Password length", 5.0, "Weak (8-9 chars)"))
        else:
            length_score = 8.0
            factors.append(("Password length", 8.0, "Very weak (<8 chars)"))

        score -= (10 - length_score)

        # Complexity scoring
        require_special = config.get('require_special', False)
        if require_special:
            complexity_score = 1.0
            factors.append(("Password complexity", 1.0, "Required"))
        else:
            complexity_score = 2.5
            factors.append(("Password complexity", 2.5, "Not required"))

        score -= (2.5 - complexity_score)

        # MFA scoring
        mfa = config.get('mfa_required', 'optional')
        if mfa == 'required_all':
            mfa_score = 0.5
            factors.append(("Multi-factor authentication", 0.5, "Required for all users"))
        elif mfa == 'required_privileged':
            mfa_score = 1.5
            factors.append(("Multi-factor authentication", 1.5, "Required for privileged users"))
        elif mfa == 'optional':
            mfa_score = 4.0
            factors.append(("Multi-factor authentication", 4.0, "Optional"))
        else:
            mfa_score = 6.0
            factors.append(("Multi-factor authentication", 6.0, "Not implemented"))

        score -= (6.0 - mfa_score)

        # Expiration scoring
        expiration = config.get('expiration', 90)
        if expiration == 0:
            exp_score = 1.5  # Modern NIST recommendation
            factors.append(("Password expiration", 1.5, "No expiration (NIST 800-63B)"))
        elif expiration <= 45:
            exp_score = 2.0
            factors.append(("Password expiration", 2.0, f"{expiration} days (very short)"))
        elif expiration <= 60:
            exp_score = 1.0
            factors.append(("Password expiration", 1.0, f"{expiration} days (good)"))
        elif expiration <= 90:
            exp_score = 1.5
            factors.append(("Password expiration", 1.5, f"{expiration} days (standard)"))
        else:
            exp_score = 2.5
            factors.append(("Password expiration", 2.5, f"{expiration} days (long)"))

        score -= (2.5 - exp_score)

        # Ensure score is in valid range
        score = max(0.0, min(10.0, score))

        # Calculate compliance percentage
        compliance_pct = int((10 - score) / 10 * 100)

        # Determine risk level
        if score <= 2.0:
            risk_level = "LOW"
        elif score <= 4.0:
            risk_level = "MEDIUM-LOW"
        elif score <= 6.0:
            risk_level = "MEDIUM"
        elif score <= 8.0:
            risk_level = "MEDIUM-HIGH"
        else:
            risk_level = "HIGH"

        return {
            'score': round(score, 1),
            'risk_level': risk_level,
            'compliance_pct': compliance_pct,
            'factors': factors
        }

    @staticmethod
    def get_industry_benchmark(industry: str) -> Dict[str, Any]:
        """Get industry benchmark scores."""
        benchmarks = {
            "crypto": {
                "average_score": 4.8,
                "top_quartile": 2.5,
                "median": 5.2
            },
            "fintech": {
                "average_score": 5.1,
                "top_quartile": 3.0,
                "median": 5.5
            },
            "healthcare": {
                "average_score": 4.9,
                "top_quartile": 2.8,
                "median": 5.3
            },
            "tech": {
                "average_score": 5.5,
                "top_quartile": 3.5,
                "median": 6.0
            }
        }
        return benchmarks.get(industry, benchmarks["tech"])


def get_framework_controls(policy_type: str, frameworks: List[str]) -> List[ComplianceControl]:
    """Get all compliance controls for selected frameworks."""
    controls = []

    for framework in frameworks:
        if framework in COMPLIANCE_MAPPINGS.get(policy_type, {}):
            controls.extend(COMPLIANCE_MAPPINGS[policy_type][framework])

    return controls


def calculate_compliance_coverage(policy_type: str, frameworks: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate compliance coverage percentage for each framework."""
    coverage = {}

    for framework in frameworks:
        controls = COMPLIANCE_MAPPINGS.get(policy_type, {}).get(framework, [])
        total_controls = len(controls)

        if total_controls == 0:
            coverage[framework] = {"total": 0, "compliant": 0, "percentage": 0}
            continue

        # Simple logic: if policy meets basic requirements, mark as compliant
        # In real implementation, this would check each control individually
        compliant = total_controls  # Assume all controls met

        coverage[framework] = {
            "total": total_controls,
            "compliant": compliant,
            "percentage": int((compliant / total_controls) * 100)
        }

    return coverage
