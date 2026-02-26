# Compliance Gap Analysis Report

**Version:** v0.2  
**Use Case:** AI essay grading and feedback tool for student assignments  
**Technology:** Anthropic Claude API  
**Industry:** US K-12 school district (education)  
**Generated:** 2026-02-26 12:41:25  
**Generation Time:** 78.3s total (planning: 9.4s, research: 10.5s, analysis: 58.4s)  

---

## Search Queries Used

- FERPA student data privacy requirements AI tools K-12 education 2024
- Anthropic Claude data retention privacy policy education FERPA compliance
- COPPA children's online privacy AI education tools under 13
- US Department of Education AI guidance K-12 schools student data 2023 2024
- state student data privacy laws AI education technology banned restricted

---

## Analysis

# AI Compliance Gap Analysis: Essay Grading Tool for K-12

## 1. APPLICABLE REGULATIONS

### Federal Laws
- **FERPA (Family Educational Rights and Privacy Act)**: Applies to all K-12 schools receiving federal funding. Protects "education records" containing personally identifiable information (PII), which includes student assignments, grades, and AI-generated feedback.

- **COPPA (Children's Online Privacy Protection Act)**: Applies when collecting personal information from children under 13. Requires verifiable parental consent before collection, use, or disclosure of personal information.

### State-Level Considerations
- Multiple states have enacted student data privacy laws beyond federal requirements
- Some states have specific AI guidance for K-12 education (Nevada's STELLAR framework, Montana's Indigenous data sovereignty requirements)
- State-specific breach notification requirements

## 2. IDENTIFIED RISKS

### High-Priority Risks

**Data Training and Retention Risk**
- According to research, AI providers have historically used customer data to train models, with one source noting that providers are "like gigantic vacuum cleaners, hoovering up your personal information and content"
- Student essays contain PII, writing samples that could reveal disabilities, race, socioeconomic status, and other protected characteristics

**"Black Box" Explainability Problem**
- FPF guidance (2024) notes: "FERPA requires schools to respond to reasonable requests for explanations and interpretations of the records, which in use cases where the tool creates new records as part of the output may be challenging since how AI technology works can be a black box"
- Parents have FERPA rights to understand how grades/feedback are determined

**Data Breach Risk**
- 23% of teachers reported their school experienced a large-scale data breach during 2023-24 school year (CDT study)
- Student essays contain sensitive educational records

**Third-Party Service Provider Risk**
- Anthropic's Consumer Terms updated September 2024 show "fundamental shift in how data gets handled"
- Unclear whether district is using Consumer API vs. Enterprise API with different data handling

## 3. COMPLIANCE GAPS

### Gap 1: Lack of School Official/FERPA Exception Documentation
**Requirement**: Under FERPA, third-party vendors accessing student records must qualify as "school officials" with "legitimate educational interest"

**Current Gap**: 
- No evidence of Business Associate Agreement (BAA) or Data Processing Agreement (DPA) with Anthropic
- Unclear if Claude API terms designate Anthropic as "school official" under FERPA
- FPF guidance emphasizes need for proper contractual frameworks

### Gap 2: Inadequate Data Use and Training Restrictions
**Requirement**: FERPA and state laws prohibit using student data for unauthorized purposes, including AI model training

**Current Gap**:
- Anthropic's updated Consumer Terms (Sept 2024) show changed "data training consent mechanisms"
- Unclear if district is using API tier that prohibits training on student data
- No documented verification that student essays won't be used for model improvement

### Gap 3: Missing COPPA Compliance for Under-13 Students
**Requirement**: COPPA requires verifiable parental consent before collecting personal information from children under 13

**Current Gap**:
- K-12 districts serve students under 13
- No evidence of parental consent mechanism specific to AI tool
- Research notes COPPA applies "when using AI that requires student input of data"

### Gap 4: Insufficient Explainability Mechanisms
**Requirement**: FERPA right to "explanations and interpretations of records"

**Current Gap**:
- No documented process for explaining AI-generated grades/feedback to parents
- Claude's decision-making process is not fully transparent
- No human review protocol for AI-generated assessments

### Gap 5: Inadequate Data Retention and Deletion Policies
**Requirement**: FERPA allows parents to request amendment of records; retention policies must align with state schedules

**Current Gap**:
- Anthropic's "layered policy approach" (as of Aug-Sept 2025) varies by deployment type
- No documentation of how long student essays/AI outputs are retained
- Unclear data deletion capabilities for individual student records

### Gap 6: Missing Data Security Assessments
**Requirement**: State laws and best practices require security assessments of ed-tech vendors

**Current Gap**:
- No evidence of security vetting process for Claude API
- Given 23% breach rate, heightened diligence required
- No encryption, access control, or incident response documentation

### Gap 7: Lack of Transparency and Informed Consent
**Requirement**: Best practices and state guidance emphasize transparency with parents/students

**Current Gap**:
- No documented parent notification about AI grading use
- Students may not understand AI vs. human assessment
- Missing bias/accuracy disclaimers

## 4. RECOMMENDATIONS

### Immediate Actions (0-30 days)

**1. Verify API Tier and Data Usage Terms**
- **Action**: Contact Anthropic to confirm whether current API usage is Consumer vs. Enterprise tier
- **Critical Question**: Does contract explicitly prohibit using student data for model training?
- **Cite**: Research shows Anthropic updated terms Sept 2024 with "fundamental shift" in data handling

**2. Execute Proper Data Processing Agreement**
- **Action**: Require Anthropic to sign DPA designating them as "school official" under FERPA
- **Must Include**:
  - Prohibition on data use beyond providing essay grading service
  - Data deletion upon request/contract termination
  - Security safeguards meeting IRS Publication 1075 or equivalent
  - Breach notification obligations
  - Subprocessor disclosure

**3. Implement COPPA Compliance Process**
- **Action**: Obtain verifiable parental consent for students under 13
- **Method**: Written consent form explaining:
  - What data is collected (essays, student names/IDs)
  - How AI processes this data
  - Parent right to refuse or withdraw consent
- **Alternative**: Use school exception under COPPA if AI tool is used exclusively for educational purposes under school supervision

### Short-Term Actions (30-90 days)

**4. Develop Explainability Protocol**
- **Action**: Create documented process for explaining AI grades/feedback
- **Components**:
  - Plain-language description of how Claude evaluates essays
  - Human review requirement before final grades recorded
  - Appeals process for students/parents who question AI assessment
  - Training for teachers on explaining AI decisions
- **Rationale**: Addresses FPF concern about "black box" problem

**5. Establish Data Minimization Practices**
- **Action**: Configure API to send minimum necessary PII
- **Techniques**:
  - Use pseudonymized student IDs instead of names
  - Strip metadata from essay submissions
  - Limit context provided to Claude to essay content only
  - Implement automated PII detection/redaction

**6. Conduct Privacy Impact Assessment (PIA)**
- **Action**: Document assessment covering:
  - What student data is collected and why
  - Data flow from submission through API to feedback delivery
  - Security controls at each stage
  - Risks and mitigation strategies
  - Retention schedule aligned with state education records requirements

**7. Implement Parent Notification and Transparency**
- **Action**: Notify parents/guardians about AI grading implementation
- **Disclosure Elements**:
  - That AI is used for grading/feedback
  - What data is shared with Anthropic
  - How student privacy is protected
  - Parent rights under FERPA
  - Contact for questions/concerns

### Medium-Term Actions (90-180 days)

**8. Develop Data Security Controls**
- **Action**: Implement technical and administrative safeguards
- **Technical Controls**:
  - Encryption in transit (TLS 1.3+) and at rest
  - Access controls limiting who can submit/retrieve student data
  - Audit logging of all API interactions
  - API key rotation and secure storage
- **Administrative Controls**:
  - Staff training on student data privacy
  - Incident response plan specific to AI tool breach
  - Regular security audits

**9. Create Bias Monitoring Program**
- **Action**: Assess AI grading for demographic disparities
- **Process**:
  - Disaggregate AI grades by student demographics (race, disability status, English learner status)
  - Compare AI grades to human grades for systematic differences
  - Document and investigate any disparities >5%
  - Quarterly bias audits with results reported to school board

**10. Establish Vendor Due Diligence Process**
- **Action**: Formalize vetting procedure for ed-tech AI tools
- **Criteria**:
  - FERPA/COPPA compliance verification
  - SOC 2 Type II or equivalent certification
  - Data usage and training policies
  - Security incident history
  - Reference checks with other K-12 districts
  - Review against state-specific requirements

**11. Build Human Oversight Mechanisms**
- **Action**: Ensure meaningful human review of AI outputs
- **Protocol**:
  - Teachers review all AI grades before recording
  - Random quality checks of AI feedback accuracy
  - Override capability when AI assessment seems incorrect
  - Prohibition on fully automated grading decisions

### Long-Term Actions (180+ days)

**12. Develop Comprehensive AI Governance Policy**
- **Action**: School board adopts district-wide AI policy
- **Components**:
  - Permissible AI use cases in education
  - Procurement requirements for AI tools
  - Student data protection standards
  - Transparency and consent requirements
  - Accountability structures
  - Regular policy review cycle

**13. Pursue State-Specific Compliance**
- **Action**: Review and comply with state AI guidance
- **Examples from Research**:
  - Nevada: STELLAR framework (Security, Transparency, Empowerment, Learning, Leadership, Achievement, Responsible Use)
  - Montana: Tribal sovereignty consultation for Indigenous students
  - Adapt implementation to state-specific requirements

**14. Consider Alternative Deployment Models**
- **Action**: Evaluate more privacy-protective options
- **Options**:
  - Anthropic Enterprise API with enhanced data protections
  - AWS Bedrock or Google Vertex AI deployments of Claude with customer-controlled infrastructure
  - On-premises AI solutions (though less practical for most K-12 districts)
  - Research mentions $20/month FERPA-compliant alternative (investigate Boodlebox or similar)

## CRITICAL SUCCESS FACTORS

1. **Documentation**: Maintain records of all compliance efforts, agreements, and assessments
2. **Legal Review**: Have school district counsel review DPA and compliance program
3. **Stakeholder Engagement**: Involve teachers, parents, and students in AI implementation decisions
4. **Continuous Monitoring**: Privacy compliance is ongoing, not one-time
5. **Budget Allocation**: Plan for costs of Enterprise API tier, legal review, and compliance infrastructure

## SUMMARY

The current implementation has **significant compliance gaps** that create legal and ethical risks. The primary concerns are:

1. **No documented FERPA-compliant agreement** with Anthropic
2. **Unclear data training practices** under updated Claude terms
3. **Missing COPPA consent** for under-13 students
4. **Inadequate explainability** for AI-generated grades
5. **Insufficient transparency** with parents/guardians

**Priority:** Address gaps 1-3 immediately before continuing to use the tool. The district faces potential FERPA violations, loss of federal funding, and reputational harm if a data breach or unauthorized use occurs.

**Estimated Timeline for Full Compliance**: 90-180 days with adequate resources and cooperation from Anthropic.
