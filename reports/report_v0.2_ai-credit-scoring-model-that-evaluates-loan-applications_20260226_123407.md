# Compliance Gap Analysis Report

**Version:** v0.2  
**Use Case:** AI credit scoring model that evaluates loan applications  
**Technology:** AWS SageMaker  
**Industry:** UK neobank (financial services)  
**Generated:** 2026-02-26 12:34:07  
**Generation Time:** 121.0s total (planning: 7.7s, research: 10.6s, analysis: 102.7s)  

---

## Search Queries Used

- UK FCA AI machine learning credit scoring requirements 2024
- AWS SageMaker data residency GDPR compliance financial services
- UK Consumer Duty algorithmic decision making credit lending
- EU AI Act high-risk credit scoring financial services requirements
- AWS SageMaker model explainability audit logging compliance features

---

## Analysis

# AI Credit Scoring Compliance Gap Analysis
**UK Neobank | AWS SageMaker Implementation**

---

## 1. APPLICABLE REGULATIONS & FRAMEWORKS

### Primary Regulatory Requirements:

**🇬🇧 UK FCA Consumer Duty (2023)**
- Applies to all retail lending products
- Requires firms to demonstrate good customer outcomes
- Mandates explainability of algorithmic decisions affecting customers
- Board-level accountability for AI governance

**🇪🇺 EU AI Act (Applicable to UK firms serving EU customers)**
- **Classification**: Credit scoring is explicitly categorized as **HIGH-RISK** under Annex III
- Triggers comprehensive compliance obligations including risk management, data governance, transparency, and human oversight
- Source: "Applications such as automated creditworthiness assessment, credit rating...are classified as high-risk systems and are subject to strict regulations" (Reply FinCon, 2024)

**🇬🇧 UK GDPR & Data Protection Act 2018**
- Article 22 rights regarding automated decision-making
- Data residency and cross-border transfer restrictions
- Right to explanation for automated decisions

**Additional Frameworks:**
- UK Consumer Credit Act requirements for creditworthiness assessment
- FCA Senior Managers & Certification Regime (SM&CR) - accountability for AI systems
- UK Centre for Data Ethics and Innovation (CDEI) bias guidelines

---

## 2. IDENTIFIED RISKS

### **Critical Risk Areas:**

#### A. **Explainability & Transparency Deficits**
**Risk Level: HIGH**

The research explicitly warns: *"Large language models and deep-learning credit scorers offer firms immense efficiencies, but their opacity threatens a cornerstone of FCA expectations: explainability"* (Sedric.ai, 2024)

**Specific concerns:**
- SageMaker may use complex ensemble models or neural networks that lack inherent interpretability
- When customers are declined, you must "trace the logic behind that path"
- FCA requirement: "Firms must be able to evidence the fairness of their algorithms"

#### B. **Algorithmic Bias & Fairness**
**Risk Level: HIGH**

- Historical lending data may contain embedded discrimination
- Protected characteristics correlation (age, gender, postcode as proxy for race/ethnicity)
- CDEI notes: "Some sectors, such as credit scoring...have a long history of using statistical techniques" but modern AI intensifies bias risks

#### C. **Data Residency & Sovereignty**
**Risk Level: MEDIUM-HIGH**

AWS operates globally, but UK/EU regulations require:
- *"Sensitive data cannot 'leave' a region (e.g., a country or jurisdiction)"* (Vaclavskarka blog, 2025)
- GDPR Article 45-46: Restricted data transfers outside UK/EU
- Financial services data is particularly sensitive

#### D. **Inadequate Human Oversight**
**Risk Level: MEDIUM**

- EU AI Act mandates human oversight for high-risk systems
- Consumer Duty requires Board Champion and annual governance reviews
- SM&CR assigns personal accountability to senior managers

#### E. **Continuous Monitoring Gaps**
**Risk Level: MEDIUM**

- Model drift detection
- Ongoing bias monitoring
- Performance degradation in production

---

## 3. COMPLIANCE GAPS ANALYSIS

### **GAP 1: Model Explainability Infrastructure**
**Current State**: AWS SageMaker offers SageMaker Clarify for explainability, but:
- May not be implemented or configured
- Default configuration insufficient for regulatory compliance
- No evidence of feature attribution documentation

**Regulatory Shortfall**:
- ❌ FCA Consumer Duty explainability requirement
- ❌ EU AI Act Article 13 (transparency obligations)
- ❌ GDPR Article 22 (right to explanation)

**Evidence**: Research shows SageMaker *can* provide "feature attribution" and "explainability" (Medium article), but it's optional, not default.

---

### **GAP 2: Data Governance & Residency Controls**

**Current State**: AWS SageMaker global service without specified data residency controls

**Regulatory Shortfall**:
- ❌ UK GDPR data localization requirements
- ❌ No documented data processing agreements specifying UK-only processing
- ❌ Potential inadvertent data transfer to non-UK AWS regions

**Evidence**: *"Aside from ensuring that such data is stored in the same region...the underlying requirement often goes further and states that sensitive data cannot 'leave' a region"* (2025 research)

**Technical Gap**: No mention of:
- AWS region locking (eu-west-2 for UK)
- SageMaker endpoint region restrictions
- Cross-region replication prevention

---

### **GAP 3: Bias Detection & Fairness Monitoring**

**Current State**: Unknown implementation of bias detection capabilities

**Regulatory Shortfall**:
- ❌ EU AI Act Article 10 (data quality and bias mitigation)
- ❌ FCA fairness evidence requirement
- ❌ CDEI algorithmic bias guidelines
- ❌ Equality Act 2010 compliance (indirect discrimination)

**Critical Missing Elements**:
- Pre-deployment bias testing across protected characteristics
- Continuous monitoring for disparate impact
- Documented fairness metrics and thresholds
- Regular bias audits

---

### **GAP 4: AI Risk Management System**

**Current State**: No evidence of comprehensive AI risk framework

**Regulatory Shortfall**:
- ❌ EU AI Act Article 9 (risk management system)
- ❌ FCA Consumer Duty governance requirements
- ❌ SM&CR accountability mapping

**Missing Components**:
- AI-specific risk register
- Documented risk mitigation strategies
- Incident response procedures for AI failures
- Regular risk reviews and updates

---

### **GAP 5: Model Governance & Audit Trail**

**Current State**: SageMaker Model Registry exists but may not be configured for compliance

**Regulatory Shortfall**:
- ❌ EU AI Act Article 12 (record-keeping obligations)
- ❌ FCA audit trail requirements
- ❌ Model versioning and lineage tracking

**Evidence**: While SageMaker can provide *"comprehensive technical documentation...including training environments, evaluation metrics, and model versions"* (AWS Plain English, 2024), this requires active implementation.

**Missing Documentation**:
- Model development methodology
- Training data provenance and quality measures
- Validation and testing results
- Post-deployment performance metrics
- Change management logs

---

### **GAP 6: Human Oversight Mechanisms**

**Current State**: Likely fully automated scoring without human review triggers

**Regulatory Shortfall**:
- ❌ EU AI Act Article 14 (human oversight)
- ❌ FCA Consumer Duty good outcomes assessment
- ❌ GDPR Article 22(3) (right to human intervention)

**Missing Controls**:
- Edge case escalation to human reviewers
- Random sample review processes
- Override capabilities with justification logging
- Clear criteria for when human review is triggered

---

### **GAP 7: Customer Rights & Transparency**

**Current State**: Unknown customer-facing transparency measures

**Regulatory Shortfall**:
- ❌ Consumer Duty requirement for clear communication
- ❌ GDPR Article 13-14 (information to data subjects)
- ❌ Credit reference agency-style transparency

**Evidence**: Research notes traditional credit scoring offers *"customers the ability to see their own credit history, and offer guidance on the factors that can affect credit scoring"* - this precedent must be matched.

**Missing Elements**:
- Plain language explanations of AI's role
- Individual-level feature contribution disclosure
- Clear adverse action notices
- Appeals/dispute mechanism

---

## 4. ACTIONABLE RECOMMENDATIONS

### **IMMEDIATE ACTIONS (0-30 days)**

#### 1. **Data Residency Lock-Down** ⚡ CRITICAL
```
Action: Configure AWS SageMaker for UK-only operations
- Set SageMaker endpoint region to eu-west-2 (London)
- Enable AWS Organizations Service Control Policies (SCPs) to prevent 
  cross-region data access
- Implement S3 bucket policies restricting data to UK regions
- Document data processing locations in GDPR Article 30 records
```
**Owner**: Cloud Infrastructure Team + DPO
**Compliance Impact**: UK GDPR, data sovereignty

#### 2. **Implement SageMaker Clarify for Explainability** ⚡ CRITICAL
```
Action: Deploy explainability framework
- Enable SageMaker Clarify for SHAP value computation
- Configure feature attribution for all credit decisions
- Set up explanation storage linked to each decision
- Create customer-facing explanation templates
```
**Owner**: ML Engineering Team
**Compliance Impact**: Consumer Duty, EU AI Act Article 13, GDPR Article 22

#### 3. **Establish Bias Monitoring Baseline** ⚡ CRITICAL
```
Action: Initial bias audit
- Use SageMaker Clarify to measure disparate impact across:
  * Age groups
  * Gender
  * Geographic regions (postcode analysis)
  * Other protected characteristics (where data available)
- Document baseline metrics
- Set alert thresholds for bias drift
```
**Owner**: ML Engineering + Compliance Team
**Compliance Impact**: EU AI Act Article 10, Equality Act 2010, FCA fairness

---

### **SHORT-TERM ACTIONS (30-90 days)**

#### 4. **Build Comprehensive AI Governance Framework**
```
Components:
a) AI Risk Register
   - Catalog all AI-related risks specific to credit scoring
   - Assign risk owners under SM&CR
   - Define risk appetite and tolerance levels

b) Model Governance Policy
   - Model development standards
   - Validation requirements (independent validation team)
   - Approval workflows for model deployment
   - Change management procedures

c) Incident Response Plan
   - Define AI failure scenarios
   - Escalation procedures
   - Customer remediation protocols
   - Regulatory notification triggers
```
**Owner**: Chief Risk Officer + ML Leadership
**Compliance Impact**: EU AI Act Article 9, FCA SM&CR

#### 5. **Implement Continuous Monitoring System**
```
Deploy SageMaker Model Monitor with:
- Data quality monitoring (input drift detection)
- Model quality monitoring (prediction accuracy tracking)
- Bias drift monitoring (ongoing fairness checks)
- Feature attribution drift

Configure CloudWatch dashboards for real-time alerting
Establish weekly automated reports to governance committee
```
**Owner**: MLOps Team
**Compliance Impact**: EU AI Act Article 61 (post-market monitoring)

#### 6. **Create Model Documentation Repository**
```
Using SageMaker Model Registry + custom documentation:
- Model Cards (intended use, limitations, performance metrics)
- Training data documentation (sources, quality checks, bias analysis)
- Validation reports (including fairness testing)
- Risk assessment documentation
- Version history with change justifications

Store in tamper-proof, auditable system (consider blockchain or WORM storage)
```
**Owner**: ML Engineering + Compliance
**Compliance Impact**: EU AI Act Article 11-12, audit readiness

#### 7. **Establish Human Oversight Mechanisms**
```
Implement tiered review system:
- Tier 1: Automatic approval (low-risk scores meeting thresholds)
- Tier 2: Automated alert + human review (borderline cases)
- Tier 3: Mandatory human review (adverse decisions, edge cases)

Create override capabilities with:
- Justification logging (why human overrode AI)
- Secondary reviewer approval for overrides
- Quarterly override pattern analysis
```
**Owner**: Credit Operations + ML Team
**Compliance Impact**: EU AI Act Article 14, GDPR Article 22(3)

---

### **MEDIUM-TERM ACTIONS (90-180 days)**

#### 8. **Develop Customer Transparency Portal**
```
Build self-service interface allowing customers to:
- View factors influencing their credit decision
- Understand feature importance (in plain language)
- See hypothetical scenarios ("What if my income were £5k higher?")
- Request human review of automated decisions
- Access historical decision explanations

Integrate with existing customer portal
Test with focus groups for comprehensibility
```
**Owner**: Product + UX Team
**Compliance Impact**: Consumer Duty, GDPR transparency

#### 9. **Conduct Independent Model Validation**
```
Engage third-party validator to:
- Review model development methodology
- Assess fairness and bias mitigation
- Test explainability accuracy
- Validate risk management processes
- Benchmark against industry standards

Repeat annually or upon significant model changes
```
**Owner**: Chief Risk Officer
**Compliance Impact**: EU AI Act conformity assessment, audit readiness

#### 10. **Implement Data Lineage Tracking**
```
Deploy comprehensive data lineage system:
- Track data from source systems through transformations to model input
- Document data quality checks at each stage
- Enable drill-down from any prediction to source data
- Automate lineage documentation updates

Consider tools: AWS DataZone, Apache Atlas, or specialized lineage platforms
```
**Owner**: Data Engineering
**Compliance Impact**: EU AI Act Article 10 (data governance)

#### 11. **Establish Board-Level AI Governance**
```
Actions:
- Appoint Consumer Duty Board Champion with AI oversight responsibility
- Assign SM&CR accountability for AI systems (likely CTO or CRO)
- Create quarterly Board AI Risk Reports including:
  * Model performance metrics
  * Bias monitoring results
  * Customer complaints related to AI
  * Regulatory compliance status
  * Emerging AI risks

- Annual strategy review of AI approach
```
**Owner**: Board + Executive Leadership
**Compliance Impact**: Consumer Duty, SM&CR, corporate governance

---

### **ONGOING REQUIREMENTS**

#### 12. **Continuous Compliance Program**
```
Quarterly Activities:
- Bias testing across protected characteristics
- Model performance validation
- Data quality audits
- Review of human override patterns
- Customer feedback analysis
- Regulatory horizon scanning

Annual Activities:
- Comprehensive model validation (internal + external)
- Board governance review
- Policy and procedure updates
- Staff training on AI risks and responsibilities
- Regulatory compliance self-assessment

Ad-Hoc:
- Pre-deployment validation for any model changes
- Post-incident reviews and remediation
- Response to regulatory inquiries or guidance updates
```

---

## 5. RISK PRIORITIZATION MATRIX

| Risk Area | Regulatory Impact | Implementation Complexity | Timeline Priority |
|-----------|------------------|--------------------------|------------------|
| Data Residency | ⚠️ CRITICAL (GDPR breach) | Low | IMMEDIATE |
| Explainability | ⚠️ CRITICAL (Consumer Duty) | Medium | IMMEDIATE |
| Bias Monitoring | ⚠️ HIGH (Equality Act) | Medium | IMMEDIATE |
| Governance Framework | 🟨 HIGH (EU AI Act) | High | SHORT-TERM |
| Human Oversight | 🟨 HIGH (GDPR Art 22) | Medium | SHORT-TERM |
| Documentation | 🟨 MEDIUM (Audit readiness) | Medium | SHORT-TERM |
| Customer Portal | 🟦 MEDIUM (Transparency) | High | MEDIUM-TERM |
| Independent Validation | 🟦 MEDIUM (Best practice) | Low | MEDIUM-TERM |

---

## 6. VENDOR-SPECIFIC CONSIDERATIONS (AWS)

### **AWS SageMaker Compliance Features to Activate:**

**Already Available (Must Configure):**
- ✅ **SageMaker Clarify**: Bias detection and explainability
- ✅ **SageMaker Model Monitor**: Continuous monitoring
- ✅ **SageMaker Model Registry**: Model versioning and metadata
- ✅ **AWS CloudTrail**: Audit logging for all SageMaker API calls
- ✅ **VPC Endpoints**: Private network connectivity
- ✅ **AWS KMS**: Encryption key management
- ✅ **IAM Policies**: Granular access control

**AWS Shared Responsibility Considerations:**
- AWS is responsible for: Infrastructure security, service availability
- **You are responsible for**: Data governance, model fairness, explainability implementation, compliance with financial services regulations

### **AWS-Specific Actions:**

1. **Enable AWS Artifact** to access compliance reports (SOC, ISO, etc.)
2. **Configure AWS Config Rules** for continuous compliance monitoring
3. **Implement AWS Audit Manager** for EU AI Act compliance tracking
4. **Use AWS Service Control Policies** to enforce regional restrictions
5. **Deploy AWS Security Hub** for unified security posture view

---

## 7. ESTIMATED RESOURCE REQUIREMENTS

### **Team Needs:**
- **ML Engineers**: 2-3 FTE for 6 months (explainability, monitoring implementation)
- **Data Engineers**: 1-2 FTE for 3 months (data lineage, residency controls)
- **Compliance Specialists**: 1 FTE ongoing (policy development, audits)
- **Cloud Architects**: 0.5 FTE for 3 months (AWS configuration)
- **Legal/Regulatory**: 0.5 FTE ongoing (regulatory interpretation)

### **Budget Estimate:**
- **AWS Service Costs**: +15-25% (monitoring, logging, regional constraints)
- **Third-Party Tools**: £50k-£100k/year (validation, lineage tracking)
- **External Audit**: £75k-£150k (initial comprehensive validation)
- **Staff Training**: £20k-£30k
- **Total First Year**: £300k-£500k (excluding internal staff costs)

---

## 8. SUCCESS METRICS

**Compliance KPIs to Track:**

✓ **Explainability Coverage**: 100% of credit decisions with documented feature attribution  
✓ **Bias Metrics**: Adverse impact ratio <1.2 across all protected characteristics  
✓ **Data Residency**: 0 instances of UK customer data leaving UK region  
✓ **Human Review Rate**: 5-10% of decisions reviewed by humans  
✓ **Documentation Completeness**: 100% of models with current validation reports  
✓ **Audit Readiness**: <48 hours to produce complete audit package  
✓ **Customer Complaints**: <1% complaints related to AI decision-making  
✓ **Regulatory Actions**: 0 FCA enforcement actions or warnings  

---

## 9. REGULATORY OUTLOOK & FUTURE-PROOFING

### **Emerging Requirements to Monitor:**

1. **UK AI Regulation Bill** (expected 2024-2025)
   - Likely to align with EU AI Act principles
   - May impose additional UK-specific requirements

2. **FCA AI Strategy Updates**
   - FCA's March 2024 consultation paper outcomes (pending)
   - Evolution of Consumer Duty guidance for AI

3. **EU AI Act Phase-In** (2024-2027)
   - High-risk systems: Compliance required by August 2026
   - Start preparation now despite phased timeline

4. **ISO Standards for AI**
   - ISO/IEC 42001 (AI Management System)
   - ISO/IEC 23894 (AI Risk Management)
   - Consider early adoption for competitive advantage

### **Recommendation**: Establish quarterly regulatory scanning process to stay ahead of changes.

---

## CONCLUSION

Your UK neobank faces **significant compliance gaps** in its AI credit scoring implementation. The combination of Consumer Duty, UK GDPR, and the incoming EU AI Act creates a stringent regulatory environment where **credit scoring is explicitly categorized as high-risk**.

### **Critical Path Forward:**

1. **Week 1**: Lock down data residency (IMMEDIATE risk mitigation)
2. **Month 1**: Deploy explainability and bias monitoring (Core compliance)
3. **Quarter 1**: Build governance framework and documentation (Systematic compliance)
4. **Quarter 2-3**: Enhance customer transparency and obtain independent validation (Competitive differentiation)

**The stakes are high**: FCA enforcement actions for Consumer Duty breaches, GDPR fines up to 4% of global turnover, and potential EU market access restrictions. However, getting this right positions your neobank as a leader in responsible AI lending.

**Next Step**: Convene cross-functional working group (Legal, Risk, ML, Product) to validate this analysis and create detailed implementation roadmap with assigned owners and deadlines.
