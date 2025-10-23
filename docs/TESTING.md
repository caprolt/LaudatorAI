# Code Quality & Testing Guide

This document describes the testing strategy, code quality standards, and continuous integration setup for LaudatorAI.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Structure](#test-structure)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Code Quality Tools](#code-quality-tools)
- [Continuous Integration](#continuous-integration)
- [Coverage Reports](#coverage-reports)
- [Pre-commit Hooks](#pre-commit-hooks)

## Testing Philosophy

### Test Pyramid

```
        /\
       /  \    E2E Tests (Few)
      /____\   - Full user workflows
     /      \  - Browser automation
    /________\ Integration Tests (Some)
   /          \ - API + Database
  /____________\ - Multiple components
 /              \
/________________\ Unit Tests (Many)
                   - Individual functions
                   - Business logic
```

### Testing Goals

1. **Confidence**: Tests should give confidence that code works
2. **Fast Feedback**: Tests should run quickly for rapid iteration
3. **Maintainable**: Tests should be easy to understand and update
4. **Comprehensive**: Cover critical paths and edge cases
5. **Isolation**: Tests should not depend on each other

### Coverage Targets

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All critical workflows
- **E2E Tests**: Happy path + major error scenarios

## Test Structure

### Backend Test Organization

```
backend/tests/
├── conftest.py                    # Pytest fixtures
├── test_unit/                     # Unit tests
│   ├── test_services/
│   │   ├── test_resume_processing.py
│   │   ├── test_job_processing.py
│   │   └── test_file_storage.py
│   └── test_utils/
├── test_integration/              # Integration tests
│   ├── test_api_jobs.py
│   ├── test_api_resumes.py
│   └── test_api_applications.py
├── test_e2e/                      # End-to-end tests
│   └── test_complete_workflow.py
└── fixtures/                      # Test data
    ├── sample_resume.pdf
    └── sample_job_description.html
```

### Frontend Test Organization

```
frontend/__tests__/
├── components/
│   ├── JobDescriptionInput.test.tsx
│   ├── ResumeUpload.test.tsx
│   └── PreviewDiff.test.tsx
├── lib/
│   ├── api.test.ts
│   └── utils.test.ts
└── integration/
    └── application-flow.test.tsx
```

## Backend Testing

### Unit Tests

Test individual functions and methods in isolation.

**Example: Resume Processing Service**

```python
# tests/test_unit/test_services/test_resume_processing.py
import pytest
from app.services.resume_processing import parse_resume, extract_skills

def test_parse_resume_valid_content():
    """Test resume parsing with valid content."""
    content = """
    John Doe
    Software Engineer
    
    Experience:
    - Senior Developer at Tech Corp (2020-2023)
    - Built scalable APIs using Python and FastAPI
    
    Skills: Python, FastAPI, PostgreSQL, Docker
    """
    
    result = parse_resume(content)
    
    assert result["name"] == "John Doe"
    assert result["title"] == "Software Engineer"
    assert len(result["experience"]) == 1
    assert "Python" in result["skills"]

def test_parse_resume_empty_content():
    """Test error handling for empty content."""
    with pytest.raises(ValueError, match="cannot be empty"):
        parse_resume("")

def test_extract_skills():
    """Test skill extraction from text."""
    text = "Experienced with Python, JavaScript, React, and Docker"
    
    skills = extract_skills(text)
    
    assert "Python" in skills
    assert "JavaScript" in skills
    assert "React" in skills
    assert "Docker" in skills
    assert len(skills) == 4

@pytest.mark.parametrize("content,expected", [
    ("Python developer", ["Python"]),
    ("Full-stack: React, Node.js, MongoDB", ["React", "Node.js", "MongoDB"]),
    ("No technical skills here", []),
])
def test_extract_skills_parametrized(content, expected):
    """Test skill extraction with multiple scenarios."""
    skills = extract_skills(content)
    assert skills == expected
```

### Integration Tests

Test multiple components working together, including database interactions.

**Example: Job API Integration**

```python
# tests/test_integration/test_api_jobs.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_job(client: AsyncClient, db: AsyncSession):
    """Test job creation via API."""
    payload = {
        "url": "https://example.com/jobs/software-engineer"
    }
    
    response = await client.post("/api/v1/jobs/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == payload["url"]
    assert "id" in data
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_get_job_not_found(client: AsyncClient):
    """Test 404 error for non-existent job."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    
    response = await client.get(f"/api/v1/jobs/{fake_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_list_jobs_pagination(client: AsyncClient, sample_jobs):
    """Test job listing with pagination."""
    # Create 15 sample jobs via fixture
    
    # Test first page
    response = await client.get("/api/v1/jobs/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    
    # Test second page
    response = await client.get("/api/v1/jobs/?skip=10&limit=10")
    assert len(response.json()["items"]) == 5
```

### E2E Tests

Test complete user workflows from start to finish.

**Example: Complete Application Workflow**

```python
# tests/test_e2e/test_complete_workflow.py
import pytest
from httpx import AsyncClient
import asyncio

@pytest.mark.asyncio
async def test_complete_application_workflow(
    client: AsyncClient,
    sample_resume_file,
    sample_job_url
):
    """Test complete workflow: create job, upload resume, create application."""
    
    # Step 1: Create job
    job_response = await client.post(
        "/api/v1/jobs/",
        json={"url": sample_job_url}
    )
    assert job_response.status_code == 201
    job_id = job_response.json()["id"]
    
    # Wait for job processing
    await wait_for_job_completion(client, job_id)
    
    # Step 2: Upload resume
    files = {"file": ("resume.pdf", sample_resume_file, "application/pdf")}
    resume_response = await client.post("/api/v1/resumes/upload", files=files)
    assert resume_response.status_code == 201
    resume_id = resume_response.json()["id"]
    
    # Wait for resume processing
    await wait_for_resume_completion(client, resume_id)
    
    # Step 3: Create application
    app_response = await client.post(
        "/api/v1/applications/",
        json={
            "job_id": job_id,
            "resume_id": resume_id
        }
    )
    assert app_response.status_code == 201
    app_id = app_response.json()["id"]
    
    # Wait for application processing
    await wait_for_application_completion(client, app_id)
    
    # Step 4: Verify outputs
    app_data = await client.get(f"/api/v1/applications/{app_id}")
    assert app_data.json()["status"] == "completed"
    assert app_data.json()["tailored_resume_path"] is not None
    assert app_data.json()["cover_letter_path"] is not None

async def wait_for_job_completion(client, job_id, timeout=30):
    """Wait for job processing to complete."""
    start_time = asyncio.get_event_loop().time()
    while True:
        response = await client.get(f"/api/v1/jobs/{job_id}")
        status = response.json()["status"]
        if status in ["completed", "failed"]:
            assert status == "completed"
            return
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError("Job processing timed out")
        await asyncio.sleep(1)
```

### Pytest Fixtures

Common test setup and teardown.

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.core.database import Base

@pytest.fixture
async def db():
    """Create test database."""
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost/test_db",
        echo=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
async def client(db):
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_resume_file():
    """Sample resume file for testing."""
    with open("tests/fixtures/sample_resume.pdf", "rb") as f:
        yield f.read()

@pytest.fixture
def sample_job_url():
    """Sample job URL for testing."""
    return "https://example.com/jobs/software-engineer"

@pytest.fixture
async def sample_jobs(db):
    """Create multiple sample jobs."""
    jobs = []
    for i in range(15):
        job = Job(
            url=f"https://example.com/jobs/job-{i}",
            title=f"Software Engineer {i}",
            company=f"Company {i}"
        )
        db.add(job)
        jobs.append(job)
    await db.commit()
    return jobs
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_integration/test_api_jobs.py

# Run specific test
pytest tests/test_integration/test_api_jobs.py::test_create_job

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run only unit tests
pytest tests/test_unit/

# Run tests matching a pattern
pytest -k "resume"

# Run tests with specific marker
pytest -m "integration"

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
```

## Frontend Testing

### Component Tests

```typescript
// __tests__/components/JobDescriptionInput.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import JobDescriptionInput from '@/components/job-description-input';

describe('JobDescriptionInput', () => {
  it('renders input field', () => {
    render(<JobDescriptionInput onSubmit={jest.fn()} />);
    
    const input = screen.getByPlaceholderText(/job posting url/i);
    expect(input).toBeInTheDocument();
  });

  it('validates URL format', async () => {
    render(<JobDescriptionInput onSubmit={jest.fn()} />);
    
    const input = screen.getByPlaceholderText(/job posting url/i);
    const button = screen.getByRole('button', { name: /submit/i });
    
    // Invalid URL
    fireEvent.change(input, { target: { value: 'not-a-url' } });
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText(/invalid url/i)).toBeInTheDocument();
    });
  });

  it('calls onSubmit with valid URL', async () => {
    const onSubmit = jest.fn();
    render(<JobDescriptionInput onSubmit={onSubmit} />);
    
    const input = screen.getByPlaceholderText(/job posting url/i);
    const button = screen.getByRole('button', { name: /submit/i });
    
    fireEvent.change(input, { 
      target: { value: 'https://example.com/jobs/engineer' } 
    });
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith('https://example.com/jobs/engineer');
    });
  });
});
```

### API Client Tests

```typescript
// __tests__/lib/api.test.ts
import { createJob, uploadResume } from '@/lib/api';

global.fetch = jest.fn();

describe('API Client', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('creates job successfully', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: '123', url: 'https://example.com' }),
    });

    const result = await createJob('https://example.com/jobs/engineer');

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/jobs/'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ url: 'https://example.com/jobs/engineer' }),
      })
    );
    expect(result.id).toBe('123');
  });

  it('handles API errors', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Invalid URL' }),
    });

    await expect(createJob('invalid')).rejects.toThrow('Invalid URL');
  });
});
```

### Running Frontend Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test JobDescriptionInput

# Update snapshots
npm test -- -u
```

## Code Quality Tools

### Backend Tools

#### Black (Code Formatter)

```bash
# Format all code
black app/

# Check without modifying
black --check app/

# Configuration in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
```

#### isort (Import Sorter)

```bash
# Sort imports
isort app/

# Check without modifying
isort --check-only app/

# Configuration in pyproject.toml
[tool.isort]
profile = "black"
line_length = 88
```

#### mypy (Type Checker)

```bash
# Type check
mypy app/

# Configuration in pyproject.toml
[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
check_untyped_defs = true
```

#### flake8 (Linter)

```bash
# Lint code
flake8 app/

# Configuration in .flake8 or setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

### Frontend Tools

#### ESLint

```bash
# Lint code
npm run lint

# Fix automatically
npm run lint -- --fix

# Configuration in .eslintrc.json
```

#### TypeScript Compiler

```bash
# Type check
npm run type-check

# Watch mode
tsc --watch
```

#### Prettier (Optional)

```bash
# Format code
npx prettier --write .

# Check formatting
npx prettier --check .
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests with coverage
      run: |
        cd backend
        pytest --cov=app --cov-report=xml tests/
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: backend
    
    - name: Code quality checks
      run: |
        cd backend
        black --check app/
        isort --check-only app/
        mypy app/
        flake8 app/

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run tests
      run: |
        cd frontend
        npm test -- --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./frontend/coverage/lcov.info
        flags: frontend
    
    - name: Type check
      run: |
        cd frontend
        npm run type-check
    
    - name: Lint
      run: |
        cd frontend
        npm run lint
    
    - name: Build
      run: |
        cd frontend
        npm run build
```

## Coverage Reports

### Generating Coverage Reports

```bash
# Backend HTML report
cd backend
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html

# Backend terminal report
pytest --cov=app --cov-report=term-missing tests/

# Frontend coverage
cd frontend
npm test -- --coverage
open coverage/lcov-report/index.html
```

### Coverage Badges

Add coverage badges to README:

```markdown
[![codecov](https://codecov.io/gh/caprolt/LaudatorAI/branch/main/graph/badge.svg)](https://codecov.io/gh/caprolt/LaudatorAI)
```

## Pre-commit Hooks

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

## Best Practices

### Test Writing Guidelines

1. **Arrange, Act, Assert**: Structure tests clearly
2. **One Assertion Per Test**: Keep tests focused
3. **Descriptive Names**: `test_create_job_with_valid_url`
4. **Use Fixtures**: Avoid repetition
5. **Mock External Services**: Don't hit real APIs
6. **Test Edge Cases**: Not just happy path
7. **Keep Tests Fast**: Slow tests won't be run

### Code Review Checklist

- [ ] All tests pass
- [ ] Code coverage hasn't decreased
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] New tests added for new features
- [ ] Edge cases tested

---

**Last Updated**: December 2024  
**Target Coverage**: 80%+  
**CI Status**: ✅ Passing
