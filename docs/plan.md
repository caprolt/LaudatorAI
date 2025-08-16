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
Status: 🔴 Not Started  
Tasks
- [ ] Set up FastAPI application structure
- [ ] Configure PostgreSQL database
- [ ] Set up Redis for Celery broker
- [ ] Implement basic API endpoints
- [ ] Set up file storage (MinIO/S3)
- [ ] Configure logging and observability

### Phase 3: Job Description Processing
Status: 🔴 Not Started  
Tasks
- [ ] Implement job posting URL ingestion
- [ ] Build web scraping with Playwright
- [ ] Create Readability fallback parser
- [ ] Develop JD normalization logic
- [ ] Build JD extraction API endpoints
- [ ] Add error handling and validation

### Phase 4: Resume Processing
Status: 🔴 Not Started  
Tasks
- [ ] Implement resume parsing into structured JSON
- [ ] Build resume template system
- [ ] Create resume tailoring logic
- [ ] Develop DOCX generation with python-docx
- [ ] Implement PDF conversion with weasyprint
- [ ] Add resume preview functionality

### Phase 5: Cover Letter Generation
Status: 🔴 Not Started  
Tasks
- [ ] Design cover letter generation prompts
- [ ] Implement LLM integration (OpenAI/Ollama/HF)
- [ ] Build cover letter template system
- [ ] Create DOCX and PDF generation for cover letters
- [ ] Add cover letter preview functionality

### Phase 6: Frontend Development
Status: 🔴 Not Started  
Tasks
- [ ] Set up Next.js with App Router
- [ ] Configure Tailwind CSS and shadcn/ui
- [ ] Build main application layout
- [ ] Implement job posting input form
- [ ] Create resume upload interface
- [ ] Build diff/preview UI for edits
- [ ] Add responsive design and accessibility

### Phase 7: Integration & Testing
Status: 🔴 Not Started  
Tasks
- [ ] Integrate frontend with backend APIs
- [ ] Implement end-to-end workflows
- [ ] Add comprehensive error handling
- [ ] Build user feedback mechanisms
- [ ] Perform security testing
- [ ] Optimize performance

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
- [ ] Unit tests for core modules
- [ ] Integration tests for critical flows
- [ ] End-to-end testing for user workflows
- [ ] Linting and formatting
- [ ] Observability (logs/metrics)
- [ ] Security testing

## 📦 Deployment
- [ ] Staging environment setup
- [ ] Production environment configuration
- [ ] CI/CD pipeline implementation
- [ ] Rollback plan
- [ ] Monitoring and alerts
- [ ] Performance optimization

<!-- End of scaffold. You can customize sections, add or remove phases, and expand tasks.
     RepoTrackr will parse checkbox items and compute progress automatically. -->