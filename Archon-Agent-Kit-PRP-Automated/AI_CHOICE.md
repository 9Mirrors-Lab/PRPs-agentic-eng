# 🤖 AI Choice Selection Guide

## Welcome to Archon-Agent-Kit-PRP-Automated!

Archon-Agent-Kit-PRP-Automated is designed to work with **multiple AI coding assistants**. Choose your preferred AI tool to get the most optimized experience.

## 🎯 **Choose Your AI Assistant**

### **Option 1: Claude (Anthropic)**
- **Best for**: Detailed analysis, comprehensive explanations, complex reasoning
- **Interface**: Claude web app, Claude Desktop, or Claude Pro
- **Commands**: Use the `.claude/commands/` directory
- **Workflow**: `/initialize-project` → `/prime-core` → `/generate-next-steps`

### **Option 2: Cursor (Cursor AI)**
- **Best for**: Integrated development, real-time assistance, code completion
- **Interface**: Cursor IDE with built-in AI features
- **Commands**: Use the `.cursor/commands/` directory
- **Workflow**: "Initialize project from INITIAL.md" → AI chat → "Generate next steps"

### **Option 3: Other AI Assistants**
- **Best for**: Custom workflows, specific AI tool preferences
- **Interface**: Various AI platforms and tools
- **Commands**: Adapt commands from `.claude/` or `.cursor/` directories
- **Workflow**: Customize based on your AI tool's capabilities

## 🚀 **Getting Started**

### **Step 1: Choose Your AI**
Decide which AI coding assistant you want to use for this project.

### **Step 2: Copy Archon-Agent-Kit-PRP-Automated**
```bash
cp -r Archon-Agent-Kit-PRP-Automated/ /path/to/new/project/
cd /path/to/new/project/
```

### **Step 3: Follow AI-Specific Instructions**

#### **For Claude Users:**
1. Use `.claude/commands/` directory
2. Run `/initialize-project INITIAL.md`
3. Run `/prime-core`
4. Run `/generate-next-steps`

#### **For Cursor Users:**
1. Use `.cursor/commands/` directory
2. Type: "Initialize project from INITIAL.md"
3. Use Cursor's AI chat for project context
4. Type: "Generate next steps for project development"

#### **For Other AIs:**
1. Adapt commands from either directory
2. Customize workflow for your AI tool
3. Follow the general Archon-Agent-Kit-PRP-Automated workflow

## 📁 **Directory Structure**

```
Archon-Agent-Kit-PRP-Automated/
├── .claude/                    # Claude-specific commands
│   └── commands/
│       └── project-setup/
│           ├── initialize-project.md
│           └── generate-next-steps.md
├── .cursor/                    # Cursor-specific commands
│   └── commands/
│       └── project-setup/
│           ├── initialize-project.md
│           └── generate-next-steps.md
├── project-initializers/       # Shared Python backend
├── claude_md_files/           # Shared CLAUDE.md files
├── PRPs/                      # Shared PRP templates
├── README.md                  # Main documentation
└── AI_CHOICE.md               # This file
```

## 🔄 **Shared vs. AI-Specific**

### **Shared Components (All AIs):**
- **Python Backend**: `project-initializers/` - Core automation logic
- **CLAUDE.md Files**: `claude_md_files/` - Technology-specific guidelines
- **PRP Templates**: `PRPs/` - Feature development templates
- **Project Structure**: Generated automatically based on INITIAL.md

### **AI-Specific Components:**
- **Commands**: Different command formats for each AI
- **Workflow**: Optimized interaction patterns
- **Documentation**: AI-specific usage instructions
- **Integration**: Platform-specific features and capabilities

## �� **Why Multiple AI Support?**

### **User Choice**: Different developers prefer different AI tools
### **Platform Optimization**: Each AI has unique strengths and interfaces
### **Workflow Flexibility**: Adapt to your existing development habits
### **Future-Proofing**: Easy to add support for new AI tools

## 🚀 **Quick Start Commands**

### **Claude:**
```bash
/initialize-project INITIAL.md
/prime-core
/generate-next-steps
```

### **Cursor:**
```
Initialize project from INITIAL.md
[Use Cursor's AI chat for project context]
Generate next steps for project development
```

### **Other AIs:**
Adapt the commands above to your AI tool's interface and capabilities.

## 🔧 **Customization**

### **Adding New AI Support:**
1. Create `.your-ai/commands/` directory
2. Adapt command files from existing directories
3. Customize workflow for your AI's capabilities
4. Update this guide with your AI's instructions

### **Modifying Commands:**
- Edit files in the appropriate AI-specific directory
- Maintain consistency across AI versions
- Test commands with your AI tool
- Update documentation as needed

## 🎉 **Ready to Start?**

1. **Choose your AI assistant** from the options above
2. **Follow the AI-specific instructions** for your chosen tool
3. **Create your INITIAL.md** with project specifications
4. **Run the initialization** using your AI's commands
5. **Enjoy automated project setup** with intelligent guidance!

---

**Archon-Agent-Kit-PRP-Automated**: Where project initialization meets artificial intelligence, regardless of your AI preference! 🚀��
