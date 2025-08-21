# Initialize Project from INITIAL.md (Cursor Version)

## Purpose
Transform an INITIAL.md file into a fully configured project with proper codebase structure, technology-specific CLAUDE.md files, and project setup. This command automates the entire project initialization process for Cursor users.

## Usage
Type this command in Cursor's command palette or chat:
```
Initialize project from INITIAL.md file
```

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

After running the initialization, you'll have:

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
# In Cursor, you can:
1. Open command palette (Cmd/Ctrl + Shift + P)
2. Type: "Initialize project from INITIAL.md"
3. Select the command
4. Choose your INITIAL.md file
5. Watch the automation happen!

# Or manually run:
cd Archon-Agent-Kit-PRP-Automated/project-initializers
python project_initializer.py INITIAL.md --project-root /path/to/new/project
```

## Success Criteria

- [ ] Technology stack correctly detected from INITIAL.md
- [ ] Appropriate CLAUDE.md files copied and customized
- [ ] Project structure generated for detected stack
- [ ] PRP templates configured for technology choices
- [ ] All configuration files properly set up
- [ ] Ready for immediate development with Cursor

## Next Steps After Initialization

1. **Review generated structure** - Ensure it matches your expectations
2. **Customize CLAUDE.md files** - Add project-specific details
3. **Use Cursor's AI features** - Leverage Cursor's built-in AI for project context
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

## Cursor-Specific Benefits

- **Integrated AI**: Use Cursor's built-in AI features with your project context
- **Smart Suggestions**: Get intelligent code completion based on your project structure
- **Context Awareness**: Cursor understands your project's technology stack and patterns
- **Seamless Workflow**: No need to switch between different AI tools

This command transforms your manual, multi-step project setup into a single automated process that understands your technology choices and sets everything up correctly from the start, optimized for Cursor's AI-powered development environment.
