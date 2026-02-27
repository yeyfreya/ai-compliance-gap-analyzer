# Compliance Gap Analysis Report

**Version:** v0.3  
**Use Case:** AI-powered resume screening tool  
**Technology:** OpenAI GPT-4 API  
**Industry:** Enterprise HR tech (US-based)  
**Generated:** 2026-02-26 16:35:19  
**Generation Time:** 69.9s total (planning: 9.7s, research: 11.7s, analysis: 48.4s)  

---

## Search Queries Used

- EEOC AI hiring discrimination guidelines 2024 automated employment decision tools
- OpenAI GPT-4 data retention privacy policy enterprise API GDPR
- US employment discrimination laws AI resume screening OFCCP regulations
- OpenAI business associate agreement BAA compliance enterprise data processing
- New York City AI hiring law Local Law 144 bias audit requirements

---

## Analysis

## Risk Prioritization Matrix

| Gap | Risk Level | Regulatory Impact | Implementation Difficulty | Priority |
|-----|-----------|-------------------|---------------------------|----------|
| No bias audit process for NYC Local Law 144 compliance | CRITICAL | NYC employers using AEDTs face penalties; mandated annual audits | Medium - requires third-party auditor engagement | 1 |
| Lack of adverse impact analysis per EEOC/OFCCP standards | CRITICAL | Direct violation of Title VII, ADA; EEOC enforcement priority 2024-2028 | High - requires statistical analysis capability and documentation | 2 |
| Missing candidate notification and alternative selection process | HIGH | NYC Local Law 144 violation; EEOC technical assistance requirements unmet | Low - procedural implementation | 3 |
| No documented record-keeping of resume search criteria | HIGH | OFCCP regulatory requirement for federal contractors; audit exposure | Medium - requires system configuration changes | 4 |
| Undefined data retention policy for candidate information | HIGH | GDPR Article 5 violation for EU candidates; CCPA implications | Medium - requires policy creation and technical controls | 5 |
| Absence of reasonable accommodation process for AI screening | MEDIUM | ADA compliance gap; EEOC June 2022 guidance | Low - policy and training needed | 6 |

## Applicable Regulatory Frameworks

**Federal Employment Discrimination Laws:**
- Title VII of the Civil Rights Act (race, color, religion, sex, national origin)
- Americans with Disabilities Act (ADA)
- Age Discrimination in Employment Act (ADEA)
- EEOC Strategic Enforcement Plan (FY 2024-2028) specifically targeting AI employment tools

**NYC-Specific Requirements:**
- Local Law 144 of 2021 (Automated Employment Decision Tools)

**Federal Contractor Requirements:**
- OFCCP AI and Equal Employment Opportunity guidelines (if applicable to federal contracts)

**Data Privacy:**
- GDPR (for EU candidate data)
- California Consumer Privacy Act (CCPA)

## Critical Compliance Gaps

### 1. **NYC Local Law 144 Non-Compliance (CRITICAL)**

**Requirement:** Annual independent bias audit of automated employment decision tools, published results, and specific candidate notifications.

**Current Gap:** No evidence of:
- Annual bias audit by independent auditor
- Published audit results (must be publicly available)
- Notification to candidates about AEDT use, data sources, retention policy
- Alternative selection process option

**Risk:** NYC can impose civil penalties. Each violation can result in fines, and continued use without compliance creates ongoing liability. The law has been in effect since July 2023.

**Recommendation (Immediate - 30 days):**
- Engage an independent bias auditor certified for Local Law 144 compliance
- Publish last 12-month audit results on company website
- Implement candidate notification system (email/application portal disclosure)
- Create alternative selection process pathway
- Document AEDT data sources and retention policies

### 2. **EEOC Adverse Impact Analysis Absence (CRITICAL)**

**Requirement:** Per EEOC guidance and the Uniform Guidelines on Employee Selection Procedures, employers must conduct adverse impact analysis using the "Four-Fifths Rule" to detect discrimination.

**Current Gap:** No documented process for:
- Statistical testing of selection rates by protected characteristics
- Regular monitoring of AI tool impact on different demographic groups
- Validation studies showing job-relatedness of screening criteria

**Risk:** The EEOC's 2024-2028 Strategic Enforcement Plan explicitly prioritizes "employment decisions, practices, or policies in which covered entities' use of technology contributes to discrimination." Recent EEOC actions against AI hiring tool developers establish direct liability.

**Recommendation (Immediate - 60 days):**
- Implement quarterly adverse impact analysis using Four-Fifths Rule
- Calculate selection rates by race, gender, age (40+), disability status
- Document any disparities and conduct validation studies
- If adverse impact found, demonstrate business necessity and job-relatedness
- Maintain 3-year statistical records per EEOC requirements

### 3. **OpenAI API Data Processing Gaps (HIGH)**

**Requirement:** GDPR Article 5 (data minimization, purpose limitation, storage limitation) and OpenAI's standard API terms.

**Current Gaps:**
- **Zero Data Retention (ZDR) configuration unclear:** OpenAI's Enterprise API offers ZDR endpoints where data isn't retained for model training. Standard API retains data for 30 days. No evidence of ZDR implementation.
- **Data Processing Addendum (DPA) status unknown:** GDPR compliance requires executed DPA with OpenAI.
- **Subprocessor documentation missing:** GDPR Article 28 requires awareness of all subprocessors.

**Risk:** GDPR fines up to €20 million or 4% of global revenue. Resume data likely contains EU candidates. CCPA also requires disclosure of data sharing.

**Recommendation (30 days):**
- Verify ZDR endpoint usage for all API calls
- Execute DPA with OpenAI via their enterprise form
- Document OpenAI's subprocessors in vendor management system
- Create candidate-facing privacy notice disclosing OpenAI processing
- Implement data retention policy (recommend 2-year maximum for compliant OFCCP records, then deletion)

### 4. **OFCCP Record-Keeping Deficiency (HIGH)**

**Requirement:** Federal contractors must "keep records of resume searches, both from searches of external websites and internal resume databases, that include the substantive search criteria used" (OFCCP AI Guidance, 2024).

**Current Gap:** No documented system for:
- Logging GPT-4 prompts used for resume screening
- Recording search criteria and ranking factors
- Maintaining audit trail of AI decision rationale

**Risk:** If organization has federal contracts, OFCCP compliance reviews will require this documentation. Inability to produce records results in enforcement actions.

**Recommendation (60 days):**
- Implement prompt logging system capturing all GPT-4 queries
- Store candidate ID, prompt used, AI response, and final decision
- Create quarterly review process of search criteria
- Maintain records for 2 years (3 years for AAP-related documentation)

### 5. **ADA Reasonable Accommodation Process Missing (MEDIUM)**

**Requirement:** EEOC June 2022 guidance on AI and ADA requires employers provide reasonable accommodations when AI tools screen out candidates with disabilities.

**Current Gap:** 
- No process for candidates to request alternative screening
- No disability disclosure mechanism
- No documented accommodation evaluation process

**Risk:** ADA complaints and litigation. EEOC explicitly stated employers cannot avoid ADA obligations by using AI vendors.

**Recommendation (90 days):**
- Add accommodation request option to application process
- Train HR team on evaluating accommodation requests for AI screening
- Create alternative evaluation pathway (e.g., human-only resume review)
- Document all requests and responses

## OpenAI-Specific Technical Controls

**Immediate Actions:**
1. **Prompt Engineering Review:** Ensure prompts don't request protected characteristic information (age, disability status, race indicators from names/locations)
2. **Output Filtering:** Implement post-processing to remove any protected characteristic mentions in GPT-4 responses
3. **API Configuration:**
   - Enable Zero Data Retention endpoints
   - Disable training data opt-in
   - Configure 30-day automatic data deletion minimum
4. **Monitoring:** Log all API interactions for bias audit capability

## Governance Recommendations

**Establish AI Hiring Governance Committee:**
- Legal counsel (employment law specialist)
- HR leadership
- IT/Data Science representative
- Diversity, Equity & Inclusion officer

**Quarterly Review Cycle:**
- Adverse impact analysis
- Prompt engineering audit
- Accommodation request review
- Regulatory update assessment

**Vendor Management:**
- Annual OpenAI compliance review
- SOC 2 Type 2 report verification
- DPA renewal tracking
- Incident response plan for OpenAI data breaches

## Implementation Timeline

**Days 1-30 (Emergency Compliance):**
- Engage NYC bias auditor
- Execute OpenAI DPA
- Implement candidate notifications
- Configure ZDR endpoints

**Days 31-60 (Core Compliance):**
- Complete first adverse impact analysis
- Implement prompt logging system
- Create accommodation request process
- Publish bias audit results

**Days 61-90 (Ongoing Compliance):**
- Establish governance committee
- Complete OFCCP record-keeping system
- Conduct validation studies if adverse impact found
- Implement quarterly monitoring schedule

**Cost Estimate:**
- Bias audit: $15,000-$40,000 annually
- Legal review: $10,000-$25,000
- Technical implementation: $20,000-$50,000
- Ongoing monitoring: $30,000-$60,000 annually

The most critical risk is **NYC Local Law 144 non-compliance**, which creates immediate legal exposure if operating in NYC. Combined with EEOC's explicit enforcement focus on AI hiring tools, this use case requires urgent remediation within 30-60 days to avoid regulatory action.
