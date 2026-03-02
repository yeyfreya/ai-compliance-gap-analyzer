# Compliance Gap Analysis Report

**Version:** v0.5  
**Run ID:** `3c8c99f8-00c7-43f9-8926-416e5c519ea0`  
**Use Case:** 3. AI credit scoring model that evaluates loan applications  
**Technology:** AWS SageMaker  
**Industry:** UK neobank (financial services)  
**Generated:** 2026-02-28 22:10:51  
**Generation Time:** 85.8s total (planning: 28.7s, research: 11.1s, analysis: 46.0s)  

---

## Search Queries Used

- UK FCA requirements AI machine learning credit scoring automated decisions 2024
- AWS SageMaker UK GDPR compliance data processing financial services
- UK algorithmic fairness credit scoring Equality Act discrimination 2024
- automated credit decision explainability requirements UK consumer credit
- EU AI Act impact UK financial services credit risk models

---

## Analysis

### 1. Compliance Gap Matrix

| Potential Gap | Risk Level | Regulatory Context | Priority |
|---------------|-----------|-------------------|----------|
| Automated decision rights & meaningful human involvement | CRITICAL | UK GDPR Article 22 equivalent, FCA consumer protection principles | 1 |
| Explainability framework for adverse credit decisions | CRITICAL | UK GDPR transparency requirements, FCA expectations on algorithmic accountability | 2 |
| Algorithmic bias testing & protected characteristics monitoring | HIGH | Equality Act 2010, FCA fair treatment requirements | 3 |
| Model governance documentation & audit trail | HIGH | FCA Senior Managers & Certification Regime (SM&CR), operational resilience | 4 |
| AWS data processing agreement & UK data residency | HIGH | UK GDPR data processor requirements, financial services data localization expectations | 5 |
| Consumer notification of AI use in credit decisions | MEDIUM | UK GDPR transparency obligations, Consumer Credit Act disclosure expectations | 6 |
| Third-party AI system modification tracking | MEDIUM | EU AI Act (if serving EU customers), shared responsibility model with AWS | 7 |

### 2. Key Regulatory Landscape

- **UK GDPR & Data Protection Act 2018**: Requires explicit protections for automated decision-making including profiling in credit decisions; mandates data processing agreements with AWS as a processor
- **FCA Principles for Businesses**: Principle 6 (customers' interests) and Principle 7 (clear information) apply directly to AI credit scoring; FCA actively researching AI explainability standards for credit decisions
- **Equality Act 2010**: Prohibits discrimination based on protected characteristics (age, race, gender, etc.); applies to algorithmic credit scoring models that may inadvertently create discriminatory outcomes
- **Consumer Credit Act 1974**: Governs credit lending in UK; intersects with data protection rights around automated creditworthiness assessments
- **EU AI Act (conditional)**: If serving EU customers, credit scoring is classified as "high-risk AI system" with stringent requirements for transparency, human oversight, and bias monitoring starting August 2026

### 3. Gap Details

**CRITICAL Gaps:**

**Automated decision rights & meaningful human involvement**
- UK GDPR requires individuals not be subject to solely automated decisions that significantly affect them without explicit consent or appropriate safeguards. Worth confirming your credit scoring workflow includes meaningful human review for final decisions, particularly for adverse outcomes. This is the highest priority gap because the FCA is actively scrutinizing how firms implement human oversight in AI-driven credit decisions.

**Explainability framework for adverse credit decisions**
- When denying credit, you need to provide specific, intelligible reasons under UK GDPR's transparency requirements. SageMaker models can be "black boxes" — it's worth ensuring you have a robust explainability layer (SHAP values, feature importance, etc.) that translates model outputs into consumer-friendly explanations. The FCA's recent research note specifically highlighted this as an area they're monitoring closely.

**HIGH Gaps:**

**Algorithmic bias testing & protected characteristics monitoring**
- The Equality Act 2010 applies to AI systems that may create indirect discrimination. If not already in place, consider implementing regular bias testing across protected characteristics and monitoring for disparate impact (e.g., approval rates by gender, ethnicity, postcode as proxy for race). This should be documented as part of your model validation process.

**Model governance documentation & audit trail**
- Financial services regulators expect robust model risk management. Worth confirming you have documented: model development methodology, validation testing results, ongoing performance monitoring, change management processes, and accountability structure. This ties into FCA's SM&CR expectations that someone senior owns the AI credit decision outcomes.

**AWS data processing agreement & UK data residency**
- You need a compliant Data Processing Agreement with AWS that meets UK GDPR Article 28 requirements. Worth verifying: where SageMaker is processing and storing customer data (UK region preferred for financial services), what sub-processors AWS uses, and whether data transfer mechanisms are documented if data leaves the UK. AWS provides UK GDPR addendum but it's worth confirming it's properly executed for your account.

**MEDIUM Gaps:**

**Consumer notification of AI use in credit decisions**: Your privacy notice and credit application process should clearly disclose that AI/ML models are used in creditworthiness assessment, including the logic involved and significance of the processing.

**Third-party AI system modification tracking**: If you've significantly customized AWS SageMaker's algorithms (not just trained on your data), this could trigger additional compliance obligations under the EU AI Act if you serve European customers — worth tracking what qualifies as "modification" versus standard use.

### 4. Recommended Next Steps

**Worth doing soon:**
1. **Audit your decision workflow** — Map out exactly where automated scoring happens versus human review. If 100% automated for any decision type, you may want to introduce a human-in-the-loop checkpoint, especially for adverse decisions.
2. **Document your explainability approach** — Work with your ML team to ensure SageMaker model outputs can generate specific, accurate reasons for credit decisions. Test these explanations with sample adverse decisions to confirm they're genuinely helpful.
3. **Review AWS contracts** — Confirm your Data Processing Agreement is signed and check which AWS region your SageMaker workloads run in. If not UK-specific, consider whether migration is appropriate for a financial services use case.

**Over the next few weeks:**
4. **Implement bias testing protocol** — Run fairness metrics (demographic parity, equalized odds) on your model's predictions across protected characteristics. Document the results and any mitigation steps taken. This should become part of your regular model validation cycle.
5. **Build model governance documentation** — Create a model risk management framework that covers development, validation, monitoring, and change control. Assign clear ownership under your SM&CR structure.

**Longer-term considerations:**
6. **Monitor EU AI Act developments** — If you have or plan to have EU customers, start preparing for high-risk AI requirements. The Act's credit scoring provisions take effect August 2026, but building compliant systems takes time.
7. **Engage with FCA on AI strategy** — The FCA is asking firms to demonstrate how they're implementing the government's five AI principles (safety, transparency, fairness, accountability, contestability). Consider documenting your approach proactively.

### 5. Bottom Line

Your AI credit scoring system sits at the intersection of data protection, consumer credit, and equality law — all areas where UK regulators are paying close attention to algorithmic decision-making. The most important potential gap to review first is ensuring meaningful human involvement in credit decisions and having a robust explainability framework for adverse outcomes. The good news: AWS SageMaker provides tools to support compliance (like SageMaker Clarify for bias detection), and the FCA is taking a principles-based rather than prescriptive approach, giving you flexibility in how you address these areas. Focus on the critical gaps around automated decision rights and explainability, and you'll be well-positioned as regulatory expectations continue to evolve.
