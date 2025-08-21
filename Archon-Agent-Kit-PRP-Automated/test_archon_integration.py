#!/usr/bin/env python3
"""
Test Script for Process2 Archon MCP Integration

This script demonstrates the new Archon MCP integration features
including project creation, knowledge crawling, and next steps generation.
"""

import sys
from pathlib import Path

# Add project-initializers to path
sys.path.insert(0, str(Path(__file__).parent / 'project-initializers'))

from archon_integration import ArchonIntegration, KnowledgeGenerator
from technology_detector import TechnologyDetector
from project_structure_generator import ProjectStructureGenerator


def test_archon_integration():
    """Test the Archon MCP integration functionality"""
    
    print("🧪 Testing Process2 Archon MCP Integration")
    print("=" * 50)
    
    # Test 1: Archon Connection
    print("\n1️⃣ Testing Archon MCP Connection...")
    archon = ArchonIntegration(base_url="http://localhost:8000")
    
    if archon.is_available():
        print("✅ Archon MCP server connected successfully")
        print(f"   URL: {archon.base_url}")
        print(f"   API Key configured: {bool(archon.api_key)}")
    else:
        print("⚠️  Archon MCP server not available")
        print("   This is expected if you don't have Archon running")
        print("   Process2 will work without Archon integration")
    
    # Test 2: Technology Detection
    print("\n2️⃣ Testing Technology Detection...")
    detector = TechnologyDetector()
    
    # Sample INITIAL.md content for testing
    sample_content = """
    # Dealership Scraper System
    
    ## Technology Stack
    - Backend: Python with FastAPI
    - Frontend: Next.js 15 + React 19
    - Database: PostgreSQL with Supabase
    - Infrastructure: Docker
    
    ## Features
    - Web scraping for dealership websites
    - Data extraction and storage
    - RESTful API endpoints
    - Dashboard interface
    """
    
    # Create temporary INITIAL.md for testing
    test_initial = Path("test_INITIAL.md")
    test_initial.write_text(sample_content)
    
    try:
        tech_stack = detector.detect_from_file(test_initial)
        print("✅ Technology stack detected successfully:")
        print(f"   Backend: {tech_stack.backend}")
        print(f"   Frontend: {tech_stack.frontend}")
        print(f"   Database: {tech_stack.database}")
        print(f"   Infrastructure: {tech_stack.infrastructure}")
        print(f"   Project Type: {tech_stack.project_type}")
    finally:
        # Clean up test file
        test_initial.unlink(missing_ok=True)
    
    # Test 3: Project Structure Generation
    print("\n3️⃣ Testing Project Structure Generation...")
    test_project_root = Path("test_project")
    
    try:
        generator = ProjectStructureGenerator(test_project_root)
        created_dirs = generator.generate_structure(tech_stack, "dealership-scraper")
        
        print("✅ Project structure generated successfully:")
        for name, path in created_dirs.items():
            print(f"   {name}: {path.relative_to(test_project_root)}")
        
        # Test 4: Knowledge Generation (if Archon available)
        if archon.is_available():
            print("\n4️⃣ Testing Knowledge Generation...")
            
            # Simulate project creation
            project_data = {
                'title': 'Dealership Scraper System',
                'description': 'Python FastAPI + Next.js dealership data scraping system',
                'tech_stack': ['Python', 'FastAPI', 'Next.js', 'React', 'PostgreSQL', 'Docker']
            }
            
            # Note: This would create a real project in Archon
            print("   (Skipping actual project creation for demo)")
            print("   In real usage, this would:")
            print("   - Create Archon project container")
            print("   - Crawl and store project knowledge")
            print("   - Create initial tasks")
            
            # Test knowledge generator
            knowledge_gen = KnowledgeGenerator(archon)
            print("✅ Knowledge generator initialized successfully")
            
        else:
            print("\n4️⃣ Skipping Knowledge Generation (Archon not available)")
        
        print("\n5️⃣ Testing Next Steps Generation...")
        print("   In real usage, /generate-next-steps would:")
        print("   - Search Archon knowledge base")
        print("   - Generate context-rich commands")
        print("   - Provide plain English explanations")
        print("   - Tailor suggestions to your tech stack")
        
    finally:
        # Clean up test project
        if test_project_root.exists():
            import shutil
            shutil.rmtree(test_project_root)
    
    print("\n🎉 Process2 Archon MCP Integration Test Complete!")
    print("\n📋 Summary of New Features:")
    print("   ✅ Archon MCP server integration")
    print("   ✅ Automatic project container creation")
    print("   ✅ Intelligent knowledge crawling")
    print("   ✅ Enhanced next steps generation")
    print("   ✅ Project task management")
    print("   ✅ Context-rich command suggestions")
    
    print("\n🚀 To use these features:")
    print("   1. Start Archon MCP server")
    print("   2. Run /initialize-project with --archon-url")
    print("   3. Use /generate-next-steps after /prime-core")
    print("   4. Enjoy intelligent, context-aware guidance!")


if __name__ == "__main__":
    test_archon_integration()
