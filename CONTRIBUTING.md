# Contributing to LaudatorAI

Thank you for your interest in contributing to LaudatorAI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Our Standards

Examples of behavior that contributes to a positive environment:
- Demonstrating empathy and kindness
- Being respectful of differing opinions
- Giving and gracefully accepting constructive feedback
- Taking responsibility and apologizing for mistakes

Examples of unacceptable behavior:
- Harassment, trolling, or insulting comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- **Backend**: Python 3.11+, PostgreSQL, Redis
- **Frontend**: Node.js 18+, npm or yarn
- **Tools**: Git, Docker (optional but recommended)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LaudatorAI.git
   cd LaudatorAI
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/caprolt/LaudatorAI.git
   ```

### Environment Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black isort flake8 mypy

# Copy environment template
cp .env.example .env
# Edit .env with your local configuration
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local
# Edit .env.local with your local configuration
```

#### Docker Setup (Alternative)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Development Workflow

### 1. Create a Branch

Create a feature branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications
- `chore/` - Maintenance tasks

### 2. Make Changes

- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new features
- Update documentation as needed
- Commit your changes with clear messages

### 3. Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Maintenance tasks

Examples:
```
feat(api): add resume tailoring endpoint

Implement new endpoint for generating tailored resumes
based on job descriptions. Includes validation and error
handling.

Closes #123
```

```
fix(frontend): resolve file upload issue on Safari

Fix MIME type handling for resume uploads in Safari browser.
```

### 4. Keep Your Branch Updated

Regularly sync with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

## Coding Standards

### Backend (Python)

#### Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 88)
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use type hints for all functions and methods

#### Code Formatting

```bash
cd backend

# Format code
black app/

# Sort imports
isort app/

# Check linting
flake8 app/

# Type checking
mypy app/
```

#### Best Practices

- Write descriptive docstrings for classes and functions
- Keep functions focused and single-purpose
- Use meaningful variable and function names
- Handle errors gracefully with appropriate error messages
- Log important operations and errors
- Write unit tests for all new functions

Example:
```python
from typing import Optional, List
from pydantic import BaseModel

def process_resume(
    resume_content: str,
    job_description: Optional[str] = None
) -> dict:
    """
    Process and parse resume content.
    
    Args:
        resume_content: Raw resume text content
        job_description: Optional job description for tailoring
        
    Returns:
        Dictionary containing parsed resume data
        
    Raises:
        ValueError: If resume content is invalid
    """
    if not resume_content:
        raise ValueError("Resume content cannot be empty")
    
    # Processing logic here
    return parsed_data
```

### Frontend (TypeScript/React)

#### Style Guide

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Use functional components with hooks
- Follow React best practices

#### Code Formatting

```bash
cd frontend

# Lint code
npm run lint

# Type checking
npm run type-check

# Format (if Prettier is configured)
npx prettier --write .
```

#### Best Practices

- Use meaningful component and variable names
- Keep components small and focused
- Extract reusable logic into custom hooks
- Use proper TypeScript types (avoid `any`)
- Handle loading and error states
- Make components accessible (ARIA labels, keyboard navigation)

Example:
```typescript
import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch user');
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }
    
    fetchUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

## Testing

### Backend Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_resume_processing.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

#### Writing Tests

- Write tests for all new features
- Aim for high test coverage (>80%)
- Use descriptive test names
- Test edge cases and error conditions
- Use fixtures for common setup

Example:
```python
import pytest
from app.services.resume_processing import parse_resume

def test_parse_resume_success():
    """Test successful resume parsing."""
    resume_content = "John Doe\nSoftware Engineer\n..."
    result = parse_resume(resume_content)
    
    assert result["name"] == "John Doe"
    assert result["title"] == "Software Engineer"

def test_parse_resume_empty_content():
    """Test error handling for empty content."""
    with pytest.raises(ValueError, match="cannot be empty"):
        parse_resume("")

@pytest.fixture
def sample_resume():
    """Fixture for sample resume data."""
    return {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "experience": [...]
    }

def test_tailor_resume(sample_resume):
    """Test resume tailoring with sample data."""
    result = tailor_resume(sample_resume, job_description="...")
    assert result is not None
```

### Frontend Testing

```bash
cd frontend

# Run tests (when configured)
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

## Pull Request Process

### Before Submitting

1. **Update Documentation**: Update README, API docs, or other documentation as needed
2. **Run Tests**: Ensure all tests pass
3. **Code Quality**: Run linters and formatters
4. **Commit Messages**: Use clear, descriptive commit messages
5. **Rebase**: Rebase on latest `main` branch

### Submitting

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template with:
   - **Description**: What does this PR do?
   - **Type of Change**: Feature, bug fix, documentation, etc.
   - **Testing**: How was this tested?
   - **Screenshots**: If applicable
   - **Related Issues**: Link to related issues

### PR Template Example

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran and how to reproduce them

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- Delete your feature branch after merging

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core configuration
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── tests/                # Test files
├── alembic/              # Database migrations
└── requirements.txt      # Python dependencies
```

### Frontend Structure

```
frontend/
├── src/
│   ├── app/              # Next.js pages (App Router)
│   ├── components/       # React components
│   ├── lib/              # Utility functions
│   └── types/            # TypeScript types
├── public/               # Static assets
└── package.json          # Node.js dependencies
```

## Areas for Contribution

### High Priority

- Performance optimizations
- Test coverage improvements
- Documentation enhancements
- Bug fixes
- Accessibility improvements

### Feature Ideas

- Multi-language support
- Advanced resume templates
- ATS optimization scoring
- Company research integration
- Mobile responsive improvements
- Dark mode support

### Good First Issues

Look for issues labeled `good first issue` or `help wanted` on GitHub. These are great starting points for new contributors.

## Questions?

If you have questions:
- Check existing documentation
- Search existing issues
- Open a new issue with the `question` label
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to LaudatorAI! 🚀
