#!/usr/bin/env python3
"""
Technology Stack Detector for INITIAL.md Files

This module parses INITIAL.md files to detect the technology stack
and determine appropriate CLAUDE.md files and project structure.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class TechnologyStack:
    """Represents the detected technology stack from INITIAL.md"""
    backend: Optional[str] = None
    frontend: Optional[str] = None
    database: Optional[str] = None
    infrastructure: Optional[str] = None
    project_type: str = "unknown"
    frameworks: List[str] = None
    languages: List[str] = None
    
    def __post_init__(self):
        if self.frameworks is None:
            self.frameworks = []
        if self.languages is None:
            self.languages = []
    
    def is_fullstack(self) -> bool:
        """Check if this is a full-stack project"""
        return bool(self.backend and self.frontend)
    
    def is_backend_only(self) -> bool:
        """Check if this is a backend-only project"""
        return bool(self.backend and not self.frontend)
    
    def is_frontend_only(self) -> bool:
        """Check if this is a frontend-only project"""
        return bool(self.frontend and not self.backend)


class TechnologyDetector:
    """Detects technology stack from INITIAL.md content"""
    
    # Technology patterns for detection
    BACKEND_PATTERNS = {
        'python': [
            r'Python\s+3\.?[xX]?',
            r'Flask',
            r'FastAPI',
            r'Django',
            r'uv\s+run',
            r'requirements\.txt',
            r'pyproject\.toml'
        ],
        'java': [
            r'Java\s+\d+',
            r'Maven',
            r'Gradle',
            r'Spring\s+Boot',
            r'JPA',
            r'\.jar'
        ],
        'nodejs': [
            r'Node\.js',
            r'npm\s+run',
            r'yarn',
            r'Express\.js',
            r'package\.json'
        ],
        'go': [
            r'Go\s+\d+',
            r'go\.mod',
            r'go\.sum',
            r'Gin',
            r'Echo'
        ]
    }
    
    FRONTEND_PATTERNS = {
        'nextjs': [
            r'Next\.js\s+\d+',
            r'App\s+Router',
            r'pages\s+router',
            r'next\.config\.js'
        ],
        'react': [
            r'React\s+\d+',
            r'React\.js',
            r'JSX',
            r'useState',
            r'useEffect'
        ],
        'vue': [
            r'Vue\.js',
            r'Vue\s+\d+',
            r'Composition\s+API',
            r'Options\s+API'
        ],
        'astro': [
            r'Astro',
            r'\.astro',
            r'astro\.config'
        ]
    }
    
    DATABASE_PATTERNS = {
        'postgresql': [
            r'PostgreSQL',
            r'postgres',
            r'psql',
            r'pg_'
        ],
        'mysql': [
            r'MySQL',
            r'mysql',
            r'MariaDB'
        ],
        'mongodb': [
            r'MongoDB',
            r'mongodb',
            r'mongo'
        ],
        'supabase': [
            r'Supabase',
            r'supabase',
            r'postgrest'
        ]
    }
    
    INFRASTRUCTURE_PATTERNS = {
        'docker': [
            r'Docker',
            r'docker-compose',
            r'Dockerfile',
            r'containerization'
        ],
        'kubernetes': [
            r'Kubernetes',
            r'k8s',
            r'kubectl'
        ],
        'aws': [
            r'AWS',
            r'Amazon\s+Web\s+Services',
            r'EC2',
            r'S3',
            r'Lambda'
        ],
        'vercel': [
            r'Vercel',
            r'vercel\.com'
        ]
    }
    
    def __init__(self):
        self.content = ""
        self.tech_stack = TechnologyStack()
    
    def detect_from_file(self, file_path: Path) -> TechnologyStack:
        """Detect technology stack from INITIAL.md file"""
        if not file_path.exists():
            raise FileNotFoundError(f"INITIAL.md file not found: {file_path}")
        
        self.content = file_path.read_text(encoding='utf-8')
        return self._detect_all()
    
    def detect_from_content(self, content: str) -> TechnologyStack:
        """Detect technology stack from content string"""
        self.content = content
        return self._detect_all()
    
    def _detect_all(self) -> TechnologyStack:
        """Detect all technology components"""
        self._detect_backend()
        self._detect_frontend()
        self._detect_database()
        self._detect_infrastructure()
        self._determine_project_type()
        self._extract_frameworks()
        self._extract_languages()
        
        return self.tech_stack
    
    def _detect_backend(self):
        """Detect backend technology"""
        for tech, patterns in self.BACKEND_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, self.content, re.IGNORECASE):
                    self.tech_stack.backend = tech
                    return
    
    def _detect_frontend(self):
        """Detect frontend technology"""
        for tech, patterns in self.FRONTEND_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, self.content, re.IGNORECASE):
                    self.tech_stack.frontend = tech
                    return
    
    def _detect_database(self):
        """Detect database technology"""
        for tech, patterns in self.DATABASE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, self.content, re.IGNORECASE):
                    self.tech_stack.database = tech
                    return
    
    def _detect_infrastructure(self):
        """Detect infrastructure technology"""
        for tech, patterns in self.INFRASTRUCTURE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, self.content, re.IGNORECASE):
                    self.tech_stack.infrastructure = tech
                    return
    
    def _determine_project_type(self):
        """Determine the overall project type"""
        if self.tech_stack.is_fullstack():
            self.tech_stack.project_type = "fullstack"
        elif self.tech_stack.is_backend_only():
            self.tech_stack.project_type = "backend"
        elif self.tech_stack.is_frontend_only():
            self.tech_stack.project_type = "frontend"
        else:
            self.tech_stack.project_type = "unknown"
    
    def _extract_frameworks(self):
        """Extract specific frameworks mentioned"""
        framework_patterns = [
            r'FastAPI',
            r'Flask',
            r'Django',
            r'Spring\s+Boot',
            r'Express\.js',
            r'Next\.js\s+\d+',
            r'React\s+\d+',
            r'Vue\.js',
            r'Astro',
            r'Gin',
            r'Echo'
        ]
        
        for pattern in framework_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                self.tech_stack.frameworks.append(match.group(0))
    
    def _extract_languages(self):
        """Extract programming languages mentioned"""
        language_patterns = [
            r'Python\s+3\.?[xX]?',
            r'Java\s+\d+',
            r'TypeScript',
            r'JavaScript',
            r'Go\s+\d+',
            r'Rust'
        ]
        
        for pattern in language_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                self.tech_stack.languages.append(match.group(0))


class CLAUDEFileSelector:
    """Selects appropriate CLAUDE.md files based on technology stack"""
    
    # Mapping of technology to CLAUDE.md files
    CLAUDE_FILE_MAPPING = {
        'python': 'CLAUDE-PYTHON-BASIC.md',
        'java': 'CLAUDE-JAVA-MAVEN.md',
        'nodejs': 'CLAUDE-NODE.md',
        'nextjs': 'CLAUDE-NEXTJS-15.md',
        'react': 'CLAUDE-REACT.md',
        'vue': 'CLAUDE-VUE.md',
        'astro': 'CLAUDE-ASTRO.md',
        'go': 'CLAUDE-GO.md',
        'rust': 'CLAUDE-RUST.md'
    }
    
    def __init__(self, process_folder: Path):
        self.process_folder = process_folder
        self.claude_files_folder = process_folder / 'claude_md_files'
    
    def get_claude_files_for_stack(self, tech_stack: TechnologyStack) -> Dict[str, Path]:
        """Get appropriate CLAUDE.md files for the technology stack"""
        selected_files = {}
        
        # Backend CLAUDE.md
        if tech_stack.backend and tech_stack.backend in self.CLAUDE_FILE_MAPPING:
            backend_file = self.claude_files_folder / self.CLAUDE_FILE_MAPPING[tech_stack.backend]
            if backend_file.exists():
                selected_files['backend'] = backend_file
        
        # Frontend CLAUDE.md
        if tech_stack.frontend and tech_stack.frontend in self.CLAUDE_FILE_MAPPING:
            frontend_file = self.claude_files_folder / self.CLAUDE_FILE_MAPPING[tech_stack.frontend]
            if frontend_file.exists():
                selected_files['frontend'] = frontend_file
        
        # If no specific files found, try to find generic ones
        if not selected_files:
            # Look for any available CLAUDE.md files
            for file in self.claude_files_folder.glob('CLAUDE-*.md'):
                tech_name = file.stem.replace('CLAUDE-', '').lower()
                if tech_name in tech_stack.languages or tech_name in tech_stack.frameworks:
                    selected_files[tech_name] = file
        
        return selected_files
    
    def get_project_structure_template(self, tech_stack: TechnologyStack) -> str:
        """Get the appropriate project structure template"""
        if tech_stack.is_fullstack():
            return "fullstack-python-nextjs"  # Default full-stack template
        elif tech_stack.is_backend_only():
            return f"{tech_stack.backend}-backend"
        elif tech_stack.is_frontend_only():
            return f"{tech_stack.frontend}-frontend"
        else:
            return "generic"
    
    def get_prp_templates(self, tech_stack: TechnologyStack) -> List[str]:
        """Get appropriate PRP templates for the technology stack"""
        templates = []
        
        if tech_stack.backend == 'python':
            templates.append('prp_base.md')  # Python backend template
        elif tech_stack.backend == 'java':
            templates.append('prp_base_java.md')
        
        if tech_stack.frontend == 'nextjs':
            templates.append('prp_base_typescript.md')  # Next.js template
        elif tech_stack.frontend == 'react':
            templates.append('prp_base_react.md')
        
        # If no specific templates found, use generic
        if not templates:
            templates.append('prp_base.md')
        
        return templates


def main():
    """Test the technology detector"""
    # Example usage
    detector = TechnologyDetector()
    
    # Test with sample content
    sample_content = """
    # Sample Project
    
    ## Technology Stack
    - Backend: Python 3.x with FastAPI
    - Frontend: Next.js 15 with React 19
    - Database: Supabase (PostgreSQL)
    - Infrastructure: Docker containerization
    
    ## Development
    Use uv for Python package management.
    """
    
    tech_stack = detector.detect_from_content(sample_content)
    print(f"Detected Technology Stack:")
    print(f"  Backend: {tech_stack.backend}")
    print(f"  Frontend: {tech_stack.frontend}")
    print(f"  Database: {tech_stack.database}")
    print(f"  Infrastructure: {tech_stack.infrastructure}")
    print(f"  Project Type: {tech_stack.project_type}")
    print(f"  Frameworks: {tech_stack.frameworks}")
    print(f"  Languages: {tech_stack.languages}")


if __name__ == "__main__":
    main()
