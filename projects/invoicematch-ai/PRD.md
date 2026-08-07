# InvoiceMatch AI — Product Requirements Document

**Document Control**
- Version: 1.0
- Status: Draft
- Created: 2026-08-06
- Author: AI SaaS Startup Factory (Pain-First Pipeline)
- Opportunity Score: 82/100
- Pain-DB Reference: pain_001

---

## 1. Executive Summary

### Vision
Eliminate manual invoice reconciliation for SMBs by automating 80% of the 15 hours/week currently spent matching invoices from 50+ vendors to bank transactions and purchase orders.

### Problem
SMBs spend 15+ hours/week manually reconciling invoices from 50+ vendors. QuickBooks and similar tools don't auto-match custom vendor formats, forcing businesses to either hire VAs ($3,200/mo) or sacrifice accuracy.

### Solution
InvoiceMatch AI: Local-first invoice reconciliation engine that:
1. Ingests invoices from any format (PDF, email, portal)
2. Extracts line items with OCR + LLM
3. Auto-matches to bank transactions and POs
4. Flags exceptions for human review
5. Posts approved matches to accounting system

### Business Value
- **Time Savings**: 12 hours/week (80% automation of 15 hrs)
- **Cost Savings**: $2,400/mo (vs $3,200/mo VA)
- **Accuracy**: 99.5% match rate (vs ~95% manual)
- **Speed**: Real-time reconciliation (vs weekly batch)

### Success Definition (12 Months)
- 500 paying customers
- $150K MRR
- 99.5% auto-match rate
- <2% exception rate
- NPS > 50

---

## 2. Strategic Context

### Market Size
- **TAM**: $12B (SMB accounting automation)
- **SAM**: $2.4B (SMBs with 50+ vendors/month)
- **SOM**: $48M (Year 3 target: 2% SAM)

### Competitors
| Competitor | Price | Gap |
|------------|-------|-----|
| QuickBooks Auto-Match | $80/mo | Doesn't handle custom formats |
| Bill.com | $399/mo | Overkill for SMB, complex setup |
| Melio | Free | Payments only, no reconciliation |
| AvidXchange | Enterprise | Too expensive for SMB |
| Manual (VA) | $3,200/mo | Error-prone, slow |

### Positioning
"QuickBooks on steroids for invoice reconciliation — 80% automation at 1/10th the cost of a VA"

### Differentiators
1. **Format-Agnostic OCR**: Handles any vendor invoice format (not just major vendors)
2. **Local-First Processing**: Privacy-focused, no cloud upload required
3. **Exception-First UX**: Only shows what needs human review (saves time)
4. **Multi-Way Matching**: Invoice ↔ Bank Transaction ↔ PO (not just 2-way)
5. **Vendor Learning**: Gets smarter with each invoice from same vendor

---

## 3. Problem Statement (Validated by Pain Signals)

### Primary Pain (from pain_001)
> "We spend 15 hours/week manually reconciling invoices from 50+ vendors. QuickBooks doesn't auto-match our vendor formats. Considering hiring VA at $20/hr but would prefer software."

### Supporting Evidence
- **Frequency**: Weekly (15 hrs)
- **Existing Spend**: $3,200/mo (VA cost)
- **Willingness to Pay**: $200-500/mo
- **Automatable**: 80%
- **Bad Incumbent**: QuickBooks (custom format gap)

### Additional Pain Signals (Cluster Analysis)
From 5 related pain statements in cluster "Invoice/Receipt Reconciliation":
1. "Invoice matching takes 3 hours every Friday" (frequency: weekly)
2. "We have 80 vendors, each with different invoice formats" (complexity: high)
3. "Our bookkeeper misses duplicates because she's rushing" (accuracy: 95%)
4. "Need to match to POs AND bank transactions" (3-way matching need)
5. "Vendor portals don't export in consistent format" (ingestion pain)

### Why Now
- **OCR Accuracy**: 99%+ at commodity prices (AWS Textract, Google Vision)
- **LLM Extraction**: Structured data from unstructured invoices (GPT-4, Claude)
- **Accounting APIs**: Plaid, QuickBooks API, Xero API mature
- **Remote Work**: Distributed teams need async reconciliation
- **AI Expectation**: SMBs expect automation (post-2023 AI boom)

---

## 4. Goals & Objectives

### Business Goals (Year 1)
| Goal | Target | Metric |
|------|--------|--------|
| Revenue | $1.8M ARR | MRR growth |
| Customers | 500 | Active subscriptions |
| Retention | 95% | Monthly churn <5% |
| NPS | 50+ | Quarterly survey |

### Product Goals (MVP → V1)
| Goal | Target | Metric |
|------|--------|--------|
| Auto-Match Rate | 80% | % invoices matched without review |
| Accuracy | 99.5% | % correct matches |
| Processing Time | <30 sec/invoice | End-to-end latency |
| Vendor Coverage | 100+ formats | Unique vendor templates |

### User Goals
| Goal | Target | Metric |
|------|--------|--------|
| Time Saved | 12 hrs/week | User self-report |
| Exception Rate | <2% | % invoices needing review |
| Setup Time | <1 hour | Time to first match |
| Confidence | 95%+ | User trust in auto-matches |

---

## 5. Personas

### Primary: Operations Olivia
**Role**: Operations Manager  
**Company**: 50-employee distribution company  
**Pain**: Spends every Friday reconciling 200+ invoices  
**Goal**: Reclaim 12 hours/week for strategic work  
**Tech Savvy**: Intermediate (uses QuickBooks daily)  
**Quote**: "I didn't become an ops manager to do data entry"

**Workflow**:
1. Downloads invoices from 50+ vendor portals
2. Manually enters into QuickBooks
3. Matches to bank transactions
4. Flags discrepancies
5. Emails vendors for corrections
6. Posts to GL

**Success**: "I want to review exceptions, not enter data"

---

### Secondary: Finance Frank
**Role**: CFO / Owner  
**Company**: $10M revenue SMB  
**Pain**: Paying $3,200/mo for VA, still worried about errors  
**Goal**: Reduce costs, improve accuracy  
**Tech Savvy**: Low (delegates to ops)  
**Quote**: "I need to know the books are right without micromanaging"

**Workflow**:
1. Reviews monthly P&L
2. Notices reconciliation errors
3. Asks ops to fix
4. Approves VA overtime

**Success**: "I want confidence in the numbers without involvement"

---

### Tertiary: Bookkeeper Beth
**Role**: External Bookkeeper (serves 10 clients)  
**Company**: Freelance  
**Pain**: Manual reconciliation limits client capacity  
**Goal**: Scale from 10 to 20 clients without hiring  
**Tech Savvy**: High (power user of accounting tools)  
**Quote**: "Every hour saved on reconciliation is a new client"

**Workflow**:
1. Logs into each client's QuickBooks
2. Reconciles invoices
3. Bills clients monthly
4. Manages team of VAs

**Success**: "I want to double my client load without doubling my team"

---

## 6. User Research

### Interviews Conducted (Pain-First Pipeline)
- **5 pain statements** extracted from Reddit, HN, GitHub
- **Cluster analysis**: 12 unique pain clusters, Invoice/Reconciliation = #1
- **WTP validation**: $200-500/mo (vs $3,200/mo VA)
- **Frequency**: Weekly (15 hrs)

### Market Validation
- **VSCode extensions**: 264K+ installs for Excel automation (adjacent pain)
- **QuickBooks complaints**: Common on G2/Capterra (format matching gap)
- **Competitor pricing**: Bill.com $399/mo (overkill), QuickBooks $80/mo (limited)

### Assumptions to Validate (Next 2 Weeks)
1. SMBs will pay $200-500/mo for 80% automation
2. 99.5% accuracy achievable with current OCR + LLM
3. Setup time <1 hour for 50+ vendors
4. Exception rate <2% achievable

---

## 7. Scope Definition

### In Scope (MVP)
1. **Invoice Ingestion**: PDF upload, email forwarding, vendor portal scraping (top 10 vendors)
2. **OCR + Extraction**: Line-item extraction with vendor format learning
3. **3-Way Matching**: Invoice ↔ Bank Transaction ↔ PO
4. **Exception Queue**: Review UI for unmatched invoices
5. **QuickBooks Integration**: Post approved matches to QBO
6. **Vendor Database**: Learn vendor formats over time
7. **Audit Trail**: Full history of matches, edits, approvals

### Out of Scope (Post-MVP)
1. **Multi-Entity Consolidation**: Holding company support
2. **International**: Multi-currency, VAT handling
3. **AP Automation**: Payment execution (Bill.com competitor)
4. **Inventory**: PO-to-inventory matching
5. **Custom ERP Integrations**: NetSuite, SAP, Microsoft Dynamics
6. **Mobile App**: iOS/Android native apps

### Future Considerations (V2+)
1. **Xero Integration**: Second accounting platform
2. **Sage, QuickBooks Desktop**: Legacy support
3. **Vendor Portal Auto-Login**: Credentials management
4. **Duplicate Detection**: Cross-vendor duplicate invoices
5. **Fraud Detection**: Anomaly detection on vendor patterns
6. **Cash Flow Forecasting**: Based on invoice due dates

---

## 8. User Journey

### Happy Path (80% of invoices)
```
1. Invoice arrives (email/PDF/upload)
2. System extracts: vendor, amount, date, PO#, line items
3. System matches to: bank transaction + PO
4. Confidence score: 98% → Auto-approve
5. Post to QuickBooks: Bill created, GL coded
6. User notified: "200 invoices reconciled, 4 exceptions"
```

### Exception Path (20% of invoices)
```
1. Invoice arrives (email/PDF/upload)
2. System extracts: vendor, amount, date, PO#, line items
3. System attempts match: No PO found OR amount mismatch
4. Confidence score: 65% → Flag for review
5. User reviews in Exception Queue:
   - Sees invoice preview
   - Sees suggested matches
   - Edits GL code / amount / PO link
   - Approves or rejects
6. If approved: Post to QuickBooks
7. If rejected: Email vendor for corrected invoice
8. System learns: Updates vendor format rules
```

### Setup Journey (First-Time User)
```
1. Sign up → Connect QuickBooks (OAuth)
2. Connect bank account (Plaid)
3. Upload 10 sample invoices (training)
4. System learns vendor formats
5. Configure matching rules:
   - Tolerance: $5 or 5%
   - Auto-approve threshold: 95% confidence
   - GL codes by vendor
6. Import historical vendors (CSV)
7. Enable email forwarding (invoices@yourcompany.invoicematch.ai)
8. First auto-reconciliation runs
9. Review exceptions (15-20% initially)
10. System improves with each invoice
```

---

## 9. Functional Requirements

### FR-001: Invoice Ingestion
**Priority**: P0  
**User Story**: As an ops manager, I want to ingest invoices from multiple sources so I don't have to manually download from vendor portals.

**Acceptance Criteria**:
- [ ] Upload PDF via web UI
- [ ] Forward email to unique address (invoices@company.invoicematch.ai)
- [ ] Auto-fetch from top 10 vendor portals (Amazon, Grainger, Uline, etc.)
- [ ] Support multi-page PDFs (up to 50 pages)
- [ ] Support scanned images (JPEG, PNG, TIFF)
- [ ] Deduplicate on upload (hash check)

**Technical Notes**:
- Email parsing: Use AWS SES or SendGrid Inbound Parse
- Portal scraping: Puppeteer + stored credentials (encrypted)
- File storage: S3 with lifecycle policy (90-day retention)

---

### FR-002: OCR + Line Item Extraction
**Priority**: P0  
**User Story**: As a system, I want to extract structured data from any vendor invoice format so I can match without manual entry.

**Acceptance Criteria**:
- [ ] Extract: vendor name, invoice #, date, due date, total, tax
- [ ] Extract line items: description, quantity, unit price, amount
- [ ] Handle 100+ vendor formats (learned over time)
- [ ] Confidence score per field (0-100%)
- [ ] Support handwritten annotations (ignore or flag)
- [ ] Handle low-quality scans (blurry, skewed, partial)

**Technical Notes**:
- OCR: AWS Textract (99% accuracy, $1.50/1000 pages)
- LLM Extraction: Claude 3.5 Sonnet (structured JSON output)
- Vendor Format Learning: Store extraction rules per vendor ID
- Fallback: Manual correction → system learns

---

### FR-003: 3-Way Matching Engine
**Priority**: P0  
**User Story**: As a finance manager, I want to match invoices to POs and bank transactions so I know we're paying for what we ordered.

**Acceptance Criteria**:
- [ ] Match invoice total to bank transaction amount (±tolerance)
- [ ] Match invoice PO# to PO system PO#
- [ ] Match line items to PO line items (quantity, price)
- [ ] Support partial matches (split invoices)
- [ ] Handle split POs (one invoice, multiple POs)
- [ ] Handle consolidated invoices (one invoice, multiple orders)
- [ ] Configurable tolerance: $5 or 5% (default)

**Technical Notes**:
- Bank transactions: Plaid API (daily sync)
- POs: QuickBooks POs or CSV import
- Matching algorithm: Rule-based + ML ranking
- Confidence score: Weighted by field matches

---

### FR-004: Exception Queue
**Priority**: P0  
**User Story**: As an ops manager, I want to see only invoices needing review so I can focus my time on exceptions.

**Acceptance Criteria**:
- [ ] Queue shows invoices with confidence <95%
- [ ] Sort by: amount (high→low), age (oldest first), vendor
- [ ] Batch actions: approve all, reject all, bulk edit
- [ ] Inline editing: GL code, PO link, amount correction
- [ ] Preview: Invoice PDF side-by-side with extracted data
- [ ] Comments: Add notes for audit trail
- [ ] SLA tracking: Invoices >7 days old highlighted

**Technical Notes**:
- Queue stored in PostgreSQL
- Real-time updates: WebSocket or polling (30 sec)
- Batch actions: Background job processing

---

### FR-005: QuickBooks Integration
**Priority**: P0  
**User Story**: As a bookkeeper, I want approved matches posted to QuickBooks automatically so I don't have to double-enter data.

**Acceptance Criteria**:
- [ ] OAuth 2.0 connection (QuickBooks Online)
- [ ] Create Bill in QBO on approval
- [ ] Map GL codes from InvoiceMatch to QBO Chart of Accounts
- [ ] Map vendors (create if not exists)
- [ ] Attach PDF to QBO Bill
- [ ] Sync status: Pending, Posted, Error
- [ ] Error handling: Retry 3x, then alert

**Technical Notes**:
- QuickBooks API: v3 (REST)
- Rate limits: 500 requests/minute (sufficient)
- Webhooks: Not supported (poll for changes)
- Attachment: QBO supports PDF up to 5MB

---

### FR-006: Vendor Database
**Priority**: P1  
**User Story**: As a system, I want to learn vendor formats over time so extraction accuracy improves.

**Acceptance Criteria**:
- [ ] Store vendor profile: name, email, typical amount, payment terms
- [ ] Store extraction rules per vendor (field mappings)
- [ ] Track accuracy per vendor (confidence vs actual)
- [ ] Auto-suggest corrections after 3+ manual edits
- [ ] Vendor scoring: reliability, on-time %, error rate
- [ ] Duplicate detection: Same vendor, different names

**Technical Notes**:
- Vendor table in PostgreSQL
- Extraction rules: JSON blob (field → regex/XPath)
- Accuracy tracking: Rolling 30-day average

---

### FR-007: Audit Trail
**Priority**: P0  
**User Story**: As a CFO, I want a complete history of all matches and edits so I can audit the reconciliation process.

**Acceptance Criteria**:
- [ ] Log every action: upload, extract, match, approve, edit, post
- [ ] Immutable log (append-only)
- [ ] User attribution: Who did what, when
- [ ] Before/after snapshots for edits
- [ ] Export: CSV, PDF audit report
- [ ] Retention: 7 years (IRS requirement)

**Technical Notes**:
- Audit log table: PostgreSQL (append-only)
- Hash chain: Prevent tampering (optional)
- Export: Background job, S3 storage

---

## 10. Feature Specifications

### 10.1 Invoice Ingestion Pipeline

#### Feature: Email Forwarding
**Description**: Users forward vendor invoices to unique email address; system auto-processes.

**Flow**:
```
Vendor Invoice → User Email → Forward to invoices@company.invoicematch.ai
→ SES Inbound Parse → S3 Bucket → Lambda Trigger → OCR Queue
```

**Configuration**:
- Unique email per company: `invoices@{subdomain}.invoicematch.ai`
- Allowed senders: Whitelist vendor domains (optional)
- Subject parsing: Extract PO# from subject line (regex configurable)

**Error Handling**:
- Unsupported attachment: Email user "We couldn't process [filename]"
- Virus detected: Quarantine, alert security team
- Duplicate: Silently ignore (hash match)

---

#### Feature: Vendor Portal Scraping
**Description**: Auto-login to top 10 vendor portals, download new invoices.

**Supported Vendors (MVP)**:
1. Amazon Business
2. Grainger
3. Uline
4. Home Depot
5. Lowe's
6. Staples
7. Office Depot
8. FedEx
9. UPS
10. USPS

**Flow**:
```
Daily Job → Load Credentials (encrypted) → Puppeteer Login
→ Download New Invoices (since last run) → S3 → OCR Queue
```

**Security**:
- Credentials: AES-256-GCM encrypted at rest
- Access: User-scoped (company isolation)
- Rotation: User updates if vendor requires 2FA

**Error Handling**:
- Login failed: Alert user "Portal login failed for [vendor]"
- CAPTCHA: Pause, alert user for manual resolution
- Format change: Flag for template update

---

### 10.2 OCR + Extraction Engine

#### Feature: Multi-Model OCR Fallback
**Description**: Use best OCR model per invoice quality; fallback if confidence low.

**Model Hierarchy**:
1. **AWS Textract** (default, 99% accuracy, $1.50/1000 pages)
2. **Google Cloud Vision** (fallback, 98.5% accuracy, $1.50/1000 pages)
3. **Azure Form Recognizer** (last resort, 98% accuracy, $1.00/1000 pages)

**Flow**:
```
Invoice PDF → Textract → Confidence Score
→ If <90%: Try Google Vision → If <90%: Try Azure
→ Best Result → LLM Extraction → Structured JSON
```

**Cost Optimization**:
- Cache OCR results (hash key)
- Skip OCR if previously processed (dedup)
- Batch processing: 100+ pages → volume discount

---

#### Feature: Vendor Format Learning
**Description**: System learns extraction rules per vendor after 3+ manual corrections.

**Flow**:
```
Invoice Processed → User Edits 3+ Fields
→ System Compares: Extracted vs Corrected
→ Identifies Pattern: "Vendor always puts PO# in bottom-right"
→ Creates Rule: Extract PO# from coordinates (x1,y1,x2,y2)
→ Applies to Future Invoices from Same Vendor
```

**Rule Types**:
- **Coordinate-based**: Extract from fixed position (common for templated invoices)
- **Keyword-based**: "PO#:" → next 10 chars
- **Regex-based**: Invoice # = `\d{6,10}`
- **Table-based**: Line items in grid (detect rows/cols)

**Accuracy Tracking**:
- Per-vendor accuracy: Rolling 30-day average
- Auto-disable rule if accuracy <80%
- Manual override: User can delete bad rules

---

### 10.3 Matching Engine

#### Feature: Confidence Scoring
**Description**: Calculate match confidence (0-100%) based on field matches.

**Scoring Weights**:
| Field | Weight | Match Criteria |
|-------|--------|----------------|
| Invoice Total | 30% | Exact or ±tolerance |
| Vendor Name | 20% | Fuzzy match (Levenshtein <3) |
| Invoice Date | 15% | ±3 days |
| PO# | 20% | Exact match |
| Line Items | 15% | 80%+ line match |

**Confidence Thresholds**:
- **95-100%**: Auto-approve (no review)
- **80-94%**: Flag for review (low priority)
- **50-79%**: Flag for review (high priority)
- **<50%**: Reject (manual entry required)

**Example**:
```
Invoice: $1,234.56, Vendor: "Acme Inc", Date: 2026-08-01, PO: PO-12345
Bank Tx: $1,234.56, Payee: "ACME INDUSTRIAL", Date: 2026-08-03
PO: PO-12345, Amount: $1,234.56

Score Calculation:
- Total: 30% (exact match)
- Vendor: 18% (fuzzy match, "Acme Inc" vs "ACME INDUSTRIAL")
- Date: 13% (within ±3 days)
- PO#: 20% (exact match)
- Lines: 15% (not checked, assume match)
Total: 96% → Auto-approve
```

---

#### Feature: Split Matching
**Description**: Handle one invoice matching multiple POs or bank transactions.

**Use Cases**:
1. **Consolidated Invoice**: One invoice, 3 POs (monthly consolidation)
2. **Split Payment**: One invoice, 2 bank transactions (partial payments)
3. **Partial Receipt**: One PO, 2 invoices (backorder split)

**Flow**:
```
Invoice Total: $5,000
→ System Finds: PO-101 ($2,000), PO-102 ($3,000)
→ Suggests: Split Match (PO-101: $2K, PO-102: $3K)
→ User Confirms → Post to QBO (2 Bills, linked to POs)
```

**UI**:
- Drag-and-drop: Allocate invoice lines to POs
- Auto-suggest: System recommends split ratios
- Validation: Sum of splits = invoice total

---

### 10.4 Exception Queue

#### Feature: Smart Prioritization
**Description**: Sort exception queue by business impact (amount, age, vendor importance).

**Priority Score**:
```
Priority = (Amount × 0.5) + (Age_Days × 10) + (Vendor_Importance × 20)

Where:
- Amount: Invoice total (normalized 0-100)
- Age_Days: Days since received (capped at 30)
- Vendor_Importance: 1-5 (user-configured, critical vendors = 5)
```

**Example**:
```
Invoice A: $10K, 1 day old, critical vendor (5)
Priority = (100 × 0.5) + (1 × 10) + (5 × 20) = 50 + 10 + 100 = 160

Invoice B: $500, 15 days old, normal vendor (3)
Priority = (5 × 0.5) + (15 × 10) + (3 × 20) = 2.5 + 150 + 60 = 212.5

Result: Invoice B shown first (older, SLA risk)
```

**Batch Actions**:
- **Approve All**: For low-amount, high-confidence exceptions
- **Reject All**: For spam/duplicate invoices
- **Bulk Edit**: Change GL code for all invoices from same vendor
- **Delegate**: Assign to team member

---

#### Feature: Inline Review
**Description**: Review and approve invoices without leaving the queue.

**UI Layout**:
```
┌─────────────────────────────────────────────────────────┐
│ Invoice #12345 | Acme Industrial | $1,234.56 | [APPROVE] │
├─────────────────────────────────────────────────────────┤
│ [PDF Preview]          │ Extracted Data                 │
│                        │ Vendor: Acme Industrial [edit] │
│ [Invoice Image]        │ Amount: $1,234.56     [edit]   │
│                        │ Date: 2026-08-01      [edit]   │
│                        │ PO#: PO-12345         [edit]   │
│                        │ GL Code: 6000-Supplies [edit]  │
│                        │                                │
│                        │ Matched To:                    │
│                        │ ✓ Bank Tx: $1,234.56 (08/03)   │
│                        │ ✓ PO-12345: $1,234.56          │
│                        │                                │
│                        │ [Reject] [Request Correction]  │
└─────────────────────────────────────────────────────────┘
```

**Keyboard Shortcuts**:
- `A`: Approve
- `R`: Reject
- `E`: Edit field
- `N`: Next invoice
- `P`: Previous invoice

---

### 10.5 QuickBooks Integration

#### Feature: Bi-Directional Sync
**Description**: Sync vendors, GL codes, POs from QBO; post bills to QBO.

**Sync Direction**:
| Data Type | Direction | Frequency |
|-----------|-----------|-----------|
| Vendors | QBO → InvoiceMatch | Daily |
| GL Codes | QBO → InvoiceMatch | Daily |
| POs | QBO → InvoiceMatch | Daily |
| Bills | InvoiceMatch → QBO | On approval |
| Payments | QBO → InvoiceMatch | Daily |

**Field Mapping**:
```
InvoiceMatch Field → QBO Field
-------------------|------------------
vendor.name        → Vendor.DisplayName
invoice.total      → Bill.TotalAmt
invoice.date       → Bill.TxnDate
invoice.due_date   → Bill.DueDate
line_items[].amount → Bill.Line.Amount
line_items[].gl_code → Bill.Line.AccountRef
```

**Error Handling**:
- **Vendor Not Found**: Create new vendor in QBO (auto)
- **GL Code Invalid**: Flag for user mapping (manual)
- **Duplicate Bill**: Skip (hash check on invoice #)
- **API Rate Limit**: Queue, retry after 60 sec

---

### 10.6 Vendor Database

#### Feature: Vendor Scoring
**Description**: Track vendor reliability for prioritization and fraud detection.

**Score Components**:
| Metric | Weight | Calculation |
|--------|--------|-------------|
| On-Time Delivery | 30% | % invoices within promised days |
| Invoice Accuracy | 25% | % invoices without corrections |
| Price Consistency | 20% | Variance from historical prices |
| Communication | 15% | Response time to correction requests |
| Compliance | 10% | % invoices with required fields (PO#, etc.) |

**Score Tiers**:
- **A (90-100)**: Preferred vendor, auto-approve higher tolerance
- **B (75-89)**: Normal vendor, standard matching
- **C (60-74)**: Review all invoices manually
- **D (<60)**: Flag for renegotiation or replacement

**Use Cases**:
- Auto-approve threshold: A vendors = 90%, B vendors = 95%, C vendors = 100% (manual)
- Fraud alert: Sudden score drop >20 points
- Negotiation leverage: "Your invoice accuracy is 72%, industry average is 95%"

---

### 10.7 Audit Trail

#### Feature: Immutable Action Log
**Description**: Append-only log of all system actions for compliance.

**Log Schema**:
```json
{
  "log_id": "log_20260806_143022_abc123",
  "timestamp": "2026-08-06T14:30:22Z",
  "user_id": "user_olivia_001",
  "action": "invoice.approve",
  "resource_type": "invoice",
  "resource_id": "inv_12345",
  "before": {"status": "pending_review", "confidence": 87},
  "after": {"status": "approved", "posted_to_qbo": true},
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0..."
}
```

**Retention Policy**:
- **Active**: 90 days (hot storage, fast query)
- **Archive**: 7 years (S3 Glacier, retrieval 3-5 hours)
- **Delete**: After 7 years + 1 month (automated)

**Compliance**:
- IRS: 7 years (audit requirement)
- SOC 2: Immutable logs (append-only)
- GDPR: User data deletion on request (anonymize logs)

---

## 11. User Flows

### Flow 1: Invoice Auto-Reconciliation (Happy Path)
```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│ Vendor  │────▶│  Email   │────▶│ Invoice   │────▶│ Matching │────▶│ QuickBooks│
│ Sends   │     │ Forward  │     │ Extraction│     │ Engine   │     │   Post   │
│ Invoice │     │          │     │           │     │          │     │          │
└─────────┘     └──────────┘     └───────────┘     └──────────┘     └──────────┘
     │                │                  │                 │                │
     │                │                  │                 │                │
  PDF attached   SES parses         OCR + LLM        3-way match      Create Bill
  to email       attachment         extraction       96% confidence   in QBO
```

### Flow 2: Exception Review (Manual Path)
```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│ Invoice │────▶│  Low     │────▶│ Exception │────▶│  User    │────▶│  Approve │
│ Extract │     │ Confidence│     │   Queue   │     │  Review  │     │  & Post  │
└─────────┘     └──────────┘     └───────────┘     └──────────┘     └──────────┘
     │                │                  │                 │                │
  65% match      <95% threshold    Sorted by         Inline edit      QBO Bill
  score                            priority          GL code, PO#     created
```

### Flow 3: Vendor Format Learning
```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│  User   │────▶│  System  │────▶│  Pattern  │────▶│  Rule    │────▶│  Future  │
│  Edits  │     │  Compares │     │ Detection │     │ Creation │     │  Auto    │
└─────────┘     └──────────┘     └───────────┘     └──────────┘     └──────────┘
     │                │                  │                 │                │
  3+ corrections  Extracted vs      "PO# always in    Store regex/    Apply rule to
  on same vendor  Corrected         bottom-right"     coordinates   next invoice
```

---

## 12. Screen Requirements

### Screen 1: Dashboard
**Purpose**: At-a-glance reconciliation status

**Components**:
- **Stats Cards**:
  - Invoices Received (today, week, month)
  - Auto-Matched (%)
  - Exceptions Pending
  - Total Value Pending
- **Chart**: Invoices per day (30-day trend)
- **Recent Activity**: Last 10 actions (user, action, timestamp)
- **Quick Actions**: Upload invoice, View exceptions, Sync QBO

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│ Dashboard                               [Upload] [Exceptions]│
├─────────────────────────────────────────────────────────────┤
│ [200]        [87%]         [12]          [$45,230]          │
│ Received     Auto-Matched  Pending       Pending Value      │
├─────────────────────────────────────────────────────────────┤
│ Invoices per Day (30-day trend)                             │
│ [███████████████████████████████████]                       │
├─────────────────────────────────────────────────────────────┤
│ Recent Activity                                             │
│ Olivia approved inv_12345 ($1,234) - 2 min ago              │
│ System auto-matched 50 invoices - 1 hour ago                │
│ Frank rejected inv_12340 (duplicate) - 3 hours ago          │
└─────────────────────────────────────────────────────────────┘
```

---

### Screen 2: Exception Queue
**Purpose**: Review and approve exceptions

**Components**:
- **Filters**: Vendor, date range, amount, confidence score
- **Sort**: Priority, amount, age, vendor
- **List View**: Invoice cards (vendor, amount, age, confidence)
- **Detail View**: PDF preview + extracted data + match info
- **Batch Actions**: Approve all, reject all, bulk edit

**Layout**: (See Inline Review mockup in Feature 10.4)

---

### Screen 3: Vendor Management
**Purpose**: Manage vendor database and format rules

**Components**:
- **Vendor List**: Name, invoice count, accuracy score, tier
- **Vendor Detail**: Profile, format rules, accuracy history
- **Rule Editor**: Coordinate, keyword, regex, table rules
- **Import/Export**: CSV vendor list, format rules

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│ Vendors                                   [Import] [Export] │
├─────────────────────────────────────────────────────────────┤
│ Acme Industrial      │ 245 invoices │ 98% accuracy │ Tier A │
│ Amazon Business      │ 189 invoices │ 99% accuracy │ Tier A │
│ Grainger             │ 156 invoices │ 95% accuracy │ Tier B │
│ Uline                │ 134 invoices │ 92% accuracy │ Tier B │
├─────────────────────────────────────────────────────────────┤
│ Acme Industrial - Format Rules                              │
│ ✓ PO#: Bottom-right corner (x:450, y:580, w:120, h:20)      │
│ ✓ Invoice #: Top-right, regex: \d{6,10}                     │
│ ✓ Line Items: Table starting at y:250, row height: 25       │
│ [Add Rule] [Edit] [Delete]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

### Screen 4: Settings
**Purpose**: Configure matching rules, integrations, team

**Tabs**:
- **Matching**: Tolerance, auto-approve threshold, priority weights
- **Integrations**: QuickBooks, Plaid, vendor portals
- **Team**: Users, roles, permissions
- **Audit**: Log retention, export settings
- **Billing**: Plan, usage, payment method

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│ Settings                                                    │
├─────────────────────────────────────────────────────────────┤
│ [Matching] [Integrations] [Team] [Audit] [Billing]          │
├─────────────────────────────────────────────────────────────┤
│ Matching Tolerance                                          │
│ Amount: $5 or 5% (whichever is greater) [edit]              │
│                                                               │
│ Auto-Approve Threshold                                      │
│ Tier A Vendors: 90% confidence [edit]                       │
│ Tier B Vendors: 95% confidence [edit]                       │
│ Tier C Vendors: 100% (manual review) [edit]                 │
│                                                               │
│ Priority Weights                                            │
│ Amount: 50% [slider]                                        │
│ Age: 30% [slider]                                           │
│ Vendor Importance: 20% [slider]                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. UX Requirements

### Design Principles
1. **Exception-First**: Show only what needs attention (reduce noise)
2. **Keyboard-Native**: Power users can review 100 invoices/hour without mouse
3. **Transparent Confidence**: Always show why system made a decision
4. **Progressive Disclosure**: Simple defaults, advanced options hidden
5. **Audit-Ready**: Every action logged, exportable, compliant

### Accessibility
- **WCAG 2.1 AA**: Color contrast, keyboard navigation, screen reader support
- **Keyboard Shortcuts**: All actions accessible without mouse
- **Focus States**: Clear focus indicators for all interactive elements
- **Alt Text**: All images (invoice previews) have descriptive alt text

### Performance
- **Page Load**: <2 seconds (dashboard, queue)
- **OCR Processing**: <30 seconds per invoice (95th percentile)
- **Matching**: <5 seconds per invoice (after OCR)
- **QBO Sync**: <10 seconds per bill (on approval)

---

## 14. Design System

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Primary Blue | `#0A66C2` | Buttons, links, active states |
| Success Green | `#22C55E` | Auto-approved, matched |
| Warning Yellow | `#F59E0B` | Pending review, medium confidence |
| Error Red | `#EF4444` | Rejected, low confidence, errors |
| Neutral Gray | `#6B7280` | Text, borders, disabled |
| Background | `#F9FAFB` | Page background |
| Surface | `#FFFFFF` | Cards, modals |

### Typography
| Style | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| Heading 1 | Inter | 24px | 700 | Page titles |
| Heading 2 | Inter | 20px | 600 | Section titles |
| Body | Inter | 14px | 400 | Body text |
| Mono | JetBrains Mono | 13px | 400 | Code, IDs, amounts |

### Spacing
- **Base Unit**: 4px
- **Card Padding**: 16px (4 units)
- **Section Spacing**: 24px (6 units)
- **Page Margins**: 32px (8 units)

### Components
- **Button**: 4 variants (primary, secondary, danger, ghost)
- **Card**: 3 elevations (flat, raised, modal)
- **Input**: 3 sizes (small, medium, large)
- **Badge**: 5 states (success, warning, error, info, neutral)

---

## 15. Information Architecture

### Site Map
```
InvoiceMatch AI
├── Dashboard
├── Invoices
│   ├── All Invoices
│   ├── Exceptions
│   └── Upload
├── Vendors
│   ├── Vendor List
│   └── Vendor Detail
├── Matching
│   ├── Bank Transactions
│   ├── Purchase Orders
│   └── Matching Rules
├── Reports
│   ├── Reconciliation Summary
│   ├── Vendor Performance
│   └── Audit Export
├── Settings
│   ├── Matching
│   ├── Integrations
│   ├── Team
│   ├── Audit
│   └── Billing
└── Help
    ├── Documentation
    ├── API Reference
    └── Support
```

### Navigation
- **Top Bar**: Logo, search, notifications, user menu
- **Sidebar**: Primary navigation (Dashboard, Invoices, Vendors, etc.)
- **Breadcrumbs**: Secondary navigation (Invoices > Exceptions > inv_12345)

---

## 16. Data Requirements

### Entities
| Entity | Fields | Relationships |
|--------|--------|---------------|
| Invoice | id, vendor_id, amount, date, due_date, status, confidence_score | belongs_to Vendor, has_many LineItems |
| Vendor | id, name, email, tier, accuracy_score, format_rules | has_many Invoices |
| LineItem | id, invoice_id, description, quantity, unit_price, amount, gl_code | belongs_to Invoice |
| BankTransaction | id, date, amount, payee, description, matched_invoice_id | belongs_to Invoice |
| PurchaseOrder | id, po_number, vendor_id, total, status, lines | belongs_to Vendor, has_many LineItems |
| User | id, email, role, company_id | belongs_to Company |
| AuditLog | id, user_id, action, resource_type, resource_id, before, after, timestamp | belongs_to User |

### Data Volume (Year 1)
| Entity | Monthly Growth | Year 1 Total |
|--------|----------------|--------------|
| Invoices | 10,000 (500 customers × 20 invoices) | 120,000 |
| Vendors | 500 (500 customers × 1 vendor) | 6,000 |
| LineItems | 50,000 (5 lines/invoice) | 600,000 |
| BankTransactions | 10,000 (1:1 with invoices) | 120,000 |
| AuditLogs | 100,000 (10 actions/invoice) | 1,200,000 |

### Storage Estimates
- **PostgreSQL**: 50 GB (structured data)
- **S3 (PDFs)**: 500 GB (120K invoices × 500KB avg)
- **Audit Logs (Glacier)**: 10 GB (compressed)

---

## 17. Database Design

### Schema (PostgreSQL)
```sql
-- Companies
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  subdomain VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(50) DEFAULT 'user', -- admin, user, viewer
  created_at TIMESTAMP DEFAULT NOW()
);

-- Vendors
CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  tier VARCHAR(10) DEFAULT 'B', -- A, B, C, D
  accuracy_score DECIMAL(5,2) DEFAULT 0.0,
  format_rules JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Invoices
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  vendor_id UUID REFERENCES vendors(id),
  invoice_number VARCHAR(100),
  amount DECIMAL(12,2) NOT NULL,
  date DATE NOT NULL,
  due_date DATE,
  status VARCHAR(50) DEFAULT 'pending', -- pending, matched, approved, rejected, posted
  confidence_score DECIMAL(5,2),
  pdf_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Line Items
CREATE TABLE line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID REFERENCES invoices(id),
  description TEXT,
  quantity DECIMAL(10,2),
  unit_price DECIMAL(12,2),
  amount DECIMAL(12,2),
  gl_code VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Bank Transactions
CREATE TABLE bank_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  date DATE NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  payee VARCHAR(255),
  description TEXT,
  matched_invoice_id UUID REFERENCES invoices(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Audit Logs
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID REFERENCES companies(id),
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),
  resource_id UUID,
  before JSONB,
  after JSONB,
  ip_address INET,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_vendor ON invoices(vendor_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_bank_transactions_date ON bank_transactions(date);
```

---

## 18. API Requirements

### Internal API (FastAPI)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/invoices` | GET | List invoices (paginated) |
| `/api/v1/invoices` | POST | Upload invoice |
| `/api/v1/invoices/{id}` | GET | Get invoice detail |
| `/api/v1/invoices/{id}/approve` | POST | Approve invoice |
| `/api/v1/invoices/{id}/reject` | POST | Reject invoice |
| `/api/v1/vendors` | GET | List vendors |
| `/api/v1/vendors/{id}` | GET | Get vendor detail |
| `/api/v1/matching/suggest` | POST | Get match suggestions |
| `/api/v1/integrations/quickbooks/sync` | POST | Sync QBO data |
| `/api/v1/audit-logs` | GET | Export audit logs |

### External APIs (Integrations)
| API | Purpose | Rate Limit |
|-----|---------|------------|
| QuickBooks Online | Post bills, sync vendors | 500 req/min |
| Plaid | Sync bank transactions | 100 req/min |
| AWS Textract | OCR processing | 1000 pages/min |
| Anthropic Claude | LLM extraction | 50 req/min |

---

## 19. AI Requirements

### OCR Model
- **Provider**: AWS Textract (primary), Google Vision (fallback)
- **Accuracy Target**: 99%+ on printed text
- **Latency**: <10 seconds per page
- **Cost**: <$0.0015 per page

### LLM Extraction Model
- **Provider**: Anthropic Claude 3.5 Sonnet
- **Prompt**: Structured extraction template (see below)
- **Output**: JSON with confidence scores per field
- **Cost**: ~$0.01 per invoice

**Extraction Prompt Template**:
```
You are an invoice data extraction specialist. Extract the following fields from the OCR text:
- vendor_name
- invoice_number
- invoice_date
- due_date
- total_amount
- tax_amount
- line_items: [{description, quantity, unit_price, amount}]

Return JSON with confidence score (0-100) for each field.

OCR TEXT:
{ocr_output}

JSON OUTPUT:
```

### Matching Algorithm
- **Type**: Rule-based + ML ranking
- **Features**: Amount, vendor, date, PO#, line items
- **Model**: Logistic regression (confidence score)
- **Training**: User corrections (feedback loop)

### Vendor Format Learning
- **Algorithm**: Pattern detection from corrections
- **Trigger**: 3+ manual corrections on same vendor
- **Output**: Extraction rules (coordinate, regex, keyword)
- **Validation**: 80%+ accuracy on next 5 invoices

---

## 20. Security

### Authentication
- **Method**: Email + password (bcrypt)
- **MFA**: TOTP (Google Authenticator)
- **Session**: JWT (7-day expiry)
- **Password Reset**: Email link (1-hour expiry)

### Authorization
- **RBAC**: Admin, User, Viewer roles
- **Company Isolation**: Row-level security (RLS)
- **API Keys**: Scoped to company, revocable

### Data Protection
- **Encryption at Rest**: AES-256-GCM (PostgreSQL TDE)
- **Encryption in Transit**: TLS 1.3
- **Secrets Management**: AWS Secrets Manager
- **Credential Encryption**: AES-256-GCM (vendor portal logins)

### Compliance
- **SOC 2 Type II**: Audit logs, access controls, encryption
- **GDPR**: Data deletion, export, consent management
- **IRS**: 7-year audit log retention
- **PCI-DSS**: Not applicable (no credit card storage)

---

## 21. Privacy

### Data Collection
- **Personal Data**: Email, name, role (user accounts)
- **Business Data**: Invoices, vendors, bank transactions
- **Usage Data**: Action logs, feature usage

### Data Usage
- **Primary**: Provide reconciliation service
- **Secondary**: Improve OCR/LLM accuracy (anonymized)
- **Not Sold**: Never sell customer data to third parties

### Data Retention
- **Active Data**: 90 days (hot storage)
- **Archive**: 7 years (compliance)
- **Deletion**: On request (GDPR) or after 7 years

### User Rights (GDPR)
- **Access**: Export all data (JSON, CSV)
- **Rectification**: Edit or correct data
- **Erasure**: Delete account + data (anonymize audit logs)
- **Portability**: Export in standard format (QBO CSV)

---

## 22. Performance

### SLAs
| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.9% | Monthly (excludes planned maintenance) |
| Page Load | <2s | 95th percentile (dashboard, queue) |
| OCR Latency | <30s | 95th percentile (per invoice) |
| API Latency | <500ms | 95th percentile (all endpoints) |
| QBO Sync | <10s | 95th percentile (per bill) |

### Scalability
- **Horizontal**: Auto-scale OCR workers (Kubernetes HPA)
- **Database**: Read replicas (PostgreSQL)
- **Cache**: Redis (session, OCR results)
- **CDN**: CloudFront (static assets, PDF previews)

### Load Testing
- **Target**: 10,000 invoices/hour (500 customers × 20 invoices)
- **Peak**: 50,000 invoices/hour (month-end surge)
- **Stress Test**: 100,000 invoices/hour (2x peak)

---

## 23. Reliability

### Redundancy
- **Multi-AZ**: PostgreSQL (primary + standby)
- **Multi-Region**: S3 (us-east-1 + us-west-2 replication)
- **Backup**: Daily snapshots (30-day retention)

### Disaster Recovery
- **RTO**: 4 hours (restore from backup)
- **RPO**: 1 hour (backup frequency)
- **Failover**: Automatic (PostgreSQL standby)

### Monitoring
- **Uptime**: Pingdom (5-min checks)
- **Errors**: Sentry (error tracking)
- **Performance**: Datadog (APM, logs, metrics)
- **Alerts**: PagerDuty (critical alerts)

---

## 24. Observability

### Logging
- **Format**: JSON (structured)
- **Level**: INFO (prod), DEBUG (staging)
- **Aggregation**: CloudWatch Logs → Elasticsearch
- **Retention**: 30 days (hot), 7 years (audit)

### Metrics
- **Business**: Invoices processed, auto-match rate, exceptions
- **Technical**: API latency, error rate, OCR queue depth
- **Cost**: OCR spend, LLM spend, AWS infrastructure

### Tracing
- **Provider**: AWS X-Ray
- **Coverage**: All API endpoints, OCR pipeline, QBO sync
- **Sampling**: 10% (prod), 100% (staging)

---

## 25. Integration

### QuickBooks Online
- **Auth**: OAuth 2.0
- **Endpoints**: Bills, Vendors, Accounts, PurchaseOrders
- **Webhooks**: Not supported (poll every 5 min)
- **Rate Limit**: 500 requests/minute

### Plaid (Bank Sync)
- **Auth**: OAuth 2.0 (Link flow)
- **Endpoints**: Transactions, Accounts, Balance
- **Webhooks**: Supported (new transactions)
- **Rate Limit**: 100 requests/minute

### Vendor Portals
- **Method**: Puppeteer (headless browser)
- **Credentials**: Encrypted (AES-256-GCM)
- **Frequency**: Daily (per vendor)
- **Error Handling**: CAPTCHA alert to user

---

## 26. Reporting

### Standard Reports
| Report | Frequency | Format | Recipients |
|--------|-----------|--------|------------|
| Reconciliation Summary | Weekly | PDF, CSV | CFO, Ops Manager |
| Vendor Performance | Monthly | PDF, CSV | Procurement |
| Exception Analysis | Weekly | PDF | Ops Manager |
| Audit Export | On-demand | CSV | Auditor |

### Custom Reports
- **Builder**: Drag-and-drop (fields, filters, groupings)
- **Schedule**: Email report (daily, weekly, monthly)
- **Export**: CSV, PDF, Excel

### Dashboards
- **Executive**: High-level metrics (invoices, savings, accuracy)
- **Ops**: Exception queue, SLA compliance
- **Finance**: GL coding accuracy, month-end close time

---

## 27. Analytics

### Product Analytics
- **Provider**: PostHog (self-hosted)
- **Events**: Upload, approve, reject, edit, sync
- **Funnels**: Setup flow, exception review, QBO sync
- **Retention**: DAU/MAU, feature adoption

### Business Analytics
- **Provider**: Metabase (self-hosted)
- **Metrics**: MRR, churn, LTV, CAC
- **Cohorts**: By plan, by industry, by signup date

### A/B Testing
- **Provider**: PostHog Experiments
- **Tests**: Pricing page, onboarding flow, exception UI
- **Significance**: 95% confidence, 80% power

---

## 28. Testing

### Unit Tests
- **Coverage**: 80%+ (backend), 70%+ (frontend)
- **Framework**: pytest (backend), Jest (frontend)
- **CI**: GitHub Actions (on every PR)

### Integration Tests
- **Coverage**: All API endpoints, QBO sync, OCR pipeline
- **Environment**: Staging (isolated QBO sandbox)
- **Frequency**: Nightly (automated)

### E2E Tests
- **Coverage**: Critical user flows (upload → approve → post)
- **Tool**: Playwright (headless browser)
- **Frequency**: Nightly (automated)

### Performance Tests
- **Tool**: k6 (load testing)
- **Scenarios**: 10K invoices/hour, 50K invoices/hour
- **Frequency**: Before each release

---

## 29. Deployment

### Environment
- **Cloud**: AWS (us-east-1 primary)
- **Compute**: ECS Fargate (containers)
- **Database**: RDS PostgreSQL (multi-AZ)
- **Storage**: S3 (PDFs, audit logs)

### CI/CD
- **CI**: GitHub Actions (test, lint, build)
- **CD**: AWS CodeDeploy (blue-green)
- **Rollback**: Automatic (error rate >5%)

### Environments
| Environment | Purpose | Data |
|-------------|---------|------|
| Development | Local dev | Mock data |
| Staging | QA, UAT | Anonymized prod data |
| Production | Live customers | Real data |

---

## 30. Migration

### Data Migration (from QuickBooks)
- **Historical Invoices**: CSV import (last 2 years)
- **Vendors**: Sync from QBO (all active)
- **POs**: Sync from QBO (open POs only)
- **Bank Transactions**: Plaid sync (last 90 days)

### Cutover Plan
1. **Week 1**: Parallel run (manual + InvoiceMatch)
2. **Week 2**: 50% invoices through InvoiceMatch
3. **Week 3**: 100% invoices through InvoiceMatch
4. **Week 4**: Disable manual process

### Rollback Plan
- **Trigger**: Critical bug (data loss, security)
- **Action**: Revert to manual process
- **Timeline**: <1 hour (feature flag)

---

## 31. Release Plan

### MVP (Month 1-2)
- Invoice upload (PDF, email)
- OCR + extraction (AWS Textract + Claude)
- 2-way matching (invoice ↔ bank transaction)
- Exception queue (review UI)
- QuickBooks integration (post bills)
- **Target**: 10 beta customers

### V1 (Month 3-4)
- 3-way matching (invoice ↔ bank ↔ PO)
- Vendor format learning
- Vendor portal scraping (top 10)
- Audit trail (immutable logs)
- **Target**: 100 paying customers

### V2 (Month 5-8)
- Xero integration
- Multi-entity support
- Advanced reporting
- Mobile app (iOS, Android)
- **Target**: 500 customers

### V3 (Month 9-12)
- International (multi-currency, VAT)
- AP automation (payment execution)
- Fraud detection (anomaly detection)
- Custom ERP integrations (NetSuite, SAP)
- **Target**: $150K MRR

---

## 32. Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OCR accuracy <99% | Medium | High | Multi-model fallback, manual correction loop |
| QBO API rate limits | Low | Medium | Queue + retry, batch processing |
| Vendor portal CAPTCHA | High | Low | Alert user for manual resolution |
| LLM extraction errors | Medium | Medium | Confidence scores, human review |

### Business Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low WTP ($200-500/mo) | Medium | High | Validate with 10 customer interviews |
| QuickBooks builds competitor | Low | High | Differentiate on format agnosticism |
| Slow customer acquisition | Medium | Medium | Partner with bookkeepers (channel) |
| High churn (>5%/mo) | Medium | High | Exception-first UX, high accuracy |

### Compliance Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| GDPR violation | Low | High | Data deletion, export, consent |
| IRS audit (7-year logs) | Low | Medium | Glacier retention, automated deletion |
| SOC 2 failure | Medium | Medium | Security controls, audit logs |

---

## 33. Assumptions

### Technical Assumptions
1. AWS Textract accuracy >99% on printed invoices
2. Claude 3.5 can extract structured data from OCR text
3. QuickBooks API supports all required operations
4. Plaid supports 95%+ of SMB bank accounts

### Business Assumptions
1. SMBs will pay $200-500/mo for 80% automation
2. 500 customers achievable in 12 months
3. Bookkeepers are effective channel partners
4. 80% auto-match rate achievable with current tech

### Market Assumptions
1. QuickBooks won't build competing feature in 12 months
2. Bill.com won't lower price for SMB segment
3. AI accuracy will continue improving (tailwind)
4. Remote work trend increases automation demand

---

## 34. Constraints

### Technical Constraints
- **Budget**: $10K/mo AWS spend (Month 1-6)
- **Team**: 3 engineers (1 backend, 1 frontend, 1 ML)
- **Timeline**: MVP in 8 weeks
- **Compliance**: SOC 2 Type II (Month 6)

### Business Constraints
- **Pricing**: Must be <1/10th of VA cost ($320/mo max)
- **Setup**: <1 hour for 50+ vendors
- **Accuracy**: 99.5%+ (or customers churn)
- **Support**: <4 hour response time (SMB expectation)

### Regulatory Constraints
- **IRS**: 7-year audit log retention
- **GDPR**: Data deletion on request
- **SOC 2**: Access controls, encryption, monitoring
- **PCI-DSS**: Not applicable (no CC storage)

---

## 35. Success Metrics

### Product Metrics
| Metric | Target | Baseline | Measurement |
|--------|--------|----------|-------------|
| Auto-Match Rate | 80% | 0% (manual) | % invoices matched without review |
| Accuracy | 99.5% | 95% (manual) | % correct matches |
| Exception Rate | <2% | 100% (manual) | % invoices needing review |
| Setup Time | <1 hour | N/A | Time to first match |

### Business Metrics
| Metric | Target | Baseline | Measurement |
|--------|--------|----------|-------------|
| MRR | $150K | $0 | Monthly recurring revenue |
| Customers | 500 | 0 | Active subscriptions |
| Churn | <5%/mo | N/A | Monthly logo churn |
| NPS | 50+ | N/A | Quarterly survey |
| LTV:CAC | 3:1 | N/A | Lifetime value / acquisition cost |

### User Metrics
| Metric | Target | Baseline | Measurement |
|--------|--------|----------|-------------|
| Time Saved | 12 hrs/week | 15 hrs/week (manual) | User self-report |
| DAU/MAU | 60% | N/A | PostHog analytics |
| Feature Adoption | 80% | N/A | % using core features |
| Support Tickets | <5/customer/mo | N/A | Intercom |

---

## 36. KPIs Dashboard

### Executive Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│ InvoiceMatch AI - Executive Dashboard                       │
├─────────────────────────────────────────────────────────────┤
│ MRR: $150,000          Customers: 500        Churn: 3.2%    │
│ [████████████████████]  [████████████████]   [████████]     │
├─────────────────────────────────────────────────────────────┤
│ Auto-Match Rate: 82%   Accuracy: 99.6%       NPS: 54        │
│ [████████████████████]  [██████████████████]  [████████████]│
├─────────────────────────────────────────────────────────────┤
│ Time Saved: 12 hrs/wk  Setup Time: 45 min    Support: 3/mo │
│ [████████████████████]  [████████████████]   [██████]       │
└─────────────────────────────────────────────────────────────┘
```

### Ops Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│ InvoiceMatch AI - Operations Dashboard                      │
├─────────────────────────────────────────────────────────────┤
│ Invoices Today: 450   Exceptions: 12        SLA: 98%        │
│ [████████████████████]  [████]              [████████████]  │
├─────────────────────────────────────────────────────────────┤
│ OCR Queue: 23         Avg Latency: 18s      Error Rate: 0.3%│
│ [████████]            [████████████████]    [██]            │
├─────────────────────────────────────────────────────────────┤
│ QBO Sync: 99.8%       Vendor Coverage: 87   Portal Errors: 2│
│ [██████████████████]  [████████████████]    [█]             │
└─────────────────────────────────────────────────────────────┘
```

---

## 37. Open Questions

### Technical
1. Should we support multi-currency in MVP or post-MVP?
2. Is Puppeteer scraping sustainable long-term (vs API partnerships)?
3. Should OCR run on-demand or batch (cost vs latency)?
4. What's the fallback if Claude API is unavailable?

### Business
1. Should we charge per invoice or per user?
2. Should we offer free tier (100 invoices/mo)?
3. Should we target bookkeepers (channel) or SMBs (direct)?
4. What's the minimum contract term (monthly, annual)?

### Product
1. Should exception queue support batch approve (risk vs speed)?
2. Should we show confidence scores to users (transparency vs trust)?
3. Should we auto-create vendors in QBO or require manual mapping?
4. Should we support PDF forms (fillable) or flat PDFs only?

---

## 38. Appendices

### Appendix A: Pain Signal Evidence
- **Source**: Reddit r/smallbusiness (pattern)
- **Quote**: "We spend 15 hours/week manually reconciling invoices from 50+ vendors"
- **Existing Spend**: $3,200/mo (VA at $20/hr)
- **WTP**: $200-500/mo
- **Automatable**: 80%
- **Bad Incumbent**: QuickBooks (custom format gap)

### Appendix B: Competitor Analysis
| Competitor | Price | Auto-Match | Custom Formats | 3-Way Match |
|------------|-------|------------|----------------|-------------|
| QuickBooks | $80/mo | 60% | ❌ | ❌ |
| Bill.com | $399/mo | 85% | ✅ | ✅ |
| Melio | Free | 0% | ❌ | ❌ |
| AvidXchange | Enterprise | 90% | ✅ | ✅ |
| **InvoiceMatch AI** | **$200-500/mo** | **80%** | **✅** | **✅** |

### Appendix C: Vendor Format Examples
- **Amazon Business**: PDF, structured table, PO# in subject line
- **Grainger**: PDF, fixed template, PO# in top-right
- **Uline**: PDF, variable layout, PO# in bottom-left
- **Home Depot**: Email body + PDF attachment, PO# in email subject
- **FedEx**: CSV export from portal, tracking # as invoice #

---

## 39. AI/Agent Architecture

### Agent Topology
```
┌─────────────────────────────────────────────────────────────┐
│                    InvoiceMatch AI Agents                   │
├─────────────────────────────────────────────────────────────┤
│  INGESTION AGENTS                                           │
│  • Email Parser Agent    • Portal Scraper Agent             │
│  • Upload Handler Agent  • Deduplication Agent              │
├─────────────────────────────────────────────────────────────┤
│  EXTRACTION AGENTS                                          │
│  • OCR Orchestrator      • LLM Extraction Agent             │
│  • Format Learner Agent  • Confidence Scorer Agent          │
├─────────────────────────────────────────────────────────────┤
│  MATCHING AGENTS                                            │
│  • Bank Match Agent      • PO Match Agent                   │
│  • 3-Way Match Agent     • Split Match Agent                │
├─────────────────────────────────────────────────────────────┤
│  REVIEW AGENTS                                              │
│  • Exception Prioritizer • Inline Review Agent              │
│  • Batch Approver Agent  • Vendor Scorer Agent              │
├─────────────────────────────────────────────────────────────┤
│  INTEGRATION AGENTS                                         │
│  • QBO Sync Agent        • Plaid Sync Agent                 │
│  • Audit Logger Agent    • Report Generator Agent           │
└─────────────────────────────────────────────────────────────┘
```

### Agent Workflows

#### OCR Orchestrator Agent
```
Input: Invoice PDF
Steps:
1. Check cache (hash match) → Return cached result if exists
2. Run AWS Textract → Get confidence score
3. If confidence <90%: Run Google Vision
4. If confidence <90%: Run Azure Form Recognizer
5. Return best result + confidence score
Output: OCR text + confidence
```

#### LLM Extraction Agent
```
Input: OCR text
Steps:
1. Format prompt with OCR text
2. Call Claude 3.5 Sonnet (JSON output)
3. Validate JSON schema (Pydantic)
4. Add confidence scores per field
5. Return structured data
Output: {vendor, invoice#, date, total, line_items[], confidence{}}
```

#### 3-Way Match Agent
```
Input: Extracted invoice data
Steps:
1. Find bank transactions (±3 days, ±5% amount)
2. Find POs (PO# match or vendor + amount match)
3. Calculate confidence score (weighted fields)
4. If confidence >95%: Auto-approve
5. If confidence 80-95%: Flag for review (low priority)
6. If confidence <80%: Flag for review (high priority)
Output: Match result + confidence + suggested action
```

### Agent Communication
- **Message Queue**: AWS SQS (async processing)
- **Event Bus**: AWS EventBridge (state changes)
- **State Store**: PostgreSQL (invoice status)
- **Cache**: Redis (OCR results, vendor rules)

---

**PRD Complete** ✅

**Next Steps**:
1. Review with stakeholders (Ops Olivia, Finance Frank, Bookkeeper Beth)
2. Validate assumptions (10 customer interviews)
3. Prioritize MVP features (MoSCoW method)
4. Create technical architecture doc
5. Start Phase 0: Scaffold project
