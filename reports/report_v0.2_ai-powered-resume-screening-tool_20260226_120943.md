# Compliance Gap Analysis Report

**Version:** v0.2  
**Use Case:** AI-powered resume screening tool  
**Technology:** OpenAI GPT-4 API  
**Industry:** Enterprise HR tech (US-based)  
**Generated:** 2026-02-26 12:09:43  

---

## Search Queries Used

- EEOC AI hiring discrimination guidelines 2024 automated employment decision systems
- OpenAI GPT-4 API data retention privacy policy enterprise
- US employment discrimination laws AI resume screening OFCCP compliance requirements
- OpenAI BAA HIPAA enterprise data processing agreement terms
- FTC AI Act employment screening bias audit requirements enforcement actions 2024

---

## Analysis

# AI Resume Screening Compliance Gap Analysis

## 1. APPLICABLE REGULATIONS & FRAMEWORKS

### Federal Employment Discrimination Law
- **Title VII of the Civil Rights Act (1964)** - Prohibits discrimination based on race, color, religion, sex, and national origin
- **Age Discrimination in Employment Act (ADEA)** - Protects workers 40+
- **Americans with Disabilities Act (ADA)** - Prohibits disability discrimination
- **EEOC Enforcement Authority** - Active oversight of AI hiring tools with new guidance applying traditional discrimination frameworks to AI systems

### Federal Contractor Compliance (if applicable)
- **OFCCP Requirements** - If you serve federal contractors, the Office of Federal Contract Compliance Programs has released specific AI guidance requiring:
  - Record retention and audit capabilities
  - Ability to provide detailed information about AI system design during compliance reviews
  - Documentation of alternative approaches considered

### Emerging State/Local Requirements
- **NYC Local Law 144** - Requires bias audits for automated employment decision tools (sets precedent other jurisdictions may follow)
- **FTC Act Section 5** - Deceptive practices related to "bias-free" AI marketing claims

### Privacy & Data Processing
- **State Privacy Laws** (CA, VA, CO, etc.) - Many include provisions about automated decision-making
- **Data Retention Requirements** - Various state laws govern employment record retention

---

## 2. IDENTIFIED RISKS

### A. Disparate Impact Liability (HIGH RISK)
**Source**: EEOC applies Uniform Guidelines on Employee Selection Procedures to AI tools

**Risk**: GPT-4 resume screening could produce statistically significant adverse impact against protected classes without your knowledge. The EEOC explicitly stated these guidelines "apply equally to AI-based selection tools."

**Recent Enforcement**: Research shows ACLU filed FTC complaint (May 2024) against Aon Consulting challenging hiring tools as discriminatory, noting "employers could be liable for vendor bias, even if they didn't design the tool."

### B. Vendor Liability & Limited Control (HIGH RISK)
**Issue**: You're dependent on OpenAI's model behavior, but legally responsible for discriminatory outcomes.

**Specific Concerns**:
- No direct control over GPT-4's training data or decision logic
- Limited ability to conduct traditional adverse impact analysis
- OpenAI's models may evolve without notice, changing screening outcomes
- Black-box nature makes it difficult to explain decisions to regulators or candidates

### C. Documentation & Transparency Gaps (MEDIUM-HIGH RISK)
**OFCCP Requirement**: Federal contractors must "adequately provide relevant, requested information and answer questions about the use of AI during compliance reviews or investigations, including information about the design of the screening or selection system and whether alternative approaches were considered."

**Your Gap**: As an API user, you likely cannot fully explain:
- Why GPT-4 ranked one resume over another
- What features it weighted most heavily
- How to replicate a specific screening decision
- What training data influenced the model

### D. Recordkeeping & Audit Trail Deficiencies (MEDIUM RISK)
**Issue**: OpenAI's default 30-day data retention may conflict with employment law requirements.

**From Research**: "The standard retention policy for the API retains data for 30 days for safety monitoring purposes."

**Legal Requirement**: Employment records typically must be retained 1-3 years depending on jurisdiction and whether OFCCP requirements apply.

### E. Inadequate Bias Testing (HIGH RISK)
**Emerging Standard**: Third-party bias audits becoming expected practice

**From Research**: "Using resume-screening algorithms without bias audits can lead to class-action exposure under Title VII and the ADEA. Organizations should require third-party bias audits where required by law or appropriate as a risk-management measure."

**Your Gap**: No evidence of systematic adverse impact analysis or ongoing monitoring.

---

## 3. COMPLIANCE GAPS

### Gap 1: No Validation Study or Adverse Impact Analysis
**Requirement**: EEOC expects employers to conduct validation studies showing selection procedures are job-related and consistent with business necessity.

**Current State**: Using GPT-4 API without formal validation testing whether it produces adverse impact by race, sex, age, or disability status.

**Regulatory Citation**: Uniform Guidelines on Employee Selection Procedures (applied to AI per EEOC guidance)

### Gap 2: Insufficient Data Retention Configuration
**Requirement**: Employment records typically must be retained 1-3 years; OFCCP requires even longer retention for federal contractors.

**Current State**: OpenAI's default 30-day retention period falls far short.

**Note from Research**: "API customers: ZDR [Zero Data Retention] is an option for API users" - but this would make retention WORSE, not better.

### Gap 3: Missing Business Associate Agreement (If Processing PHI)
**Requirement**: HIPAA requires BAA if processing Protected Health Information.

**Current State**: While HR data isn't typically PHI, if you're processing any health-related information (disability accommodations, health insurance elections, etc.), you need a BAA.

**From OpenAI Policy**: "Customer agrees not to use the Services to create, receive, maintain, transmit, or otherwise process Protected Health Information, unless it has signed the Healthcare Addendum."

**Action Required**: Contact baa@openai.com if any health data involved.

### Gap 4: No Vendor Audit Rights or AI System Documentation
**Requirement**: OFCCP requires ability to provide "information about the design of the screening or selection system."

**Current State**: Standard API access provides limited visibility into model behavior, training data, or decision logic.

**Problem**: You cannot fulfill regulatory information requests about how the AI system works.

### Gap 5: Lack of Human Review Protocol
**Best Practice/Emerging Requirement**: Meaningful human oversight of AI decisions.

**Current State**: Unclear whether human recruiters substantively review AI rankings or merely rubber-stamp them.

**Risk**: Courts increasingly skeptical of "human in the loop" claims when humans don't actually override AI recommendations.

### Gap 6: No Ongoing Monitoring Program
**Requirement**: Continuous monitoring for adverse impact (not one-time testing).

**Current State**: No systematic tracking of screening outcomes by protected class over time.

**Issue**: AI models can drift; outcomes may change as candidate pools evolve.

### Gap 7: Missing Alternative Selection Procedure Analysis
**Requirement**: Employers must consider less discriminatory alternatives if adverse impact exists.

**Current State**: No documentation of why GPT-4 screening was chosen over alternatives or how less discriminatory approaches were evaluated.

---

## 4. RECOMMENDATIONS

### IMMEDIATE ACTIONS (Within 30 Days)

#### 1. Configure Extended Data Retention
**Action**: Work with OpenAI to extend API data retention to minimum 3 years.
- Contact your OpenAI account team about enterprise data retention options
- Ensure you're capturing and storing: full resume text, GPT-4 prompts, model outputs, screening scores, and timestamps
- Implement separate backup system if OpenAI cannot provide sufficient retention

**Why**: Required for regulatory compliance and defending against discrimination claims.

#### 2. Implement Demographic Data Collection
**Action**: Begin collecting (voluntary) demographic data from applicants separately from the AI screening process.
- Use standard EEOC categories
- Keep demographic data isolated from resume screening inputs
- Design system to link screening outcomes to demographics for analysis only

**Why**: Cannot conduct adverse impact analysis without demographic data.

#### 3. Document Your AI System
**Action**: Create comprehensive documentation including:
- Detailed description of how GPT-4 is used in screening process
- Exact prompts/instructions given to the model
- Scoring/ranking methodology
- Human review procedures
- Version control (GPT-4 model version, prompt versions)
- Business justification for using AI screening

**Why**: Required for regulatory inquiries and litigation defense.

#### 4. Establish Human Review Protocol
**Action**: Implement mandatory meaningful human review:
- Train recruiters on when/how to override AI recommendations
- Document override decisions and rationale
- Set triggers for automatic human escalation (e.g., borderline scores)
- Track override rates

**Why**: Reduces legal risk and ensures human accountability.

---

### SHORT-TERM ACTIONS (30-90 Days)

#### 5. Conduct Initial Adverse Impact Analysis
**Action**: Engage industrial-organizational psychologist or employment testing expert to:
- Analyze screening outcomes by race, sex, age (40+), and disability status
- Calculate selection rates and impact ratios
- Apply "four-fifths rule" and statistical significance tests
- Document findings

**Why**: Identifies whether current system creates legal exposure.

**Critical**: If adverse impact found, you must either:
- Validate the procedure as job-related and consistent with business necessity, OR
- Modify/discontinue use

#### 6. Commission Third-Party Bias Audit
**Action**: Hire independent auditor to:
- Test for bias across protected classes
- Review prompt engineering for potentially biased language
- Analyze disparate treatment risks
- Provide remediation recommendations
- Issue audit report

**Why**: Demonstrates good faith and due diligence; may become legally required.

**From Research**: "Organizations should require third-party bias audits where required by law or appropriate as a risk-management measure."

#### 7. Evaluate Alternative Approaches
**Action**: Document consideration of less discriminatory alternatives:
- Traditional keyword screening
- Structured resume review rubrics
- Work sample tests
- Hybrid approaches

**Why**: Required under EEOC framework if adverse impact exists; shows reasonable alternative analysis.

#### 8. Review OpenAI Terms and Negotiate Enterprise Agreement
**Action**: 
- Review current OpenAI Services Agreement limitations
- Negotiate enterprise terms addressing:
  - Extended data retention commitments
  - Audit rights
  - Notification of model changes
  - Indemnification for discrimination claims
  - Access to model documentation for regulatory purposes

**Why**: Standard API terms likely insufficient for regulated employment use.

---

### ONGOING ACTIONS (Establish Permanent Processes)

#### 9. Implement Continuous Monitoring Program
**Action**: Establish quarterly review process:
- Calculate selection rates by protected class
- Track adverse impact ratios over time
- Monitor for model drift or outcome changes
- Review human override patterns
- Document findings and corrective actions

**Why**: One-time testing insufficient; ongoing monitoring legally expected.

#### 10. Create Regulatory Response Plan
**Action**: Develop procedures for responding to:
- EEOC charges or investigations
- OFCCP compliance reviews (if applicable)
- Candidate requests for explanations
- Subpoenas for AI system information

**Include**:
- Data retrieval procedures
- Legal hold protocols
- Designated response team
- Communication templates

**Why**: Proactive preparation reduces response time and legal risk.

#### 11. Establish AI Governance Committee
**Action**: Create cross-functional team including:
- HR leadership
- Legal counsel
- Data science/IT
- DEI officer
- External employment law advisor

**Responsibilities**:
- Review AI system changes
- Approve prompt modifications
- Review monitoring reports
- Authorize vendor selection
- Oversee compliance program

**Why**: Ensures sustained organizational accountability.

#### 12. Develop Candidate Transparency Materials
**Action**: Create clear disclosures:
- Notice that AI is used in screening
- Description of factors considered
- Information about human review
- Process for requesting reconsideration
- Contact information for questions

**Why**: Builds trust, may reduce legal risk, aligns with emerging transparency requirements.

---

### STRATEGIC CONSIDERATIONS

#### 13. Assess Total Cost of Compliance
**Analysis Needed**: The compliance infrastructure for AI resume screening may exceed the efficiency gains. Consider:

**Compliance Costs**:
- Third-party audits: $50,000-150,000+ annually
- I-O psychologist validation: $75,000-200,000+
- Extended data storage and management systems
- Legal review and risk assessment
- Staff training and oversight

**Alternative**: Some organizations find structured human review with clear rubrics more defensible and cost-effective than AI screening for regulatory-sensitive functions.

#### 14. Consider Model Alternatives
**Action**: Evaluate purpose-built, validated employment screening tools versus general-purpose LLMs:

**Purpose-Built Advantages**:
- Pre-validated for adverse impact
- Designed for EEOC compliance
- Vendor assumes more liability
- Better audit trails
- Clearer explainability

**GPT-4 Challenges**:
- Not designed/validated for employment decisions
- Limited control over behavior
- Difficult to validate under EEOC guidelines
- Vendor terms shift liability to you

#### 15. Develop Prompt Engineering Guidelines
**Action**: If continuing with GPT-4, establish rigorous prompt controls:
- Avoid protected class references
- Focus on job-related qualifications only
- Test prompts for disparate impact
- Version control and change management
- Regular legal review of prompt language

**Example Risk**: Prompts asking GPT-4 to identify "culture fit" or "leadership potential" could introduce bias.

---

## CRITICAL RISK SUMMARY

**Immediate Legal Exposure**: 
You are currently operating an AI-based employment selection tool without:
1. Adverse impact analysis (primary EEOC requirement)
2. Adequate recordkeeping (cannot defend against claims)
3. Validation showing job-relatedness (required if adverse impact found)
4. Vendor agreements suitable for regulated use

**Liability**: Recent enforcement actions show employers are held liable for vendor AI bias "even if they didn't design the tool" (Aon/ACLU case).

**Priority Recommendation**: Pause GPT-4 resume screening for new applications until adverse impact analysis is complete. The risk of a class-action discrimination claim far exceeds the operational efficiency gains.

---

## RESOURCES & NEXT STEPS

**Immediate Consultations Needed**:
1. Employment discrimination attorney with AI expertise
2. Industrial-organizational psychologist for validation study
3. OpenAI enterprise sales team re: extended retention and enterprise terms

**Regulatory Guidance to Review**:
- EEOC "The Americans with Disabilities Act and the Use of Software, Algorithms, and Artificial Intelligence to Assess Job Applicants and Employees" (2022)
- OFCCP "Artificial Intelligence and Equal Employment Opportunity for Federal Contractors"
- Uniform Guidelines on Employee Selection Procedures (29 CFR Part 1607)

**Timeline**: Address Immediate Actions within 30 days. If adverse impact found in initial analysis, be prepared to modify or discontinue use pending validation.
