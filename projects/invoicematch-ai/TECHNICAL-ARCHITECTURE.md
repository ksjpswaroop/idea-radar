# InvoiceMatch AI — Technical Architecture

**Document Type**: Architecture Specification  
**Product**: InvoiceMatch AI  
**Version**: 1.0 (MVP)  
**Created**: 2026-08-06  
**Author**: AI SaaS Startup Factory  
**Status**: Draft

---

## 1. Executive Summary

InvoiceMatch AI is a cloud-native SaaS platform for automated invoice reconciliation. The system ingests invoices from multiple sources (email, upload, vendor portals), extracts structured data using OCR + LLM, matches to purchase orders and bank transactions, and posts approved bills to QuickBooks Online.

**Key Architectural Decisions**:
- **Cloud**: AWS (us-east-1 primary)
- **Compute**: ECS Fargate (serverless containers)
- **Database**: PostgreSQL (RDS, multi-AZ)
- **Storage**: S3 (PDFs, audit logs)
- **OCR**: Multi-provider fallback (AWS Textract → Google Vision → Azure)
- **LLM**: Anthropic Claude 3.5 Sonnet
- **Integration**: QuickBooks Online, Plaid

---

## 2. System Context

### 2.1 System Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                     InvoiceMatch AI System                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Email   │    │   Web    │    │  Vendor  │    │  Quick   │ │
│  │  (SES)   │───▶│  Upload  │───▶│  Portal  │───▶│  Books   │ │
│  │          │    │          │    │  Scraper │    │  (QBO)   │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │               │               │               │       │
│        ▼               ▼               ▼               ▼       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Invoice Processing Pipeline                 │  │
│  │  OCR → LLM Extraction → Matching → Approval → Sync      │  │
│  └──────────────────────────────────────────────────────────┘  │
│        │               │               │               │       │
│        ▼               ▼               ▼               ▼       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Bank    │    │  Audit   │    │  Vendor  │    │  User    │ │
│  │  (Plaid) │    │  Trail   │    │   DB     │    │Dashboard │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 External Systems

| System | Purpose | Integration Method | Frequency |
|--------|---------|-------------------|-----------|
| **AWS SES** | Inbound email parsing | API (Lambda trigger) | Real-time |
| **AWS Textract** | OCR processing | API (sync) | Per invoice |
| **Google Vision** | OCR fallback | API (sync) | On Textract failure |
| **Azure Form Recognizer** | OCR last resort | API (sync) | On Google failure |
| **Anthropic Claude** | LLM extraction | API (sync) | Per invoice |
| **QuickBooks Online** | Bill posting, vendor sync | OAuth 2.0 + REST API | Daily sync, real-time post |
| **Plaid** | Bank transaction sync | OAuth 2.0 + REST API | Daily sync |
| **Vendor Portals** | Invoice scraping | Puppeteer (headless browser) | Daily (2 AM UTC) |

---

## 3. Architecture Principles

### 3.1 Design Principles

1. **Local-First Processing**: OCR and LLM run in cloud, but data is customer-isolated
2. **Exception-Only UX**: Automate 80%, show humans only exceptions (20%)
3. **Multi-Provider Redundancy**: OCR fallback chain (Textract → Google → Azure)
4. **Immutable Audit Trail**: Append-only logs, 7-year retention
5. **Company Isolation**: Row-level security (RLS) in PostgreSQL

### 3.2 Quality Attributes

| Attribute | Target | Measurement |
|-----------|--------|-------------|
| **Availability** | 99.9% | Monthly uptime (excludes planned maintenance) |
| **Latency** | <2s page load | 95th percentile (dashboard, queue) |
| **OCR Accuracy** | >99% | Field-level accuracy on printed text |
| **Match Accuracy** | >99.5% | % correct auto-matches |
| **Throughput** | 10K invoices/hour | Peak load (month-end) |
| **RTO** | 4 hours | Recovery time objective |
| **RPO** | 1 hour | Recovery point objective |

---

## 4. System Architecture

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud (us-east-1)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    CloudFront CDN                       │   │
│  │              (Static assets, PDF previews)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Application Load Balancer              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│         ┌──────────────────┴──────────────────┐                 │
│         ▼                                     ▼                 │
│  ┌─────────────┐                       ┌─────────────┐         │
│  │  ECS Task   │                       │  ECS Task   │         │
│  │  (Frontend) │                       │   (API)     │         │
│  │  React app  │                       │  FastAPI    │         │
│  │  :80/:443   │                       │  :8000      │         │
│  └─────────────┘                       └─────────────┘         │
│                                               │                 │
│                              ┌────────────────┼────────────┐   │
│                              │                │            │   │
│                              ▼                ▼            ▼   │
│                       ┌──────────┐    ┌──────────┐  ┌──────────┐│
│                       │  RDS     │    │  Redis   │  │   S3     ││
│                       │PostgreSQL│    │  Elasti  │  │  Bucket  ││
│                       │  :5432   │    │  Cache   │  │  (PDFs)  ││
│                       └──────────┘    └──────────┘  └──────────┘│
│                              │                                     │
│                              ▼                                     │
│                       ┌──────────┐                                 │
│                       │  RDS     │                                 │
│                       │ Standby  │                                 │
│                       │ (multi-AZ)│                                │
│                       └──────────┘                                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Background Workers (ECS)               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │   OCR    │  │ Matching │  │  QBO     │  │  Audit   │ │   │
│  │  │ Worker   │  │ Worker   │  │  Sync    │  │ Archival │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Event Queue (SQS)                   │   │
│  │  OCR Queue │ Match Queue │ QBO Queue │ Alert Queue     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    InvoiceMatch AI Components                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INGESTION LAYER                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Email Parser │  │  PDF Upload  │  │   Portal     │         │
│  │   (Lambda)   │  │   (React)    │  │   Scraper    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                 │                  │                  │
│         └─────────────────┴──────────────────┘                  │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              S3 Bucket (Raw Invoices)                   │   │
│  │           (Trigger → SQS OCR Queue)                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  PROCESSING LAYER                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ OCR Worker   │─▶│ LLM Worker   │─▶│ Match Worker │         │
│  │ (Textract/   │  │ (Claude      │  │ (3-Way       │         │
│  │  Google/     │  │  API)        │  │  Matching)   │         │
│  │  Azure)      │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                 │                  │                  │
│         └─────────────────┴──────────────────┘                  │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           PostgreSQL (Matched Invoices)                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  INTEGRATION LAYER                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   QBO Sync   │  │  Plaid Sync  │  │  Alerting    │         │
│  │   Worker     │  │   Worker     │  │  (Email/     │         │
│  │              │  │              │  │   Slack)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  PRESENTATION LAYER                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │  Exception   │  │   Vendor     │         │
│  │  (React)     │  │  Queue       │  │   Management │         │
│  │              │  │  (React)     │  │   (React)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Architecture

### 5.1 Entity-Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐
│    companies     │       │      users       │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │◀──────│ id (PK)          │
│ name             │  1:N  │ company_id (FK)  │
│ subdomain        │       │ email            │
│ created_at       │       │ role             │
│ updated_at       │       │ created_at       │
└──────────────────┘       └──────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────┐       ┌──────────────────┐
│     vendors      │       │    invoices      │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │◀──────│ id (PK)          │
│ company_id (FK)  │  1:N  │ company_id (FK)  │
│ name             │       │ vendor_id (FK)   │
│ email            │       │ invoice_number   │
│ tier             │       │ amount           │
│ accuracy_score   │       │ date             │
│ format_rules     │       │ due_date         │
│ created_at       │       │ status           │
└──────────────────┘       │ confidence_score │
                           │ pdf_url          │
                           │ created_at       │
                           └──────────────────┘
                                    │
                                    │ 1:N
                                    ▼
                           ┌──────────────────┐
                           │   line_items     │
                           ├──────────────────┤
                           │ id (PK)          │
                           │ invoice_id (FK)  │
                           │ description      │
                           │ quantity         │
                           │ unit_price       │
                           │ amount           │
                           │ gl_code          │
                           └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│bank_transactions │       │  purchase_orders │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ company_id (FK)  │       │ company_id (FK)  │
│ date             │       │ vendor_id (FK)   │
│ amount           │       │ po_number        │
│ payee            │       │ total            │
│ description      │       │ status           │
│ matched_invoice_ │       │ created_at       │
│   id (FK)        │       └──────────────────┘
│ created_at       │
└──────────────────┘

┌──────────────────┐
│   audit_logs     │
├──────────────────┤
│ id (PK)          │
│ company_id (FK)  │
│ user_id (FK)     │
│ action           │
│ resource_type    │
│ resource_id      │
│ before (JSONB)   │
│ after (JSONB)    │
│ ip_address       │
│ created_at       │
└──────────────────┘
```

### 5.2 Database Schema (PostgreSQL)

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies
CREATE TABLE companies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  subdomain VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users (with RLS)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(company_id, email)
);

-- Vendors
CREATE TABLE vendors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  tier VARCHAR(10) DEFAULT 'B' CHECK (tier IN ('A', 'B', 'C', 'D')),
  accuracy_score DECIMAL(5,2) DEFAULT 0.0,
  format_rules JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Invoices
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  vendor_id UUID REFERENCES vendors(id),
  invoice_number VARCHAR(100),
  amount DECIMAL(12,2) NOT NULL,
  date DATE NOT NULL,
  due_date DATE,
  status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'matched', 'approved', 'rejected', 'posted')),
  confidence_score DECIMAL(5,2),
  pdf_url VARCHAR(500),
  matched_bank_tx_id UUID,
  matched_po_id UUID,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Line Items
CREATE TABLE line_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
  description TEXT,
  quantity DECIMAL(10,2),
  unit_price DECIMAL(12,2),
  amount DECIMAL(12,2),
  gl_code VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Bank Transactions
CREATE TABLE bank_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  amount DECIMAL(12,2) NOT NULL,
  payee VARCHAR(255),
  description TEXT,
  matched_invoice_id UUID REFERENCES invoices(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Purchase Orders
CREATE TABLE purchase_orders (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
  vendor_id UUID REFERENCES vendors(id),
  po_number VARCHAR(100) NOT NULL,
  total DECIMAL(12,2),
  status VARCHAR(50) DEFAULT 'open' CHECK (status IN ('open', 'closed', 'cancelled')),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(company_id, po_number)
);

-- Audit Logs (append-only)
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
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
CREATE INDEX idx_invoices_company ON invoices(company_id, status);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_company ON audit_logs(company_id, created_at);
CREATE INDEX idx_bank_transactions_date ON bank_transactions(date);
CREATE INDEX idx_bank_transactions_company ON bank_transactions(company_id, date);

-- Row-Level Security (RLS)
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE line_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE bank_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchase_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies (example for invoices)
CREATE POLICY company_isolation ON invoices
  FOR ALL
  USING (company_id = current_setting('app.current_company_id')::UUID);

-- Append-only constraint for audit_logs
CREATE OR REPLACE FUNCTION audit_logs_append_only()
RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'UPDATE' OR TG_OP = 'DELETE') THEN
    RAISE EXCEPTION 'Audit logs are append-only';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_logs_append_only_trigger
  BEFORE UPDATE OR DELETE ON audit_logs
  FOR EACH ROW
  EXECUTE FUNCTION audit_logs_append_only();
```

### 5.3 Data Volume Estimates

| Entity | Monthly Growth | Year 1 Total | Storage (Year 1) |
|--------|----------------|--------------|------------------|
| Companies | 50 | 600 | 50 KB |
| Users | 150 | 1,800 | 200 KB |
| Vendors | 500 | 6,000 | 2 MB |
| Invoices | 10,000 | 120,000 | 500 MB (metadata) |
| Line Items | 50,000 | 600,000 | 200 MB |
| Bank Transactions | 10,000 | 120,000 | 50 MB |
| Purchase Orders | 2,000 | 24,000 | 20 MB |
| Audit Logs | 100,000 | 1,200,000 | 2 GB |
| **Total (PostgreSQL)** | | | **~3 GB** |
| PDFs (S3) | 10,000 × 500KB | 60 GB | 60 GB |
| Audit Archive (Glacier) | - | 10 GB (compressed) | 10 GB |

---

## 6. API Architecture

### 6.1 API Gateway Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                             │
│                    (Application Load Balancer)                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Middleware Stack                     │   │
│  │  CORS → Authentication → Rate Limiting → Logging        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      Routers                            │   │
│  │  /auth  /invoices  /vendors  /matching  /qbo  /audit    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Service Layer                         │   │
│  │  InvoiceService, MatchingService, QBOService, etc.      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Data Access Layer                     │   │
│  │  SQLAlchemy ORM, Redis Cache, S3 Client                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 API Endpoints (OpenAPI 3.0)

```yaml
openapi: 3.0.0
info:
  title: InvoiceMatch AI API
  version: 1.0.0
  description: Invoice reconciliation automation API

servers:
  - url: https://api.invoicematch.ai/v1

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

paths:
  /auth/login:
    post:
      summary: User login
      tags: [Auth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email: { type: string, format: email }
                password: { type: string }
      responses:
        200:
          description: JWT token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }
                  refresh_token: { type: string }

  /invoices:
    get:
      summary: List invoices
      tags: [Invoices]
      security: [bearerAuth]
      parameters:
        - name: status
          in: query
          schema: { type: string, enum: [pending, matched, approved, rejected, posted] }
        - name: vendor_id
          in: query
          schema: { type: string, format: uuid }
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 50, maximum: 100 }
      responses:
        200:
          description: List of invoices
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items: { $ref: '#/components/schemas/Invoice' }
                  total: { type: integer }
                  page: { type: integer }

    post:
      summary: Upload invoice
      tags: [Invoices]
      security: [bearerAuth]
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        201:
          description: Invoice uploaded
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Invoice' }

  /invoices/{id}:
    get:
      summary: Get invoice detail
      tags: [Invoices]
      security: [bearerAuth]
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        200:
          description: Invoice detail
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Invoice' }

  /invoices/{id}/approve:
    post:
      summary: Approve invoice
      tags: [Invoices]
      security: [bearerAuth]
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        200:
          description: Invoice approved
          content:
            application/json:
              schema: { $ref: '#/components/schemas/StatusResponse' }

  /invoices/{id}/reject:
    post:
      summary: Reject invoice
      tags: [Invoices]
      security: [bearerAuth]
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                reason: { type: string }
      responses:
        200:
          description: Invoice rejected

  /vendors:
    get:
      summary: List vendors
      tags: [Vendors]
      security: [bearerAuth]
      responses:
        200:
          description: List of vendors

  /matching/suggest:
    post:
      summary: Get match suggestions
      tags: [Matching]
      security: [bearerAuth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                invoice_id: { type: string, format: uuid }
      responses:
        200:
          description: Match suggestions
          content:
            application/json:
              schema:
                type: object
                properties:
                  suggestions:
                    type: array
                    items:
                      type: object
                      properties:
                        type: { type: string, enum: [bank_transaction, purchase_order] }
                        id: { type: string, format: uuid }
                        confidence: { type: number, minimum: 0, maximum: 100 }

  /integrations/quickbooks/sync:
    post:
      summary: Sync QuickBooks data
      tags: [Integrations]
      security: [bearerAuth]
      responses:
        200:
          description: Sync completed

  /audit-logs:
    get:
      summary: Export audit logs
      tags: [Audit]
      security: [bearerAuth]
      parameters:
        - name: start_date
          in: query
          required: true
          schema: { type: string, format: date }
        - name: end_date
          in: query
          required: true
          schema: { type: string, format: date }
      responses:
        200:
          description: Audit log export (CSV)
          content:
            text/csv:
              schema:
                type: string

components:
  schemas:
    Invoice:
      type: object
      properties:
        id: { type: string, format: uuid }
        vendor_id: { type: string, format: uuid }
        invoice_number: { type: string }
        amount: { type: number, format: decimal }
        date: { type: string, format: date }
        status: { type: string }
        confidence_score: { type: number }
        created_at: { type: string, format: date-time }

    StatusResponse:
      type: object
      properties:
        status: { type: string }
        message: { type: string }
```

---

## 7. Infrastructure Architecture

### 7.1 AWS Resources

| Resource | Service | Configuration | Purpose |
|----------|---------|---------------|---------|
| **VPC** | EC2 | 10.0.0.0/16, 3 AZs | Network isolation |
| **Public Subnets** | EC2 | 10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24 | ALB, NAT Gateway |
| **Private Subnets** | EC2 | 10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24 | ECS, RDS, ElastiCache |
| **ALB** | ELB | Application Load Balancer, HTTPS | Traffic distribution |
| **ECS Cluster** | ECS | Fargate, 3 tasks (API), 2 tasks (Frontend) | Container orchestration |
| **RDS** | RDS | PostgreSQL 15, db.r6g.large, multi-AZ | Primary database |
| **ElastiCache** | ElastiCache | Redis 7, cache.r6g.medium | Session cache, OCR cache |
| **S3** | S3 | Standard (PDFs), Glacier (audit archive) | File storage |
| **SQS** | SQS | 4 queues (OCR, Match, QBO, Alert) | Async processing |
| **Lambda** | Lambda | 3 functions (email parsing, OCR trigger, archival) | Event-driven processing |
| **CloudFront** | CloudFront | CDN distribution | Static assets, PDF previews |
| **Secrets Manager** | Secrets Manager | KMS-encrypted secrets | API keys, DB credentials |
| **CloudWatch** | CloudWatch | Logs, Metrics, Alarms | Monitoring |

### 7.2 ECS Task Definitions

**API Task** (FastAPI):
```json
{
  "family": "invoicematch-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/invoicematch-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        { "name": "DATABASE_URL", "value": "postgresql://..." },
        { "name": "REDIS_URL", "value": "redis://..." },
        { "name": "AWS_TEXTRACT_REGION", "value": "us-east-1" }
      ],
      "secrets": [
        { "name": "ANTHROPIC_API_KEY", "valueFrom": "arn:aws:secretsmanager:..." },
        { "name": "QBO_CLIENT_SECRET", "valueFrom": "arn:aws:secretsmanager:..." }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/invoicematch-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      }
    }
  ]
}
```

**OCR Worker Task**:
```json
{
  "family": "invoicematch-ocr-worker",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "ocr-worker",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/invoicematch-ocr-worker:latest",
      "command": ["python", "-m", "workers.ocr_consumer"],
      "environment": [
        { "name": "SQS_QUEUE_URL", "value": "https://sqs.us-east-1.amazonaws.com/.../ocr-queue" },
        { "name": "TEXTRACT_REGION", "value": "us-east-1" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/invoicematch-ocr-worker",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "worker"
        }
      }
    }
  ]
}
```

### 7.3 Infrastructure as Code (Terraform)

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "invoicematch-vpc"
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier = "invoicematch-db"
  engine = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.large"
  allocated_storage = 100
  storage_type = "gp3"
  multi_az = true
  
  db_name = "invoicematch"
  username = "invoicematch"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
  
  backup_retention_period = 30
  backup_window = "03:00-04:00"
  maintenance_window = "Mon:04:00-Mon:05:00"

  tags = {
    Name = "invoicematch-db"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "invoicematch-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# S3 Bucket for PDFs
resource "aws_s3_bucket" "invoices" {
  bucket = "invoicematch-invoices-${var.environment}"
  
  lifecycle_rule {
    id = "archive-old-pdfs"
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 2555  # 7 years
    }
  }
}

# SQS Queues
resource "aws_sqs_queue" "ocr_queue" {
  name = "invoicematch-ocr-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds = 86400
}

resource "aws_sqs_queue" "match_queue" {
  name = "invoicematch-match-queue"
  visibility_timeout_seconds = 60
}

resource "aws_sqs_queue" "qbo_queue" {
  name = "invoicematch-qbo-queue"
  visibility_timeout_seconds = 120
}
```

---

## 8. Security Architecture

### 8.1 Authentication & Authorization

**Authentication Flow**:
```
User → Login (email/password) → bcrypt verification
     → JWT issued (7-day expiry)
     → JWT stored in HttpOnly cookie
     → Subsequent requests: JWT validated in middleware
```

**Authorization**:
- **RBAC**: Admin, User, Viewer roles
- **Company Isolation**: Row-level security (RLS) in PostgreSQL
- **API Scoping**: All queries filtered by `company_id`

### 8.2 Data Protection

| Data Type | Encryption at Rest | Encryption in Transit |
|-----------|-------------------|----------------------|
| Database | PostgreSQL TDE (AES-256) | TLS 1.3 |
| S3 (PDFs) | S3 SSE-S3 (AES-256) | TLS 1.3 |
| Secrets | AWS Secrets Manager (KMS) | TLS 1.3 |
| Vendor Credentials | AES-256-GCM (application-level) | TLS 1.3 |
| Session Tokens | Redis encryption | TLS 1.3 |

### 8.3 Compliance

| Standard | Requirement | Implementation |
|----------|-------------|----------------|
| **SOC 2 Type II** | Access controls, encryption, monitoring | RBAC, encryption, CloudWatch |
| **GDPR** | Data deletion, export, consent | User data export API, deletion workflow |
| **IRS** | 7-year audit log retention | S3 Glacier archival, automated deletion |
| **PCI-DSS** | Not applicable (no CC storage) | N/A |

---

## 9. Performance Architecture

### 9.1 Caching Strategy

**Redis Cache Layers**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        Redis Cache                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Session Store (TTL: 7 days)                                   │
│  Key: session:{user_id} → {user_data, company_id, role}        │
│                                                                 │
│  OCR Cache (TTL: 30 days)                                      │
│  Key: ocr:{pdf_hash} → {ocr_text, confidence, provider}        │
│                                                                 │
│  Vendor Cache (TTL: 1 hour)                                    │
│  Key: vendor:{vendor_id} → {vendor_data, format_rules}         │
│                                                                 │
│  QBO Cache (TTL: 5 minutes)                                    │
│  Key: qbo:vendors:{company_id} → {vendor_list}                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Database Optimization

**Indexing Strategy**:
```sql
-- Composite indexes for common queries
CREATE INDEX idx_invoices_company_status ON invoices(company_id, status);
CREATE INDEX idx_invoices_vendor_status ON invoices(vendor_id, status, created_at);
CREATE INDEX idx_bank_transactions_company_date ON bank_transactions(company_id, date DESC);

-- Partial indexes for status filtering
CREATE INDEX idx_invoices_pending ON invoices(company_id) WHERE status = 'pending';
CREATE INDEX idx_invoices_exceptions ON invoices(company_id) WHERE status IN ('matched', 'approved');

-- Covering indexes for list queries
CREATE INDEX idx_invoices_list ON invoices(company_id, status, created_at) INCLUDE (vendor_id, amount, confidence_score);
```

**Query Optimization**:
- Use `EXPLAIN ANALYZE` for slow queries (>100ms)
- Avoid N+1 queries (use SQLAlchemy `joinedload`)
- Paginate large result sets (max 100 per page)
- Use materialized views for complex aggregations

### 9.3 Load Testing Targets

| Scenario | Target | Measurement |
|----------|--------|-------------|
| **API Latency** | <500ms | 95th percentile (all endpoints) |
| **OCR Processing** | <30s | 95th percentile (per invoice) |
| **Matching** | <5s | 95th percentile (per invoice) |
| **QBO Sync** | <10s | 95th percentile (per bill) |
| **Concurrent Users** | 500 | Simultaneous active users |
| **Throughput** | 10K invoices/hour | Peak load (month-end) |

---

## 10. Monitoring & Observability

### 10.1 Metrics (CloudWatch)

**Business Metrics**:
- `invoicematch.invoices.received` (count/day)
- `invoicematch.invoices.auto_matched` (count/day, %)
- `invoicematch.invoices.exceptions` (count/day)
- `invoicematch.matching.confidence_avg` (average confidence score)
- `invoicematch.qbo.sync_success_rate` (%)

**Technical Metrics**:
- `api.latency.p95` (ms)
- `ocr.processing_time.p95` (ms)
- `database.connections.active` (count)
- `cache.hit_rate` (%)
- `sqs.queue.depth` (count)
- `error.rate` (%)

### 10.2 Logging

**Log Structure** (JSON):
```json
{
  "timestamp": "2026-08-06T14:30:22Z",
  "level": "INFO",
  "service": "invoicematch-api",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "user_001",
  "company_id": "company_001",
  "action": "invoice.upload",
  "resource_type": "invoice",
  "resource_id": "inv_12345",
  "latency_ms": 234,
  "status_code": 201
}
```

**Log Aggregation**:
- CloudWatch Logs → Elasticsearch (OpenSearch)
- Retention: 30 days (hot), 7 years (audit archive)
- Alerting: Error rate >5% → PagerDuty

### 10.3 Distributed Tracing

**X-Ray Integration**:
```python
from aws_xray_sdk.core import xray_recorder

@xray_recorder.capture('ocr_processing')
def process_ocr(pdf_url: str) -> dict:
    # ... OCR logic
    return ocr_result
```

**Trace Propagation**:
- All API requests include `X-Amzn-Trace-Id` header
- Trace context propagated to SQS, Lambda, RDS
- Trace visualization in AWS X-Ray console

---

## 11. Disaster Recovery

### 11.1 Backup Strategy

| Resource | Backup Method | Frequency | Retention |
|----------|---------------|-----------|-----------|
| RDS PostgreSQL | Automated snapshots | Daily | 30 days |
| S3 (PDFs) | Versioning + Cross-Region Replication | Real-time | 7 years |
| Secrets Manager | Built-in redundancy | N/A | Indefinite |
| Terraform State | S3 backend with versioning | On every apply | Indefinite |

### 11.2 Recovery Procedures

**RDS Failure**:
1. Automatic failover to standby (multi-AZ)
2. DNS update (RDS endpoint)
3. Application reconnects automatically
4. **RTO**: <5 minutes, **RPO**: <1 hour

**S3 Data Loss**:
1. Restore from versioning (accidental deletion)
2. Restore from cross-region replica (region failure)
3. **RTO**: <1 hour, **RPO**: 0 (versioning)

**Region Failure**:
1. DNS failover to us-west-2 (Route53 health checks)
2. RDS restore from cross-region snapshot
3. ECS deploy to us-west-2 cluster
4. **RTO**: 4 hours, **RPO**: 1 hour

---

## 12. Cost Estimates (Monthly)

| Resource | Configuration | Monthly Cost |
|----------|---------------|--------------|
| **ECS Fargate** | 5 tasks (2 vCPU, 4GB) × 730 hours | $300 |
| **RDS PostgreSQL** | db.r6g.large, multi-AZ | $500 |
| **ElastiCache Redis** | cache.r6g.medium | $150 |
| **S3** | 60 GB Standard + 10 GB Glacier | $10 |
| **CloudFront** | 1 TB data transfer | $100 |
| **SQS** | 1M requests/month | $5 |
| **Lambda** | 1M invocations/month | $20 |
| **AWS Textract** | 100K pages/month @ $1.50/1000 | $150 |
| **Google Vision** | 10K pages/month @ $1.50/1000 | $15 |
| **Anthropic Claude** | 100K invoices/month @ $0.01 | $1,000 |
| **Plaid** | 500 companies @ $0.10/company | $50 |
| **QuickBooks API** | Free (developer tier) | $0 |
| **CloudWatch** | Logs + Metrics + Alarms | $100 |
| **Total** | | **$2,400/month** |

**Cost per Invoice** (at 100K invoices/month): $0.024

---

## 13. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **OCR accuracy <99%** | Medium | High | Multi-provider fallback, manual correction loop |
| **QBO API rate limits** | Low | Medium | Queue + retry, batch processing |
| **Vendor portal CAPTCHA** | High | Low | Alert user for manual resolution |
| **LLM extraction errors** | Medium | Medium | Confidence scores, human review |
| **Data breach** | Low | Critical | Encryption, RBAC, audit logging, SOC 2 |
| **AWS region failure** | Low | High | Multi-region DR plan, cross-region backups |
| **QuickBooks builds competitor** | Low | High | Differentiate on format agnosticism, speed |

---

## 14. Future Considerations

### 14.1 Scalability Enhancements

**Horizontal Scaling**:
- ECS auto-scaling based on SQS queue depth
- RDS read replicas for reporting queries
- S3 Transfer Acceleration for global users

**Database Sharding** (at 1M+ invoices/month):
- Shard by `company_id` (hash-based)
- Use Citus (PostgreSQL extension) for distributed queries

### 14.2 Feature Extensions

**V2 (Months 5-8)**:
- Xero integration
- Multi-entity support
- Advanced reporting
- Mobile app (iOS, Android)

**V3 (Months 9-12)**:
- International (multi-currency, VAT)
- AP automation (payment execution)
- Fraud detection (anomaly detection)
- Custom ERP integrations (NetSuite, SAP)

---

**Architecture Document Complete** ✅

**Next Steps**:
1. Review with engineering team
2. Validate cost estimates
3. Set up AWS account and infrastructure
4. Implement CI/CD pipeline
5. Start Phase 1: Foundation

---

*Document Version: 1.0*  
*Created: 2026-08-06*  
*Review Date: 2026-09-06*
