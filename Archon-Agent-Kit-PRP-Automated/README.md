# Archon-Agent-Kit-PRP-Automated - Enhanced AI Engineering Framework with Archon MCP Integration

## 🚀 What's New in Archon-Agent-Kit-PRP-Automated
## 🤖 **AI Choice Selection**

Archon-Agent-Kit-PRP-Automated supports **multiple AI coding assistants**! Choose your preferred AI tool:

- **Claude**: Use `.claude/commands/` directory
- **Cursor**: Use `.cursor/commands/` directory  
- **Other AIs**: Adapt commands from either directory

**See `AI_CHOICE.md` for detailed instructions for each AI.**

---

Archon-Agent-Kit-PRP-Automated is an enhanced version of the original Process folder that **automates project initialization** from `INITIAL.md` files and **integrates with Archon MCP** for centralized knowledge management and intelligent guidance. Instead of manually copying files and setting up project structure, Archon-Agent-Kit-PRP-Automated intelligently detects your technology stack, sets everything up automatically, and provides context-rich next steps through Archon's knowledge base.

## 🔄 **Enhanced Workflow vs. Original**

### **Original Process Workflow (Manual):**
1. Copy `.claude/commands/` to project
2. Copy `PRPs/templates/` to project  
3. Create `CLAUDE.md` with project guidelines
4. Use `/prime-core` to initialize Claude
5. Create `INITIAL.md` for project context
6. **Manually set up project structure**
7. **Manually select appropriate CLAUDE.md files**

### **Archon-Agent-Kit-PRP-Automated Workflow (Automated + Intelligent):**
1. Copy `Archon-Agent-Kit-PRP-Automated/` folder to new project location
2. Create `INITIAL.md` with your project specification
3. Run `/initialize-project INITIAL.md`
4. **Everything else is automated!**
   - Technology stack detection
   - CLAUDE.md file selection and customization
   - Project structure generation
   - PRP template configuration
   - **🆕 Archon MCP project container creation**
   - **🆕 Project knowledge crawling and storage**
5. Use `/prime-core` to initialize Claude
6. **🆕 Run `/generate-next-steps` for intelligent guidance**
7. Start developing with context-rich, project-specific suggestions

## 🏗️ **New Architecture**

```
Archon-Agent-Kit-PRP-Automated/
├── .claude/commands/           # Claude-specific commands including /initialize-project and /generate-next-steps
├── .cursor/commands/           # Cursor-specific commands including initialize-project and generate-next-steps
├── project-initializers/       # Python-based automation system
│   ├── technology_detector.py  # Detects tech stack from INITIAL.md
│   ├── project_structure_generator.py  # Generates project structure
│   ├── project_initializer.py # Main orchestrator with Archon integration
│   └── archon_integration.py  # 🆕 Archon MCP server integration
├── claude_md_files/           # Technology-specific CLAUDE.md files
├── PRPs/                      # PRP templates and structure
└── README.md                  # This file
```

## 🎯 **Key Benefits**

### **1. Intelligent Technology Detection**
- **Automatically reads** your `INITIAL.md` file
- **Detects backend** technologies (Python, Java, Node.js, Go)
- **Detects frontend** technologies (Next.js, React, Vue, Astro)
- **Identifies databases** (PostgreSQL, MySQL, MongoDB, Supabase)
- **Recognizes infrastructure** (Docker, Kubernetes, AWS, Vercel)

### **2. Smart CLAUDE.md Selection**
- **Automatically selects** the right technology-specific CLAUDE.md files
- **Customizes content** with your project details
- **Places files** in the correct component directories
- **Creates root CLAUDE.md** with project overview

### **3. Intelligent Project Structure**
- **Generates appropriate** directory structure for your tech stack
- **Creates scaffolding** files (requirements.txt, package.json, etc.)
- **Sets up configuration** files (.gitignore, Dockerfile, etc.)
- **Handles full-stack** projects with separate backend/frontend directories

### **4. Automated PRP Setup**
- **Selects appropriate** PRP templates for your technology choices
- **Copies relevant** templates to your project
- **Configures validation** commands and testing frameworks

### **5. 🆕 Archon MCP Integration**
- **Creates project container** for centralized knowledge management
- **Crawls and stores** project knowledge automatically
- **Enables intelligent search** through project patterns and best practices
- **Provides context-rich guidance** for next development steps

## 🚀 **Getting Started with Archon-Agent-Kit-PRP-Automated**

### **Step 1: Copy Archon-Agent-Kit-PRP-Automated to New Project**
```bash
# Copy the entire Archon-Agent-Kit-PRP-Automated folder to your new project location
cp -r Archon-Agent-Kit-PRP-Automated/ /path/to/new/project/
cd /path/to/new/project/Archon-Agent-Kit-PRP-Automated
```

### **Step 2: Create Your INITIAL.md**
Create an `INITIAL.md` file that describes your project and technology stack:

```markdown
# My Awesome Project

## Technology Stack
- Backend: Python 3.x with FastAPI
- Frontend: Next.js 15 with React 19
- Database: Supabase (PostgreSQL)
- Infrastructure: Docker containerization

## Project Description
[Your project description here]
```

### **Step 3: Run the Initializer**
```bash
# Option 1: Use the Claude command
/initialize-project INITIAL.md

# Option 2: Run manually
cd project-initializers
python project_initializer.py ../INITIAL.md --project-root ../
```

### **Step 4: Review and Customize**
- Review the generated project structure
- Customize CLAUDE.md files with project-specific details
- Run `/prime-core` to initialize Claude

### **Step 5: 🆕 Generate Intelligent Next Steps**
```bash
/generate-next-steps
```

This command automatically:
- Searches Archon knowledge base for relevant patterns
- Generates context-rich commands with plain English descriptions
- Provides specific, actionable next steps
- Tailors suggestions to your detected technology stack

### **Step 6: Start Development**
- Execute suggested commands with confidence
- Create PRPs with full project context
- Build features using established patterns

## 🔍 **Technology Detection Examples**

### **Full-Stack Python + Next.js**
```
INITIAL.md mentions:
- Python 3.x, FastAPI
- Next.js 15, React 19
- Supabase, Docker

Result:
- backend/CLAUDE.md (from CLAUDE-PYTHON-BASIC.md)
- frontend/CLAUDE.md (from CLAUDE-NEXTJS-15.md)
- Full-stack project structure
- Docker Compose setup
```

### **Python Backend Only**
```
INITIAL.md mentions:
- Python 3.x, FastAPI
- PostgreSQL

Result:
- CLAUDE.md (from CLAUDE-PYTHON-BASIC.md)
- Python backend structure
- Database configuration
```

### **Next.js Frontend Only**
```
INITIAL.md mentions:
- Next.js 15, React 19
- Tailwind CSS

Result:
- CLAUDE.md (from CLAUDE-NEXTJS-15.md)
- Next.js project structure
- Frontend configuration
```

## 🛠️ **Supported Technologies**

### **Backend Technologies**
- **Python**: FastAPI, Flask, Django
- **Java**: Spring Boot, Maven, Gradle
- **Node.js**: Express.js, npm/yarn
- **Go**: Gin, Echo, go modules
- **Rust**: Cargo, common frameworks

### **Frontend Technologies**
- **Next.js**: App Router, Pages Router
- **React**: Modern React patterns
- **Vue**: Composition API, Options API
- **Astro**: Static site generation

### **Databases**
- **PostgreSQL**: Native, Supabase
- **MySQL**: MariaDB variants
- **MongoDB**: Document database
- **SQLite**: Lightweight database

### **Infrastructure**
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **AWS**: Cloud services
- **Vercel**: Frontend hosting

## 🧠 **🆕 Intelligent Next Steps Generation**

### **What `/generate-next-steps` Provides**

Instead of guessing what to do next, the system generates intelligent suggestions with full context:

```markdown
## 🚀 Next Steps for Your Project

### 1. Create Core PRP Structure
**Command:** `/prp-base-create "Implement dealership website scraper with data extraction and API endpoints"`
**What it does:** Creates a comprehensive PRP for the main scraping functionality, including data models, API endpoints, and integration with your existing dealer management system. This will establish the foundation for your entire scraping workflow.

**Expected outcome:** A detailed PRP document with implementation blueprint, validation gates, and specific tasks for building the scraper system.

### 2. Set Up Database Schema
**Command:** `/prp-base-create "Design and implement PostgreSQL database schema for dealership data"`
**What it does:** Creates a PRP for designing the database structure that will store scraped dealership information, inventory data, and historical pricing. This includes table design, relationships, and data validation rules.

**Expected outcome:** A complete database schema PRP with entity relationships, migration scripts, and data integrity constraints.
```

### **Technology-Specific Examples**

#### Python/FastAPI Backend
```markdown
### 3. API Endpoint Development
**Command:** `/prp-base-create "Build RESTful API endpoints for dealership data management"`
**What it does:** Creates a PRP for implementing FastAPI endpoints including GET /dealers, POST /dealers, PUT /dealers/{id}, and DELETE /dealers/{id}. This will establish the complete API surface for your dealership management system.

**Expected outcome:** A comprehensive API PRP with endpoint specifications, request/response models, validation, and error handling.
```

#### Next.js/React Frontend
```markdown
### 4. Dashboard Interface
**Command:** `/prp-base-create "Create React dashboard for dealership data visualization and management"`
**What it does:** Creates a PRP for building a modern, responsive dashboard using Next.js 15 and React 19. This includes data tables, charts, search functionality, and real-time updates for dealership information.

**Expected outcome:** A complete frontend PRP with component architecture, state management, and user experience design.
```

### **How It Works**

1. **Archon Knowledge Search**: Searches stored project patterns and best practices
2. **Context Analysis**: Analyzes your specific technology stack and requirements
3. **Intelligent Generation**: Creates tailored suggestions based on detected patterns
4. **Plain English Context**: Provides clear explanations of what each command accomplishes

## 🔧 **Customization and Extension**

### **Adding New Technologies**
1. **Update `technology_detector.py`** with new patterns
2. **Add CLAUDE.md file** to `claude_md_files/`
3. **Update mapping** in `CLAUDE_FILE_MAPPING`
4. **Add structure generation** in `project_structure_generator.py`

### **Modifying Project Structures**
- Edit the appropriate `_generate_*_structure` methods
- Add new configuration file templates
- Customize directory layouts

### **Extending CLAUDE.md Selection**
- Modify detection patterns
- Add new technology categories
- Customize file placement logic

## 🧪 **Testing the System**

### **Test with Sample INITIAL.md**
```bash
cd project-initializers
python project_initializer.py --help
python project_initializer.py test_INITIAL.md --project-root ./test-output
```

### **🆕 Archon MCP Configuration**

Archon-Agent-Kit-PRP-Automated includes optional integration with Archon MCP server for enhanced knowledge management:

```bash
# With Archon MCP server
python project_initializer.py INITIAL.md \
  --archon-url http://localhost:8000 \
  --archon-api-key your-api-key

# Without Archon (default)
python project_initializer.py INITIAL.md
```

**Archon MCP Benefits:**
- **Centralized knowledge management** across projects
- **Intelligent next steps generation** with full context
- **Project task tracking** and organization
- **Persistent knowledge** across development sessions

### **Validate Generated Structure**
- Check that all expected directories are created
- Verify CLAUDE.md files are properly customized
- Confirm PRP templates are copied correctly
- Test that the project can be built/run

## 🚨 **Troubleshooting**

### **Common Issues**

**Technology Not Detected**
- Check spelling and formatting in INITIAL.md
- Add new patterns to `technology_detector.py`
- Verify technology is in supported list

**CLAUDE.md Files Missing**
- Ensure source files exist in `claude_md_files/`
- Check file naming conventions
- Verify mapping in `CLAUDE_FILE_MAPPING`

**Project Structure Issues**
- Review technology detection output
- Check project type classification
- Verify structure generation methods

### **Debug Mode**
```bash
# Run with verbose output
python project_initializer.py INITIAL.md --verbose
```

## 🔮 **Future Enhancements**

### **Planned Features**
- **Template customization**: Allow users to customize generated structures
- **Plugin system**: Support for third-party technology detectors
- **Validation**: Built-in validation of generated project structures
- **Integration**: Better integration with existing development tools

### **Community Contributions**
- **New technology support**: Community-driven technology additions
- **Template improvements**: Better project structure templates
- **Documentation**: Enhanced guides and examples

## 📚 **Documentation and Resources**

- **Commands**: See `.claude/commands/` for available commands
- **Examples**: Check `project-initializers/` for usage examples
- **Templates**: Review `PRPs/templates/` for available PRP templates
- **CLAUDE.md Files**: Examine `claude_md_files/` for technology guidelines

## 🎉 **Success Story**

Archon-Agent-Kit-PRP-Automated transforms this:
```
Manual Setup + Guesswork (30+ minutes):
1. Copy files manually
2. Create directories by hand
3. Select appropriate CLAUDE.md files
4. Customize each file individually
5. Set up project structure
6. Configure build systems
7. Test setup manually
8. **Guess what to do next**
9. **Manually figure out commands**
10. **Hope you're on the right track**
```

Into this:
```
Intelligent Automated Setup (2 minutes + 30 seconds):
1. Create INITIAL.md
2. Run /initialize-project
3. Everything else is automatic!
4. Run /prime-core for context
5. **🆕 Run /generate-next-steps for intelligent guidance**
6. **🆕 Get context-rich, project-specific suggestions**
7. **🆕 Execute commands with confidence**
```

**Result**: You save 28+ minutes per project, get a consistent, professional setup every time, and **eliminate the guesswork** of what to do next with intelligent, context-aware guidance.

---

**Archon-Agent-Kit-PRP-Automated**: Where project initialization meets artificial intelligence and intelligent guidance. 🚀🧠
