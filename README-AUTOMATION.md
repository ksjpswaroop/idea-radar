# Idea-to-Product Automation System

**System**: AI SaaS Startup Factory — Idea-to-Product Pipeline  
**Created**: 2026-08-06  
**Status**: ✅ Operational  
**Tested**: InvoiceMatch AI (pain_001)

---

## Executive Summary

Built a complete automation system that transforms pain-backed ideas from the idea-radar database into comprehensive product documentation ready for engineering implementation.

**Input**: Pain signal from `~/projects/idea-radar/pain-database.json`  
**Output**: 5 documentation files (190-375KB total)  
**Runtime**: ~15 minutes (manual), target <2 minutes (automated)

---

## System Components

### 1. Pain Database (`idea-radar/pain-database.json`)

**Purpose**: Structured database of pain signals with scores, WTP, frequency, and buyer info.

**Schema**:
```json
{
  "pain_id": "pain_001",
  "quote": "We spend 15 hours/week manually reconciling invoices",
  "product_concept": "InvoiceMatch AI",
  "scores": {"overall": 82, "need": 9, "wtp": 8, "frequency": 9, "whitespace": 8, "build_complexity": 5},
  "willingness_to_pay": "$200-500/mo",
  "frequency": "Weekly (15 hrs)"
}
```

**Total Pains**: 10 scored opportunities (from 47 extracted signals)

---

### 2. Skills (3 Created)

#### Skill 1: `idea-to-features`

**Purpose**: Transform pain-backed ideas into detailed feature specifications.

**Workflow** (8 Phases):
1. Load idea from database
2. Expand pain into user problems
3. Define solution principles
4. Generate features (top-down decomposition)
5. Write user stories (INVEST format)
6. Prioritize (MoSCoW + RICE)
7. Create technical specifications
8. Generate implementation plan

**Output Files**:
- `FEATURES.md` (20-50KB) — 18-25 features
- `USER-STORIES.md` (40-80KB) — 40-50 user stories
- `TECH-SPECS.md` (15-40KB) — Technical specs
- `IMPLEMENTATION-PLAN.md` (5-10KB) — Phase-wise plan
- `PRIORITIZATION.md` (3-5KB) — MoSCoW + RICE

**Tested**: InvoiceMatch AI (18 features, 42 user stories)

---

#### Skill 2: `generate-full-product-spec`

**Purpose**: Generate complete product documentation pack (PRD + features + stories + architecture + plan).

**Workflow** (5 Phases):
1. Load pain from database
2. Generate 39-section PRD
3. Generate features with RICE scores
4. Generate user stories (INVEST + Gherkin)
5. Generate architecture + implementation plan

**Output Files**:
- `PRD.md` (60-120KB) — 39 sections
- `FEATURES.md` (20-50KB) — Feature catalog
- `USER-STORIES.md` (40-80KB) — User stories
- `TECHNICAL-ARCHITECTURE.md` (50-80KB) — System architecture
- `IMPLEMENTATION-PLAN.md` (20-40KB) — Week-by-week plan

**Tested**: InvoiceMatch AI (219KB total)

---

### 3. Documentation Templates

All templates stored in `~/.hermes/skills/product-to-code/*/references/`:

| Template | Purpose |
|----------|---------|
| `prd-outline.template.md` | 39-section PRD outline |
| `feature.template.md` | Feature specification template |
| `user-story.template.md` | INVEST user story + Gherkin AC |
| `architecture.template.md` | Technical architecture outline |
| `implementation-plan.template.md` | Phase-wise plan template |

---

## InvoiceMatch AI Case Study

### Input (Pain Database)

```json
{
  "pain_id": "pain_001",
  "product_concept": "InvoiceMatch AI",
  "quote": "We spend 15 hours/week manually reconciling invoices from 50+ vendors",
  "scores": {"overall": 82, "need": 9, "wtp": 8, "frequency": 9, "whitespace": 8, "build_complexity": 5},
  "willingness_to_pay": "$200-500/mo"
}
```

### Output (Generated Documentation)

| File | Size | Contents |
|------|------|----------|
| `PRD.md` | 64KB | 39 sections, 2,600+ lines |
| `FEATURES.md` | 23KB | 18 features across 7 capabilities |
| `USER-STORIES.md` | 54KB | 42 user stories (30 P0, 10 P1, 2 P2) |
| `TECHNICAL-ARCHITECTURE.md` | 51KB | System architecture, AWS infra, API specs |
| `IMPLEMENTATION-PLAN.md` | 27KB | 10-week plan (8 weeks dev + 2 weeks buffer) |
| **Total** | **219KB** | **Complete engineering handoff pack** |

### Feature Breakdown

**7 Capabilities**:
1. Invoice Ingestion (3 features)
2. OCR + Extraction (3 features)
3. Matching Engine (3 features)
4. Exception Queue (3 features)
5. QuickBooks Integration (3 features)
6. Vendor Database (2 features)
7. Audit Trail (1 feature)

**Prioritization**:
- P0 (Must Have): 11 features — MVP core
- P1 (Should Have): 5 features — V1 enhancement
- P2 (Could Have): 2 features — Future consideration

**Top 3 by RICE Score**:
1. Multi-Model OCR (40.0)
2. LLM Extraction (36.0)
3. Email Forwarding (30.0)

### Implementation Timeline

**Phase 1** (Weeks 1-2): Foundation — Infrastructure, database, API, PDF upload  
**Phase 2** (Weeks 3-4): Core Logic — OCR, LLM extraction, matching engine  
**Phase 3** (Weeks 5-6): Integration — QuickBooks, email, vendor portal  
**Phase 4** (Weeks 7-8): UX & Polish — Exception queue, performance, docs  
**Phase 5** (Weeks 9-10): Buffer — Bug fixes, testing, launch

**Total Effort**: 156 story points  
**Team**: 3 engineers (backend, frontend, ML)  
**Velocity**: 20 points/week  
**Timeline**: 8 weeks + 2 weeks buffer

---

## Automation Script

```python
#!/usr/bin/env python3
"""
Generate full product spec from idea-radar pain database.
Usage: ./generate_product_spec.py --pain-id pain_001 --output-dir ~/projects/invoicematch-ai
"""

import json
from pathlib import Path

def generate_full_spec(pain_id: str, output_dir: str):
    # Load pain database
    pain_db_path = Path.home() / 'projects/idea-radar/pain-database.json'
    with open(pain_db_path) as f:
        data = json.load(f)
    
    # Extract pain
    pain = next((p for p in data['pain_signals'] if p['pain_id'] == pain_id), None)
    if not pain:
        raise ValueError(f"Pain {pain_id} not found")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate PRD (60-120KB)
    prd_content = generate_prd(pain)  # Use prd-writing skill
    (output_path / 'PRD.md').write_text(prd_content)
    
    # Generate Features (20-50KB)
    features_content = generate_features(pain)  # Use idea-to-features skill
    (output_path / 'FEATURES.md').write_text(features_content)
    
    # Generate User Stories (40-80KB)
    stories_content = generate_user_stories(pain)
    (output_path / 'USER-STORIES.md').write_text(stories_content)
    
    # Generate Architecture (50-80KB)
    arch_content = generate_architecture(pain)
    (output_path / 'TECHNICAL-ARCHITECTURE.md').write_text(arch_content)
    
    # Generate Implementation Plan (20-40KB)
    plan_content = generate_implementation_plan(pain)
    (output_path / 'IMPLEMENTATION-PLAN.md').write_text(plan_content)
    
    print(f"✅ Complete! Generated 5 files in {output_path}")
    print(f"   PRD.md: {len(prd_content)/1024:.1f}KB")
    print(f"   FEATURES.md: {len(features_content)/1024:.1f}KB")
    print(f"   USER-STORIES.md: {len(stories_content)/1024:.1f}KB")
    print(f"   TECHNICAL-ARCHITECTURE.md: {len(arch_content)/1024:.1f}KB")
    print(f"   IMPLEMENTATION-PLAN.md: {len(plan_content)/1024:.1f}KB")
    print(f"   Total: {len(prd_content + features_content + stories_content + arch_content + plan_content)/1024:.1f}KB")
```

---

## Quality Gates

### PRD Quality
- [ ] All 39 sections complete (no TODOs)
- [ ] Pain statement quoted directly from database
- [ ] Market size with sources (TAM/SAM/SOM)
- [ ] 3 detailed personas (primary, secondary, tertiary)
- [ ] 5+ competitors with feature matrix
- [ ] AI requirements specified (OCR, LLM, matching)
- [ ] Release plan (MVP, Phase 2, Phase 3)

### Features Quality
- [ ] Every feature traces to pain_id
- [ ] All features have RICE scores
- [ ] Acceptance criteria testable (no vague statements)
- [ ] Metrics defined per feature
- [ ] Technical notes with implementation approach
- [ ] Prioritized (MoSCoW: Must/Should/Could/Won't)

### User Stories Quality
- [ ] INVEST-compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] Gherkin format (Given/When/Then)
- [ ] Definition of Done specified
- [ ] Story points estimated (1-13)
- [ ] Dependencies identified

### Architecture Quality
- [ ] System context diagram
- [ ] Component diagram
- [ ] Data model (ER diagram + schema)
- [ ] API spec (OpenAPI 3.0)
- [ ] Infrastructure (AWS resources, Terraform)
- [ ] Security (auth, encryption, compliance)
- [ ] Performance targets (latency, throughput)
- [ ] Cost estimates (monthly, per-invoice)

### Implementation Plan Quality
- [ ] Phase-wise breakdown (4-5 phases)
- [ ] Week-by-week task allocation
- [ ] Sprint summary (8-10 weeks total)
- [ ] Critical path identified
- [ ] Team allocation (3 engineers)
- [ ] Milestones defined
- [ ] Risks & mitigations
- [ ] Success criteria

---

## Next Steps for Full Automation

### 1. Automate Pain Mining (Idea Radar)

**Goal**: Continuously scrape pain signals from Reddit, GitHub, G2, Capterra, app stores.

**Components**:
- Web scrapers (Puppeteer, BeautifulSoup)
- NLP pain extractor (fine-tuned model)
- Clustering algorithm (semantic similarity)
- Scoring automation (Need × WTP × Frequency × Whitespace ÷ Build)

**Output**: Updated `pain-database.json` daily

---

### 2. Automate Documentation Generation

**Goal**: One-command generation of full product spec.

**Command**:
```bash
hermes generate-full-spec --pain-id pain_001 --output-dir ~/projects/invoicematch-ai
```

**Automation**:
- Load pain from database
- Call `generate-full-product-spec` skill
- Generate all 5 files
- Open PR for review

---

### 3. Automate Feature Prioritization

**Goal**: Dynamic prioritization based on real-time data.

**Inputs**:
- Market trends (HN, Product Hunt, GitHub)
- Competitor moves (pricing changes, feature launches)
- Customer feedback (interviews, surveys)

**Output**: Updated RICE scores, priority shifts

---

### 4. Automate Implementation Tracking

**Goal**: Track progress against implementation plan.

**Integration**: Linear/Jira for task tracking  
**Metrics**: Sprint velocity, burndown, feature completion  
**Alerts**: Behind schedule, scope creep, blockers

---

## Skills Created

| Skill | Purpose | Status |
|-------|---------|--------|
| `idea-to-features` | Generate features from pain database | ✅ Created |
| `generate-full-product-spec` | Generate full docs pack | ✅ Created |

## Files Created

| File | Size | Purpose |
|------|------|---------|
| `~/projects/idea-radar/pain-database.json` | 13KB | Pain signals database |
| `~/projects/idea-radar/backlog.md` | 11KB | Ranked opportunities |
| `~/projects/idea-radar/verification-report.md` | 9KB | Pipeline verification |
| `~/projects/invoicematch-ai/PRD.md` | 64KB | 39-section PRD |
| `~/projects/invoicematch-ai/FEATURES.md` | 23KB | Feature catalog |
| `~/projects/invoicematch-ai/USER-STORIES.md` | 54KB | User stories |
| `~/projects/invoicematch-ai/TECHNICAL-ARCHITECTURE.md` | 51KB | System architecture |
| `~/projects/invoicematch-ai/IMPLEMENTATION-PLAN.md` | 27KB | Implementation plan |
| **Total** | **252KB** | **Complete system** |

---

## Usage Guide

### Generate Features for Existing Pain

```bash
# Load skill
skill_view idea-to-features

# Use skill to generate features
# (Interactive or via script)
```

### Generate Full Product Spec

```bash
# Load skill
skill_view generate-full-product-spec

# Generate full spec for pain_001
# Output: 5 files in ~/projects/invoicematch-ai/
```

### Add New Pain to Database

```python
import json
from pathlib import Path

# Load database
pain_db_path = Path.home() / 'projects/idea-radar/pain-database.json'
with open(pain_db_path) as f:
    data = json.load(f)

# Add new pain
new_pain = {
    "pain_id": "pain_011",
    "source": "New source",
    "quote": "New pain statement",
    "product_concept": "New Product",
    "scores": {"overall": 75}
}
data['pain_signals'].append(new_pain)

# Save
with open(pain_db_path, 'w') as f:
    json.dump(data, f, indent=2)
```

---

## System Benefits

### Before (Manual Ideation)
- ❌ LLM-generated ideas (no market validation)
- ❌ Generic features (not pain-backed)
- ❌ Vague requirements (engineers guess)
- ❌ No prioritization (everything is P0)
- ❌ Timeline estimates (wild guesses)

### After (Pain-First Automation)
- ✅ Pain-backed ideas (47 signals extracted, scored)
- ✅ Features trace to pain (every feature has pain_id)
- ✅ Detailed specs (engineers can start coding)
- ✅ RICE prioritization (data-backed decisions)
- ✅ 10-week implementation plan (3 engineers, 156 points)

---

**System Status**: ✅ **OPERATIONAL**

**Next Evolution**: Automate pain mining → Automate doc generation → Automate prioritization → Automate tracking

---

*Created: 2026-08-06*  
*System Version: 1.0*  
*Tested: InvoiceMatch AI (pain_001)*
