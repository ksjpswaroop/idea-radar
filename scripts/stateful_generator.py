#!/usr/bin/env python3
"""
Stateful Document Generator with Progress Tracking

Generates large documents recursively with:
- Stateful tracking (resume from failures)
- Chunked generation (not all at once)
- Stitching mechanism (combine chunks)
- Observability (logs, metrics, status)
- Error recovery (checkpoint-based resume)

Usage:
    python3 stateful_generator.py --pain-id pain_001 --output-dir ~/projects/test
"""

import argparse
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class GenerationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class DocumentSection:
    """Represents a section/chunk of a document."""
    
    def __init__(self, section_id: str, name: str, content: str = ""):
        self.section_id = section_id
        self.name = name
        self.content = content
        self.status = GenerationStatus.PENDING
        self.attempts = 0
        self.last_error = None
        self.started_at = None
        self.completed_at = None
        self.checksum = None
    
    def to_dict(self) -> dict:
        return {
            "section_id": self.section_id,
            "name": self.name,
            "content": self.content,
            "status": self.status.value,
            "attempts": self.attempts,
            "last_error": str(self.last_error) if self.last_error else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "checksum": self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        section = cls(
            section_id=data["section_id"],
            name=data["name"],
            content=data.get("content", "")
        )
        section.status = GenerationStatus(data.get("status", "pending"))
        section.attempts = data.get("attempts", 0)
        section.last_error = data.get("last_error")
        section.started_at = datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None
        section.completed_at = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        section.checksum = data.get("checksum")
        return section


class GenerationState:
    """Tracks the state of document generation."""
    
    def __init__(self, pain_id: str, output_dir: str):
        self.pain_id = pain_id
        self.output_dir = Path(output_dir)
        self.state_file = self.output_dir / ".generation_state.json"
        self.log_file = self.output_dir / ".generation.log"
        
        self.started_at = datetime.now()
        self.completed_at = None
        self.status = GenerationStatus.PENDING
        self.sections: Dict[str, DocumentSection] = {}
        self.metadata = {
            "pain_id": pain_id,
            "output_dir": str(output_dir),
            "total_sections": 0,
            "completed_sections": 0,
            "failed_sections": 0,
            "retry_count": 0,
            "total_size_bytes": 0
        }
        
        # Load existing state if available
        if self.state_file.exists():
            self.load()
    
    def add_section(self, section_id: str, name: str):
        """Add a section to track."""
        self.sections[section_id] = DocumentSection(section_id, name)
        self.metadata["total_sections"] = len(self.sections)
    
    def start_section(self, section_id: str):
        """Mark section as in-progress."""
        if section_id in self.sections:
            self.sections[section_id].status = GenerationStatus.IN_PROGRESS
            self.sections[section_id].started_at = datetime.now()
            self.sections[section_id].attempts += 1
            self.save()
    
    def complete_section(self, section_id: str, content: str):
        """Mark section as completed."""
        if section_id in self.sections:
            section = self.sections[section_id]
            section.content = content
            section.status = GenerationStatus.COMPLETED
            section.completed_at = datetime.now()
            section.checksum = hashlib.sha256(content.encode()).hexdigest()[:16]
            
            self.metadata["completed_sections"] = sum(
                1 for s in self.sections.values() 
                if s.status == GenerationStatus.COMPLETED
            )
            self.save()
    
    def fail_section(self, section_id: str, error: Exception):
        """Mark section as failed."""
        if section_id in self.sections:
            section = self.sections[section_id]
            section.status = GenerationStatus.FAILED
            section.last_error = str(error)
            self.metadata["failed_sections"] = sum(
                1 for s in self.sections.values() 
                if s.status == GenerationStatus.FAILED
            )
            self.save()
    
    def get_pending_sections(self) -> List[str]:
        """Get list of pending or failed section IDs."""
        return [
            section_id for section_id, section in self.sections.items()
            if section.status in [GenerationStatus.PENDING, GenerationStatus.FAILED]
        ]
    
    def get_progress(self) -> dict:
        """Get current progress."""
        total = len(self.sections)
        completed = sum(1 for s in self.sections.values() if s.status == GenerationStatus.COMPLETED)
        failed = sum(1 for s in self.sections.values() if s.status == GenerationStatus.FAILED)
        in_progress = sum(1 for s in self.sections.values() if s.status == GenerationStatus.IN_PROGRESS)
        
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "pending": total - completed - failed - in_progress,
            "percent": (completed / total * 100) if total > 0 else 0
        }
    
    def save(self):
        """Save state to file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        state_data = {
            "pain_id": self.pain_id,
            "output_dir": self.metadata["output_dir"],
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status.value,
            "metadata": self.metadata,
            "sections": {
                section_id: section.to_dict() 
                for section_id, section in self.sections.items()
            }
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    def load(self):
        """Load state from file."""
        with open(self.state_file) as f:
            state_data = json.load(f)
        
        self.started_at = datetime.fromisoformat(state_data["started_at"])
        self.completed_at = datetime.fromisoformat(state_data["completed_at"]) if state_data.get("completed_at") else None
        self.status = GenerationStatus(state_data.get("status", "pending"))
        self.metadata = state_data.get("metadata", {})
        self.sections = {
            section_id: DocumentSection.from_dict(section_data)
            for section_id, section_data in state_data.get("sections", {}).items()
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Write to log file."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        # Also print to console
        print(f"[{level}] {message}")
    
    def mark_complete(self):
        """Mark entire generation as complete."""
        self.status = GenerationStatus.COMPLETED
        self.completed_at = datetime.now()
        self.metadata["total_size_bytes"] = sum(
            len(section.content.encode()) for section in self.sections.values()
            if section.content
        )
        self.save()
    
    def mark_failed(self):
        """Mark entire generation as failed."""
        self.status = GenerationStatus.FAILED
        self.completed_at = datetime.now()
        self.save()


class StatefulDocumentGenerator:
    """Generates documents with stateful tracking."""
    
    # Define document structure with sections
    DOCUMENT_TEMPLATES = {
        "PRD": {
            "sections": [
                ("executive_summary", "Executive Summary"),
                ("strategic_context", "Strategic Context"),
                ("problem_statement", "Problem Statement"),
                ("goals_objectives", "Goals & Objectives"),
                ("personas", "Personas"),
                ("user_research", "User Research"),
                ("scope_definition", "Scope Definition"),
                ("user_journey", "User Journey"),
                ("functional_requirements", "Functional Requirements"),
                ("feature_specifications", "Feature Specifications"),
                ("user_flows", "User Flows"),
                ("screen_requirements", "Screen Requirements"),
                ("ux_requirements", "UX Requirements"),
                ("design_system", "Design System"),
                ("information_architecture", "Information Architecture"),
                ("data_requirements", "Data Requirements"),
                ("database_design", "Database Design"),
                ("api_requirements", "API Requirements"),
                ("ai_requirements", "AI Requirements"),
                ("security", "Security"),
                ("privacy", "Privacy"),
                ("performance", "Performance"),
                ("reliability", "Reliability"),
                ("observability", "Observability"),
                ("integration", "Integration"),
                ("reporting", "Reporting"),
                ("analytics", "Analytics"),
                ("testing", "Testing"),
                ("deployment", "Deployment"),
                ("migration", "Migration"),
                ("release_plan", "Release Plan"),
                ("risk_assessment", "Risk Assessment"),
                ("assumptions", "Assumptions"),
                ("constraints", "Constraints"),
                ("success_metrics", "Success Metrics"),
                ("kpis", "KPIs Dashboard"),
                ("open_questions", "Open Questions"),
                ("appendices", "Appendices"),
                ("ai_agent_architecture", "AI/Agent Architecture"),
            ]
        },
        "FEATURES": {
            "sections": [
                ("capability_1", "Capability 1: Invoice Ingestion"),
                ("capability_2", "Capability 2: OCR + Extraction"),
                ("capability_3", "Capability 3: Matching Engine"),
                ("capability_4", "Capability 4: Exception Queue"),
                ("capability_5", "Capability 5: QuickBooks Integration"),
                ("capability_6", "Capability 6: Vendor Database"),
                ("capability_7", "Capability 7: Audit Trail"),
                ("prioritization_summary", "Prioritization Summary"),
            ]
        },
        "USER_STORIES": {
            "sections": [
                ("stories_p0", "P0 User Stories (Must Have)"),
                ("stories_p1", "P1 User Stories (Should Have)"),
                ("stories_p2", "P2 User Stories (Could Have)"),
                ("sprint_allocation", "Sprint Allocation"),
            ]
        }
    }
    
    def __init__(self, pain_id: str, output_dir: str, max_retries: int = 3):
        self.pain_id = pain_id
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.state = GenerationState(pain_id, output_dir)
        
        # Load pain data
        self.pain_data = self._load_pain_data()
    
    def _load_pain_data(self) -> dict:
        """Load pain data from database."""
        pain_db_path = Path.home() / 'projects/idea-radar/pain-database.json'
        
        if not pain_db_path.exists():
            raise FileNotFoundError(f"Pain database not found at {pain_db_path}")
        
        with open(pain_db_path) as f:
            data = json.load(f)
        
        pain = next((p for p in data['pain_signals'] if p['pain_id'] == self.pain_id), None)
        if not pain:
            raise ValueError(f"Pain {self.pain_id} not found in database")
        
        return pain
    
    def generate_document(self, doc_type: str) -> bool:
        """Generate a complete document with stateful tracking."""
        
        if doc_type not in self.DOCUMENT_TEMPLATES:
            self.state.log(f"Unknown document type: {doc_type}", "ERROR")
            return False
        
        template = self.DOCUMENT_TEMPLATES[doc_type]
        
        # Initialize sections
        for section_id, section_name in template["sections"]:
            self.state.add_section(section_id, section_name)
        
        self.state.log(f"Starting {doc_type} generation for {self.pain_id}")
        self.state.log(f"Total sections: {len(template['sections'])}")
        
        # Generate sections
        all_completed = True
        for section_id, section_name in template["sections"]:
            success = self._generate_section(doc_type, section_id, section_name)
            
            if not success:
                all_completed = False
                self.state.log(f"Section {section_id} failed after {self.max_retries} retries", "ERROR")
        
        # Stitch document
        if all_completed:
            self.state.log(f"Stitching {doc_type} document...")
            stitched_content = self._stitch_document(doc_type)
            
            if stitched_content:
                # Save final document
                output_file = self.output_dir / f"{doc_type}.md"
                output_file.write_text(stitched_content)
                
                self.state.log(f"Saved {doc_type}.md ({len(stitched_content)} bytes)")
                self.state.mark_complete()
                return True
        
        self.state.mark_failed()
        return False
    
    def _generate_section(self, doc_type: str, section_id: str, section_name: str) -> bool:
        """Generate a single section with retry logic."""
        
        section = self.state.sections.get(section_id)
        if not section:
            self.state.log(f"Section {section_id} not found", "ERROR")
            return False
        
        # Skip if already completed
        if section.status == GenerationStatus.COMPLETED:
            self.state.log(f"Section {section_id} already completed, skipping", "INFO")
            return True
        
        # Attempt generation with retries
        for attempt in range(1, self.max_retries + 1):
            self.state.start_section(section_id)
            self.state.log(f"Generating section {section_id} (attempt {attempt}/{self.max_retries})")
            
            try:
                # Generate section content
                content = self._generate_section_content(doc_type, section_id, section_name)
                
                if content:
                    self.state.complete_section(section_id, content)
                    self.state.log(f"Section {section_id} completed ({len(content)} bytes)")
                    return True
                else:
                    raise Exception("Empty content generated")
            
            except Exception as e:
                self.state.fail_section(section_id, e)
                self.state.log(f"Section {section_id} failed: {str(e)}", "ERROR")
                
                if attempt < self.max_retries:
                    self.state.log(f"Retrying section {section_id} in 2 seconds...", "WARN")
                    time.sleep(2)
                    self.state.metadata["retry_count"] += 1
        
        return False
    
    def _generate_section_content(self, doc_type: str, section_id: str, section_name: str) -> str:
        """
        Generate content for a single section.
        
        In production, this would call Hermes skills or LLM APIs.
        For now, returns template content.
        """
        
        product_name = self.pain_data.get('product_concept', 'Product')
        pain_quote = self.pain_data.get('quote', 'Pain statement')
        
        # Template-based generation (replace with actual skill/API calls)
        templates = {
            "executive_summary": f"""## Executive Summary

### Vision
{product_name} automates the pain point identified in our research.

### Problem
> "{pain_quote}"

### Solution
AI-powered automation with intelligent processing.

### Business Value
- Market Size: $12B TAM
- Revenue Target: $1.8M ARR
- WTP: {self.pain_data.get('willingness_to_pay', '$200-500/mo')}
""",
            
            "problem_statement": f"""## Problem Statement

### Pain Evidence
> "{pain_quote}"

**Frequency**: {self.pain_data.get('frequency', 'Weekly')}
**Existing Workaround**: {self.pain_data.get('existing_workaround', 'Manual')}
**Existing Spend**: {self.pain_data.get('existing_spend', self.pain_data.get('willingness_to_pay', 'Unknown'))}
""",
            
            # Add more section templates as needed
        }
        
        # Return template or default content
        return templates.get(section_id, f"""## {section_name}

[Content for {section_name} - generated for {product_name}]

*Section ID: {section_id}*
*Generated: {datetime.now().isoformat()}*
""")
    
    def _stitch_document(self, doc_type: str) -> str:
        """Stitch all completed sections into final document."""
        
        sections = []
        for section_id, section in self.state.sections.items():
            if section.status == GenerationStatus.COMPLETED and section.content:
                sections.append(section.content)
        
        if not sections:
            self.state.log("No completed sections to stitch", "ERROR")
            return ""
        
        # Add document header
        header = f"""# {self.pain_data.get('product_concept', 'Product')} — {doc_type}

**Generated From**: {self.pain_id}
**Generated At**: {datetime.now().isoformat()}
**Sections**: {len(sections)}
**Status**: Complete

---

"""
        
        return header + "\n\n---\n\n".join(sections)
    
    def get_status(self) -> dict:
        """Get current generation status."""
        progress = self.state.get_progress()
        
        return {
            "pain_id": self.pain_id,
            "output_dir": str(self.output_dir),
            "status": self.state.status.value,
            "progress": progress,
            "started_at": self.state.started_at.isoformat(),
            "completed_at": self.state.completed_at.isoformat() if self.state.completed_at else None,
            "sections": {
                section_id: {
                    "name": section.name,
                    "status": section.status.value,
                    "attempts": section.attempts,
                    "size_bytes": len(section.content) if section.content else 0
                }
                for section_id, section in self.state.sections.items()
            }
        }


def main():
    parser = argparse.ArgumentParser(description='Stateful document generator with progress tracking')
    parser.add_argument('--pain-id', required=True, help='Pain ID from database')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--doc-type', default='PRD', choices=['PRD', 'FEATURES', 'USER_STORIES'], help='Document type')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retries per section')
    parser.add_argument('--status', action='store_true', help='Show status instead of generating')
    args = parser.parse_args()
    
    # Create generator
    generator = StatefulDocumentGenerator(
        pain_id=args.pain_id,
        output_dir=args.output_dir,
        max_retries=args.max_retries
    )
    
    # Show status or generate
    if args.status:
        status = generator.get_status()
        print(json.dumps(status, indent=2))
    else:
        # Generate document
        success = generator.generate_document(args.doc_type)
        
        # Print final status
        print("\n" + "="*60)
        print("GENERATION COMPLETE")
        print("="*60)
        
        status = generator.get_status()
        progress = status['progress']
        
        print(f"Pain ID: {status['pain_id']}")
        print(f"Status: {status['status']}")
        print(f"Progress: {progress['completed']}/{progress['total']} sections ({progress['percent']:.1f}%)")
        print(f"Failed: {progress['failed']} sections")
        print(f"Retries: {status.get('retry_count', 0)}")
        
        if success:
            print(f"\n✅ Document generated successfully!")
            print(f"   Output: {status['output_dir']}/{args.doc_type}.md")
        else:
            print(f"\n❌ Document generation failed!")
            print(f"   Check logs: {status['output_dir']}/.generation.log")
            print(f"   Check state: {status['output_dir']}/.generation_state.json")
        
        return 0 if success else 1


if __name__ == '__main__':
    exit(main())
