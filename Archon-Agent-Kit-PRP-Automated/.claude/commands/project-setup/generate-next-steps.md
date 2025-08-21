# Generate Next Steps with Archon Context

## Purpose
After running `/prime-core`, automatically generate intelligent next steps with plain English context for each command. This command leverages Archon MCP knowledge to provide project-specific guidance and eliminate the need to manually figure out what to write for each command.

## Usage
/generate-next-steps

## What It Does

### 1. Archon Knowledge Integration
- Access project-specific knowledge base through MCP tools
- Search for existing patterns and conventions
- Reference project structure and technology choices
- Leverage stored best practices and examples

### 2. Intelligent Command Generation
- Analyze current project state and requirements
- Generate context-rich commands with plain English descriptions
- Tailor suggestions to detected technology stack
- Provide specific, actionable next steps

### 3. Plain English Context
- Explain what each command will accomplish
- Provide business context and user value
- Reference specific project features and requirements
- Include expected outcomes and success criteria

## When to Use

**Run this command immediately after `/prime-core`** to get intelligent guidance on what to do next.

## Output Format

The command generates a structured list of next steps with:

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

### 3. Implement Authentication System
**Command:** `/prp-base-create "Build secure authentication system with JWT tokens and role-based access"`
**What it does:** Creates a PRP for implementing user authentication, including login/logout functionality, JWT token management, and role-based permissions for different user types (admins, analysts, viewers).

**Expected outcome:** A secure authentication PRP with user management, token handling, and access control implementation.
```

## Technology-Specific Examples

### Python/FastAPI Backend
```markdown
### 4. API Endpoint Development
**Command:** `/prp-base-create "Build RESTful API endpoints for dealership data management"`
**What it does:** Creates a PRP for implementing FastAPI endpoints including GET /dealers, POST /dealers, PUT /dealers/{id}, and DELETE /dealers/{id}. This will establish the complete API surface for your dealership management system.

**Expected outcome:** A comprehensive API PRP with endpoint specifications, request/response models, validation, and error handling.
```

### Next.js/React Frontend
```markdown
### 5. Dashboard Interface
**Command:** `/prp-base-create "Create React dashboard for dealership data visualization and management"`
**What it does:** Creates a PRP for building a modern, responsive dashboard using Next.js 15 and React 19. This includes data tables, charts, search functionality, and real-time updates for dealership information.

**Expected outcome:** A complete frontend PRP with component architecture, state management, and user experience design.
```

## Archon MCP Knowledge Sources

The command leverages these knowledge sources to generate intelligent suggestions:

### 1. Project Context
- **INITIAL.md content** - Project requirements and goals
- **Technology stack** - Detected frameworks and tools
- **Project structure** - Generated directories and files
- **CLAUDE.md files** - Technology-specific guidelines

### 2. Archon Knowledge Base
- **Existing patterns** - Similar project implementations
- **Best practices** - Framework-specific conventions
- **Common pitfalls** - Lessons learned from other projects
- **Integration examples** - How to connect different components

### 3. Codebase Intelligence
- **Current state** - What's already implemented
- **Dependencies** - Required libraries and tools
- **Configuration** - Environment and build settings
- **Testing strategy** - Validation and quality assurance

## Command Categories

### Core Development
- **PRP Creation** - Building feature specifications
- **Architecture Design** - System structure and patterns
- **Integration Planning** - Connecting different components

### Implementation
- **API Development** - Backend endpoints and services
- **Frontend Building** - User interfaces and interactions
- **Database Design** - Data models and storage

### Quality & Operations
- **Testing Strategy** - Validation and quality assurance
- **Deployment Planning** - Infrastructure and hosting
- **Monitoring Setup** - Logging and performance tracking

## Success Criteria

- [ ] Commands are specific to your project context
- [ ] Plain English descriptions are clear and actionable
- [ ] Suggestions align with detected technology stack
- [ ] Commands follow logical development sequence
- [ ] Each suggestion includes expected outcomes
- [ ] Guidance leverages Archon MCP knowledge

## Usage Examples

```bash
# Generate next steps after prime-core
/prime-core
/generate-next-steps

# Generate next steps for specific feature area
/generate-next-steps --feature "authentication"

# Generate next steps with custom context
/generate-next-steps --context "focus on backend API development"
```

## Integration with Archon MCP

This command automatically:

1. **Creates Archon project container** if not exists
2. **Crawls and stores project knowledge** for future reference
3. **Searches knowledge base** for relevant patterns and examples
4. **Generates context-rich suggestions** based on stored knowledge
5. **Creates project tasks** for tracking progress

## Next Steps After This Command

1. **Review generated suggestions** - Understand what each command will accomplish
2. **Choose your next step** - Pick the most logical next action
3. **Execute the command** - Run the suggested command with confidence
4. **Repeat the process** - Use `/generate-next-steps` again after completing each step

## Error Handling

- **No Archon connection** - Clear instructions for MCP setup
- **Missing project context** - Guidance to run `/prime-core` first
- **Empty knowledge base** - Suggestions based on INITIAL.md analysis
- **Technology conflicts** - Warnings and alternative suggestions

This command transforms the guesswork of "what should I do next?" into intelligent, context-aware guidance that leverages your project's specific requirements and Archon's accumulated knowledge.
