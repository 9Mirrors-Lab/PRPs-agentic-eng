# Initialize Project from INITIAL.md

## Purpose
Transform an INITIAL.md file into a fully configured project with proper codebase structure, technology-specific CLAUDE.md files, and project setup. This command automates the entire project initialization process.

## Usage
/initialize-project [INITIAL.md file path]

## What It Does

### 1. Technology Stack Detection
- Parse INITIAL.md for technology stack information
- Detect backend technologies (Python, Java, Node.js, etc.)
- Detect frontend technologies (Next.js, React, Vue, etc.)
- Detect database and infrastructure choices
- Identify project type (backend-only, frontend-only, full-stack)

### 2. CLAUDE.md File Selection & Customization
- Automatically select appropriate technology-specific CLAUDE.md files
- Copy relevant files to project directories
- Customize with project-specific details from INITIAL.md
- Create root CLAUDE.md with project overview

### 3. Project Structure Generation
- Generate appropriate directory structure based on detected stack
- Create initial scaffolding files
- Set up configuration files
- Initialize version control structure

### 4. PRP Template Configuration
- Select appropriate PRP templates for the technology stack
- Customize validation commands and testing frameworks
- Set up build system configurations

## Technology Detection Examples

### Python Backend + Next.js Frontend (Your Dealership Project)
```
Detected Stack:
- Backend: Python (Flask/FastAPI)
- Frontend: Next.js 15 + React 19
- Database: Supabase (PostgreSQL)
- Infrastructure: Docker

Actions:
- Copy CLAUDE-PYTHON-BASIC.md → backend/CLAUDE.md
- Copy CLAUDE-NEXTJS-15.md → frontend/CLAUDE.md
- Create root CLAUDE.md with project overview
- Generate full-stack project structure
```

### Python Backend Only
```
Detected Stack:
- Backend: Python (FastAPI)
- Database: PostgreSQL
- Infrastructure: Docker

Actions:
- Copy CLAUDE-PYTHON-BASIC.md → CLAUDE.md
- Generate Python backend structure
- Set up Python-specific PRP templates
```

### Next.js Frontend Only
```
Detected Stack:
- Frontend: Next.js 15 + React 19
- Styling: Tailwind CSS
- Infrastructure: Vercel

Actions:
- Copy CLAUDE-NEXTJS-15.md → CLAUDE.md
- Generate Next.js project structure
- Set up React/TypeScript PRP templates
```

## Output Structure

After running `/initialize-project`, you'll have:

```
your-project/
├── CLAUDE.md                    # Project overview + cross-cutting concerns
├── INITIAL.md                   # Your project specification
├── SETUP.md                     # Step-by-step setup instructions
├── backend/                     # If backend detected
│   ├── CLAUDE.md               # Backend-specific guidelines
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/                    # If frontend detected
│   ├── CLAUDE.md               # Frontend-specific guidelines
│   ├── src/
│   ├── tests/
│   └── package.json
├── docker-compose.yml           # If Docker detected
├── .gitignore
└── README.md
```

## Implementation

This command uses the Python-based project initializer in `Archon-Agent-Kit-PRP-Automated/project-initializers/`:

- **`technology_detector.py`**: Detects technology stack from INITIAL.md
- **`project_structure_generator.py`**: Generates appropriate project structure
- **`project_initializer.py`**: Main orchestrator that ties everything together

## Usage Examples

```bash
# Initialize from current directory's INITIAL.md
/initialize-project INITIAL.md

# Initialize from specific path
/initialize-project /path/to/project/INITIAL.md

# Initialize with custom project name
/initialize-project INITIAL.md --name "my-awesome-project"
```

## Success Criteria

- [ ] Technology stack correctly detected from INITIAL.md
- [ ] Appropriate CLAUDE.md files copied and customized
- [ ] Project structure generated for detected stack
- [ ] PRP templates configured for technology choices
- [ ] All configuration files properly set up
- [ ] Ready for immediate development with `/prime-core`

## Next Steps After Initialization

1. **Review generated structure** - Ensure it matches your expectations
2. **Customize CLAUDE.md files** - Add project-specific details
3. **Run `/prime-core`** - Initialize Claude with the project context
4. **Create your first PRP** - Start building features

## Error Handling

- **Invalid INITIAL.md**: Clear error message with format requirements
- **Unsupported technology**: Warning with fallback to generic template
- **File conflicts**: Automatic resolution or user choice
- **Missing dependencies**: Clear instructions for manual setup

## Manual Execution

If you prefer to run the initializer manually:

```bash
cd Archon-Agent-Kit-PRP-Automated/project-initializers
python project_initializer.py INITIAL.md --project-root /path/to/new/project
```

This command transforms your manual, multi-step project setup into a single automated process that understands your technology choices and sets everything up correctly from the start.
