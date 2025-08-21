#!/usr/bin/env python3
"""
Project Structure Generator

This module generates appropriate project directory structures based on
the detected technology stack from INITIAL.md files.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional
from technology_detector import TechnologyStack


class ProjectStructureGenerator:
    """Generates project directory structures based on technology stack"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.project_root.mkdir(exist_ok=True)
    
    def generate_structure(self, tech_stack: TechnologyStack, project_name: str) -> Dict[str, Path]:
        """Generate project structure based on technology stack"""
        created_dirs = {}
        
        if tech_stack.is_fullstack():
            created_dirs.update(self._generate_fullstack_structure(project_name))
        elif tech_stack.is_backend_only():
            created_dirs.update(self._generate_backend_structure(tech_stack.backend, project_name))
        elif tech_stack.is_frontend_only():
            created_dirs.update(self._generate_frontend_structure(tech_stack.frontend, project_name))
        else:
            created_dirs.update(self._generate_generic_structure(project_name))
        
        # Create common files
        self._create_common_files(project_name, tech_stack)
        
        return created_dirs
    
    def _generate_fullstack_structure(self, project_name: str) -> Dict[str, Path]:
        """Generate full-stack project structure"""
        dirs = {}
        
        # Backend structure
        backend_dir = self.project_root / "backend"
        dirs.update(self._generate_backend_structure("python", project_name, backend_dir))
        
        # Frontend structure
        frontend_dir = self.project_root / "frontend"
        dirs.update(self._generate_frontend_structure("nextjs", project_name, frontend_dir))
        
        # Root level files
        self._create_docker_compose()
        self._create_root_readme(project_name)
        
        return dirs
    
    def _generate_backend_structure(self, backend_tech: str, project_name: str, base_dir: Optional[Path] = None) -> Dict[str, Path]:
        """Generate backend-only project structure"""
        if base_dir is None:
            base_dir = self.project_root
        
        dirs = {}
        
        if backend_tech == "python":
            dirs.update(self._generate_python_backend_structure(base_dir))
        elif backend_tech == "java":
            dirs.update(self._generate_java_backend_structure(base_dir))
        elif backend_tech == "nodejs":
            dirs.update(self._generate_nodejs_backend_structure(base_dir))
        else:
            dirs.update(self._generate_generic_backend_structure(base_dir))
        
        return dirs
    
    def _generate_frontend_structure(self, frontend_tech: str, project_name: str, base_dir: Optional[Path] = None) -> Dict[str, Path]:
        """Generate frontend-only project structure"""
        if base_dir is None:
            base_dir = self.project_root
        
        dirs = {}
        
        if frontend_tech == "nextjs":
            dirs.update(self._generate_nextjs_structure(base_dir))
        elif frontend_tech == "react":
            dirs.update(self._generate_react_structure(base_dir))
        elif frontend_tech == "vue":
            dirs.update(self._generate_vue_structure(base_dir))
        else:
            dirs.update(self._generate_generic_frontend_structure(base_dir))
        
        return dirs
    
    def _generate_python_backend_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate Python backend structure"""
        dirs = {}
        
        # Source directories
        src_dir = base_dir / "src"
        dirs['src'] = src_dir
        src_dir.mkdir(exist_ok=True)
        
        (src_dir / "__init__.py").touch()
        (src_dir / "main.py").touch()
        
        # Feature directories
        for feature in ["models", "services", "api", "utils", "config"]:
            feature_dir = src_dir / feature
            dirs[feature] = feature_dir
            feature_dir.mkdir(exist_ok=True)
            (feature_dir / "__init__.py").touch()
        
        # Tests directory
        tests_dir = base_dir / "tests"
        dirs['tests'] = tests_dir
        tests_dir.mkdir(exist_ok=True)
        (tests_dir / "__init__.py").touch()
        (tests_dir / "conftest.py").touch()
        
        # Configuration files
        (base_dir / "requirements.txt").touch()
        (base_dir / "pyproject.toml").touch()
        (base_dir / "Dockerfile").touch()
        (base_dir / ".env.example").touch()
        (base_dir / ".gitignore").touch()
        
        return dirs
    
    def _generate_java_backend_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate Java backend structure"""
        dirs = {}
        
        # Maven structure
        src_dir = base_dir / "src"
        dirs['src'] = src_dir
        src_dir.mkdir(exist_ok=True)
        
        main_dir = src_dir / "main" / "java"
        main_dir.mkdir(parents=True, exist_ok=True)
        
        test_dir = src_dir / "test" / "java"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration files
        (base_dir / "pom.xml").touch()
        (base_dir / "Dockerfile").touch()
        (base_dir / ".gitignore").touch()
        
        return dirs
    
    def _generate_nodejs_backend_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate Node.js backend structure"""
        dirs = {}
        
        # Source directories
        src_dir = base_dir / "src"
        dirs['src'] = src_dir
        src_dir.mkdir(exist_ok=True)
        
        for feature in ["routes", "middleware", "models", "services", "utils"]:
            feature_dir = src_dir / feature
            dirs[feature] = feature_dir
            feature_dir.mkdir(exist_ok=True)
        
        # Configuration files
        (base_dir / "package.json").touch()
        (base_dir / "Dockerfile").touch()
        (base_dir / ".gitignore").touch()
        
        return dirs
    
    def _generate_nextjs_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate Next.js frontend structure"""
        dirs = {}
        
        # Source directories
        src_dir = base_dir / "src"
        dirs['src'] = src_dir
        src_dir.mkdir(exist_ok=True)
        
        # App Router structure
        app_dir = src_dir / "app"
        dirs['app'] = app_dir
        app_dir.mkdir(exist_ok=True)
        
        (app_dir / "layout.tsx").touch()
        (app_dir / "page.tsx").touch()
        (app_dir / "globals.css").touch()
        
        # Component directories
        components_dir = src_dir / "components"
        dirs['components'] = components_dir
        components_dir.mkdir(exist_ok=True)
        
        for subdir in ["ui", "forms", "layout"]:
            (components_dir / subdir).mkdir(exist_ok=True)
        
        # Utility directories
        lib_dir = src_dir / "lib"
        dirs['lib'] = lib_dir
        lib_dir.mkdir(exist_ok=True)
        
        types_dir = src_dir / "types"
        dirs['types'] = types_dir
        types_dir.mkdir(exist_ok=True)
        
        # Configuration files
        (base_dir / "package.json").touch()
        (base_dir / "next.config.js").touch()
        (base_dir / "tailwind.config.js").touch()
        (base_dir / "tsconfig.json").touch()
        (base_dir / "Dockerfile").touch()
        (base_dir / ".gitignore").touch()
        
        return dirs
    
    def _generate_react_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate React frontend structure"""
        dirs = {}
        
        # Source directories
        src_dir = base_dir / "src"
        dirs['src'] = src_dir
        src_dir.mkdir(exist_ok=True)
        
        # Component directories
        components_dir = src_dir / "components"
        dirs['components'] = components_dir
        components_dir.mkdir(exist_ok=True)
        
        # Configuration files
        (base_dir / "package.json").touch()
        (base_dir / "vite.config.ts").touch()
        (base_dir / "tsconfig.json").touch()
        (base_dir / "Dockerfile").touch()
        (base_dir / ".gitignore").touch()
        
        return dirs
    
    def _generate_generic_structure(self, project_name: str) -> Dict[str, Path]:
        """Generate generic project structure"""
        dirs = {}
        
        # Basic directories
        for dir_name in ["src", "tests", "docs", "config"]:
            dir_path = self.project_root / dir_name
            dirs[dir_name] = dir_path
            dir_path.mkdir(exist_ok=True)
        
        # Configuration files
        (self.project_root / "README.md").touch()
        (self.project_root / ".gitignore").touch()
        
        return dirs
    
    def _generate_generic_backend_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate generic backend structure"""
        dirs = {}
        
        # Basic backend directories
        for dir_name in ["src", "tests", "config"]:
            dir_path = base_dir / dir_name
            dirs[dir_name] = dir_path
            dir_path.mkdir(exist_ok=True)
        
        return dirs
    
    def _generate_generic_frontend_structure(self, base_dir: Path) -> Dict[str, Path]:
        """Generate generic frontend structure"""
        dirs = {}
        
        # Basic frontend directories
        for dir_name in ["src", "public", "tests"]:
            dir_path = base_dir / dir_name
            dirs[dir_name] = dir_path
            dir_path.mkdir(exist_ok=True)
        
        return dirs
    
    def _create_common_files(self, project_name: str, tech_stack: TechnologyStack):
        """Create common project files"""
        # Root README
        self._create_root_readme(project_name)
        
        # Root .gitignore
        self._create_root_gitignore()
        
        # Root CLAUDE.md
        self._create_root_claude_md(project_name, tech_stack)
    
    def _create_root_readme(self, project_name: str):
        """Create root README.md"""
        readme_content = f"""# {project_name}

This project was automatically generated using the Process2 initialization system.

## Project Structure

This is a multi-component project with the following structure:

- `backend/` - Backend services and API
- `frontend/` - Frontend application
- `CLAUDE.md` - Project-specific development guidelines
- `INITIAL.md` - Original project specification

## Getting Started

1. Review the `CLAUDE.md` files in each component directory
2. Follow the setup instructions for each component
3. Use the provided PRP templates for feature development

## Development Workflow

1. Use `/prime-core` to initialize Claude with project context
2. Create PRPs using the appropriate templates
3. Execute PRPs to build features
4. Follow the validation and testing guidelines

## Technology Stack

See `INITIAL.md` for complete technology stack details.
"""
        
        readme_path = self.project_root / "README.md"
        readme_path.write_text(readme_content)
    
    def _create_root_gitignore(self):
        """Create root .gitignore"""
        gitignore_content = """# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.env

# Build outputs
dist/
build/
*.egg-info/
.next/
out/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
.coverage
htmlcov/

# Docker
.dockerignore
"""
        
        gitignore_path = self.project_root / ".gitignore"
        gitignore_path.write_text(gitignore_content)
    
    def _create_root_claude_md(self, project_name: str, tech_stack: TechnologyStack):
        """Create root CLAUDE.md with project overview"""
        claude_content = f"""# CLAUDE.md - {project_name}

This file provides project-wide development guidelines and cross-cutting concerns.

## Project Overview

**Project Name**: {project_name}
**Project Type**: {tech_stack.project_type.title()}
**Technology Stack**: {', '.join(filter(None, [tech_stack.backend, tech_stack.frontend, tech_stack.database, tech_stack.infrastructure]))}

## Architecture

This project follows a **{tech_stack.project_type}** architecture:

"""
        
        if tech_stack.is_fullstack():
            claude_content += """- **Backend**: Python-based API services
- **Frontend**: Next.js 15 React application
- **Database**: Supabase (PostgreSQL)
- **Infrastructure**: Docker containerization

## Development Guidelines

### Cross-Cutting Concerns
- **Environment Variables**: Use `.env.local` for local development
- **Configuration**: Follow 12-factor app principles
- **Logging**: Structured logging across all components
- **Error Handling**: Consistent error response formats

### Code Quality Standards
- **Backend**: Follow Python PEP 8, use type hints, comprehensive testing
- **Frontend**: TypeScript strict mode, React best practices, component testing
- **Database**: Use migrations, validate schemas, handle connections properly

### Testing Strategy
- **Unit Tests**: Co-located with source code
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Full user journey validation
- **Coverage Target**: 80%+ for all components

### Deployment
- **Development**: Local Docker Compose setup
- **Staging**: Automated deployment pipeline
- **Production**: Infrastructure as Code with monitoring

## Component-Specific Guidelines

See the `CLAUDE.md` files in each component directory for detailed guidelines:
- `backend/CLAUDE.md` - Python backend development
- `frontend/CLAUDE.md` - Next.js frontend development

## Getting Started

1. **Setup Environment**: Follow component-specific setup instructions
2. **Initialize Claude**: Use `/prime-core` to load project context
3. **Create Features**: Use appropriate PRP templates for each component
4. **Validate Changes**: Follow the validation loops in each PRP

## Common Commands

```bash
# Backend development
cd backend
uv sync
uv run pytest

# Frontend development
cd frontend
npm install
npm run dev

# Full project
docker-compose up -d
```

## Troubleshooting

- **Backend Issues**: Check Python version, dependencies, environment variables
- **Frontend Issues**: Verify Node.js version, clear cache, check TypeScript errors
- **Database Issues**: Verify connection strings, check Supabase status
- **Docker Issues**: Rebuild containers, check port conflicts

Remember: Each component has its own detailed CLAUDE.md file with specific guidelines and patterns.
"""
        elif tech_stack.is_backend_only():
            claude_content += f"""- **Backend**: {tech_stack.backend.title()}-based services
- **Database**: {tech_stack.database or 'Not specified'}
- **Infrastructure**: {tech_stack.infrastructure or 'Not specified'}

## Development Guidelines

See `CLAUDE.md` in the root directory for detailed {tech_stack.backend.title()} development guidelines.
"""
        elif tech_stack.is_frontend_only():
            claude_content += f"""- **Frontend**: {tech_stack.frontend.title()}-based application
- **Styling**: Modern CSS framework
- **Infrastructure**: {tech_stack.infrastructure or 'Not specified'}

## Development Guidelines

See `CLAUDE.md` in the root directory for detailed {tech_stack.frontend.title()} development guidelines.
"""
        
        claude_path = self.project_root / "CLAUDE.md"
        claude_path.write_text(claude_content)
    
    def _create_docker_compose(self):
        """Create docker-compose.yml for full-stack projects"""
        docker_compose_content = """version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    depends_on:
      - database
    volumes:
      - ./backend:/app
      - /app/node_modules

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend

  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
        
        docker_compose_path = self.project_root / "docker-compose.yml"
        docker_compose_path.write_text(docker_compose_content)


def main():
    """Test the project structure generator"""
    # Example usage
    from technology_detector import TechnologyDetector
    
    # Test with sample content
    sample_content = """
    # Sample Project
    
    ## Technology Stack
    - Backend: Python 3.x with FastAPI
    - Frontend: Next.js 15 with React 19
    - Database: Supabase (PostgreSQL)
    - Infrastructure: Docker containerization
    """
    
    # Detect technology stack
    detector = TechnologyDetector()
    tech_stack = detector.detect_from_content(sample_content)
    
    # Generate project structure
    generator = ProjectStructureGenerator(Path("./test-project"))
    created_dirs = generator.generate_structure(tech_stack, "Sample Project")
    
    print(f"Generated project structure:")
    for name, path in created_dirs.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
