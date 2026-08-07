# InvoiceMatch AI — Feature Catalog

**Generated From**: pain_001 (Invoice/Receipt Reconciliation)  
**Opportunity Score**: 82/100  
**Product**: InvoiceMatch AI  
**Version**: 1.0 (MVP Scope)  
**Generated**: 2026-08-06

---

## Summary

| Metric | Value |
|--------|-------|
| Total Features | 18 |
| Must Have (P0) | 11 |
| Should Have (P1) | 5 |
| Could Have (P2) | 2 |
| Total User Stories | 42 |
| Estimated Build Time | 8 weeks (MVP) |

---

## Capability 1: Invoice Ingestion

### Feature 1.1: Email Forwarding (FR-001)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "15 hours/week manually reconciling invoices"  
**User Story**: As an ops manager, I want to forward invoices via email so I don't have to manually download from vendor portals.

**Acceptance Criteria**:
- [ ] User can forward email with PDF attachment to `invoices@{company}.invoicematch.ai`
- [ ] System extracts PDF attachment automatically
- [ ] System parses subject line for PO# (regex: `PO[:\s]*([0-9A-Z-]+)`)
- [ ] System validates sender is from allowed domain (configurable whitelist)
- [ ] System sends confirmation email within 5 minutes ("Received invoice #12345 from Acme")
- [ ] System rejects non-PDF attachments with error email ("Unsupported format: .xlsx")

**Metrics**:
- Success Rate: >95% emails processed without error
- Latency: <5 minutes from send to confirmation
- Coverage: 80% of invoices via email (Month 1)

**Technical Notes**:
- AWS SES for inbound email parsing
- S3 bucket for attachment storage
- Lambda trigger on S3 upload
- Deduplication via content hash (SHA-256)

**RICE Score**: 30.0 (Reach: 10, Impact: 9, Confidence: 100%, Effort: 3)

---

### Feature 1.2: PDF Upload (FR-002)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — Manual download from vendor portals  
**User Story**: As an ops manager, I want to upload PDF invoices via web UI so I can process batches quickly.

**Acceptance Criteria**:
- [ ] User can drag-and-drop PDF files onto upload zone
- [ ] User can select multiple files (max 50 per batch)
- [ ] System shows upload progress (files completed / total)
- [ ] System validates file type (PDF only, max 50MB)
- [ ] System displays preview of uploaded invoice (first page)
- [ ] System auto-extracts vendor name, amount, date on upload
- [ ] User can add tags (vendor, PO#, custom fields) before processing

**Metrics**:
- Upload Success Rate: >99%
- Batch Processing Time: <30 seconds for 50 invoices
- User Satisfaction: >4.5/5 (upload UX survey)

**Technical Notes**:
- React Dropzone component
- Presigned S3 URLs (direct upload)
- Progress bar with WebSocket updates
- Client-side PDF validation (file type, size)

**RICE Score**: 24.0 (Reach: 8, Impact: 8, Confidence: 100%, Effort: 2.5)

---

### Feature 1.3: Vendor Portal Scraping (FR-003)

**Priority**: P1 (Should Have)  
**Pain Reference**: pain_001 — "50+ vendors, different invoice formats"  
**User Story**: As a system, I want to auto-fetch invoices from vendor portals so users don't have to manually download.

**Acceptance Criteria**:
- [ ] System supports top 10 vendor portals (Amazon, Grainger, Uline, Home Depot, Lowe's, Staples, Office Depot, FedEx, UPS, USPS)
- [ ] User can store portal credentials (encrypted)
- [ ] System logs in daily and downloads new invoices (since last fetch)
- [ ] System handles CAPTCHA by pausing and alerting user
- [ ] System retries failed logins (max 3 attempts)
- [ ] System stores credentials encrypted (AES-256-GCM)

**Metrics**:
- Portal Coverage: 10 vendors (MVP)
- Fetch Success Rate: >90% (excluding CAPTCHA)
- Time Saved: 2 hours/week per user

**Technical Notes**:
- Puppeteer for headless browser automation
- Credentials encrypted with AWS KMS
- Scheduled job (cron: 0 2 * * *)
- Alert via email/Slack on CAPTCHA

**RICE Score**: 14.0 (Reach: 6, Impact: 7, Confidence: 90%, Effort: 6)

---

## Capability 2: OCR + Extraction

### Feature 2.1: Multi-Model OCR (FR-004)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — Manual data entry from invoices  
**User Story**: As a system, I want to extract text from invoices with 99%+ accuracy so matching can be automated.

**Acceptance Criteria**:
- [ ] System uses AWS Textract as primary OCR engine
- [ ] System falls back to Google Vision if Textract confidence <90%
- [ ] System falls back to Azure Form Recognizer if Google confidence <90%
- [ ] System caches OCR results (hash key: PDF content hash)
- [ ] System processes 100 pages/minute (throughput)
- [ ] System handles low-quality scans (blurry, skewed, partial)

**Metrics**:
- OCR Accuracy: >99% (printed text)
- Latency: <10 seconds per page (95th percentile)
- Cost: <$0.0015 per page (blended across providers)

**Technical Notes**:
- AWS Textract API ($1.50/1000 pages)
- Google Cloud Vision ($1.50/1000 pages)
- Azure Form Recognizer ($1.00/1000 pages)
- Redis cache for OCR results (TTL: 30 days)

**RICE Score**: 40.0 (Reach: 10, Impact: 10, Confidence: 100%, Effort: 2.5)

---

### Feature 2.2: LLM Line Item Extraction (FR-005)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "QuickBooks doesn't auto-match our vendor formats"  
**User Story**: As a system, I want to extract structured line items from OCR text so I can match to POs accurately.

**Acceptance Criteria**:
- [ ] System extracts: vendor name, invoice #, date, due date, total, tax
- [ ] System extracts line items: description, quantity, unit price, amount
- [ ] System returns confidence score (0-100) per field
- [ ] System handles 100+ vendor formats (no hardcoding)
- [ ] System supports multi-page invoices (up to 50 pages)
- [ ] System ignores handwritten annotations (or flags for review)

**Metrics**:
- Extraction Accuracy: >95% (field-level)
- Line Item Accuracy: >90% (per-item)
- Confidence Calibration: 95% confidence = 95% actual accuracy

**Technical Notes**:
- Anthropic Claude 3.5 Sonnet (structured JSON output)
- Prompt template with few-shot examples (10 vendor formats)
- Pydantic schema validation
- Fallback: Manual correction → system learns

**RICE Score**: 36.0 (Reach: 10, Impact: 9, Confidence: 100%, Effort: 2.5)

---

### Feature 2.3: Vendor Format Learning (FR-006)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "50+ vendors, different invoice formats"  
**User Story**: As a system, I want to learn vendor formats over time so extraction accuracy improves without manual configuration.

**Acceptance Criteria**:
- [ ] System tracks manual corrections per vendor
- [ ] After 3+ corrections, system identifies pattern (coordinates, keywords, regex)
- [ ] System creates extraction rule automatically
- [ ] System applies rule to next invoice from same vendor
- [ ] System validates rule accuracy (must be >80% on next 5 invoices)
- [ ] User can view/edit/delete extraction rules per vendor

**Metrics**:
- Learning Trigger: 3 corrections (configurable)
- Rule Accuracy: >80% on next 5 invoices
- Coverage: 80% of vendors have learned rules after 30 days

**Technical Notes**:
- Rule types: coordinate-based, keyword-based, regex-based, table-based
- Stored in PostgreSQL (JSONB column)
- Accuracy tracking: rolling 30-day average
- Auto-disable rule if accuracy drops <80%

**RICE Score**: 28.0 (Reach: 8, Impact: 9, Confidence: 95%, Effort: 4)

---

## Capability 3: Matching Engine

### Feature 3.1: 3-Way Matching (FR-007)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Need to match to POs AND bank transactions"  
**User Story**: As a finance manager, I want to match invoices to POs and bank transactions so I know we're paying for what we ordered.

**Acceptance Criteria**:
- [ ] System matches invoice total to bank transaction (±tolerance: $5 or 5%)
- [ ] System matches invoice PO# to PO system PO# (exact match)
- [ ] System matches line items to PO line items (quantity, price)
- [ ] System supports partial matches (split invoices)
- [ ] System supports split POs (one invoice, multiple POs)
- [ ] System calculates confidence score (weighted fields)

**Metrics**:
- Auto-Match Rate: >80% (invoices matched without review)
- Match Accuracy: >99.5% (correct matches)
- Confidence Calibration: 95% confidence = 95% actual accuracy

**Technical Notes**:
- Bank transactions: Plaid API (daily sync)
- POs: QuickBooks POs or CSV import
- Matching algorithm: Rule-based + ML ranking
- Confidence weights: Total (30%), Vendor (20%), Date (15%), PO# (20%), Lines (15%)

**RICE Score**: 32.0 (Reach: 10, Impact: 8, Confidence: 100%, Effort: 5)

---

### Feature 3.2: Confidence Scoring (FR-008)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — Trust issues with automation  
**User Story**: As an ops manager, I want to see confidence scores for matches so I know which invoices to review.

**Acceptance Criteria**:
- [ ] System calculates confidence score (0-100%) for each match
- [ ] Score breakdown shown per field (total, vendor, date, PO#, lines)
- [ ] Auto-approve if confidence ≥95%
- [ ] Flag for review if confidence 80-94% (low priority)
- [ ] Flag for review if confidence <80% (high priority)
- [ ] User can adjust auto-approve threshold (default 95%)

**Metrics**:
- Auto-Approve Rate: 80% (invoices approved without review)
- Review Rate: 20% (invoices needing human review)
- False Positive Rate: <0.5% (auto-approved but incorrect)

**Technical Notes**:
- Confidence formula: Weighted sum of field matches
- Thresholds configurable per vendor tier (A: 90%, B: 95%, C: 100%)
- UI: Progress bar with color (green: >95%, yellow: 80-94%, red: <80%)

**RICE Score**: 28.0 (Reach: 10, Impact: 7, Confidence: 100%, Effort: 2)

---

### Feature 3.3: Split Matching (FR-009)

**Priority**: P1 (Should Have)  
**Pain Reference**: pain_001 — "Consolidated invoices, split payments"  
**User Story**: As a bookkeeper, I want to match one invoice to multiple POs so I can handle consolidated billing.

**Acceptance Criteria**:
- [ ] User can split invoice total across multiple POs
- [ ] System validates: Sum of splits = invoice total
- [ ] System supports drag-and-drop allocation (invoice lines to POs)
- [ ] System auto-suggests split ratios (based on PO amounts)
- [ ] System posts multiple bills to QuickBooks (one per PO)
- [ ] System links split bills (audit trail)

**Metrics**:
- Split Match Rate: 10% of invoices (estimated)
- User Time Saved: 5 minutes per split invoice (vs manual)

**Technical Notes**:
- UI: Drag-and-drop with allocation bars
- Validation: Sum check before approval
- QBO: Create multiple bills with cross-reference

**RICE Score**: 12.0 (Reach: 5, Impact: 6, Confidence: 90%, Effort: 4)

---

## Capability 4: Exception Queue

### Feature 4.1: Smart Prioritization (FR-010)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Our bookkeeper misses duplicates because she's rushing"  
**User Story**: As an ops manager, I want to see high-priority exceptions first so I don't miss critical invoices.

**Acceptance Criteria**:
- [ ] System calculates priority score: `(Amount × 0.5) + (Age_Days × 10) + (Vendor_Importance × 20)`
- [ ] Queue sorted by priority (highest first)
- [ ] User can filter by: vendor, date range, amount, confidence
- [ ] User can sort by: priority, amount, age, vendor
- [ ] System highlights invoices >7 days old (SLA risk)
- [ ] System highlights invoices from critical vendors (Tier A)

**Metrics**:
- SLA Compliance: >98% (invoices reviewed within 7 days)
- Critical Vendor Coverage: 100% (all Tier A vendors reviewed same-day)

**Technical Notes**:
- Priority score calculated on ingestion
- Real-time updates (WebSocket or 30-sec polling)
- Vendor importance: User-configured (1-5 scale)

**RICE Score**: 20.0 (Reach: 8, Impact: 7, Confidence: 100%, Effort: 3)

---

### Feature 4.2: Inline Review (FR-011)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — Manual review bottleneck  
**User Story**: As an ops manager, I want to review and approve invoices without leaving the queue so I can process exceptions quickly.

**Acceptance Criteria**:
- [ ] Queue shows invoice cards (vendor, amount, age, confidence)
- [ ] Clicking card opens detail view (no page navigation)
- [ ] Detail view shows: PDF preview (left), extracted data (right)
- [ ] User can edit fields inline (vendor, amount, date, PO#, GL code)
- [ ] User can approve or reject with one click
- [ ] Keyboard shortcuts: A (approve), R (reject), E (edit), N (next), P (previous)

**Metrics**:
- Review Speed: 100 invoices/hour (target)
- Keyboard Usage: >50% of actions via shortcuts
- User Satisfaction: >4.5/5 (review UX survey)

**Technical Notes**:
- React modal for inline review
- PDF preview: PDF.js renderer
- Keyboard event listeners (global)
- Optimistic UI updates (instant feedback)

**RICE Score**: 24.0 (Reach: 10, Impact: 8, Confidence: 100%, Effort: 3)

---

### Feature 4.3: Batch Actions (FR-012)

**Priority**: P1 (Should Have)  
**Pain Reference**: pain_001 — High volume of exceptions  
**User Story**: As an ops manager, I want to approve/reject multiple invoices at once so I can clear the queue faster.

**Acceptance Criteria**:
- [ ] User can select multiple invoices (checkboxes)
- [ ] User can "approve all" selected invoices
- [ ] User can "reject all" selected invoices
- [ ] User can bulk edit GL code for selected invoices (same vendor)
- [ ] System validates each invoice before batch approval
- [ ] System shows batch results (success/failure per invoice)

**Metrics**:
- Batch Usage: >30% of approvals via batch actions
- Time Saved: 2 minutes per batch (vs individual approvals)

**Technical Notes**:
- Checkbox selection (shift-click for range)
- Background job processing (batch approve)
- Results modal with per-invoice status

**RICE Score**: 16.0 (Reach: 7, Impact: 6, Confidence: 95%, Effort: 3)

---

## Capability 5: QuickBooks Integration

### Feature 5.1: Bi-Directional Sync (FR-013)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Double-entry frustration"  
**User Story**: As a bookkeeper, I want InvoiceMatch to sync with QuickBooks so I don't have to enter data twice.

**Acceptance Criteria**:
- [ ] User can connect QuickBooks Online via OAuth 2.0
- [ ] System syncs vendors from QBO daily (DisplayName, Email, Balance)
- [ ] System syncs GL codes from QBO daily (Chart of Accounts)
- [ ] System syncs POs from QBO daily (open POs only)
- [ ] System posts approved invoices to QBO as Bills
- [ ] System attaches PDF to QBO Bill (up to 5MB)

**Metrics**:
- Sync Reliability: >99% (successful syncs)
- Latency: <10 seconds per bill (on approval)
- Error Rate: <1% (API errors, rate limits)

**Technical Notes**:
- QuickBooks API v3 (REST)
- Rate limit: 500 requests/minute
- Webhooks: Not supported (poll every 5 min)
- Attachment: QBO supports PDF up to 5MB

**RICE Score**: 32.0 (Reach: 10, Impact: 8, Confidence: 100%, Effort: 4)

---

### Feature 5.2: GL Code Mapping (FR-014)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — Manual GL coding  
**User Story**: As a bookkeeper, I want to map vendors to GL codes automatically so I don't have to code each invoice manually.

**Acceptance Criteria**:
- [ ] User can set default GL code per vendor
- [ ] System suggests GL code based on historical invoices
- [ ] System learns from manual corrections (after 3+ edits)
- [ ] System validates GL code against QBO Chart of Accounts
- [ ] System flags invalid GL codes for manual review
- [ ] System supports multi-code mapping (by line item)

**Metrics**:
- Auto-Coding Rate: >80% (invoices coded automatically)
- Accuracy: >95% (correct GL codes)

**Technical Notes**:
- Mapping table: Vendor ID → GL Code
- ML suggestion: Based on vendor category + historical patterns
- Validation: QBO API (list valid accounts)

**RICE Score**: 20.0 (Reach: 8, Impact: 7, Confidence: 95%, Effort: 3)

---

### Feature 5.3: Error Handling & Retry (FR-015)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Errors slip through when rushing"  
**User Story**: As a system, I want to handle QBO API errors gracefully so data integrity is maintained.

**Acceptance Criteria**:
- [ ] System retries failed QBO requests (max 3 attempts, exponential backoff)
- [ ] System alerts user after 3 failures ("QBO sync failed for invoice #12345")
- [ ] System queues failed invoices for manual review
- [ ] System logs all API errors (audit trail)
- [ ] System handles rate limits (pause 60 seconds, retry)
- [ ] System validates data before posting (schema check)

**Metrics**:
- Retry Success Rate: >90% (failed requests recovered)
- Alert Response Time: <4 hours (user resolves error)
- Data Integrity: 100% (no corrupted bills in QBO)

**Technical Notes**:
- Retry logic: Exponential backoff (1s, 10s, 60s)
- Alert: Email + Slack notification
- Queue: PostgreSQL (status: pending_retry)
- Logging: Structured JSON (CloudWatch)

**RICE Score**: 16.0 (Reach: 6, Impact: 7, Confidence: 95%, Effort: 2)

---

## Capability 6: Vendor Database

### Feature 6.1: Vendor Scoring (FR-016)

**Priority**: P1 (Should Have)  
**Pain Reference**: pain_001 — "50+ vendors, different reliability"  
**User Story**: As a procurement manager, I want to track vendor reliability so I can prioritize negotiations.

**Acceptance Criteria**:
- [ ] System calculates vendor score (0-100) based on:
  - On-Time Delivery (30%)
  - Invoice Accuracy (25%)
  - Price Consistency (20%)
  - Communication (15%)
  - Compliance (10%)
- [ ] System assigns tier: A (90-100), B (75-89), C (60-74), D (<60)
- [ ] System auto-adjusts matching threshold by tier (A: 90%, B: 95%, C: 100%)
- [ ] System alerts on score drop >20 points (fraud detection)
- [ ] User can view vendor score history (30-day trend)

**Metrics**:
- Score Accuracy: >90% (correlates with manual assessment)
- Fraud Detection: 100% (score drops flagged within 24 hours)

**Technical Notes**:
- Score calculation: Nightly batch job
- Tier thresholds: Configurable in settings
- Alert: Email + Slack (critical score drops)

**RICE Score**: 14.0 (Reach: 6, Impact: 6, Confidence: 90%, Effort: 3)

---

### Feature 6.2: Vendor Format Rules (FR-017)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Different invoice formats"  
**User Story**: As a system, I want to store extraction rules per vendor so I can auto-process future invoices.

**Acceptance Criteria**:
- [ ] System stores rules per vendor (coordinate, keyword, regex, table)
- [ ] User can view/edit rules in vendor detail page
- [ ] System shows rule accuracy (rolling 30-day average)
- [ ] System auto-disables rules with <80% accuracy
- [ ] User can import/export rules (CSV format)
- [ ] System suggests rules after 3+ manual corrections

**Metrics**:
- Rule Coverage: 80% of vendors have rules after 30 days
- Rule Accuracy: >85% (average across all rules)

**Technical Notes**:
- Rule storage: PostgreSQL (JSONB column)
- Rule types: Coordinate (x,y,w,h), keyword (regex), table (row/col detection)
- Import/Export: CSV with rule definitions

**RICE Score**: 20.0 (Reach: 8, Impact: 7, Confidence: 95%, Effort: 3)

---

## Capability 7: Audit Trail

### Feature 7.1: Immutable Action Log (FR-018)

**Priority**: P0 (Must Have)  
**Pain Reference**: pain_001 — "Audit compliance requirement"  
**User Story**: As a CFO, I want a complete history of all actions so I can audit the reconciliation process.

**Acceptance Criteria**:
- [ ] System logs every action: upload, extract, match, approve, edit, post
- [ ] Log is append-only (immutable)
- [ ] Log includes: user_id, timestamp, action, resource_type, resource_id, before, after
- [ ] System retains logs for 7 years (IRS requirement)
- [ ] User can export logs (CSV, PDF)
- [ ] System supports audit queries (by date, user, resource)

**Metrics**:
- Log Completeness: 100% (all actions logged)
- Retention: 7 years (automated archival to Glacier)
- Query Performance: <5 seconds (audit report generation)

**Technical Notes**:
- Log table: PostgreSQL (append-only constraint)
- Archival: S3 Glacier (after 90 days)
- Export: Background job (CSV/PDF generation)
- Hash chain: Optional tamper detection

**RICE Score**: 20.0 (Reach: 8, Impact: 7, Confidence: 100%, Effort: 2)

---

## Prioritization Summary

### MoSCoW Breakdown

| Priority | Count | % | Total Effort (weeks) |
|----------|-------|---|---------------------|
| **Must Have (P0)** | 11 | 61% | 5.5 weeks |
| **Should Have (P1)** | 5 | 28% | 2.5 weeks |
| **Could Have (P2)** | 2 | 11% | 1 week |
| **Total** | **18** | **100%** | **9 weeks** |

### MVP Scope (Weeks 1-8)

**Included (P0 Must Have)**:
- FR-001: Email Forwarding
- FR-002: PDF Upload
- FR-004: Multi-Model OCR
- FR-005: LLM Extraction
- FR-006: Vendor Format Learning
- FR-007: 3-Way Matching
- FR-008: Confidence Scoring
- FR-010: Smart Prioritization
- FR-011: Inline Review
- FR-013: QBO Bi-Directional Sync
- FR-014: GL Code Mapping
- FR-015: Error Handling & Retry
- FR-017: Vendor Format Rules
- FR-018: Immutable Action Log

**Deferred to V1 (Weeks 9-12)**:
- FR-003: Vendor Portal Scraping
- FR-009: Split Matching
- FR-012: Batch Actions
- FR-016: Vendor Scoring

---

## RICE Ranking (Top 10)

| Rank | Feature | RICE Score | Priority |
|------|---------|------------|----------|
| 1 | FR-004: Multi-Model OCR | 40.0 | P0 |
| 2 | FR-005: LLM Extraction | 36.0 | P0 |
| 3 | FR-001: Email Forwarding | 30.0 | P0 |
| 4 | FR-007: 3-Way Matching | 32.0 | P0 |
| 5 | FR-013: QBO Sync | 32.0 | P0 |
| 6 | FR-006: Vendor Format Learning | 28.0 | P0 |
| 7 | FR-008: Confidence Scoring | 28.0 | P0 |
| 8 | FR-002: PDF Upload | 24.0 | P0 |
| 9 | FR-011: Inline Review | 24.0 | P0 |
| 10 | FR-010: Smart Prioritization | 20.0 | P0 |

---

## Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- FR-002: PDF Upload
- FR-004: Multi-Model OCR (basic integration)
- FR-018: Immutable Action Log (schema)
- Database schema, API scaffolding

### Phase 2: Core Logic (Weeks 3-4)
- FR-005: LLM Extraction
- FR-006: Vendor Format Learning
- FR-007: 3-Way Matching
- FR-008: Confidence Scoring

### Phase 3: Integration (Weeks 5-6)
- FR-001: Email Forwarding
- FR-013: QBO Bi-Directional Sync
- FR-014: GL Code Mapping
- FR-015: Error Handling

### Phase 4: UX & Polish (Weeks 7-8)
- FR-010: Smart Prioritization
- FR-011: Inline Review
- FR-017: Vendor Format Rules (UI)
- Performance optimization, documentation

---

**Feature Catalog Complete** ✅

**Next Steps**:
1. Review features with engineering team
2. Estimate story points per feature
3. Create user stories (USER-STORIES.md)
4. Write technical specs (TECH-SPECS.md)
5. Start Phase 1 implementation

---

*Generated by idea-to-features skill v1.0*  
*Source: pain_001 (Invoice/Receipt Reconciliation)*  
*Opportunity Score: 82/100*
