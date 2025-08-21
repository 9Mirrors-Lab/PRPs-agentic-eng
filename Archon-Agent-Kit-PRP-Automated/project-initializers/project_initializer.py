#!/usr/bin/env python3
"""
Project Initializer with Archon MCP Integration

Main orchestrator that reads INITIAL.md, detects technology stack,
generates complete project structure with appropriate CLAUDE.md files,
and integrates with Archon MCP for knowledge management and task tracking.
"""

import shutil
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional

from technology_detector import TechnologyDetector, CLAUDEFileSelector
from project_structure_generator import ProjectStructureGenerator
from archon_integration import ArchonIntegration, KnowledgeGenerator


class ProjectInitializer:
    """Main project initialization orchestrator with Archon MCP integration"""
    
    def __init__(self, process_folder: Path, archon_url: str = "http://localhost:8000", archon_api_key: Optional[str] = None):
        self.process_folder = process_folder
        self.detector = TechnologyDetector()
        self.claude_selector = CLAUDEFileSelector(process_folder)
        self.structure_generator = None  # Will be set when project root is known
        
        # Initialize Archon integration
        self.archon = ArchonIntegration(base_url=archon_url, api_key=archon_api_key)
        self.knowledge_generator = KnowledgeGenerator(self.archon)
        self.archon_project_id = None
    
    def initialize_project(self, initial_md_path: Path, project_root: Path, project_name: Optional[str] = None) -> Dict:
        """Initialize a complete project from INITIAL.md"""
        
        print(f"🚀 Initializing project from {initial_md_path}")
        print(f"📁 Project root: {project_root}")
        
        # Step 1: Detect technology stack
        print("\n🔍 Step 1: Detecting technology stack...")
        tech_stack = self.detector.detect_from_file(initial_md_path)
        self._print_tech_stack(tech_stack)
        
        # Step 2: Select appropriate CLAUDE.md files
        print("\n📚 Step 2: Selecting CLAUDE.md files...")
        claude_files = self.claude_selector.get_claude_files_for_stack(tech_stack)
        self._print_claude_files(claude_files)
        
        # Step 3: Generate project structure
        print("\n🏗️ Step 3: Generating project structure...")
        self.structure_generator = ProjectStructureGenerator(project_root)
        created_dirs = self.structure_generator.generate_structure(tech_stack, project_name or project_root.name)
        self._print_project_structure(created_dirs)
        
        # Step 4: Copy and customize CLAUDE.md files
        print("\n📋 Step 4: Setting up CLAUDE.md files...")
        claude_setup = self._setup_claude_files(claude_files, tech_stack, project_root)
        
        # Step 5: Copy PRP templates
        print("\n📝 Step 5: Setting up PRP templates...")
        prp_setup = self._setup_prp_templates(tech_stack, project_root)
        
        # Step 6: Copy INITIAL.md to project
        print("\n📄 Step 6: Copying project specification...")
        self._copy_initial_md(initial_md_path, project_root)
        
        # Step 7: Create setup instructions
        print("\n📖 Step 7: Creating setup instructions...")
        setup_instructions = self._create_setup_instructions(tech_stack, project_name or project_root.name)
        
        # Step 8: Integrate with Archon MCP (if available)
        print("\n🔗 Step 8: Integrating with Archon MCP...")
        archon_setup = self._setup_archon_integration(tech_stack, project_root, project_name or project_root.name)
        
        print(f"\n✅ Project initialization complete!")
        print(f"📁 Project created at: {project_root}")
        
        if self.archon_project_id:
            print(f"🔗 Archon project created: {self.archon_project_id}")
            print(f"📚 Knowledge base ready for next steps generation")
        
        return {
            'tech_stack': tech_stack,
            'claude_files': claude_setup,
            'project_structure': created_dirs,
            'prp_templates': prp_setup,
            'setup_instructions': setup_instructions,
            'archon_integration': archon_setup
        }
    
    def _print_tech_stack(self, tech_stack):
        """Print detected technology stack"""
        print(f"  Backend: {tech_stack.backend or 'None'}")
        print(f"  Frontend: {tech_stack.frontend or 'None'}")
        print(f"  Database: {tech_stack.database or 'None'}")
        print(f"  Infrastructure: {tech_stack.infrastructure or 'None'}")
        print(f"  Project Type: {tech_stack.project_type}")
        print(f"  Frameworks: {', '.join(tech_stack.frameworks) if tech_stack.frameworks else 'None'}")
        print(f"  Languages: {', '.join(tech_stack.languages) if tech_stack.languages else 'None'}")
    
    def _print_claude_files(self, claude_files: Dict[str, Path]):
        """Print selected CLAUDE.md files"""
        if not claude_files:
            print("  ⚠️  No specific CLAUDE.md files found, will use generic templates")
        else:
            for component, file_path in claude_files.items():
                print(f"  {component}: {file_path.name}")
    
    def _print_project_structure(self, created_dirs: Dict[str, Path]):
        """Print created project structure"""
        print(f"  Created {len(created_dirs)} directories:")
        for name, path in created_dirs.items():
            print(f"    {name}: {path.relative_to(self.structure_generator.project_root)}")
    
    def _setup_claude_files(self, claude_files: Dict[str, Path], tech_stack, project_root: Path) -> Dict[str, Path]:
        """Set up CLAUDE.md files in the project"""
        setup_results = {}
        
        for component, source_file in claude_files.items():
            if component == 'backend':
                target_dir = project_root / 'backend'
                target_file = target_dir / 'CLAUDE.md'
            elif component == 'frontend':
                target_dir = project_root / 'frontend'
                target_file = target_dir / 'CLAUDE.md'
            else:
                # Generic component, place in root
                target_file = project_root / f'CLAUDE-{component.upper()}.md'
            
            # Ensure target directory exists
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy and customize the file
            self._customize_claude_file(source_file, target_file, tech_stack, component)
            setup_results[component] = target_file
            
            print(f"    ✅ {component}: {target_file.relative_to(project_root)}")
        
        return setup_results
    
    def _customize_claude_file(self, source_file: Path, target_file: Path, tech_stack, component: str):
        """Customize CLAUDE.md file with project-specific information"""
        content = source_file.read_text(encoding='utf-8')
        
        # Add project-specific header
        project_header = f"""# CLAUDE.md - {component.title()} Development Guidelines

> **Auto-generated from {source_file.name}**
> 
> This file contains development guidelines specific to the {component} component.
> 
> **Project Type**: {tech_stack.project_type.title()}
> **Technology**: {getattr(tech_stack, component, 'Not specified')}
> 
> ---
> 
"""
        
        customized_content = project_header + content
        
        # Write customized content
        target_file.write_text(customized_content, encoding='utf-8')
    
    def _setup_prp_templates(self, tech_stack, project_root: Path) -> Dict[str, Path]:
        """Set up PRP templates in the project"""
        prp_templates_dir = self.process_folder / 'PRPs' / 'templates'
        project_prp_dir = project_root / 'PRPs' / 'templates'
        
        # Create PRP templates directory
        project_prp_dir.mkdir(parents=True, exist_ok=True)
        
        # Get appropriate templates for the technology stack
        template_names = self.claude_selector.get_prp_templates(tech_stack)
        
        copied_templates = {}
        for template_name in template_names:
            source_template = prp_templates_dir / template_name
            if source_template.exists():
                target_template = project_prp_dir / template_name
                shutil.copy2(source_template, target_template)
                copied_templates[template_name] = target_template
                print(f"    ✅ PRP Template: {template_name}")
            else:
                print(f"    ⚠️  PRP Template not found: {template_name}")
        
        # Copy the entire PRPs folder structure for reference
        prp_source = self.process_folder / 'PRPs'
        prp_target = project_root / 'PRPs'
        
        if prp_source.exists():
            # Copy everything except templates (we already handled those)
            for item in prp_source.iterdir():
                if item.name != 'templates':
                    if item.is_dir():
                        shutil.copytree(item, prp_target / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, prp_target / item.name)
        
        return copied_templates
    
    def _copy_initial_md(self, source_path: Path, project_root: Path):
        """Copy INITIAL.md to project root"""
        target_path = project_root / 'INITIAL.md'
        shutil.copy2(source_path, target_path)
        print(f"    ✅ Project specification: INITIAL.md")
    
    def _create_setup_instructions(self, tech_stack, project_name: str) -> str:
        """Create setup instructions for the user"""
        instructions = f"""# Setup Instructions for {project_name}

## 🚀 Quick Start

Your project has been automatically initialized with the following structure:

**Project Type**: {tech_stack.project_type.title()}
**Technology Stack**: {', '.join(filter(None, [tech_stack.backend, tech_stack.frontend, tech_stack.database, tech_stack.infrastructure]))}

## 📋 Next Steps

### 1. Review Project Structure
- Check the generated directories and files
- Review the `CLAUDE.md` files for development guidelines
- Examine the PRP templates for feature development

### 2. Environment Setup
"""
        
        if tech_stack.backend == 'python':
            instructions += """
**Backend (Python)**
```bash
cd backend
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install dependencies
uv sync
# Run tests
uv run pytest
```
"""
        
        if tech_stack.frontend == 'nextjs':
            instructions += """
**Frontend (Next.js)**
```bash
cd frontend
# Install dependencies
npm install
# Start development server
npm run dev
```
"""
        
        if tech_stack.infrastructure == 'docker':
            instructions += """
**Full Stack (Docker)**
```bash
# Start all services
docker-compose up -d
# View logs
docker-compose logs -f
# Stop services
docker-compose down
```
"""
        
        instructions += f"""
### 3. Initialize Claude
Use the `/prime-core` command to initialize Claude with your project context.

### 4. Start Development
- Create your first PRP using the appropriate template
- Follow the validation loops in the PRP templates
- Use the component-specific CLAUDE.md files for guidance

## 🔧 Customization

- **CLAUDE.md files**: Customize with project-specific details
- **PRP templates**: Modify validation commands and testing frameworks
- **Project structure**: Add or modify directories as needed

## 📚 Documentation

- **INITIAL.md**: Your original project specification
- **CLAUDE.md**: Development guidelines and patterns
- **PRP templates**: Feature development templates
- **README.md**: Project overview and setup instructions

## 🆘 Troubleshooting

If you encounter issues:

1. **Check technology stack detection**: Review the detected stack in the root CLAUDE.md
2. **Verify file paths**: Ensure all generated files are in the expected locations
3. **Review CLAUDE.md files**: Check for component-specific setup requirements
4. **Check dependencies**: Verify required tools and versions are installed

## 🎯 Success Criteria

Your project is ready when:
- [ ] All directories and files are generated
- [ ] CLAUDE.md files contain appropriate guidelines
- [ ] PRP templates are available for feature development
- [ ] `/prime-core` command works correctly
- [ ] You can run basic setup commands for each component

Happy coding! 🚀
"""
        
        # Write instructions to project
        instructions_path = self.structure_generator.project_root / 'SETUP.md'
        instructions_path.write_text(instructions, encoding='utf-8')
        
        return instructions_path
    
    def _setup_archon_integration(self, tech_stack, project_root: Path, project_name: str) -> Dict:
        """Set up Archon MCP integration for the project"""
        setup_results = {
            'archon_available': False,
            'project_created': False,
            'knowledge_crawled': False,
            'tasks_created': False
        }
        
        # Check if Archon is available
        if not self.archon.is_available():
            print("    ⚠️  Archon MCP server not available, skipping integration")
            return setup_results
        
        setup_results['archon_available'] = True
        print("    ✅ Archon MCP server connected")
        
        try:
            # Create Archon project container
            project_data = {
                'title': project_name,
                'description': f'Project initialized from INITIAL.md with {tech_stack.project_type} architecture',
                'tech_stack': [
                    tech_stack.backend or 'No backend',
                    tech_stack.frontend or 'No frontend', 
                    tech_stack.database or 'No database',
                    tech_stack.infrastructure or 'No infrastructure'
                ]
            }
            
            archon_project = self.archon.create_project(project_data)
            if archon_project:
                self.archon_project_id = archon_project.id
                setup_results['project_created'] = True
                print(f"    ✅ Archon project created: {archon_project.title}")
                
                # Crawl and store project knowledge
                knowledge_sources = self._prepare_knowledge_sources(project_root, tech_stack)
                if self.archon.crawl_knowledge(self.archon_project_id, project_root, knowledge_sources):
                    setup_results['knowledge_crawled'] = True
                    print("    ✅ Project knowledge crawled and stored")
                
                # Create initial project tasks
                initial_tasks = self._create_initial_tasks(tech_stack, project_name)
                if self.archon.create_tasks(self.archon_project_id, initial_tasks):
                    setup_results['tasks_created'] = True
                    print("    ✅ Initial project tasks created")
                
            else:
                print("    ⚠️  Failed to create Archon project")
                
        except Exception as e:
            print(f"    ⚠️  Error during Archon integration: {e}")
        
        return setup_results
    
    def _prepare_knowledge_sources(self, project_root: Path, tech_stack) -> List[Dict[str, str]]:
        """Prepare list of knowledge sources to crawl"""
        sources = []
        
        # Key project files
        key_files = [
            'INITIAL.md', 'README.md', 'SETUP.md', '.gitignore'
        ]
        
        for file_name in key_files:
            file_path = project_root / file_name
            if file_path.exists():
                sources.append({
                    'path': file_name,
                    'type': 'project_specification',
                    'description': f'Project {file_name.lower()} file'
                })
        
        # Technology-specific files
        if tech_stack.backend:
            backend_dir = project_root / 'backend'
            if backend_dir.exists():
                sources.append({
                    'path': 'backend/CLAUDE.md',
                    'type': 'backend_guidelines',
                    'description': 'Backend development guidelines'
                })
        
        if tech_stack.frontend:
            frontend_dir = project_root / 'frontend'
            if frontend_dir.exists():
                sources.append({
                    'path': 'frontend/CLAUDE.md',
                    'type': 'frontend_guidelines',
                    'description': 'Frontend development guidelines'
                })
        
        # Root CLAUDE.md
        root_claude = project_root / 'CLAUDE.md'
        if root_claude.exists():
            sources.append({
                'path': 'CLAUDE.md',
                'type': 'project_guidelines',
                'description': 'Root project development guidelines'
            })
        
        return sources
    
    def _create_initial_tasks(self, tech_stack, project_name: str) -> List[Dict]:
        """Create initial project tasks in Archon"""
        tasks = []
        
        # Core setup task
        tasks.append({
            'title': f'Complete {project_name} project setup',
            'description': f'Finalize project initialization and prepare for development',
            'status': 'todo',
            'priority': 1,
            'feature': 'project_setup'
        })
        
        # Technology-specific tasks
        if tech_stack.backend:
            tasks.append({
                'title': f'Set up {tech_stack.backend} backend environment',
                'description': f'Configure {tech_stack.backend} development environment, dependencies, and basic structure',
                'status': 'todo',
                'priority': 2,
                'feature': 'backend_setup'
            })
        
        if tech_stack.frontend:
            tasks.append({
                'title': f'Set up {tech_stack.frontend} frontend environment',
                'description': f'Configure {tech_stack.frontend} development environment, dependencies, and basic structure',
                'status': 'todo',
                'priority': 2,
                'feature': 'frontend_setup'
            })
        
        if tech_stack.database:
            tasks.append({
                'title': f'Configure {tech_stack.database} database',
                'description': f'Set up {tech_stack.database} database connection, schema, and configuration',
                'status': 'todo',
                'priority': 3,
                'feature': 'database_setup'
            })
        
        # Development workflow task
        tasks.append({
            'title': 'Run /prime-core and generate next steps',
            'description': 'Initialize Claude with project context and generate intelligent next steps using Archon knowledge',
            'status': 'todo',
            'priority': 1,
            'feature': 'workflow_setup'
        })
        
        return tasks


def main():
    """Command-line interface for project initialization"""
    parser = argparse.ArgumentParser(description='Initialize project from INITIAL.md')
    parser.add_argument('initial_md', help='Path to INITIAL.md file')
    parser.add_argument('--project-root', '-o', help='Output directory for project (default: current directory)')
    parser.add_argument('--project-name', '-n', help='Name for the project (default: directory name)')
    parser.add_argument('--process-folder', '-p', default='.', help='Path to Process folder (default: current directory)')
    parser.add_argument('--archon-url', '-a', default='http://localhost:8000', help='Archon MCP server URL (default: http://localhost:8000)')
    parser.add_argument('--archon-api-key', '-k', help='Archon MCP server API key (optional)')
    
    args = parser.parse_args()
    
    # Resolve paths
    initial_md_path = Path(args.initial_md).resolve()
    process_folder = Path(args.process_folder).resolve()
    
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        project_root = Path.cwd()
    
    project_name = args.project_name or project_root.name
    
    # Validate inputs
    if not initial_md_path.exists():
        print(f"❌ Error: INITIAL.md file not found: {initial_md_path}")
        return 1
    
    if not process_folder.exists():
        print(f"❌ Error: Process folder not found: {process_folder}")
        return 1
    
    # Initialize project
    try:
        initializer = ProjectInitializer(
            process_folder, 
            archon_url=args.archon_url,
            archon_api_key=args.archon_api_key
        )
        result = initializer.initialize_project(initial_md_path, project_root, project_name)
        
        print(f"\n🎉 Project '{project_name}' initialized successfully!")
        print(f"📁 Location: {project_root}")
        print(f"📖 Setup instructions: {result['setup_instructions']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error initializing project: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
