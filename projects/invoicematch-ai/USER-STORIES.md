# InvoiceMatch AI — User Stories

**Product**: InvoiceMatch AI  
**Generated From**: pain_001 (Invoice/Receipt Reconciliation)  
**Opportunity Score**: 82/100  
**Total Stories**: 42  
**Version**: 1.0 (MVP Scope)  
**Generated**: 2026-08-06

---

## Story Index by Capability

| Capability | Stories | P0 | P1 | P2 |
|------------|---------|----|----|----|
| 1. Invoice Ingestion | 8 | 5 | 2 | 1 |
| 2. OCR + Extraction | 7 | 5 | 2 | 0 |
| 3. Matching Engine | 7 | 5 | 2 | 0 |
| 4. Exception Queue | 6 | 4 | 2 | 0 |
| 5. QuickBooks Integration | 6 | 5 | 1 | 0 |
| 6. Vendor Database | 5 | 3 | 2 | 0 |
| 7. Audit Trail | 3 | 3 | 0 | 0 |
| **Total** | **42** | **30** | **10** | **2** |

---

## Capability 1: Invoice Ingestion

### Story 1.1.1: Email Forwarding Setup

**Feature**: FR-001 (Email Forwarding)  
**Priority**: P0  
**Story ID**: US-001

**As a** ops manager  
**I want** to get a unique email address for invoice forwarding  
**So that** I can forward invoices from any email client

**Acceptance Criteria**:
```gherkin
Scenario: User signs up and gets invoice email
  Given I am a new user at acme-company.com
  When I complete signup
  Then I receive a unique email: invoices@acme-company.invoicematch.ai
  And the email is displayed in my dashboard
  And I can copy it to clipboard with one click

Scenario: User forwards invoice via email
  Given I have an invoice PDF from Acme Industrial
  When I forward the email to invoices@acme-company.invoicematch.ai
  Then the system receives the email within 1 minute
  And extracts the PDF attachment
  And sends me a confirmation: "Received invoice from Acme Industrial"

Scenario: Email with unsupported attachment
  Given I forward an email with .xlsx attachment
  When the system processes the email
  Then it rejects the attachment
  And sends me an error email: "Unsupported format: .xlsx. Please forward PDF only."
```

**Definition of Done**:
- [ ] Email parsing implemented (AWS SES)
- [ ] Unique email generation per company
- [ ] Confirmation email template created
- [ ] Error handling for unsupported formats
- [ ] Tests passing (unit + integration)
- [ ] Documentation updated

**Estimate**: 3 story points  
**Dependencies**: AWS SES setup, S3 bucket configuration

---

### Story 1.1.2: Email Subject Parsing

**Feature**: FR-001 (Email Forwarding)  
**Priority**: P0  
**Story ID**: US-002

**As a** system  
**I want** to extract PO# from email subject lines  
**So that** I can auto-link invoices to purchase orders

**Acceptance Criteria**:
```gherkin
Scenario: Subject contains PO#
  Given an email with subject "Invoice from Acme - PO: 12345"
  When the system parses the subject
  Then it extracts PO# = "12345"
  And links the invoice to PO-12345 in QuickBooks

Scenario: Subject contains PO# in different formats
  Given an email with subject "PO#98765 - Invoice Attached"
  When the system parses the subject
  Then it extracts PO# = "98765"
  And links the invoice to PO-98765

Scenario: Subject has no PO#
  Given an email with subject "Monthly Invoice"
  When the system parses the subject
  Then PO# = null
  And the invoice is flagged for manual PO matching
```

**Definition of Done**:
- [ ] Regex pattern implemented (`PO[:\s]*([0-9A-Z-]+)`)
- [ ] Multiple format support tested
- [ ] PO linking logic implemented
- [ ] Tests passing
- [ ] Edge cases documented

**Estimate**: 2 story points  
**Dependencies**: US-001 (Email Forwarding Setup)

---

### Story 1.1.3: Sender Whitelist

**Feature**: FR-001 (Email Forwarding)  
**Priority**: P1  
**Story ID**: US-003

**As a** finance manager  
**I want** to whitelist allowed sender domains  
**So that** only legitimate vendor invoices are processed

**Acceptance Criteria**:
```gherkin
Scenario: User configures allowed domains
  Given I am a finance manager
  When I go to Settings > Email Integration
  Then I can add domains: acme.com, grainger.com, uline.com
  And I can remove domains
  And changes are saved immediately

Scenario: Email from allowed domain
  Given an email from billing@acme.com
  And acme.com is in the whitelist
  When the system processes the email
  Then it accepts the email
  And processes the invoice normally

Scenario: Email from unknown domain
  Given an email from unknown@random.com
  And random.com is NOT in the whitelist
  When the system processes the email
  Then it flags the invoice for review
  And notifies me: "Invoice from unknown domain: random.com"
```

**Definition of Done**:
- [ ] Domain whitelist UI implemented
- [ ] Validation on email processing
- [ ] Notification system integrated
- [ ] Tests passing
- [ ] User guide updated

**Estimate**: 3 story points  
**Dependencies**: US-001 (Email Forwarding Setup)

---

### Story 1.2.1: Drag-and-Drop Upload

**Feature**: FR-002 (PDF Upload)  
**Priority**: P0  
**Story ID**: US-004

**As a** ops manager  
**I want** to drag-and-drop multiple PDF invoices  
**So that** I can quickly upload batches from my computer

**Acceptance Criteria**:
```gherkin
Scenario: User uploads single PDF
  Given I am on the Upload page
  When I drag a PDF file onto the upload zone
  Then the file is highlighted (visual feedback)
  And I can drop it
  And the upload starts immediately
  And I see a progress bar

Scenario: User uploads multiple PDFs
  Given I select 50 PDF files
  When I drag them onto the upload zone
  Then all 50 files are uploaded
  And I see a batch progress: "25/50 completed"
  And I can cancel the upload

Scenario: User uploads unsupported file type
  Given I try to upload an .xlsx file
  When I drop it onto the upload zone
  Then the system rejects it
  And shows an error: "PDF files only. You uploaded: invoice.xlsx"
```

**Definition of Done**:
- [ ] React Dropzone component integrated
- [ ] Multi-file upload supported (max 50)
- [ ] Progress bar implemented
- [ ] File type validation (client-side)
- [ ] Cancel functionality working
- [ ] Tests passing (unit + E2E)

**Estimate**: 5 story points  
**Dependencies**: S3 presigned URL setup, backend API

---

### Story 1.2.2: Upload Progress Tracking

**Feature**: FR-002 (PDF Upload)  
**Priority**: P0  
**Story ID**: US-005

**As a** user  
**I want** to see real-time upload progress  
**So that** I know when my invoices are ready for processing

**Acceptance Criteria**:
```gherkin
Scenario: Upload progress updates in real-time
  Given I upload 10 PDF files
  When the upload is in progress
  Then I see: "3/10 files uploaded (30%)"
  And the progress bar updates every second
  And completed files show a green checkmark

Scenario: Upload completes
  Given all 10 files are uploaded
  When the upload finishes
  Then I see: "All files uploaded successfully"
  And I'm redirected to the Processing page
  And I receive an email: "10 invoices uploaded, processing started"

Scenario: Upload fails midway
  Given I upload 10 files
  When file 7 fails (network error)
  Then I see: "7/10 uploaded, 1 failed"
  And I can retry the failed file
  And successful files continue processing
```

**Definition of Done**:
- [ ] WebSocket connection for real-time updates
- [ ] Progress bar component implemented
- [ ] Per-file status tracking
- [ ] Retry mechanism for failed uploads
- [ ] Email notification on completion
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-004 (Drag-and-Drop Upload), WebSocket setup

---

### Story 1.2.3: Invoice Preview

**Feature**: FR-002 (PDF Upload)  
**Priority**: P1  
**Story ID**: US-006

**As a** user  
**I want** to preview uploaded invoices before processing  
**So that** I can verify I uploaded the correct files

**Acceptance Criteria**:
```gherkin
Scenario: User previews uploaded invoice
  Given I uploaded an invoice PDF
  When I click on the invoice in the upload list
  Then a preview modal opens
  And shows the first page of the PDF
  And I can zoom in/out
  And I can navigate to next/previous page

Scenario: User identifies wrong invoice
  Given I preview an invoice
  And I realize it's the wrong file
  When I click "Remove"
  Then the invoice is removed from the queue
  And I can upload a replacement
```

**Definition of Done**:
- [ ] PDF.js renderer integrated
- [ ] Preview modal implemented
- [ ] Zoom controls working
- [ ] Page navigation working
- [ ] Remove functionality implemented
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-004 (Drag-and-Drop Upload)

---

### Story 1.3.1: Vendor Portal Credentials

**Feature**: FR-003 (Vendor Portal Scraping)  
**Priority**: P1  
**Story ID**: US-007

**As a** ops manager  
**I want** to store vendor portal credentials securely  
**So that** the system can auto-fetch invoices

**Acceptance Criteria**:
```gherkin
Scenario: User adds vendor credentials
  Given I am on the Vendors page
  When I click "Add Credentials" for Amazon Business
  Then a modal opens
  And I can enter username and password
  And the credentials are encrypted (AES-256-GCM)
  And saved securely

Scenario: User updates credentials
  Given I have stored credentials for Grainger
  When the password expires
  And I update it in the system
  Then the new credentials are encrypted
  And the old credentials are deleted

Scenario: User views credential status
  Given I have credentials for 5 vendors
  When I go to Settings > Vendor Portals
  Then I see a list of vendors with credentials
  And their status: Active, Failed, CAPTCHA Required
```

**Definition of Done**:
- [ ] Credential storage UI implemented
- [ ] AES-256-GCM encryption implemented
- [ ] AWS KMS integration for key management
- [ ] Credential status dashboard
- [ ] Tests passing (security audit)

**Estimate**: 5 story points  
**Dependencies**: AWS KMS setup, encryption library

---

### Story 1.3.2: Daily Invoice Fetch

**Feature**: FR-003 (Vendor Portal Scraping)  
**Priority**: P2  
**Story ID**: US-008

**As a** system  
**I want** to fetch invoices from vendor portals daily  
**So that** users have all invoices without manual download

**Acceptance Criteria**:
```gherkin
Scenario: Daily fetch runs successfully
  Given it is 2:00 AM UTC
  When the scheduled job runs
  Then it logs into each vendor portal
  And downloads invoices since last fetch
  And stores them in S3
  And triggers OCR processing

Scenario: Fetch encounters CAPTCHA
  Given the system tries to login to Home Depot
  When a CAPTCHA is displayed
  Then the system pauses
  And alerts the user: "CAPTCHA required for Home Depot"
  And the user can resolve it manually

Scenario: Fetch fails (login error)
  Given the system tries to login to Grainger
  When the credentials are invalid
  Then it retries 3 times
  And alerts the user: "Login failed for Grainger"
  And marks the vendor as "Failed"
```

**Definition of Done**:
- [ ] Puppeteer scraping implemented (10 vendors)
- [ ] Scheduled job configured (cron: 0 2 * * *)
- [ ] CAPTCHA handling implemented
- [ ] Retry logic (3 attempts)
- [ ] User alerts (email/Slack)
- [ ] Tests passing

**Estimate**: 8 story points  
**Dependencies**: US-007 (Vendor Portal Credentials), Puppeteer setup

---

## Capability 2: OCR + Extraction

### Story 2.1.1: AWS Textract Integration

**Feature**: FR-004 (Multi-Model OCR)  
**Priority**: P0  
**Story ID**: US-009

**As a** system  
**I want** to use AWS Textract as the primary OCR engine  
**So that** I get 99%+ accuracy on printed invoices

**Acceptance Criteria**:
```gherkin
Scenario: System processes invoice with Textract
  Given a PDF invoice is uploaded
  When the system sends it to AWS Textract
  Then it receives OCR text within 10 seconds
  And the confidence score is >99%
  And the text is stored in cache

Scenario: Textract returns low confidence
  Given a low-quality scan (blurry)
  When Textract processes it
  And confidence is <90%
  Then the system falls back to Google Vision
  And uses the better result

Scenario: Textract API is unavailable
  Given AWS Textract API is down
  When the system tries to process an invoice
  Then it immediately falls back to Google Vision
  And logs the error
  And retries Textract on next invoice
```

**Definition of Done**:
- [ ] AWS Textract API integration
- [ ] Confidence score parsing
- [ ] Fallback logic implemented
- [ ] Error handling and logging
- [ ] Redis cache for results
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: AWS account setup, Textract access

---

### Story 2.1.2: Multi-Provider Fallback

**Feature**: FR-004 (Multi-Model OCR)  
**Priority**: P0  
**Story ID**: US-010

**As a** system  
**I want** to fall back to Google Vision and Azure if Textract fails  
**So that** OCR processing never fails due to provider issues

**Acceptance Criteria**:
```gherkin
Scenario: Textract fails, Google Vision succeeds
  Given Textract API returns an error
  When the system falls back to Google Vision
  Then Google Vision processes the invoice
  And returns OCR text with confidence score
  And the result is cached

Scenario: All providers fail
  Given Textract, Google, and Azure all fail
  When the system tries to process an invoice
  Then it flags the invoice for manual entry
  And alerts the user: "OCR processing failed for invoice #12345"
  And logs all three errors

Scenario: Cost optimization
  Given 100 invoices are uploaded
  When 95 are processed by Textract (high confidence)
  And 5 fall back to Google Vision
  Then the blended cost is <$0.0015 per page
```

**Definition of Done**:
- [ ] Google Cloud Vision API integration
- [ ] Azure Form Recognizer integration
- [ ] Fallback chain implemented
- [ ] Cost tracking per provider
- [ ] Error aggregation and alerting
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-009 (AWS Textract Integration), Google/Azure accounts

---

### Story 2.2.1: LLM Field Extraction

**Feature**: FR-005 (LLM Line Item Extraction)  
**Priority**: P0  
**Story ID**: US-011

**As a** system  
**I want** to extract structured fields from OCR text using Claude  
**So that** I can match invoices to POs accurately

**Acceptance Criteria**:
```gherkin
Scenario: System extracts standard fields
  Given OCR text from an invoice
  When the system sends it to Claude 3.5 Sonnet
  Then it receives JSON with:
    | vendor_name | invoice_number | invoice_date | due_date | total_amount | tax_amount |
  And each field has a confidence score (0-100)
  And the JSON matches the Pydantic schema

Scenario: System extracts line items
  Given OCR text with a line item table
  When the system sends it to Claude
  Then it receives line_items array:
    | description | quantity | unit_price | amount |
  And each line item has a confidence score
  And the sum of line amounts matches the total (±tolerance)

Scenario: System handles ambiguous data
  Given OCR text with unclear vendor name
  When Claude processes it
  Then it returns vendor_name with low confidence (<50%)
  And the system flags it for manual review
```

**Definition of Done**:
- [ ] Claude 3.5 Sonnet API integration
- [ ] Prompt template with few-shot examples
- [ ] Pydantic schema validation
- [ ] Confidence score per field
- [ ] Line item extraction
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: Anthropic API key, prompt engineering

---

### Story 2.2.2: Confidence Score Calibration

**Feature**: FR-005 (LLM Line Item Extraction)  
**Priority**: P0  
**Story ID**: US-012

**As a** system  
**I want** confidence scores to be calibrated  
**So that** 95% confidence means 95% actual accuracy

**Acceptance Criteria**:
```gherkin
Scenario: Confidence matches accuracy
  Given 100 invoices processed by Claude
  When 95 have 95%+ confidence on vendor_name
  Then at least 93 actually have correct vendor_name (95% ±2%)
  And the calibration is tracked over time

Scenario: System detects miscalibration
  Given confidence is 95% but actual accuracy is 80%
  When the system detects this (after 50 invoices)
  Then it adjusts the confidence scores downward
  And flags more invoices for review
  And alerts the engineering team

Scenario: User sees confidence breakdown
  Given an invoice is processed
  When the user views the invoice detail
  Then they see confidence per field:
    | Vendor: 98% | Amount: 99% | Date: 95% | PO#: 65% |
  And they can click to see why PO# is low confidence
```

**Definition of Done**:
- [ ] Calibration tracking implemented
- [ ] Automatic adjustment logic
- [ ] UI for confidence breakdown
- [ ] Alerting on miscalibration
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-011 (LLM Field Extraction)

---

### Story 2.3.1: Vendor Format Learning Trigger

**Feature**: FR-006 (Vendor Format Learning)  
**Priority**: P0  
**Story ID**: US-013

**As a** system  
**I want** to detect when a user corrects extraction errors  
**So that** I can learn the vendor's format

**Acceptance Criteria**:
```gherkin
Scenario: User corrects extraction
  Given the system extracted vendor_name = "Acme Ind"
  When the user edits it to "Acme Industrial"
  Then the system logs the correction
  And increments the correction count for this vendor
  And stores: extracted_value, corrected_value, field_name

Scenario: System detects pattern after 3 corrections
  Given the user corrected PO# location 3 times for Acme
  When the 3rd correction is made
  Then the system triggers format learning
  And analyzes the 3 corrections for patterns
  And creates a candidate extraction rule

Scenario: System validates learned rule
  Given a candidate rule is created
  When the system tests it on the next 5 invoices from Acme
  And accuracy is >80%
  Then the rule is activated
  And applied to future invoices
```

**Definition of Done**:
- [ ] Correction tracking implemented
- [ ] Pattern detection algorithm
- [ ] Rule validation logic
- [ ] Rule activation/deactivation
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-011 (LLM Field Extraction), correction logging

---

### Story 2.3.2: Rule Editor UI

**Feature**: FR-006 (Vendor Format Learning)  
**Priority**: P1  
**Story ID**: US-014

**As a** user  
**I want** to view and edit extraction rules per vendor  
**So that** I can fix incorrect rules manually

**Acceptance Criteria**:
```gherkin
Scenario: User views vendor rules
  Given I am on the Vendor Detail page for Acme
  When I click "Extraction Rules"
  Then I see a list of rules:
    | Field | Type | Pattern | Accuracy |
    | PO# | Coordinate | x:450, y:580, w:120, h:20 | 95% |
    | Invoice# | Regex | \d{6,10} | 98% |
  And I can see when each rule was created

Scenario: User edits a rule
  Given I see a rule with 70% accuracy
  When I edit the coordinates
  And save the changes
  Then the rule is updated
  And the accuracy resets (will be recalculated)

Scenario: User deletes a rule
  Given I see a rule that's causing errors
  When I click "Delete"
  Then the rule is removed
  And the system reverts to LLM extraction for that field
```

**Definition of Done**:
- [ ] Rule list UI implemented
- [ ] Rule editor modal
- [ ] Delete functionality
- [ ] Accuracy display
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-013 (Vendor Format Learning Trigger)

---

### Story 2.3.3: Rule Import/Export

**Feature**: FR-006 (Vendor Format Learning)  
**Priority**: P1  
**Story ID**: US-015

**As a** bookkeeper  
**I want** to export and import extraction rules  
**So that** I can share rules across clients or restore from backup

**Acceptance Criteria**:
```gherkin
Scenario: User exports rules
  Given I have 50 vendors with extraction rules
  When I click "Export Rules"
  Then a CSV file is downloaded
  With columns: vendor_name, field, rule_type, pattern, accuracy
  And all 50 vendors are included

Scenario: User imports rules
  Given I have a CSV file with extraction rules
  When I upload it via "Import Rules"
  Then the system validates the CSV format
  And imports the rules
  And shows a summary: "Imported 50 rules, 2 errors"

Scenario: Import with errors
  Given the CSV has invalid patterns
  When I upload it
  Then the valid rules are imported
  And the invalid rules are skipped
  And I see an error report: "Row 23: Invalid regex pattern"
```

**Definition of Done**:
- [ ] CSV export implemented
- [ ] CSV import with validation
- [ ] Error reporting
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-013 (Vendor Format Learning Trigger)

---

## Capability 3: Matching Engine

### Story 3.1.1: Bank Transaction Sync

**Feature**: FR-007 (3-Way Matching)  
**Priority**: P0  
**Story ID**: US-016

**As a** system  
**I want** to sync bank transactions from Plaid daily  
**So that** I can match invoices to actual payments

**Acceptance Criteria**:
```gherkin
Scenario: Daily bank sync runs
  Given it is 3:00 AM UTC
  When the scheduled job runs
  Then it fetches new transactions from Plaid
  And stores them in the database
  And links them to the company's bank account

Scenario: Transaction matches invoice
  Given a bank transaction: $1,234.56 to Acme Industrial on 2026-08-03
  And an invoice: $1,234.56 from Acme Industrial dated 2026-08-01
  When the matching engine runs
  Then it suggests a match with 95% confidence
  And the user can approve or reject

Scenario: Transaction has no match
  Given a bank transaction with no corresponding invoice
  When the matching engine runs
  Then it's flagged as "Unmatched Transaction"
  And the user can manually link it or ignore it
```

**Definition of Done**:
- [ ] Plaid API integration
- [ ] Daily sync job configured
- [ ] Transaction storage schema
- [ ] Matching algorithm (amount, date, payee)
- [ ] Manual linking UI
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: Plaid account setup, bank connection flow

---

### Story 3.1.2: PO Import from QuickBooks

**Feature**: FR-007 (3-Way Matching)  
**Priority**: P0  
**Story ID**: US-017

**As a** system  
**I want** to import purchase orders from QuickBooks  
**So that** I can match invoices to POs

**Acceptance Criteria**:
```gherkin
Scenario: POs are synced from QBO
  Given the user has 50 open POs in QuickBooks
  When the daily QBO sync runs
  Then all 50 POs are imported
  With fields: PO#, vendor, line_items, total, status
  And stored in the database

Scenario: PO is closed in QBO
  Given a PO was imported as "Open"
  When it's marked as "Closed" in QBO
  And the sync runs
  Then the PO status is updated to "Closed"
  And no new invoices can be matched to it

Scenario: PO line items match invoice
  Given PO-12345 has line items: Widget × 10 @ $100 = $1,000
  And an invoice has: Widget × 10 @ $100 = $1,000
  When the matching engine runs
  Then it suggests a match with 98% confidence
```

**Definition of Done**:
- [ ] QBO PO API integration
- [ ] Daily sync job
- [ ] PO status tracking
- [ ] Line item matching logic
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-016 (Bank Transaction Sync), QBO API access

---

### Story 3.1.3: 3-Way Match Algorithm

**Feature**: FR-007 (3-Way Matching)  
**Priority**: P0  
**Story ID**: US-018

**As a** system  
**I want** to calculate match confidence across invoice, PO, and bank transaction  
**So that** I can auto-approve high-confidence matches

**Acceptance Criteria**:
```gherkin
Scenario: Perfect 3-way match
  Given invoice: $1,234.56, Acme Industrial, PO-12345, 2026-08-01
  And PO: $1,234.56, Acme Industrial, PO-12345
  And bank tx: $1,234.56, ACME INDUSTRIAL, 2026-08-03
  When the matching engine runs
  Then confidence = 98% (all fields match)
  And the invoice is auto-approved

Scenario: Partial match (amount mismatch)
  Given invoice: $1,234.56
  And PO: $1,200.00
  And bank tx: $1,234.56
  When the matching engine runs
  Then confidence = 75% (amount mismatch >5%)
  And the invoice is flagged for review

Scenario: No PO match
  Given invoice has no PO#
  And no matching PO by vendor + amount
  When the matching engine runs
  Then confidence = 60% (2-way match only: invoice + bank)
  And the invoice is flagged for review
```

**Definition of Done**:
- [ ] Matching algorithm implemented
- [ ] Confidence calculation (weighted fields)
- [ ] Auto-approve logic (threshold: 95%)
- [ ] Review flagging (80-94%, <80%)
- [ ] Tests passing (100+ test cases)

**Estimate**: 8 story points  
**Dependencies**: US-016 (Bank Sync), US-017 (PO Import)

---

### Story 3.2.1: Confidence Score Display

**Feature**: FR-008 (Confidence Scoring)  
**Priority**: P0  
**Story ID**: US-019

**As a** user  
**I want** to see confidence scores for each match  
**So that** I know which invoices to review

**Acceptance Criteria**:
```gherkin
Scenario: User sees confidence in queue
  Given I am on the Exception Queue page
  When I see invoice cards
  Then each card shows:
    | Vendor | Amount | Confidence: 87% | Priority: High |
  And the confidence is color-coded (green/yellow/red)

Scenario: User sees confidence breakdown
  Given I click on an invoice
  When the detail view opens
  Then I see a breakdown:
    | Amount: 30/30 | Vendor: 18/20 | Date: 13/15 | PO#: 20/20 | Lines: 15/15 |
    | Total: 96/100 = 96% |
  And I can see which fields lowered the score

Scenario: User adjusts threshold
  Given the default auto-approve threshold is 95%
  When I go to Settings > Matching
  And I change it to 90%
  Then more invoices are auto-approved
  And the system logs the change
```

**Definition of Done**:
- [ ] Confidence display in queue UI
- [ ] Color coding (green/yellow/red)
- [ ] Breakdown modal
- [ ] Threshold settings
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-018 (3-Way Match Algorithm)

---

### Story 3.3.1: Split Match UI

**Feature**: FR-009 (Split Matching)  
**Priority**: P1  
**Story ID**: US-020

**As a** bookkeeper  
**I want** to split one invoice across multiple POs  
**So that** I can handle consolidated billing

**Acceptance Criteria**:
```gherkin
Scenario: User splits invoice manually
  Given an invoice for $5,000
  And two POs: PO-101 ($2,000), PO-102 ($3,000)
  When I open the split match UI
  Then I can allocate:
    | PO-101: $2,000 |
    | PO-102: $3,000 |
  And the system validates: $2,000 + $3,000 = $5,000
  And I can approve the split match

Scenario: System suggests split
  Given an invoice for $5,000 from Acme
  And two open POs from Acme: $2,000 and $3,000
  When the matching engine runs
  Then it suggests a split match
  And shows: "Suggested: PO-101 ($2K) + PO-102 ($3K)"
  And I can approve with one click

Scenario: Split validation fails
  Given I try to allocate $2,500 + $3,000 = $5,500
  When I click "Approve"
  Then the system shows an error: "Total allocation ($5,500) exceeds invoice total ($5,000)"
  And I cannot approve until fixed
```

**Definition of Done**:
- [ ] Split match UI (drag-and-drop allocation)
- [ ] Validation logic (sum check)
- [ ] Auto-suggest algorithm
- [ ] QBO integration (multiple bills)
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-018 (3-Way Match Algorithm)

---

### Story 3.3.2: Split Match Audit Trail

**Feature**: FR-009 (Split Matching)  
**Priority**: P1  
**Story ID**: US-021

**As a** CFO  
**I want** split matches to be fully auditable  
**So that** I can trace which POs were matched to which invoices

**Acceptance Criteria**:
```gherkin
Scenario: Split match is logged
  Given an invoice is split across PO-101 and PO-102
  When the match is approved
  Then the audit log shows:
    | Action: split_match | Invoice: inv_12345 | POs: PO-101, PO-102 | User: Olivia |
  And each PO link is stored in the database

Scenario: User views split match history
  Given I am on the PO Detail page for PO-101
  When I click "Matched Invoices"
  Then I see inv_12345 (split: $2,000 of $5,000)
  And I can click to view the full invoice

Scenario: Audit report includes splits
  Given I export the audit report for Q3
  When I open the CSV
  Then split matches are shown with all linked POs
  And the allocation amounts are included
```

**Definition of Done**:
- [ ] Audit logging for split matches
- [ ] PO detail page shows matched invoices
- [ ] Audit report includes split data
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-020 (Split Match UI), FR-018 (Audit Trail)

---

## Capability 4: Exception Queue

### Story 4.1.1: Priority Score Calculation

**Feature**: FR-010 (Smart Prioritization)  
**Priority**: P0  
**Story ID**: US-022

**As a** system  
**I want** to calculate priority scores for exceptions  
**So that** users see the most important invoices first

**Acceptance Criteria**:
```gherkin
Scenario: Priority score is calculated
  Given an invoice: $10,000, 1 day old, Tier A vendor
  When the priority formula runs
  Then score = (100 × 0.5) + (1 × 10) + (5 × 20) = 160
  And the invoice is sorted accordingly

Scenario: High-priority invoice is shown first
  Given the queue has 100 invoices
  When the user opens the queue
  Then invoices are sorted by priority (highest first)
  And the top invoice has the highest score

Scenario: SLA risk is highlighted
  Given an invoice is >7 days old
  When it appears in the queue
  Then it has a red "SLA Risk" badge
  And it's sorted higher (age factor increases daily)
```

**Definition of Done**:
- [ ] Priority formula implemented
- [ ] Sorting by priority
- [ ] SLA risk badge
- [ ] Real-time score updates
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-018 (3-Way Match Algorithm)

---

### Story 4.1.2: Queue Filtering

**Feature**: FR-010 (Smart Prioritization)  
**Priority**: P0  
**Story ID**: US-023

**As a** user  
**I want** to filter the exception queue  
**So that** I can focus on specific invoices

**Acceptance Criteria**:
```gherkin
Scenario: User filters by vendor
  Given the queue has invoices from 50 vendors
  When I select "Acme Industrial" in the vendor filter
  Then only Acme invoices are shown
  And the count updates: "Showing 15 of 200 invoices"

Scenario: User filters by amount range
  Given the queue has invoices from $100 to $50,000
  When I set the amount filter: $1,000 - $10,000
  Then only invoices in that range are shown

Scenario: User filters by confidence
  Given the queue has invoices with 50-94% confidence
  When I set the confidence filter: <70%
  Then only low-confidence invoices are shown
  And they're highlighted (high priority)
```

**Definition of Done**:
- [ ] Filter UI (vendor, amount, confidence, date)
- [ ] Real-time filtering
- [ ] Count display
- [ ] Filter persistence (user preference)
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-022 (Priority Score Calculation)

---

### Story 4.2.1: Inline Review Modal

**Feature**: FR-011 (Inline Review)  
**Priority**: P0  
**Story ID**: US-024

**As a** user  
**I want** to review invoices without leaving the queue  
**So that** I can process exceptions quickly

**Acceptance Criteria**:
```gherkin
Scenario: User opens inline review
  Given I am on the Exception Queue page
  When I click an invoice card
  Then a modal opens (no page navigation)
  And shows: PDF preview (left), extracted data (right)
  And I can see the confidence breakdown

Scenario: User edits extracted data
  Given the extracted vendor_name is "Acme Ind"
  When I edit it to "Acme Industrial"
  And save
  Then the change is saved
  And the invoice is re-matched (confidence may change)

Scenario: User approves invoice
  Given I reviewed the invoice
  When I click "Approve"
  Then the invoice is approved
  And posted to QuickBooks (if configured)
  And removed from the queue
  And the next invoice is shown
```

**Definition of Done**:
- [ ] Modal component implemented
- [ ] PDF preview (PDF.js)
- [ ] Inline editing
- [ ] Approve/reject actions
- [ ] Auto-advance to next invoice
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-022 (Priority Score Calculation)

---

### Story 4.2.2: Keyboard Shortcuts

**Feature**: FR-011 (Inline Review)  
**Priority**: P0  
**Story ID**: US-025

**As a** power user  
**I want** keyboard shortcuts for review actions  
**So that** I can process invoices faster

**Acceptance Criteria**:
```gherkin
Scenario: User approves with keyboard
  Given I am reviewing an invoice
  When I press 'A'
  Then the invoice is approved
  And the next invoice is shown

Scenario: User rejects with keyboard
  Given I am reviewing an invoice
  When I press 'R'
  Then a reject reason modal opens
  And I can select a reason
  And the invoice is rejected

Scenario: User navigates with keyboard
  Given I am in the queue
  When I press 'N'
  Then the next invoice is shown
  When I press 'P'
  Then the previous invoice is shown
  When I press 'E'
  Then edit mode is activated
```

**Definition of Done**:
- [ ] Keyboard event listeners
- [ ] Shortcuts: A, R, N, P, E
- [ ] Shortcut help modal (press '?')
- [ ] Shortcuts can be disabled (user preference)
- [ ] Tests passing

**Estimate**: 2 story points  
**Dependencies**: US-024 (Inline Review Modal)

---

### Story 4.3.1: Batch Selection

**Feature**: FR-012 (Batch Actions)  
**Priority**: P1  
**Story ID**: US-026

**As a** user  
**I want** to select multiple invoices  
**So that** I can batch approve or reject them

**Acceptance Criteria**:
```gherkin
Scenario: User selects multiple invoices
  Given I am on the Exception Queue page
  When I click checkboxes on 10 invoices
  Then all 10 are selected
  And the batch action bar appears: "10 invoices selected"

Scenario: User selects range with Shift-click
  Given I click invoice #1
  When I Shift-click invoice #20
  Then invoices #1-20 are selected (20 total)
  And the batch action bar appears

Scenario: User deselects all
  Given I have 10 invoices selected
  When I click "Clear Selection"
  Then all invoices are deselected
  And the batch action bar disappears
```

**Definition of Done**:
- [ ] Checkbox selection
- [ ] Shift-click range selection
- [ ] Select all / Clear selection
- [ ] Batch action bar
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-024 (Inline Review Modal)

---

### Story 4.3.2: Batch Approve

**Feature**: FR-012 (Batch Actions)  
**Priority**: P1  
**Story ID**: US-027

**As a** user  
**I want** to approve multiple invoices at once  
**So that** I can clear the queue faster

**Acceptance Criteria**:
```gherkin
Scenario: User batch approves
  Given I have 10 invoices selected
  When I click "Approve All"
  Then each invoice is validated
  And approved invoices are posted to QBO
  And I see results: "8 approved, 2 failed"
  And failed invoices show error reasons

Scenario: Batch approve with validation errors
  Given 2 of 10 invoices have validation errors (duplicate PO#)
  When I click "Approve All"
  Then 8 invoices are approved
  And 2 invoices remain in queue with error badges
  And I see: "Invoice #12345: Duplicate PO#", "Invoice #12346: Amount mismatch"

Scenario: User views batch results
  Given I batch approved 10 invoices
  When I click "View Results"
  Then I see a summary modal:
    | Approved: 8 | Failed: 2 | Total: 10 |
  And I can export the results as CSV
```

**Definition of Done**:
- [ ] Batch approve API endpoint
- [ ] Background job processing
- [ ] Results modal
- [ ] Error handling per invoice
- [ ] CSV export
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-026 (Batch Selection), FR-013 (QBO Sync)

---

## Capability 5: QuickBooks Integration

### Story 5.1.1: OAuth Connection

**Feature**: FR-013 (QBO Bi-Directional Sync)  
**Priority**: P0  
**Story ID**: US-028

**As a** user  
**I want** to connect my QuickBooks account via OAuth  
**So that** InvoiceMatch can sync data

**Acceptance Criteria**:
```gherkin
Scenario: User connects QBO
  Given I am on Settings > Integrations
  When I click "Connect QuickBooks"
  Then I'm redirected to Intuit OAuth page
  And I log in and grant permissions
  And I'm redirected back to InvoiceMatch
  And I see: "QuickBooks connected: Acme Company"

Scenario: User disconnects QBO
  Given QBO is connected
  When I click "Disconnect"
  Then the OAuth token is revoked
  And sync stops
  And I see: "QuickBooks disconnected"

Scenario: OAuth token expires
  Given the OAuth token expires (180 days)
  When the system tries to sync
  Then it detects the expiration
  And alerts the user: "QuickBooks connection expired, please reconnect"
```

**Definition of Done**:
- [ ] OAuth 2.0 flow implemented
- [ ] Token storage (encrypted)
- [ ] Token refresh logic
- [ ] Disconnect functionality
- [ ] Expiration handling
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: QuickBooks developer account, OAuth setup

---

### Story 5.1.2: Vendor Sync

**Feature**: FR-013 (QBO Bi-Directional Sync)  
**Priority**: P0  
**Story ID**: US-029

**As a** system  
**I want** to sync vendors from QuickBooks daily  
**So that** I have the latest vendor data

**Acceptance Criteria**:
```gherkin
Scenario: Daily vendor sync runs
  Given it is 3:00 AM UTC
  When the scheduled job runs
  Then it fetches all vendors from QBO
  And updates the local vendor database
  And logs: "Synced 150 vendors from QBO"

Scenario: New vendor is added in QBO
  Given a new vendor "Acme Industrial" is added in QBO
  When the daily sync runs
  Then the vendor is imported
  And available for invoice matching

Scenario: Vendor is deactivated in QBO
  Given a vendor is marked inactive in QBO
  When the daily sync runs
  Then the vendor is marked inactive locally
  And no new invoices can be matched to it
```

**Definition of Done**:
- [ ] QBO Vendor API integration
- [ ] Daily sync job
- [ ] Vendor status tracking (active/inactive)
- [ ] Error handling (API failures)
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-028 (OAuth Connection)

---

### Story 5.1.3: Post Bill to QBO

**Feature**: FR-013 (QBO Bi-Directional Sync)  
**Priority**: P0  
**Story ID**: US-030

**As a** system  
**I want** to post approved invoices as bills to QuickBooks  
**So that** users don't have to double-enter data

**Acceptance Criteria**:
```gherkin
Scenario: Approved invoice is posted to QBO
  Given an invoice is approved by the user
  When the post job runs
  Then a Bill is created in QBO
  With vendor, amount, date, line items, GL codes
  And the PDF is attached (if <5MB)
  And the invoice status is updated to "Posted"

Scenario: Bill creation fails
  Given the QBO API is unavailable
  When the post job runs
  Then it retries 3 times (exponential backoff)
  And if still failing, alerts the user
  And the invoice remains in "Approved" status

Scenario: Duplicate bill detection
  Given an invoice was already posted to QBO
  When the user tries to approve it again
  Then the system detects the duplicate (QBO Bill ID)
  And prevents posting
  And shows: "Already posted as Bill #5678 in QBO"
```

**Definition of Done**:
- [ ] QBO Bill API integration
- [ ] PDF attachment (up to 5MB)
- [ ] Retry logic (3 attempts)
- [ ] Duplicate detection
- [ ] Status tracking (Pending, Posted, Failed)
- [ ] Tests passing

**Estimate**: 5 story points  
**Dependencies**: US-028 (OAuth Connection), US-029 (Vendor Sync)

---

### Story 5.2.1: GL Code Mapping UI

**Feature**: FR-014 (GL Code Mapping)  
**Priority**: P0  
**Story ID**: US-031

**As a** bookkeeper  
**I want** to map vendors to default GL codes  
**So that** invoices are auto-coded correctly

**Acceptance Criteria**:
```gherkin
Scenario: User sets default GL code for vendor
  Given I am on the Vendor Detail page for Acme
  When I set "Default GL Code" to "6000-Supplies"
  And save
  Then all future invoices from Acme are auto-coded to 6000-Supplies
  And existing invoices are not changed

Scenario: System suggests GL code
  Given Acme has 10 historical invoices
  And 8 were coded to "6000-Supplies"
  When I open the GL code dropdown
  Then the system suggests "6000-Supplies (80% match)"
  And I can accept or choose a different code

Scenario: User validates GL code
  Given I enter an invalid GL code "9999-Invalid"
  When I save
  Then the system checks against QBO Chart of Accounts
  And shows an error: "GL code 9999-Invalid not found in QBO"
  And I cannot save until I choose a valid code
```

**Definition of Done**:
- [ ] GL code mapping UI
- [ ] Suggestion algorithm (historical patterns)
- [ ] Validation against QBO Chart of Accounts
- [ ] Auto-coding on invoice ingestion
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-029 (Vendor Sync), QBO Chart of Accounts API

---

### Story 5.2.2: Auto-Coding from History

**Feature**: FR-014 (GL Code Mapping)  
**Priority**: P0  
**Story ID**: US-032

**As a** system  
**I want** to learn GL codes from historical invoices  
**So that** I can auto-code new invoices

**Acceptance Criteria**:
```gherkin
Scenario: System learns from historical coding
  Given 20 invoices from Acme were manually coded
  And 18 were coded to "6000-Supplies"
  When a new invoice from Acme is ingested
  Then the system auto-codes it to "6000-Supplies"
  With confidence: 90% (18/20 = 90%)

Scenario: System handles multiple GL codes
  Given Acme has invoices coded to:
    | 6000-Supplies (60%) | 6100-Equipment (30%) | 6200-Services (10%) |
  When a new invoice is ingested
  Then the system suggests the most common: "6000-Supplies"
  And shows: "Also used: 6100-Equipment (30%)"
  And the user can choose

Scenario: System detects coding change
  Given Acme was coded to "6000-Supplies" for 20 invoices
  And the last 5 invoices were coded to "6100-Equipment"
  When a new invoice is ingested
  Then the system suggests "6100-Equipment" (recent pattern)
  And notes: "Vendor changed GL code preference"
```

**Definition of Done**:
- [ ] Historical pattern analysis
- [ ] Confidence calculation
- [ ] Multiple code handling
- [ ] Recent pattern detection
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-031 (GL Code Mapping UI)

---

### Story 5.3.1: Error Alerting

**Feature**: FR-015 (Error Handling & Retry)  
**Priority**: P0  
**Story ID**: US-033

**As a** user  
**I want** to be alerted when QBO sync fails  
**So that** I can resolve issues quickly

**Acceptance Criteria**:
```gherkin
Scenario: User receives email alert
  Given QBO sync fails for 3 consecutive invoices
  When the error threshold is reached
  Then an email is sent: "QBO sync failed for 3 invoices"
  With details: invoice numbers, error messages
  And a link to resolve

Scenario: User receives Slack alert
  Given Slack integration is configured
  When QBO sync fails
  Then a Slack message is posted to #accounting
  With: "⚠️ QBO sync failed for invoice #12345: Invalid GL code"
  And a link to the invoice

Scenario: User resolves error
  Given I receive an alert
  When I click the link
  Then I'm taken to the invoice detail page
  And I can see the error
  And I can fix it (edit GL code, etc.)
  And retry the sync
```

**Definition of Done**:
- [ ] Email alert template
- [ ] Slack integration
- [ ] Error threshold configuration
- [ ] Alert links to invoice detail
- [ ] Retry functionality
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-030 (Post Bill to QBO), email/Slack setup

---

## Capability 6: Vendor Database

### Story 6.1.1: Vendor Score Calculation

**Feature**: FR-016 (Vendor Scoring)  
**Priority**: P1  
**Story ID**: US-034

**As a** system  
**I want** to calculate vendor reliability scores  
**So that** users can prioritize negotiations

**Acceptance Criteria**:
```gherkin
Scenario: System calculates vendor score
  Given a vendor has:
    | On-Time: 95% | Accuracy: 90% | Price Consistency: 85% | Communication: 80% | Compliance: 100% |
  When the nightly job runs
  Then score = (95×0.30) + (90×0.25) + (85×0.20) + (80×0.15) + (100×0.10) = 89.25
  And tier = B (75-89)

Scenario: Vendor tier affects matching threshold
  Given a vendor is Tier A (score 95)
  When invoices from this vendor are matched
  Then the auto-approve threshold is 90% (instead of 95%)
  And more invoices are auto-approved

Scenario: Score drops significantly
  Given a vendor's score drops from 90 to 65 (25 points)
  When the nightly job runs
  Then an alert is sent: "Vendor score dropped: Acme Industrial (90 → 65)"
  And the vendor is flagged for review
```

**Definition of Done**:
- [ ] Score calculation formula
- [ ] Tier assignment (A/B/C/D)
- [ ] Threshold adjustment by tier
- [ ] Alert on significant score drop
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: Invoice data, matching history

---

### Story 6.2.1: Vendor Format Rule Storage

**Feature**: FR-017 (Vendor Format Rules)  
**Priority**: P0  
**Story ID**: US-035

**As a** system  
**I want** to store extraction rules per vendor  
**So that** I can auto-process future invoices

**Acceptance Criteria**:
```gherkin
Scenario: System stores coordinate rule
  Given the user corrected PO# location 3 times
  When the system creates a rule
  Then it stores:
    | vendor_id: uuid | field: PO# | type: coordinate | x:450, y:580, w:120, h:20 | accuracy: 95% |
  And the rule is applied to future invoices

Scenario: System stores regex rule
  Given the system detects invoice# pattern
  When it creates a rule
  Then it stores:
    | field: invoice# | type: regex | pattern: \d{6,10} | accuracy: 98% |

Scenario: Rule accuracy is tracked
  Given a rule is created with 95% accuracy
  When it's applied to 10 invoices
  And 2 are corrected by the user
  Then accuracy is updated: 8/10 = 80%
  And if accuracy <80%, the rule is auto-disabled
```

**Definition of Done**:
- [ ] Rule storage schema (PostgreSQL JSONB)
- [ ] Coordinate rule type
- [ ] Regex rule type
- [ ] Accuracy tracking
- [ ] Auto-disable logic
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-013 (Vendor Format Learning Trigger)

---

### Story 6.2.2: Rule Accuracy Dashboard

**Feature**: FR-017 (Vendor Format Rules)  
**Priority**: P1  
**Story ID**: US-036

**As a** user  
**I want** to see rule accuracy per vendor  
**So that** I know which rules need attention

**Acceptance Criteria**:
```gherkin
Scenario: User views rule accuracy
  Given I am on the Vendor Detail page
  When I click "Extraction Rules"
  Then I see a table:
    | Field | Type | Pattern | Accuracy | Created | Last Used |
    | PO# | Coordinate | x:450, y:580... | 95% | 2026-08-01 | 2026-08-05 |
  And rules are sorted by accuracy (lowest first)

Scenario: User sees accuracy trend
  Given I click on a rule
  When the detail modal opens
  Then I see a chart: "Accuracy over time (30 days)"
  And I can see when accuracy dropped
  And correlate with invoice changes

Scenario: User filters by accuracy
  Given I have 50 vendors with rules
  When I filter "Accuracy <80%"
  Then I see 5 vendors with low-accuracy rules
  And I can prioritize fixing them
```

**Definition of Done**:
- [ ] Rule accuracy table
- [ ] Accuracy trend chart
- [ ] Filtering by accuracy
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-035 (Vendor Format Rule Storage)

---

## Capability 7: Audit Trail

### Story 7.1.1: Action Logging

**Feature**: FR-018 (Immutable Action Log)  
**Priority**: P0  
**Story ID**: US-037

**As a** system  
**I want** to log every user action  
**So that** there's a complete audit trail

**Acceptance Criteria**:
```gherkin
Scenario: User uploads invoice
  Given I upload an invoice PDF
  When the upload completes
  Then a log entry is created:
    | action: invoice.upload | user_id: uuid | resource_type: invoice | resource_id: uuid | timestamp: 2026-08-06T14:30:22Z |

Scenario: User approves invoice
  Given I approve an invoice
  When the approval completes
  Then a log entry is created:
    | action: invoice.approve | before: {status: pending} | after: {status: approved} |

Scenario: User edits GL code
  Given I change GL code from 6000 to 6100
  When the edit is saved
  Then a log entry is created:
    | action: invoice.edit | before: {gl_code: 6000} | after: {gl_code: 6100} |
```

**Definition of Done**:
- [ ] Log table schema (append-only)
- [ ] Action logging middleware
- [ ] Before/after snapshots
- [ ] Timestamp and user attribution
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: Database schema, authentication

---

### Story 7.1.2: Audit Log Export

**Feature**: FR-018 (Immutable Action Log)  
**Priority**: P0  
**Story ID**: US-038

**As a** CFO  
**I want** to export audit logs for compliance  
**So that** I can provide them to auditors

**Acceptance Criteria**:
```gherkin
Scenario: User exports audit log as CSV
  Given I am on the Audit page
  When I select date range: 2026-01-01 to 2026-12-31
  And click "Export CSV"
  Then a CSV file is downloaded
  With columns: timestamp, user, action, resource_type, resource_id, before, after
  And all actions in the date range are included

Scenario: User exports audit log as PDF
  Given I need a formatted report for auditors
  When I click "Export PDF"
  Then a PDF report is generated
  With: cover page, table of contents, action details
  And it's digitally signed (tamper-evident)

Scenario: Export is restricted by role
  Given I am a viewer (not admin)
  When I try to export audit logs
  Then I see an error: "Permission denied: Admin role required"
  And the export is blocked
```

**Definition of Done**:
- [ ] CSV export functionality
- [ ] PDF report generation
- [ ] Digital signature (tamper-evident)
- [ ] Role-based access control
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-037 (Action Logging)

---

### Story 7.1.3: 7-Year Retention

**Feature**: FR-018 (Immutable Action Log)  
**Priority**: P0  
**Story ID**: US-039

**As a** system  
**I want** to retain audit logs for 7 years  
**So that** we comply with IRS requirements

**Acceptance Criteria**:
```gherkin
Scenario: Logs are archived after 90 days
  Given a log entry is 91 days old
  When the nightly archival job runs
  Then the log is moved to S3 Glacier
  And removed from the hot database
  And a pointer is kept for retrieval

Scenario: Logs are deleted after 7 years
  Given a log entry is 7 years and 1 month old
  When the deletion job runs
  Then the log is permanently deleted
  And a deletion log is created: "Deleted log_id: xyz (retention expired)"

Scenario: User retrieves archived log
  Given I need a log from 1 year ago (in Glacier)
  When I request it via the Audit page
  Then the system initiates retrieval (3-5 hours)
  And notifies me when ready: "Archived log retrieved"
```

**Definition of Done**:
- [ ] Archival job (90 days → Glacier)
- [ ] Deletion job (7 years → permanent delete)
- [ ] Glacier retrieval process
- [ ] Retention policy documentation
- [ ] Tests passing

**Estimate**: 3 story points  
**Dependencies**: US-037 (Action Logging), S3 Glacier setup

---

## Story Summary by Priority

### P0 (Must Have) — 30 Stories

| Story ID | Feature | Estimate |
|----------|---------|----------|
| US-001 | Email Forwarding Setup | 3 |
| US-002 | Email Subject Parsing | 2 |
| US-004 | Drag-and-Drop Upload | 5 |
| US-005 | Upload Progress Tracking | 5 |
| US-007 | Vendor Portal Credentials | 5 |
| US-009 | AWS Textract Integration | 5 |
| US-010 | Multi-Provider Fallback | 5 |
| US-011 | LLM Field Extraction | 5 |
| US-012 | Confidence Score Calibration | 3 |
| US-013 | Vendor Format Learning Trigger | 5 |
| US-016 | Bank Transaction Sync | 5 |
| US-017 | PO Import from QBO | 5 |
| US-018 | 3-Way Match Algorithm | 8 |
| US-019 | Confidence Score Display | 3 |
| US-022 | Priority Score Calculation | 3 |
| US-023 | Queue Filtering | 3 |
| US-024 | Inline Review Modal | 5 |
| US-025 | Keyboard Shortcuts | 2 |
| US-028 | OAuth Connection | 5 |
| US-029 | Vendor Sync | 3 |
| US-030 | Post Bill to QBO | 5 |
| US-031 | GL Code Mapping UI | 3 |
| US-032 | Auto-Coding from History | 3 |
| US-033 | Error Alerting | 3 |
| US-035 | Vendor Format Rule Storage | 3 |
| US-037 | Action Logging | 3 |
| US-038 | Audit Log Export | 3 |
| US-039 | 7-Year Retention | 3 |
| **Total P0** | **28 stories** | **111 points** |

### P1 (Should Have) — 10 Stories

| Story ID | Feature | Estimate |
|----------|---------|----------|
| US-003 | Sender Whitelist | 3 |
| US-006 | Invoice Preview | 3 |
| US-014 | Rule Editor UI | 3 |
| US-015 | Rule Import/Export | 3 |
| US-020 | Split Match UI | 5 |
| US-021 | Split Match Audit Trail | 3 |
| US-026 | Batch Selection | 3 |
| US-027 | Batch Approve | 5 |
| US-034 | Vendor Score Calculation | 3 |
| US-036 | Rule Accuracy Dashboard | 3 |
| **Total P1** | **10 stories** | **34 points** |

### P2 (Could Have) — 2 Stories

| Story ID | Feature | Estimate |
|----------|---------|----------|
| US-008 | Daily Invoice Fetch | 8 |
| US-021 | Split Match Audit Trail | 3 |
| **Total P2** | **2 stories** | **11 points** |

---

## Total Estimates

| Priority | Stories | Points | Weeks (at 20 pts/week) |
|----------|---------|--------|------------------------|
| P0 | 28 | 111 | 5.5 weeks |
| P1 | 10 | 34 | 1.5 weeks |
| P2 | 2 | 11 | 0.5 weeks |
| **Total** | **40** | **156** | **7.5 weeks** |

**Note**: 1 week = 20 story points (team velocity estimate for 3 engineers)

---

## Sprint Allocation (8-Week MVP)

### Sprint 1-2 (Weeks 1-2): Foundation
- US-004, US-005: PDF Upload
- US-009, US-010: OCR Integration
- US-037, US-038, US-039: Audit Trail
- **Total**: 24 points

### Sprint 3-4 (Weeks 3-4): Core Logic
- US-011, US-012: LLM Extraction
- US-013: Vendor Learning
- US-016, US-017, US-018: Matching Engine
- **Total**: 33 points

### Sprint 5-6 (Weeks 5-6): Integration
- US-001, US-002: Email Forwarding
- US-028, US-029, US-030: QBO Sync
- US-031, US-032: GL Code Mapping
- **Total**: 34 points

### Sprint 7-8 (Weeks 7-8): UX & Polish
- US-019, US-022, US-023: Exception Queue
- US-024, US-025: Inline Review
- US-033: Error Alerting
- US-035: Vendor Rules
- **Total**: 20 points

### Buffer (Week 9-10): Testing & Fixes
- Bug fixes, performance optimization
- Documentation, user guides
- **Total**: 20 points buffer

---

**User Stories Complete** ✅

**Next Steps**:
1. Review stories with product owner
2. Estimate with engineering team (planning poker)
3. Prioritize for Sprint 1
4. Create tasks in project management tool
5. Start development

---

*Generated by idea-to-features skill v1.0*  
*Source: pain_001 (Invoice/Receipt Reconciliation)*  
*Opportunity Score: 82/100*
