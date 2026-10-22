# AI Agent Configuration

This project is configured for multiple AI coding assistants.

---

## How Skills Are Discovered

| Tool | Discovery Method | Configuration Needed? |
|------|------------------|----------------------|
| **Claude Code** | Auto-discovers `.claude/skills/*` | ❌ No |
| **OpenCode** | Reads `.opencode/opencode.jsonc` | ✅ Yes |
| **GitHub Copilot** | Reads `.github/copilot-instructions/*.md` | Context only |

> **Note:** Claude Code automatically loads all skills in `.claude/skills/` - no explicit registration needed!

---

## Directory Structure

```
.opencode/
├── opencode.jsonc        # OpenCode config (references .claude/skills)
└── agents/
    └── playwright-writer.md

.claude/
├── agents/
│   └── playwright-writer.md
└── skills/
    ├── playwright-cli/                    # Official Playwright CLI skill
    │   └── SKILL.md
    └── playwright-tests-best-practices/   # Your team's standards
        └── SKILL.md

.github/
└── copilot-instructions/
    ├── playwright-testing.md
    └── project-context.md
```

---

## Available Skills

### playwright-cli (Official)
Browser automation commands.

```bash
/playwright-cli open https://demoqa.com
/playwright-cli screenshot
/playwright-cli click "button[name='Submit']"
```

### playwright-tests-best-practices (Custom)
Your team's coding standards and rules.

```bash
/playwright-tests-best-practices
```

---

## AI Tools

| Tool | Configuration |
|------|---------------|
| **OpenCode** | `.opencode/opencode.jsonc` |
| **Claude Code** | `.claude/skills/` (auto-discovered) |
| **GitHub Copilot** | `.github/copilot-instructions/` |

---

## Usage Examples

### OpenCode
```bash
# Use playwright-cli skill
/playwright-cli open https://demoqa.com
/playwright-cli screenshot
```

### Claude Code
```bash
# Use playwright-cli skill
/playwright-cli open https://demoqa.com
/playwright-cli click "button[name='Submit']"
```

### GitHub Copilot
Copilot uses context from `.github/copilot-instructions/` automatically when writing code.

---

## Project Context

See these files for project-specific information:
- `README.md` - Project overview
- `PRESENTATION.md` - Presentation outline
- `RUN_TESTS.md` - How to run tests
- `TEST_RESULTS.md` - Test results summary

---

## Test Files

| File | Tests | Status |
|------|-------|--------|
| `tests/test_lego_homepage.py` | 12 | ⚠️ Blocked by bot protection |
| `tests/test_lego_product_cards.py` | 18 | ⚠️ Blocked by bot protection |
| `tests/test_backend_data_validation.py` | 12 | ⚠️ Blocked by bot protection |
| `tests/test_lego_ai_generated.py` | 12 | ⚠️ Blocked by bot protection |

---

## Running Tests

See `RUN_TESTS.md` for full details.