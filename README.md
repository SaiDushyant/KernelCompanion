# KernelSense

KernelSense is a **safety-first natural language shell** that converts human intent into system commands using an intelligent language model, while enforcing **strict local validation, explanation, and user control**.

Unlike traditional AI-powered tools, KernelSense **never executes commands blindly**. Every command is inspected, explained, and explicitly approved by the user before execution.

---

## 🚀 Motivation

Modern operating systems expose powerful command-line tools, but they require:

- memorizing commands and flags
- understanding system-level risks
- careful handling of destructive operations

KernelSense bridges this gap by allowing users to interact with the terminal using **natural language**, while preserving the **safety, transparency, and control** expected from system software.

---

## ✨ Key Features

- **Natural language → shell commands**
- Intelligent model used **only for command suggestions**
- **Hard-blocks dangerous commands**
- **Explain-before-run** workflow
- Fully **local command execution**
- Explicit **user confirmation**
- Configurable behavior
- Persistent command history

---

## 🧠 Architecture Overview

```
User Input (Natural Language)
        ↓
Language Model (Suggestion Only)
        ↓
Command Parser
        ↓
Safety Validator
        ↓
Explain-Before-Run
        ↓
User Confirmation
        ↓
Local Command Execution
```

### Architectural Principles

- The language model has **no execution rights**
- All validation happens **locally**
- Safety rules override intelligence
- The user is always in control

---

## 🔐 Why KernelSense is Safe

- Suggested commands are **never executed automatically**
- Dangerous commands are **hard-blocked**
- Risky commands require explicit confirmation
- Commands are explained before execution
- Execution is fully local (no remote execution)

---

## 🖥️ Example Usage

```
KernelSense > list files with size

----------------------------------------
Command : ls -l
----------------------------------------
Explain this command? (y/n): y

Command Explanation:
Command 1: ls
  ls : List directory contents
  -l : Option flag

Run this command? (y/n): y
----------------------------------------
Output :
total 12
drwxrwxr-x 7 user user 4096 kernelsense
-rw-r--r-- 1 user user  185 pyproject.toml
----------------------------------------
KernelSense >
```

---

## ⚙️ Installation

### Development Mode (Recommended)

```bash
python -m kernelsense.main start
```

### CLI Mode

```bash
pip install -e .
kernelsense start
```

---

## 🛠️ Configuration

KernelSense supports user preferences via a local config file:

```json
{
  "auto_explain": false,
  "auto_confirm": false,
  "show_alternatives": false
}
```

This allows customization of:

- explanation prompts
- confirmation behavior
- suggestion visibility

---

## 🧪 Testing & Reliability

- Dangerous commands are blocked by deterministic rules
- Failure scenarios (timeouts, invalid responses) are handled gracefully
- No stack traces are exposed during normal usage
- Designed to be safe for live demos and evaluations

---

## 📦 Project Structure

```
kernelsense/
├── kernelsense/
│   ├── shell.py        # Interactive REPL
│   ├── llm/            # Language model interface
│   ├── parser/         # Command parsing
│   ├── safety/         # Safety validation
│   ├── explain/        # Command explanation
│   ├── executor.py    # Secure execution
│   ├── config.py      # User configuration
│   └── history.py     # Usage logging
├── tests/
├── pyproject.toml
└── README.md
```

---

## 🔮 Future Scope

- Local language model fallback
- Plugin-based safety and rule engine
- Advanced command explanation system
- User behavior–based command preferences
- OS-specific optimization (Linux / macOS)

---

## 🎓 Academic Relevance

KernelSense demonstrates concepts from:

- Operating Systems
- Secure Systems Design
- Software Engineering
- Human–Computer Interaction
- AI-assisted tooling (with safety constraints)

---

## 📌 One-Line Description

> **KernelSense is a safety-first natural language terminal that suggests system commands using an intelligent model while enforcing strict local validation and user control.**

---

## 📜 License

MIT License
