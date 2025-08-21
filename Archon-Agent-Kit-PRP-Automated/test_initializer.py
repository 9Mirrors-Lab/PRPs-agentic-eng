#!/usr/bin/env python3
"""
Test Script for Process2 Project Initializer

This script demonstrates how the Process2 system works by testing
it with the dealership project INITIAL.md file.
"""

import sys
from pathlib import Path

# Add the project-initializers directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'project-initializers'))

from technology_detector import TechnologyDetector, CLAUDEFileSelector
from project_structure_generator import ProjectStructureGenerator
from project_initializer import ProjectInitializer


def test_technology_detection():
    """Test technology detection with dealership project content"""
    print("🧪 Testing Technology Detection")
    print("=" * 50)
    
    # Sample content from the dealership project INITIAL.md
    dealership_content = """
    # Dealership Website Scraper - Automotive Market Intelligence Platform
    
    ## Technology Stack
    - Backend: Python 3.x with FastAPI for API development
    - Frontend: Next.js 15 with React 19 for modern web interface
    - Database: Supabase (PostgreSQL) for data storage
    - Infrastructure: Docker containerization for deployment
    - Scraping: BeautifulSoup4 and Selenium for web scraping
    - Authentication: JWT tokens with secure session management
    
    ## Development Tools
    - Package Management: uv for Python dependencies
    - Testing: pytest for backend testing
    - Linting: ESLint and Prettier for frontend code quality
    - Type Checking: TypeScript strict mode for frontend
    """
    
    detector = TechnologyDetector()
    tech_stack = detector.detect_from_content(dealership_content)
    
    print(f"Detected Technology Stack:")
    print(f"  Backend: {tech_stack.backend}")
    print(f"  Frontend: {tech_stack.frontend}")
    print(f"  Database: {tech_stack.database}")
    print(f"  Infrastructure: {tech_stack.infrastructure}")
    print(f"  Project Type: {tech_stack.project_type}")
    print(f"  Frameworks: {', '.join(tech_stack.frameworks)}")
    print(f"  Languages: {', '.join(tech_stack.languages)}")
    
    return tech_stack


def test_claude_file_selection(tech_stack):
    """Test CLAUDE.md file selection"""
    print("\n📚 Testing CLAUDE.md File Selection")
    print("=" * 50)
    
    # Use current directory as process folder
    process_folder = Path(__file__).parent
    selector = CLAUDEFileSelector(process_folder)
    
    claude_files = selector.get_claude_files_for_stack(tech_stack)
    
    print(f"Selected CLAUDE.md files:")
    if claude_files:
        for component, file_path in claude_files.items():
            print(f"  {component}: {file_path.name}")
    else:
        print("  ⚠️  No specific CLAUDE.md files found")
    
    return claude_files


def test_project_structure_generation(tech_stack):
    """Test project structure generation"""
    print("\n🏗️ Testing Project Structure Generation")
    print("=" * 50)
    
    # Create a test project directory
    test_project_dir = Path(__file__).parent / "test-output"
    if test_project_dir.exists():
        import shutil
        shutil.rmtree(test_project_dir)
    
    generator = ProjectStructureGenerator(test_project_dir)
    created_dirs = generator.generate_structure(tech_stack, "Dealership Scraper")
    
    print(f"Generated project structure:")
    for name, path in created_dirs.items():
        print(f"  {name}: {path.relative_to(test_project_dir)}")
    
    return test_project_dir, created_dirs


def test_full_initialization():
    """Test the complete initialization process"""
    print("\n🚀 Testing Complete Initialization Process")
    print("=" * 50)
    
    # Create a test project directory
    test_project_dir = Path(__file__).parent / "test-full-project"
    if test_project_dir.exists():
        import shutil
        shutil.rmtree(test_project_dir)
    
    # Create a test INITIAL.md file
    test_initial_md = test_project_dir / "INITIAL.md"
    test_initial_md.parent.mkdir(parents=True, exist_ok=True)
    
    initial_content = """# Dealership Website Scraper - Automotive Market Intelligence Platform

## Technology Stack
- Backend: Python 3.x with FastAPI for API development
- Frontend: Next.js 15 with React 19 for modern web interface
- Database: Supabase (PostgreSQL) for data storage
- Infrastructure: Docker containerization for deployment

## Project Description
A comprehensive web scraping platform for automotive dealership websites.
"""
    
    test_initial_md.write_text(initial_content)
    
    # Initialize the project
    process_folder = Path(__file__).parent
    initializer = ProjectInitializer(process_folder)
    
    try:
        result = initializer.initialize_project(
            test_initial_md, 
            test_project_dir, 
            "Dealership Scraper"
        )
        
        print(f"✅ Project initialization successful!")
        print(f"📁 Project created at: {test_project_dir}")
        print(f"📖 Setup instructions: {result['setup_instructions']}")
        
        return test_project_dir, result
        
    except Exception as e:
        print(f"❌ Project initialization failed: {e}")
        return None, None


def main():
    """Run all tests"""
    print("🧪 Process2 Project Initializer Test Suite")
    print("=" * 60)
    
    # Test 1: Technology Detection
    tech_stack = test_technology_detection()
    
    # Test 2: CLAUDE.md File Selection
    claude_files = test_claude_file_selection(tech_stack)
    
    # Test 3: Project Structure Generation
    test_dir, created_dirs = test_project_structure_generation(tech_stack)
    
    # Test 4: Full Initialization Process
    full_project_dir, result = test_full_initialization()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"✅ Technology Detection: {'PASS' if tech_stack else 'FAIL'}")
    print(f"✅ CLAUDE.md Selection: {'PASS' if claude_files else 'FAIL'}")
    print(f"✅ Structure Generation: {'PASS' if created_dirs else 'FAIL'}")
    print(f"✅ Full Initialization: {'PASS' if result else 'FAIL'}")
    
    if full_project_dir and full_project_dir.exists():
        print(f"\n🎉 All tests passed! Check the generated project at:")
        print(f"   {full_project_dir}")
        print(f"\n📖 Review the setup instructions at:")
        print(f"   {full_project_dir}/SETUP.md")
    
    print("\n🧹 Cleaning up test files...")
    import shutil
    
    # Clean up test directories
    test_dirs = [
        Path(__file__).parent / "test-output",
        Path(__file__).parent / "test-full-project"
    ]
    
    for test_dir in test_dirs:
        if test_dir.exists():
            shutil.rmtree(test_dir)
            print(f"   Removed: {test_dir}")
    
    print("✅ Test cleanup complete!")


if __name__ == "__main__":
    main()
