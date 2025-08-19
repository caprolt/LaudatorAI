# LaudatorAI — AI-Powered Job Application Assistant

**LaudatorAI** is your AI advocate in the job market, inspired by the ancient *laudator* — one who praises and elevates others' achievements. This platform automates the tailoring of resumes and the crafting of cover letters to match specific job postings, ensuring your applications stand out with precision and polish.

---

# LaudatorAI — AI-Powered Job Application Assistant — Implementation Plan

> Drop this file into your repo as `IMPLEMENTATION_PLAN.md`. It’s a build-first plan with tasks, commands, API specs, schemas, prompts, and acceptance criteria.

---

## 0) Goals & Non-Goals

**Goals**
- Ingest a job posting URL, extract a normalized Job Description (JD).
- Parse a base resume into structured JSON.
- Generate a tailored resume (DOCX + PDF) and a cover letter (DOCX + PDF).
- Provide a diff/preview UI for human-in-the-loop edits.

**Non-Goals (MVP)**
- Account creation & billing.
- Multi-language JD parsing (beyond English).
- Advanced ATS scoring and company intel.

---

## 1) Architecture

- **Frontend**: Next.js (App Router), Tailwind, shadcn/ui
- **API**: FastAPI (Python 3.11+)
- **Workers**: Celery (Redis broker)
- **Data**: Postgres (metadata), local MinIO/S3 (files)
- **Vector (optional, M3+)**: Qdrant/FAISS
- **Scraping**: Playwright + Readability fallback
- **LLM Provider**: pluggable (OpenAI/Ollama/HF via one interface)
- **PDF/DOCX**: `python-docx` + `weasyprint` (or `docx-template` + `wkhtmltopdf`)
- **Observability**: Sentry + basic logging; Prometheus later

---
