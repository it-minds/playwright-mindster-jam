# Project Context

## Mindster Jam - Playwright Test Automation

This project demonstrates AI-assisted Playwright test generation for a Mindster Jam presentation.

## Purpose

1. **Show AI capabilities** - Demonstrate how AI can generate test code quickly
2. **Show real challenges** - Bot protection, environment issues, iteration needed
3. **Provide learning resource** - Templates and patterns for attendees

## Key Files

| File | Purpose |
|------|---------|
| `ACTUAL_PROMPTS_USED.md` | Record of prompts used in this session |
| `PROMPT_WORKFLOW.md` | Example prompt sequence for presentations |
| `TEST_RESULTS.md` | Test results summary |
| `RUN_TESTS.md` | How to run tests |
| `PRESENTATION.md` | Presentation outline |

## Test Files

| File | Tests | Status |
|------|-------|--------|
| `tests/test_demoqa_products.py` | 19 | ✅ Passing |
| `tests/test_lego_homepage.py` | 12 | ⚠️ Blocked by bot protection |
| `tests/test_lego_product_cards.py` | 18 | ⚠️ Blocked by bot protection |
| `tests/test_backend_data_validation.py` | 12 | ⚠️ Blocked by bot protection |

## Technology Stack

- **Python**: 3.14.4
- **Playwright**: 1.64.0
- **pytest**: 9.1.1
- **pytest-playwright**: 0.10.0

## AI Tools Used

- **OpenCode** (qwen3.5) - Primary development
- **Claude Code** - Alternative agent
- **GitHub Copilot** - IDE assistance

## Agent Configuration

Each AI tool has its own configuration:

- **OpenCode**: `.opencode/agents/`, `.opencode/skills/`
- **Claude Code**: `.claude/agents/`, `.claude/skills/`
- **GitHub Copilot**: `.github/copilot-instructions/`

## Presentation Flow

1. Show initial AI-generated tests
2. Discuss what AI got right/wrong
3. Show bot protection challenge
4. Demonstrate working DemoQA tests
5. Workshop: Attendees write their own tests

## Contact

For questions about this project, refer to the README.md or PRESENTATION.md files.