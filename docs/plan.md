<!--
This file is a scaffolded project plan that RepoTrackr can parse automatically.

What is RepoTrackr?
- A lightweight dashboard that reads a Markdown plan from your repo, extracts checkbox tasks,
  and shows progress (percent complete, counts, status) with minimal setup.

How to use this file:
1) Fill in the placeholders below (project name, dates, etc.).
2) Add tasks using these markers (RepoTrackr recognizes them):
   - [ ] Task not started (todo)
   - [~] Task in progress (doing)
   - [x] Task completed (done)
   - [!] Task blocked (blocked)
3) Commit and push. Then add this repository to RepoTrackr with the plan path (default: docs/plan.md).
4) Update tasks as you work—RepoTrackr will reflect changes automatically.

Notes:
- You can place this file at docs/plan.md (recommended), plan.md, or keep a Plan section in README.md.
- Advanced: You may include a repotrackr.yml at repo root to declare the plan path(s) and customize markers.
-->

# LaudatorAI — AI-Powered Job Application Assistant

## 📋 Project Overview

**Project Name:** LaudatorAI  
**Repository:** https://github.com/caprolt/LaudatorAI  
**Start Date:** 2024-12-19  
**Target Completion:** 2025-03-19  
**Status:** 🟡 In Progress

**Description:** LaudatorAI is your AI advocate in the job market, inspired by the ancient *laudator* — one who praises and elevates others' achievements. This platform automates the tailoring of resumes and the crafting of cover letters to match specific job postings, ensuring your applications stand out with precision and polish.

## 🎯 Goals

- [x] Define clear project objectives
- [x] Identify target users/audience
- [ ] Establish success metrics
- [x] Set project scope and boundaries

### Core Goals
- [ ] Ingest a job posting URL, extract a normalized Job Description (JD)
- [ ] Parse a base resume into structured JSON
- [ ] Generate a tailored resume (DOCX + PDF) and a cover letter (DOCX + PDF)
- [ ] Provide a diff/preview UI for human-in-the-loop edits

### Non-Goals (MVP)
- [x] Account creation & billing (excluded)
- [x] Multi-language JD parsing beyond English (excluded)
- [x] Advanced ATS scoring and company intel (excluded)

## 🧩 Architecture & Design

### System Architecture
- [x] Design high-level system architecture
- [x] Choose technology stack
- [ ] Plan database schema
- [ ] Define API structure
- [ ] Plan deployment strategy

### Technology Stack
- **Frontend**: Next.js (App Router), Tailwind, shadcn/ui
- **API**: FastAPI (Python 3.11+)
- **Workers**: Celery (Redis broker)
- **Data**: Postgres (metadata), local MinIO/S3 (files)
- **Vector (optional, M3+)**: Qdrant/FAISS
- **Scraping**: Playwright + Readability fallback
- **LLM Provider**: pluggable (OpenAI/Ollama/HF via one interface)
- **PDF/DOCX**: `python-docx` + `weasyprint` (or `docx-template` + `wkhtmltopdf`)
- **Observability**: Sentry + basic logging; Prometheus later

### UI/UX
- [ ] Create wireframes and mockups
- [ ] Design core interface components
- [ ] Map user flows
- [ ] Establish design system

## 🚀 Phases

### Phase 1: Foundation & Setup
Status: 🟢 Completed  
Tasks
- [x] Initialize repository
- [x] Set up dev environment
- [x] Configure CI/CD
- [x] Add documentation structure
- [x] Set up project scaffolding
- [x] Configure development tools and linting

### Phase 2: Core Backend Infrastructure
Status: 🟢 Completed  
Tasks
- [x] Set up FastAPI application structure
- [x] Configure PostgreSQL database
- [x] Set up Redis for Celery broker
- [x] Implement basic API endpoints
- [x] Set up file storage (MinIO/S3)
- [x] Configure logging and observability

### Phase 3: Job Description Processing
Status: 🟢 Completed  
Tasks
- [x] Implement job posting URL ingestion
- [x] Build web scraping with Playwright
- [x] Create Readability fallback parser
- [x] Develop JD normalization logic
- [x] Build JD extraction API endpoints
- [x] Add error handling and validation

### Phase 4: Resume Processing
Status: 🟢 Completed  
Tasks
- [x] Implement resume parsing into structured JSON
- [x] Build resume template system
- [x] Create resume tailoring logic
- [x] Develop DOCX generation with python-docx
- [x] Implement PDF conversion with weasyprint
- [x] Add resume preview functionality

### Phase 5: Cover Letter Generation
Status: 🟢 Completed  
Tasks
- [x] Design cover letter generation prompts
- [x] Implement LLM integration (OpenAI/Ollama/HF)
- [x] Build cover letter template system
- [x] Create DOCX and PDF generation for cover letters
- [x] Add cover letter preview functionality

### Phase 6: Frontend Development
Status: 🟢 Completed  
Tasks
- [x] Set up Next.js with App Router
- [x] Configure Tailwind CSS and shadcn/ui
- [x] Build main application layout
- [x] Implement job posting input form
- [x] Create resume upload interface
- [x] Build diff/preview UI for edits
- [x] Add responsive design and accessibility

### Phase 7: Integration & Testing
Status: 🟢 Completed  
Tasks
- [x] Integrate frontend with backend APIs
- [x] Implement end-to-end workflows
- [x] Add comprehensive error handling
- [x] Build user feedback mechanisms
- [x] Perform security testing
- [x] Optimize performance

### Phase 8: Deployment & Launch
Status: 🔴 Not Started  
Tasks
- [ ] Set up staging environment
- [ ] Configure production environment
- [ ] Implement monitoring and alerts
- [ ] Create rollback procedures
- [ ] Perform load testing
- [ ] Launch MVP

## 📈 Progress & Status Notes
- [ ] Document current risks and mitigations
- [ ] Record milestone achievements
- [ ] Capture blockers and next steps

## 🧪 Testing & Quality
- [x] Unit tests for core modules
- [x] Integration tests for critical flows
- [x] End-to-end testing for user workflows
- [x] Linting and formatting
- [x] Observability (logs/metrics)
- [x] Security testing

## 📦 Deployment
- [ ] Staging environment setup
- [ ] Production environment configuration
- [ ] CI/CD pipeline implementation
- [ ] Rollback plan
- [ ] Monitoring and alerts
- [ ] Performance optimization

<!-- End of scaffold. You can customize sections, add or remove phases, and expand tasks.
     RepoTrackr will parse checkbox items and compute progress automatically. -->