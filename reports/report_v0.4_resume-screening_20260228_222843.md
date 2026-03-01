# Compliance Gap Analysis Report

**Version:** v0.4  
**Run ID:** `5ec4675e-e25d-4a29-95a3-2c850a5f2440`  
**Use Case:** resume screening  
**Technology:** my homerun local LLM  
**Industry:** ENterprise HR (US based)  
**Generated:** 2026-02-28 14:28:43  
**Source:** Synced from Supabase (cloud session)  
**Generation Time:** 223.1s total (planning: 25.8s, research: 7.4s, analysis: 189.9s)  

---

## Search Queries Used

- EEOC AI hiring discrimination guidance resume screening 2024
- New York City Illinois California AI employment law automated hiring decisions
- homerun LLM AI vendor data privacy policy compliance
- CPRA CCPA automated employment decision making requirements California

---

## Analysis

## Risk Prioritization Matrix

| Gap | Risk Level | Regulatory Impact | Implementation Difficulty | Priority |
|-----|-----------|-------------------|--------------------------|----------|
| No adverse impact testing or validation study for Title VII compliance | CRITICAL | EEOC enforcement, class action lawsuits, back pay liability | High - requires statistical validation, third-party testing | 1 |
| Missing California CPRA automated decision-making risk assessment | CRITICAL | $7,500 per violation, AG enforcement, required by April 1, 2028 for 2026-2027 assessments | High - comprehensive technical and legal assessment required | 2 |
| No pre-use notice to California applicants about automated decision-making | HIGH | CPRA violations, private right of action, damages per applicant | Medium - notice templates and delivery mechanisms needed | 3 |
| Failure to provide Illinois HB 3773 AI use notifications (effective Jan 1, 2026) | HIGH | Back pay, reinstatement, emotional distress damages under Illinois Human Rights Act | Medium - notification system and disclosure language needed | 4 |
| Lack of human oversight and meaningful human involvement documentation | HIGH | Multiple state laws require employer oversight; liability for discriminatory outcomes | Medium - process redesign and documentation | 5 |
| Unknown training data provenance and bias in local LLM | HIGH | Title VII disparate impact, inability to defend selection procedures | High - requires model documentation, possible retraining | 6 |
| No explainability mechanism for adverse hiring decisions | HIGH | EEOC investigation difficulties, inability to provide adverse action notices | High - technical implementation of interpretability tools | 7 |
| Missing California CPRA opt-out mechanism for ADMT | MEDIUM | CPRA violations, $2,500-$7,500 per violation | Medium - alternative screening process needed | 8 |
| Inadequate vendor oversight and data processing agreements | MEDIUM | Data breach liability, compliance responsibility remains with employer | Low - contractual and policy updates | 9 |
| No model monitoring for drift and ongoing validation | MEDIUM | Degraded model performance may create disparate impact over time | Medium - technical monitoring infrastructure | 10 |
| Unclear data retention and deletion procedures | MEDIUM | CPRA right to deletion, potential data minimization violations | Low - policy documentation and technical controls | 11 |

## Applicable Regulations and Framework Requirements

### Federal Law: EEOC Title VII Compliance

The **EEOC's May 2023 guidance** on AI in employment selection makes clear that Title VII of the Civil Rights Act applies to algorithmic hiring tools. Your organization faces three specific compliance obligations:

1. **Adverse Impact Analysis**: Employers must assess whether the LLM-based resume screening produces disparate impact on protected classes (race, color, religion, sex, national origin). The research indicates the EEOC expects "considerations for assessing disparate impacts" to be documented.

2. **Validation Requirements**: Selection procedures showing adverse impact must be validated according to the Uniform Guidelines on Employee Selection Procedures (UGESP). This requires demonstrating job-relatedness and business necessity.

3. **Employer Liability**: The guidance "focuses on the use by employers of AI in selection processes" - liability cannot be transferred to vendors. Your use of a "homerun local LLM" means you own compliance responsibility entirely.

### California: CPRA Automated Decision-Making Technology (ADMT) Requirements

California's expanded CPRA regulations create **the most immediate compliance burden** for your resume screening use case:

**Risk Assessment Mandate**: As noted in the Littler analysis, "Employers subject to the CCPA who use automated decisionmaking technology (ADMT) for employment-related decisions, without meaningful human involvement, must now conduct detailed risk assessments." The research specifies:
- Assessments conducted in 2026 and 2027 must be submitted by April 1, 2028
- Must be produced to CalPrivacy or AG within 30 days of request
- Covers technology that screens, scores, ranks or recommends candidates

**Pre-Use Notice Requirement**: "The pre-use notice adds to the" existing CPRA obligations. You must notify California applicants before using ADMT, explaining:
- The use of automated decision-making
- Categories of personal information processed
- Purpose and logic involved
- Opt-out rights

**Access and Opt-Out Rights**: California applicants have the right to:
- Opt out of ADMT (requiring you to maintain alternative screening processes)
- Access information about the automated decision-making logic
- Correct inaccurate personal information

### Illinois: House Bill 3773 (Effective January 1, 2026)

The research indicates Illinois "requires employers to notify employees when using AI for recruitment, hiring, promotion, discipline, discharge, or other employment decisions." Key provisions:

- **Notification Requirement**: Must inform applicants about AI use before deployment
- **Anti-Discrimination Standards**: "The prohibition is straightforward: employers cannot use AI that discriminates against protected classes"
- **Employer Oversight Emphasis**: The law "emphasizes employer oversight of automated systems rather than an outright prohibition on their use"
- **Enforcement**: Illinois Department of Human Rights enforcement with "remedies including back pay, reinstatement, emotional distress" damages

### Additional State Considerations

While not covered in depth in the research, **New York City's Local Law 144** applies if you recruit NYC residents. This requires:
- Independent bias audits annually
- Notice to candidates about AEDT use
- Alternative selection process availability

## Identified Compliance Gaps

### Gap 1: Complete Absence of Adverse Impact Testing (CRITICAL)

**The Risk**: Your local LLM resume screening system has likely never undergone formal adverse impact analysis. Without this analysis, you cannot determine if the tool disproportionately screens out protected classes. 

The EEOC guidance emphasizes that AI tools screening resumes based on learned patterns may perpetuate historical biases. For example:
- If training data included resumes from historically homogeneous workforces
- If the model learned proxies for protected characteristics (e.g., college names as proxies for race/socioeconomic status)
- If the model penalizes career gaps (disparate impact on women) or certain language patterns

**Compliance Shortfall**: The UGESP's "4/5ths rule" requires selection rates for protected groups to be at least 80% of the rate for the highest-performing group. You have no data on whether your LLM meets this threshold.

**Legal Exposure**: Class action lawsuits, EEOC investigations, back pay liability, and injunctive relief requiring process changes.

### Gap 2: No California CPRA Risk Assessment (CRITICAL)

**The Risk**: The research specifies that California regulations require "detailed risk assessments" for ADMT. Your local LLM clearly qualifies as ADMT because it "screen[s], score[s], rank[s] or recommend[s] candidates."

**Compliance Shortfall**: You lack:
- Documented risk assessment methodology
- Analysis of potential discriminatory outcomes
- Evaluation of data security risks
- Assessment of privacy impacts
- Mitigation strategies for identified risks

**Timing Urgency**: "Assessments conducted in 2026 and 2027 must be submitted by April 1, 2028." If you're currently using the system, you need a 2026 assessment completed immediately.

**Legal Exposure**: "$7,500 per violation" and potential AG enforcement action.

### Gap 3: Missing Pre-Use Notices to California Applicants (HIGH)

**The Risk**: California law requires pre-use notice before automated decision-making. Your research shows no evidence that applicants receive any disclosure about LLM-based screening.

**Compliance Shortfall**: Applicants are not informed about:
- The fact that automated screening is used
- What personal information is processed by the LLM
- The logic or purpose of the automated decision
- Their opt-out rights

**Legal Exposure**: CPRA provides private right of action. Each California applicant not given proper notice represents a separate violation with potential $2,500-$7,500 damages.

### Gap 4: No Illinois AI Use Notifications (HIGH - Effective Jan 1, 2026)

**The Risk**: Illinois HB 3773 becomes enforceable in weeks. The research indicates "employers cannot use AI" without proper notification and anti-discrimination safeguards.

**Compliance Shortfall**: No disclosure to Illinois applicants that AI screens their resumes. The law requires notification "when using AI for recruitment, hiring" decisions.

**Legal Exposure**: Illinois Department of Human Rights enforcement with "back pay, reinstatement, emotional distress" remedies. The law is new, so early enforcement actions may be aggressive to establish precedent.

### Gap 5: Undefined Human Oversight and "Meaningful Human Involvement"

**The Risk**: Multiple frameworks require human oversight. California CPRA specifically references "without meaningful human involvement" as a trigger for heightened requirements. The research notes Illinois law "emphasizes employer oversight of automated systems."

**Compliance Shortfall**: You haven't documented:
- What "human review" means in your process
- Whether reviewers can override LLM recommendations
- Whether reviewers have sufficient information and training to identify bias
- Whether the human review is substantive or merely a rubber stamp

**Why This Matters**: If your human review is perfunctory, courts and regulators may find you don't have "meaningful human involvement," triggering more stringent requirements and eliminating a key defense.

### Gap 6: Unknown Training Data and Model Bias (HIGH)

**The Risk**: The phrase "homerun local LLM" suggests a locally-deployed language model, but critical questions remain unanswered:
- What data was used to train the model?
- Was it pre-trained on internet data (which contains societal biases)?
- Was it fine-tuned on your historical hiring data (which may reflect past discrimination)?
- Has it been tested for demographic bias in resume evaluation?

**Compliance Shortfall**: The LLM data privacy research emphasizes "data minimization, purpose limitation, and the right to erasure" often conflict with how LLMs operate. You likely cannot:
- Identify what specific training data influenced a decision about a particular candidate
- Remove an individual's data from the model after training
- Prove the model wasn't trained on biased historical data

**Legal Exposure**: Inability to defend your selection procedure in EEOC investigation. The EEOC expects documentation of how tools were developed and validated.

### Gap 7: No Explainability for Adverse Decisions (HIGH)

**The Risk**: When you reject a candidate, you must provide adverse action notice under the Fair Credit Reporting Act (for background checks) and best practices for transparency. LLMs are notoriously difficult to explain - they make decisions based on billions of parameters learned from training data.

**Compliance Shortfall**: You likely cannot provide meaningful explanations like:
- "We rejected you because your experience in X area was insufficient"
- "Your resume lacked Y qualifications we prioritized"

Instead, you can only say "an AI reviewed your application," which:
- Prevents candidates from understanding and contesting decisions
- Makes EEOC investigations difficult
- May violate various state transparency requirements

**Technical Challenge**: Adding explainability to an existing LLM is "High" implementation difficulty, potentially requiring model architecture changes or additional interpretability layers.

### Gap 8: No California ADMT Opt-Out Mechanism (MEDIUM)

**The Risk**: California law requires you to honor opt-out requests from ADMT. The research confirms this is a specific CPRA right.

**Compliance Shortfall**: You have no alternative screening process for California applicants who opt out. This means:
- You cannot legally screen California applicants who invoke this right
- You may be illegally discriminating against California residents vs. other applicants
- You're in per-applicant violation of CPRA

**Operational Impact**: Implementing opt-out requires maintaining a parallel manual screening process, which increases costs but is legally required.

### Gap 9: Inadequate Vendor Oversight (MEDIUM)

**The Risk**: Even though you're using a "local" LLM, the Homerun privacy statement indicates they "use third parties in order to provide our services, and those third parties may process your personal data." The research shows they use Mailchimp, Google Analytics, Tag Manager, Hotjar, and Microsoft Clarity.

**Compliance Shortfall**: You haven't established:
- Data processing agreements with clear compliance responsibilities
- Audit rights over the LLM vendor's practices
- Verification that the vendor's practices meet your compliance obligations
- Subprocessor controls

**Why This Matters**: The EEOC guidance makes clear that employer liability cannot be transferred. The statement "Homerun does not and will not sell your data" is insufficient - you need comprehensive compliance documentation.

### Gap 10: No Ongoing Model Monitoring (MEDIUM)

**The Risk**: AI models can "drift" over time, changing their behavior as they process new data or as the applicant pool changes. What shows no bias today may develop disparate impact in 6 months.

**Compliance Shortfall**: You lack:
- Continuous adverse impact monitoring
- Model performance metrics tracked by demographic group
- Alerts for statistically significant changes in screening patterns
- Scheduled revalidation procedures

**Legal Exposure**: Even if you validated the model initially (which you haven't), failing to monitor means you won't detect when it becomes discriminatory over time.

### Gap 11: Unclear Data Practices (MEDIUM)

**The Risk**: The LLM privacy research emphasizes that "data minimization, purpose limitation, and the right to erasure" create challenges for LLMs. The CPRA research notes requirements around data retention and correction.

**Compliance Shortfall**: You likely haven't documented:
- How long resume data is retained in the LLM system
- Whether data can be deleted upon request (CPRA right to deletion)
- How incorrect information is corrected (CPRA right to correction)
- Whether the LLM stores or indexes PII unnecessarily

**Example Scenario**: A California applicant requests deletion of their data. Can you remove their resume from the LLM's training data? Can you ensure the model no longer "remembers" patterns learned from their information? Most LLMs cannot do this without retraining, creating compliance problems.

## Actionable Recommendations

### IMMEDIATE ACTIONS (0-30 Days)

**1. Suspend LLM Screening for California and Illinois Applicants**

Until you achieve basic compliance, halt automated screening for applicants from these jurisdictions:
- Implement geographic filters in your application system
- Route CA/IL applications to manual review
- Document this temporary accommodation

This limits immediate legal exposure while you implement compliance measures.

**2. Conduct Emergency Adverse Impact Analysis**

Engage a third-party industrial-organizational (I/O) psychologist or HR analytics firm to:
- Pull screening data for the past 12 months (or maximum available)
- Analyze selection rates by race, sex, and other protected characteristics
- Calculate 4/5ths rule compliance
- Document findings in formal validation report

**Cost Estimate**: $15,000-$50,000 depending on data volume and complexity.

**3. Draft and Deploy Immediate Disclosure Notices**

Create transparent disclosures for all applicants stating:
- "We use artificial intelligence to assist in reviewing resumes"
- Categories of data processed
- Contact information for questions or concerns
- For California: explicit opt-out instructions and link

Deploy these notices immediately on your careers page and in application confirmations.

**4. Establish Human Review Protocol**

Document and train hiring managers on meaningful review:
- Hiring managers must review LLM-flagged candidates independently
- Provide reviewers with candidate information separate from LLM scores
- Require documented rationale for final decisions
- Create audit trail showing human reviewer can and does override LLM

**5. Legal Counsel Review**

Engage employment law counsel familiar with AI hiring to:
- Review your exposure in each jurisdiction where you recruit
- Assess litigation risk based on your historical screening data
- Advise on privilege protection for validation studies
- Review draft notices and policies

### SHORT-TERM ACTIONS (30-90 Days)

**6. Complete California CPRA Risk Assessment**

Hire a privacy/AI compliance consultant to conduct formal ADMT risk assessment covering:

*Technical Assessment*:
- Model architecture and decision-making logic
- Data inputs and processing
- Security controls and access restrictions
- Third-party dependencies

*Legal Assessment*:
- Potential discriminatory impacts
- Privacy risks and data minimization
- Compliance with existing frameworks
- Documentation of mitigation measures

*Deliverable*: Formal written assessment ready for CalPrivacy submission by April 1, 2028 deadline.

**Cost Estimate**: $25,000-$75,000 for comprehensive assessment.

**7. Implement Illinois HB 3773 Notification System**

Before January 1, 2026 (if not already passed):
- Update application system to detect Illinois applicants
- Auto-deliver AI use notification to Illinois candidates
- Maintain records of notification delivery
- Train HR team on Illinois-specific requirements

**8. Develop Training Data Documentation**

Work with your LLM vendor or internal team to document:
- Sources of training data
- Date ranges of training data
- Demographic composition of training data (if available)
- Known limitations or biases in training data
- Any fine-tuning performed on your organization's historical data

If this documentation doesn't exist or shows problematic patterns, plan for model replacement or retraining.

**9. Implement Explainability Layer**

Add technical capabilities to provide decision explanations:
- Integrate SHAP (SHapley Additive exPlanations) or LIME (Local Interpretable Model-agnostic Explanations)
- Generate human-readable summaries of why resumes were scored positively or negatively
- Test explanations for consistency and accuracy
- Train HR team to use explanations in candidate communications

**Cost Estimate**: $30,000-$100,000 for technical implementation plus ongoing maintenance.

**10. Establish Vendor Data Processing Agreement (DPA)**

Update your agreement with the LLM vendor to include:
- Explicit compliance obligations under EEOC, CPRA, Illinois law
- Audit rights for your organization
- Data security and encryption requirements
- Breach notification procedures
- Subprocessor restrictions and disclosure
- Indemnification for compliance failures
- Right to terminate if compliance obligations aren't met

### MEDIUM-TERM ACTIONS (90-180 Days)

**11. Build California Opt-Out Alternative Process**

Develop parallel screening capability:
- Structured resume review rubric for manual screening
- Trained human reviewers
- Equivalent evaluation criteria to LLM process
- Documentation that alternative process is truly equivalent
- System to flag and route opt-out requests

**12. Implement Continuous Monitoring System**

Deploy technical infrastructure for ongoing compliance:
- Automated adverse impact calculation (monthly at minimum)
- Dashboard showing selection rates by protected class
- Alerts for statistical anomalies or adverse impact emergence
- Model drift detection
- Performance metrics stratified by demographics

**Cost Estimate**: $50,000-$150,000 for custom development, or $20,000-$60,000 annually for SaaS solutions.

**13. Create Comprehensive Documentation Package**

Prepare documentation demonstrating compliance due diligence:
- Job analysis showing resume screening criteria are job-related
- Validation study demonstrating business necessity
- Risk assessments (required for CA)
- Monitoring reports
- Training records for human reviewers
- Policy and procedure manuals
- Adverse action notice templates

This documentation is critical for defending against EEOC charges or lawsuits.

**14. Conduct Bias Audit (NYC and Best Practice)**

Engage third-party auditor to:
- Test model for bias across protected characteristics
- Generate formal bias audit report
- Publish summary results (required in NYC, best practice elsewhere)
- Identify and remediate specific bias sources

**Cost Estimate**: $25,000-$75,000 for independent audit.

**15. Develop Data Lifecycle Management**

Implement policies and technical controls for:
- Data retention schedules (retain only as long as needed)
- Deletion procedures honoring CPRA rights
- Data correction procedures
- Logging of all data access and modifications
- Regular purging of outdated applicant data

### LONG-TERM STRATEGIC ACTIONS (6-12 Months)

**16. Consider Model Replacement or Redesign**

Based on validation findings, consider:
- Switching to a model specifically designed for unbiased hiring
- Engaging vendor specializing in compliant AI hiring tools
- Building custom model with documented bias mitigation
- Implementing "fairness constraints" in model training

**17. Establish AI Governance Framework**

Create organizational structure for ongoing AI compliance:
- AI Ethics Review Board including legal, HR, IT, diversity & inclusion
- Quarterly compliance reviews
- Annual validation and revalidation schedule
- Process for evaluating new AI tools before deployment
- Incident response plan for discrimination complaints
- Continuous training for all stakeholders

**18. Expand Compliance to Additional Jurisdictions**

Research and implement requirements for:
- Any other states where you recruit (Colorado, Maryland, etc. may have new laws)
- International applicants if any (GDPR has significant AI requirements)
- Federal contractor obligations if applicable (OFCCP compliance)

**19. Proactive Transparency Measures**

Go beyond minimum requirements:
- Publish AI use policy on careers site
- Explain how AI augments (not replaces) human decision-making
- Provide candidate resources for understanding AI hiring
- Offer feedback to rejected candidates
- Track and report diversity metrics publicly

This positions your organization as a responsible AI user and reduces litigation risk.

**20. Insurance and Risk Transfer**

Evaluate insurance products:
- Employment Practices Liability Insurance (EPLI) with AI coverage
- Cyber liability insurance covering AI systems
- Directors & Officers coverage for compliance failures
- Confirm coverage isn't voided by non-compliance

## Implementation Roadmap Summary

**Phase 1 (Immediate - 30 days): Risk Mitigation**
- Suspend CA/IL screening
- Emergency adverse impact analysis
- Deploy basic disclosures
- Establish human review
- Legal counsel engagement

**Phase 2 (30-90 days): Core Compliance**
- Complete CA risk assessment
- Implement IL notifications
- Add explainability
- Vendor agreement updates
- Training data documentation

**Phase 3 (90-180 days): Systematic Compliance**
- Build opt-out alternative
- Deploy monitoring systems
- Complete documentation package
- Conduct bias audit
- Data lifecycle management

**Phase 4 (6-12 months): Strategic Positioning**
- Evaluate model replacement
- AI governance framework
- Expand jurisdictional coverage
- Proactive transparency
- Insurance optimization

## Estimated Budget

- **Immediate compliance (Phase 1)**: $50,000-$100,000
- **Core implementation (Phase 2)**: $80,000-$200,000
- **Systematic compliance (Phase 3)**: $100,000-$300,000
- **Strategic positioning (Phase 4)**: $50,000-$150,000 initial + ongoing costs

**Total First-Year Investment**: $280,000-$750,000 depending on implementation choices, vendor costs, and whether you develop custom solutions vs. purchase existing tools.

**Ongoing Annual Costs**: $75,000-$200,000 for monitoring, audits, updates, and governance.

## Critical Success Factors

1. **Executive Sponsorship**: AI compliance requires cross-functional coordination and significant investment. Secure C-suite buy-in early.

2. **Legal Privilege**: Structure validation studies and risk assessments under attorney-client privilege where possible to protect sensitive findings.

3. **Documentation Culture**: Every decision, every test, every change must be documented. In litigation, if it wasn't documented, it didn't happen.

4. **Continuous Improvement**: Compliance is not one-and-done. Regulations are evolving rapidly (note Illinois law effective Jan 1, 2026). Build adaptive processes.

5. **Transparency vs. Risk**: Balance transparency (which builds trust) against legal exposure (detailed disclosures can be used against you). Work with counsel on communications strategy.

## Agent Reasoning

### Prioritization Rationale for Risk Matrix

I prioritized the gaps based on three factors:

1. **Imminence of Legal Exposure**: Title VII adverse impact testing ranked #1 because you're currently exposed to EEOC enforcement and class action litigation *right now*, with no statute of limitations protection. Every resume screened without validation increases liability. California's CPRA risk assessment ranked #2 due to the specific April 1, 2028 submission deadline for assessments conducted in 2026-2027—you need this completed immediately if you're using the system in 2026.

2. **Magnitude of Potential Damages**: Class actions under Title VII can result in massive back pay awards affecting hundreds or thousands of applicants. CPRA violations carry statutory damages of $7,500 per violation, which compounds rapidly with high application volumes. Illinois HB 3773's remedies (back pay, reinstatement, emotional distress) rank high because the law is brand new and enforcement agencies often make examples with early violations.

3. **Difficulty of Remediation**: I weighted "High" implementation difficulty items lower in priority when legal exposure was moderate. For example, implementing explainability (Gap #7) is technically complex but ranked below human oversight documentation (Gap #5) because documenting procedures is faster to implement even though both are important.

The "meaningful human involvement" gap ranked #5 despite being relatively easier to implement because it's a lynchpin defense across multiple frameworks—California CPRA, Illinois HB 3773, and EEOC guidance all emphasize employer oversight. Fixing this gap partially mitigates multiple other risks.

### Most Influential Research Findings

**Most Critical Finding**: The Littler analysis stating "Employers subject to the CCPA who use automated decisionmaking technology (ADMT) for employment-related decisions, without meaningful human involvement, must now conduct detailed risk assessments" was the single most actionable finding. It confirmed that:
- California's requirements are already in effect (not proposed)
- They specifically apply to employment screening
- The definition of ADMT includes systems that "screen, score, rank or recommend candidates"—directly describing your use case
- There are specific, time-bound deliverables (April 1, 2028 submission)

**Second Most Critical**: The SHRM article confirming Illinois HB 3773's January 1, 2026 effective date created urgency. With the current date being late 2025 or early 2026 (based on article references), this law is either just enacted or about to be. This explains why I prioritized Illinois notification requirements at #4—you have weeks to months, not years.

**Third Most Critical**: The EEOC guidance from May 2023 establishing that Title VII applies to AI hiring. The finding that employers remain responsible "focuses on the use by employers of AI in selection processes" demolished any potential defense that your vendor bears liability. This elevated all gaps related to validation and adverse impact testing.

**Less Influential but Important**: The Homerun privacy statement showing use of third-party processors (Mailchimp, Google Analytics, etc.) was useful for identifying vendor oversight gaps, but those gaps ranked lower because the immediate legal exposure from discrimination and privacy violations is higher than data processing control issues.

### Research Insufficiencies and Information Needs

**Critical Gap #1: Homerun LLM Technical Specifications**

The research provided almost no information about what "homerun local LLM" actually is:
- Is this a branded product or a custom implementation?
- What base model is it built on (GPT, LLaMA, Claude, proprietary)?
- Is it truly "local" (on-premise) or is "local" marketing language for a private cloud deployment?
- What training data was used?

*Why This Matters*: Without knowing the technical architecture, I cannot assess:
- Whether the model can be audited for bias
- Whether explainability tools are compatible
- Whether retraining is feasible vs. requiring complete replacement
- Data residency and privacy implications

*Additional Research Needed*:
- Technical documentation from Homerun or the LLM provider
- Search for "Homerun AI resume screening technical specifications"
- Search for any existing bias audits or validations of this specific tool
- Information about whether this is a common platform or custom deployment

**Critical Gap #2: Federal Contractor Status**

The analysis assumes a private employer not subject to OFCCP (Office of Federal Contract Compliance Programs) requirements. If your organization is a federal contractor:
- Additional validation requirements apply
- Internet Applicant Rule implications
- Affirmative action plan considerations
- Different adverse impact thresholds

*Additional Research Needed*:
- Confirmation of federal contractor status
- OFCCP AI guidance (separate from EEOC)
- Internet Applicant recordkeeping requirements for AI systems

**Critical Gap #3: Current Application Volume and Demographics**

I cannot calculate actual legal exposure without knowing:
- How many applicants you screen monthly/annually
- Geographic distribution of applicants (California percentage, Illinois percentage)
- Historical demographic data of applicants (even anonymized/aggregated)
- Current selection rates

*Why This Matters*: 
- Validates whether CPRA applies (threshold requirements)
- Determines per-violation exposure (e.g., 10,000 CA applicants × $7,500 per violation)
- Affects budget estimates (small employer vs. enterprise-scale implementation)

*Additional Research Needed*:
- Internal HR analytics data
- ATS (Applicant Tracking System) reporting

**Moderate Gap #4: NYC and Other Jurisdictions**

The research mentioned NYC Local Law 144 but didn't provide detailed requirements. If you recruit in NYC, additional compliance obligations exist. Similarly, I found references to Colorado and Maryland potentially having AI employment laws but no specifics.

*Additional Research Needed*:
- Search for "NYC Local Law 144 AEDT bias audit requirements 2024"
- Search for "Colorado Maryland AI employment law 2024 2025"
- Map recruiting geographic footprint against state law database

**Moderate Gap #5: Industry-Specific Requirements**

"Enterprise HR" is broad. Certain industries have additional obligations:
- Financial services: GLBA, FCRA implications
- Healthcare: If hiring for HIPAA-covered roles
- Unionized environments: NLRA considerations, collective bargaining agreements

*Additional Research Needed*:
- Specific industry sector
- Union presence
- Any industry-specific accreditation or compliance frameworks

### Key Assumptions and Their Basis

**Assumption #1: High Application Volume**

I assumed you process enough applications to make CPRA compliance mandatory. **Basis**: You're described as "Enterprise HR," suggesting significant scale. If you're a small business (<$25M revenue, <100K consumers/households), CPRA may not apply, significantly changing the analysis.

**Assumption #2: Material Reliance on LLM Scoring**

I assumed the LLM's recommendations substantially influence hiring decisions rather than being purely advisory. **Basis**: You described it as "resume screening," implying it determines which candidates advance. If the LLM only assists human reviewers who make independent assessments, several gaps are less severe (but still present).

**Assumption #3: No Existing Validation Studies**

I assumed you've never conducted formal validation because you asked for compliance gap analysis. **Basis**: Organizations with validated tools typically know their compliance posture. If validation exists but is outdated or incomplete, the remediation path differs.

**Assumption #4: Direct Employer Use, Not Vendor-Managed**

I assumed you operate the LLM directly rather than a third-party vendor managing the entire process. **Basis**: The phrase "my homerun local LLM" suggests ownership/control. If a vendor manages the screening end-to-end, compliance responsibility partially shifts (though employer liability remains under EEOC guidance).

**Assumption #5: Active Current Use**

I assumed the system is currently deployed and screening live applicants. **Basis**: You requested compliance gap analysis, not pre-deployment review. If this is pre-deployment, you have more time to implement compliance before exposure begins.

**Assumption #6: No Existing Human Review Process**

I assumed pure AI screening without meaningful human review. **Basis**: Most compliance gaps exist. If you have robust human review, several risks are mitigated, though documentation gaps may still exist.

**Assumption #7: United States-Only Recruiting**

I assumed all applicants are US-based. **Basis**: You specified "US based" organization. If you recruit internationally, GDPR Article 22 (automated decision-making), UK GDPR, and other frameworks apply, significantly expanding compliance obligations.

These assumptions shaped my risk assessment and recommendations. Confirming or correcting them would refine the analysis significantly.
