# Demo Script for Interview

## Setup (Before Interview)

1. Navigate to the tool directory:
```bash
cd grc_policy_generator
```

2. Have this ready to run:
```bash
python3 grc_policy_generator.py
```

## Demo Flow (2-3 minutes)

### Opening (15 seconds)

"I built an intelligent GRC automation tool to demonstrate my understanding of the challenges mentioned in the role description - specifically around automating GRC reporting, surfacing risk insights, and supporting SOC 2, ISO 27001, and NYDFS audits.

Let me show you how it works..."

### Run the Tool (2 minutes)

**User Inputs to Provide:**
1. Industry: `2` (Crypto/Digital Assets - perfect for Fireblocks)
2. Confirm frameworks: `y` (SOC 2, ISO 27001, NYDFS)
3. Current policy exists: `y`
4. Current min length: `8`
5. Current special chars: `n`
6. Current MFA status: `2` (Optional)
7. Current MFA adoption: `45`
8. Hardware tokens: `n`
9. Current expiration: `90`
10. Target min length: `14`
11. Target special chars: `y`
12. Target MFA: `3` (Required for all - best practice)
13. Target expiration: `60`
14. Next steps menu: `3` (View audit readiness) or `4` (Exit)

### Key Points to Highlight While Running

**As industry is selected:**
"Notice it auto-detected this is crypto/digital assets and applied NYDFS requirements - that's the New York Department of Financial Services cybersecurity regulation that applies to Fireblocks."

**As current state is assessed:**
"This current state assessment is what enables the gap analysis - comparing where you are vs. where you need to be."

**As target policy is configured:**
"See the real-time risk scoring and compliance feedback? As I make security decisions, it shows which frameworks are satisfied."

**As risk assessment displays:**
"Final risk score of 2.8/10 - that puts this in the top 25% for crypto custody firms. This kind of benchmarking helps justify security investments to leadership."

**As artifacts generate:**
"In about 10 seconds, it's generating 9 different artifacts that would normally take 20-30 hours of manual work:
- Professional policy document
- Compliance matrices for SOC 2, ISO 27001, and NYDFS
- Control testing checklist for auditors
- Gap analysis with remediation roadmap
- ServiceNow and Jira exports for tracking"

**At gap analysis:**
"The gap analysis identifies specific actions needed - like upgrading from 8 to 14 character passwords, enabling universal MFA. Each gap includes timeline, effort estimate, and cost - exactly what you need for project planning."

### Closing (30 seconds)

"This tool directly addresses the job requirements:

✅ **Automate GRC reporting** - Generates all compliance matrices and audit artifacts automatically

✅ **Surface risk insights** - Real-time risk scoring with industry benchmarking

✅ **Support audits** - SOC 2, ISO 27001, NYDFS all covered with control mappings

✅ **Platform integration** - ServiceNow and Jira export formats included

✅ **Customer due-diligence** - Professional artifacts ready to share with customers

The value proposition is clear: this saves 20-30 hours per audit cycle and ensures nothing falls through the cracks.

I see this fitting into the role's focus on leveraging automation to maintain intelligent dashboards integrated with platforms like ServiceNow and Jira."

## Follow-Up Questions You Might Get

**Q: How long did this take to build?**
A: "About 2-3 days. I focused on the features that would deliver maximum value for Fireblocks' specific context - crypto regulatory requirements, the frameworks you audit against, and integration with your toolchain."

**Q: Could this be extended to other policy types?**
A: "Absolutely. The architecture is modular - adding incident response policies, data protection policies, etc. would just require adding new templates and compliance mappings. The gap analysis and export logic is already generic."

**Q: How did you know about NYDFS requirements?**
A: "I researched Fireblocks' regulatory context. Since you're in crypto custody, NYDFS 23 NYCRR 500 is a key regulation. I also included SOC 2 and ISO 27001 since those are standard for SaaS/infrastructure companies serving enterprises."

**Q: Could this integrate with actual ServiceNow/Jira APIs?**
A: "Yes. Right now it generates import files, but the next step would be direct API integration using their REST APIs. The data structure is already formatted for their import schemas."

**Q: What about risk assessments for other areas?**
A: "The risk scoring engine could be extended to any security domain - just need to define the risk factors and scoring algorithm. The pattern is the same: assess current state, define target, calculate gap, provide remediation roadmap."

## What to Show If Time Permits

1. **Open a generated policy document** - Show professional formatting with framework references

2. **Open compliance matrix** - Show specific control mappings (e.g., SOC 2 CC6.1, ISO 27001 A.9.2.4)

3. **Open gap analysis report** - Show remediation details with timelines and costs

4. **Show ServiceNow JSON** - Demonstrate it's ready for platform import

## Technical Questions You Might Get

**Q: What's the tech stack?**
A: "Pure Python, no external dependencies. Used standard library to keep it simple and portable. The CLI uses ANSI color codes for the interface."

**Q: How is risk scored?**
A: "Multi-factor algorithm considering password length, complexity, MFA status, expiration. Each factor contributes to a 0-10 scale where lower is better. Benchmarks are based on industry research."

**Q: Where do the compliance mappings come from?**
A: "I manually mapped requirements from the actual framework documents - SOC 2 Trust Services Criteria, ISO 27001:2022 Annex A, NYDFS 23 NYCRR 500. Each control is linked to specific policy sections."

**Q: How would you handle policy versioning?**
A: "Add version control metadata, track changes between versions, generate diff reports. Could integrate with Git for change tracking."

## Backup Plan (If Technical Issues)

Have screenshots ready of:
1. The tool running
2. Generated policy document
3. Compliance matrix
4. Gap analysis report

Walk through the screenshots if live demo fails.

## Post-Demo

"I have the code on GitHub if you'd like to review the implementation. Happy to walk through the architecture or discuss how this could be extended for Fireblocks' specific needs."

---

**Remember:**
- Speak confidently about GRC concepts
- Connect everything back to the job description
- Show you understand Fireblocks' business (crypto custody, regulatory requirements)
- Emphasize automation and measurable value (time saved, risk reduced)
- Be ready to discuss both technical and GRC aspects
