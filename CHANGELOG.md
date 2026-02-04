# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-04

### Added

- Initial release as Claude Code plugin
- Plugin manifest (`.claude-plugin/plugin.json`)
- Marketplace configuration (`marketplace.json`)
- Skills:
  - `proc-creating-skills-skill`: Custom agent skill creation workflow
  - `proc-reviewing-code-skill`: Multi-perspective code review (Frontend, Backend, Infrastructure, Security)
  - `proc-importing-skill`: External skill/agent definition import
- Agents:
  - `deshi-skill-expert`: Skill creation specialist
  - `deshi-code-reviewer`: Code review specialist
- YAML frontmatter for all active skills and agents
- CI/CD workflow for plugin sync verification
