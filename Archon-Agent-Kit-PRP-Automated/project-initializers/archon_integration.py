"""
Archon MCP Integration Module

This module handles integration with the Archon MCP server for:
- Project container creation
- Knowledge base crawling and storage
- Task management and organization
- Knowledge search and retrieval
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ArchonProject:
    """Represents an Archon project container"""
    id: str
    title: str
    description: str
    tech_stack: List[str]
    created_at: str
    status: str = "active"


@dataclass
class ArchonTask:
    """Represents an Archon project task"""
    id: str
    title: str
    description: str
    status: str
    priority: int
    feature: str
    assignee: str = "AI IDE Agent"


class ArchonIntegration:
    """Handles integration with Archon MCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        """
        Initialize Archon integration
        
        Args:
            base_url: Base URL for Archon MCP server
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to Archon MCP server"""
        try:
            response = self.session.get(f"{self.base_url}/api/mcp/health")
            if response.status_code == 200:
                logger.info("✅ Connected to Archon MCP server")
                return True
            else:
                logger.warning(f"⚠️ Archon MCP server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Could not connect to Archon MCP server: {e}")
            return False
    
    def create_project(self, project_data: Dict[str, Any]) -> Optional[ArchonProject]:
        """
        Create a new Archon project container
        
        Args:
            project_data: Project information including title, description, tech_stack
            
        Returns:
            ArchonProject object if successful, None otherwise
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/projects",
                json=project_data
            )
            
            if response.status_code == 201:
                project_info = response.json()
                logger.info(f"✅ Created Archon project: {project_info['title']}")
                return ArchonProject(**project_info)
            else:
                logger.error(f"❌ Failed to create project: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creating project: {e}")
            return None
    
    def crawl_knowledge(self, project_id: str, project_root: Path, 
                       knowledge_sources: List[Dict[str, str]]) -> bool:
        """
        Crawl and store project knowledge in Archon
        
        Args:
            project_id: Archon project ID
            project_root: Path to project root directory
            knowledge_sources: List of knowledge sources to crawl
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Upload project structure and key files
            for source in knowledge_sources:
                source_path = project_root / source['path']
                if source_path.exists():
                    self._upload_knowledge_item(
                        project_id=project_id,
                        file_path=source_path,
                        source_type=source['type'],
                        description=source['description']
                    )
            
            # Crawl project structure
            self._crawl_project_structure(project_id, project_root)
            
            logger.info(f"✅ Successfully crawled knowledge for project {project_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error crawling knowledge: {e}")
            return False
    
    def _upload_knowledge_item(self, project_id: str, file_path: Path, 
                              source_type: str, description: str) -> bool:
        """Upload a single knowledge item to Archon"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f, 'text/plain')}
                data = {
                    'project_id': project_id,
                    'source_type': source_type,
                    'description': description,
                    'tags': [file_path.suffix[1:], source_type]
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/knowledge/upload",
                    files=files,
                    data=data
                )
                
                if response.status_code == 201:
                    logger.debug(f"✅ Uploaded {file_path.name}")
                    return True
                else:
                    logger.warning(f"⚠️ Failed to upload {file_path.name}: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.warning(f"⚠️ Error uploading {file_path.name}: {e}")
            return False
    
    def _crawl_project_structure(self, project_id: str, project_root: Path):
        """Crawl and document project structure"""
        try:
            # Generate project structure overview
            structure_info = {
                'project_id': project_id,
                'structure': self._get_directory_structure(project_root),
                'technology_files': self._identify_technology_files(project_root),
                'configuration_files': self._identify_config_files(project_root)
            }
            
            # Store as knowledge item
            response = self.session.post(
                f"{self.base_url}/api/knowledge/upload",
                json={
                    'project_id': project_id,
                    'content': json.dumps(structure_info, indent=2),
                    'source_type': 'project_structure',
                    'description': f'Project structure analysis for {project_root.name}',
                    'tags': ['structure', 'analysis', 'project_setup']
                }
            )
            
            if response.status_code != 201:
                logger.warning(f"⚠️ Failed to store project structure: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"⚠️ Error crawling project structure: {e}")
    
    def _get_directory_structure(self, root_path: Path, max_depth: int = 3) -> Dict:
        """Get directory structure as nested dictionary"""
        structure = {}
        
        def _scan_directory(path: Path, depth: int = 0):
            if depth > max_depth:
                return
            
            items = []
            for item in sorted(path.iterdir()):
                if item.name.startswith('.') and item.name != '.claude':
                    continue
                    
                if item.is_dir():
                    items.append({
                        'name': item.name,
                        'type': 'directory',
                        'contents': _scan_directory(item, depth + 1)
                    })
                else:
                    items.append({
                        'name': item.name,
                        'type': 'file',
                        'size': item.stat().st_size,
                        'extension': item.suffix
                    })
            
            return items
        
        structure[root_path.name] = _scan_directory(root_path)
        return structure
    
    def _identify_technology_files(self, project_root: Path) -> List[Dict]:
        """Identify technology-specific files in project"""
        tech_files = []
        
        # Common technology files
        tech_patterns = {
            'python': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile'],
            'node': ['package.json', 'package-lock.json', 'yarn.lock'],
            'docker': ['Dockerfile', 'docker-compose.yml', '.dockerignore'],
            'database': ['schema.sql', 'migrations/', 'prisma/'],
            'frontend': ['next.config.js', 'vite.config.js', 'webpack.config.js']
        }
        
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                if '*' in pattern:
                    # Handle glob patterns
                    for file_path in project_root.glob(pattern):
                        tech_files.append({
                            'technology': tech,
                            'file': str(file_path.relative_to(project_root)),
                            'type': 'configuration'
                        })
                else:
                    # Handle exact file names
                    file_path = project_root / pattern
                    if file_path.exists():
                        tech_files.append({
                            'technology': tech,
                            'file': pattern,
                            'type': 'configuration'
                        })
        
        return tech_files
    
    def _identify_config_files(self, project_root: Path) -> List[Dict]:
        """Identify configuration files in project"""
        config_files = []
        
        config_patterns = [
            '.env*', '.gitignore', 'README.md', 'CLAUDE.md',
            'tsconfig.json', 'eslint.config.js', 'prettier.config.js',
            'tailwind.config.js', 'postcss.config.js'
        ]
        
        for pattern in config_patterns:
            if '*' in pattern:
                # Handle glob patterns
                for file_path in project_root.glob(pattern):
                    config_files.append({
                        'file': str(file_path.relative_to(project_root)),
                        'type': 'configuration',
                        'category': self._categorize_config_file(file_path.name)
                    })
            else:
                # Handle exact file names
                file_path = project_root / pattern
                if file_path.exists():
                    config_files.append({
                        'file': pattern,
                        'type': 'configuration',
                        'category': self._categorize_config_file(pattern)
                    })
        
        return config_files
    
    def _categorize_config_file(self, filename: str) -> str:
        """Categorize configuration file by type"""
        if filename.startswith('.env'):
            return 'environment'
        elif filename in ['README.md', 'CLAUDE.md']:
            return 'documentation'
        elif filename in ['.gitignore']:
            return 'version_control'
        elif 'config' in filename.lower():
            return 'framework_config'
        else:
            return 'other'
    
    def search_knowledge(self, project_id: str, query: str, 
                        match_count: int = 5) -> List[Dict]:
        """
        Search project knowledge base
        
        Args:
            project_id: Archon project ID
            query: Search query
            match_count: Maximum number of results
            
        Returns:
            List of matching knowledge items
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/knowledge/search",
                json={
                    'project_id': project_id,
                    'query': query,
                    'match_count': match_count
                }
            )
            
            if response.status_code == 200:
                results = response.json()
                logger.debug(f"✅ Found {len(results)} knowledge items for query: {query}")
                return results
            else:
                logger.warning(f"⚠️ Knowledge search failed: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Error searching knowledge: {e}")
            return []
    
    def create_tasks(self, project_id: str, tasks: List[Dict]) -> List[ArchonTask]:
        """
        Create project tasks in Archon
        
        Args:
            project_id: Archon project ID
            tasks: List of task definitions
            
        Returns:
            List of created ArchonTask objects
        """
        created_tasks = []
        
        try:
            for task_data in tasks:
                response = self.session.post(
                    f"{self.base_url}/api/projects/{project_id}/tasks",
                    json=task_data
                )
                
                if response.status_code == 201:
                    task_info = response.json()
                    created_task = ArchonTask(**task_info)
                    created_tasks.append(created_task)
                    logger.info(f"✅ Created task: {created_task.title}")
                else:
                    logger.warning(f"⚠️ Failed to create task: {response.status_code}")
            
            return created_tasks
            
        except Exception as e:
            logger.error(f"❌ Error creating tasks: {e}")
            return created_tasks
    
    def get_project_tasks(self, project_id: str) -> List[ArchonTask]:
        """
        Get all tasks for a project
        
        Args:
            project_id: Archon project ID
            
        Returns:
            List of project tasks
        """
        try:
            response = self.session.get(f"{self.base_url}/api/projects/{project_id}/tasks")
            
            if response.status_code == 200:
                tasks_data = response.json()
                tasks = [ArchonTask(**task) for task in tasks_data]
                logger.debug(f"✅ Retrieved {len(tasks)} tasks for project {project_id}")
                return tasks
            else:
                logger.warning(f"⚠️ Failed to get tasks: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Error getting tasks: {e}")
            return []
    
    def update_task_status(self, project_id: str, task_id: str, 
                          status: str) -> bool:
        """
        Update task status
        
        Args:
            project_id: Archon project ID
            task_id: Task ID to update
            status: New status
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.put(
                f"{self.base_url}/api/projects/{project_id}/tasks/{task_id}",
                json={'status': status}
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Updated task {task_id} status to {status}")
                return True
            else:
                logger.warning(f"⚠️ Failed to update task status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Error updating task status: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Archon MCP server is available"""
        return self._test_connection()
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information and status"""
        return {
            'base_url': self.base_url,
            'connected': self.is_available(),
            'api_key_configured': bool(self.api_key)
        }


class KnowledgeGenerator:
    """Generates intelligent next steps using Archon knowledge"""
    
    def __init__(self, archon: ArchonIntegration):
        self.archon = archon
    
    def generate_next_steps(self, project_id: str, tech_stack: Dict, 
                           project_context: Dict) -> List[Dict]:
        """
        Generate intelligent next steps with plain English context
        
        Args:
            project_id: Archon project ID
            tech_stack: Detected technology stack
            project_context: Project requirements and context
            
        Returns:
            List of next step suggestions with commands and context
        """
        # Search knowledge base for relevant patterns
        knowledge_items = self.archon.search_knowledge(
            project_id=project_id,
            query=f"{tech_stack.get('backend', '')} {tech_stack.get('frontend', '')} project setup patterns",
            match_count=5
        )
        
        # Generate next steps based on technology stack and context
        next_steps = []
        
        # Core development steps
        if tech_stack.get('backend'):
            next_steps.extend(self._generate_backend_steps(tech_stack, project_context))
        
        if tech_stack.get('frontend'):
            next_steps.extend(self._generate_frontend_steps(tech_stack, project_context))
        
        # Database and infrastructure steps
        if tech_stack.get('database'):
            next_steps.extend(self._generate_database_steps(tech_stack, project_context))
        
        if tech_stack.get('infrastructure'):
            next_steps.extend(self._generate_infrastructure_steps(tech_stack, project_context))
        
        # Quality and operations steps
        next_steps.extend(self._generate_quality_steps(tech_stack, project_context))
        
        return next_steps
    
    def _generate_backend_steps(self, tech_stack: Dict, context: Dict) -> List[Dict]:
        """Generate backend-specific next steps"""
        steps = []
        
        if 'Python' in tech_stack.get('backend', ''):
            steps.append({
                'command': f'/prp-base-create "Implement {context.get("project_name", "core")} API endpoints with FastAPI"',
                'what_it_does': f'Creates a comprehensive PRP for building the main API functionality using FastAPI, including data models, endpoints, validation, and error handling for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A detailed PRP with FastAPI implementation blueprint, Pydantic models, and API endpoint specifications.',
                'category': 'Backend Development',
                'priority': 1
            })
            
            steps.append({
                'command': f'/prp-base-create "Set up authentication and authorization system"',
                'what_it_does': f'Creates a PRP for implementing secure user authentication using JWT tokens, role-based access control, and user management for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A complete authentication PRP with user management, token handling, and security best practices.',
                'category': 'Backend Development',
                'priority': 2
            })
        
        elif 'Node.js' in tech_stack.get('backend', ''):
            steps.append({
                'command': f'/prp-base-create "Build Express.js API server for {context.get("project_name", "core functionality")}"',
                'what_it_does': f'Creates a PRP for building a Node.js/Express.js API server with proper middleware, routing, and error handling for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A comprehensive PRP with Express.js server setup, API routes, and middleware configuration.',
                'category': 'Backend Development',
                'priority': 1
            })
        
        return steps
    
    def _generate_frontend_steps(self, tech_stack: Dict, context: Dict) -> List[Dict]:
        """Generate frontend-specific next steps"""
        steps = []
        
        if 'Next.js' in tech_stack.get('frontend', ''):
            steps.append({
                'command': f'/prp-base-create "Create Next.js dashboard interface for {context.get("project_name", "data management")}"',
                'what_it_does': f'Creates a PRP for building a modern, responsive dashboard using Next.js with React components, state management, and data visualization for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A complete frontend PRP with Next.js architecture, component design, and user experience specifications.',
                'category': 'Frontend Development',
                'priority': 1
            })
            
            steps.append({
                'command': f'/prp-base-create "Implement responsive design and mobile optimization"',
                'what_it_does': f'Creates a PRP for implementing responsive design patterns, mobile-first approach, and cross-device compatibility for your {context.get("project_name", "project")} interface.',
                'expected_outcome': 'A comprehensive design PRP with responsive layouts, mobile optimization, and accessibility considerations.',
                'category': 'Frontend Development',
                'priority': 2
            })
        
        elif 'React' in tech_stack.get('frontend', ''):
            steps.append({
                'command': f'/prp-base-create "Build React application with component architecture"',
                'what_it_does': f'Creates a PRP for building a React application with proper component structure, state management, and modern React patterns for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A complete React PRP with component design, state management strategy, and application architecture.',
                'category': 'Frontend Development',
                'priority': 1
            })
        
        return steps
    
    def _generate_database_steps(self, tech_stack: Dict, context: Dict) -> List[Dict]:
        """Generate database-specific next steps"""
        steps = []
        
        if 'PostgreSQL' in tech_stack.get('database', ''):
            steps.append({
                'command': f'/prp-base-create "Design PostgreSQL database schema for {context.get("project_name", "data storage")}"',
                'what_it_does': f'Creates a PRP for designing the database structure, including tables, relationships, indexes, and data validation rules for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A comprehensive database PRP with schema design, migration scripts, and data integrity constraints.',
                'category': 'Database Design',
                'priority': 1
            })
        
        elif 'MongoDB' in tech_stack.get('database', ''):
            steps.append({
                'command': f'/prp-base-create "Design MongoDB data models and collections"',
                'what_it_does': f'Creates a PRP for designing MongoDB collections, data models, and indexing strategies for your {context.get("project_name", "project")}.',
                'expected_outcome': 'A complete MongoDB PRP with collection design, data modeling, and performance optimization.',
                'category': 'Database Design',
                'priority': 1
            })
        
        return steps
    
    def _generate_infrastructure_steps(self, tech_stack: Dict, context: Dict) -> List[Dict]:
        """Generate infrastructure-specific next steps"""
        steps = []
        
        if 'Docker' in tech_stack.get('infrastructure', ''):
            steps.append({
                'command': f'/prp-base-create "Set up Docker containerization and deployment"',
                'what_it_does': f'Creates a PRP for containerizing your {context.get("project_name", "project")} with Docker, including multi-stage builds, environment configuration, and deployment strategies.',
                'expected_outcome': 'A comprehensive Docker PRP with containerization strategy, deployment pipeline, and environment management.',
                'category': 'Infrastructure',
                'priority': 2
            })
        
        return steps
    
    def _generate_quality_steps(self, tech_stack: Dict, context: Dict) -> List[Dict]:
        """Generate quality and operations next steps"""
        steps = []
        
        steps.append({
            'command': f'/prp-base-create "Implement testing strategy and quality assurance"',
            'what_it_does': f'Creates a PRP for implementing comprehensive testing including unit tests, integration tests, and end-to-end testing for your {context.get("project_name", "project")}.',
            'expected_outcome': 'A complete testing PRP with test strategy, framework selection, and quality assurance processes.',
            'category': 'Quality Assurance',
            'priority': 3
        })
        
        steps.append({
            'command': f'/prp-base-create "Set up CI/CD pipeline and deployment automation"',
            'what_it_does': f'Creates a PRP for implementing continuous integration and deployment automation for your {context.get("project_name", "project")}, including testing, building, and deployment workflows.',
            'expected_outcome': 'A comprehensive CI/CD PRP with pipeline design, automation strategies, and deployment processes.',
            'category': 'Operations',
            'priority': 4
        })
        
        return steps
