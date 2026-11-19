# DemiGod Roadmap

**Status:** Directional roadmap; phase completion requires evidence  
**Last updated:** 2026-11-19

This roadmap turns the North Star into an incremental build sequence. It is capability-based rather than date-based. Do not skip foundational safety, storage or validation work to make a demo appear more complete.

## Phase 0 — Product and engineering foundations

**Goal:** Establish a buildable Android project and shared engineering contracts.

- Confirm Android application ID, minimum/target SDK policy, Kotlin and Compose baseline.
- Establish module boundaries, dependency/version management, formatting, static analysis and CI.
- Create the initial app shell, navigation, theme system and design tokens.
- Define data models for conversations, messages, attachments, tasks, tool calls and model profiles.
- Define interfaces for model providers, storage providers and tools before choosing implementation details.
- Record supported-device assumptions and unresolved hardware facts.

**Exit criteria:** Reproducible debug APK build; basic automated checks in CI; architecture decisions documented; no model capability claims.

## Phase 1 — Chat-first Android APK

**Goal:** Deliver the core mobile conversation experience.

- ChatGPT/Claude-familiar interaction patterns with original DemiGod identity.
- Conversation list, new chat, message composer and streaming response UI.
- Markdown, code syntax highlighting, copy actions, stop/regenerate and error states.
- Local conversation persistence and recovery after app restart.
- Settings, accessibility, dark/light themes and model status.
- A deterministic mock model provider for UI and state-machine testing.

**Exit criteria:** The app can be installed as an APK and used end-to-end with a mock provider; chat history survives restart; offline UI flows work.

## Phase 2 — Local model and storage foundation

**Goal:** Run a realistically supported local model and prove removable-storage behavior.

- Implement model catalog, import, manifest validation and integrity checks.
- Add internal-storage and Android SAF adapters for removable media.
- Implement bounded reads/caches and safe detach/reconnect behavior.
- Integrate one model/runtime combination that is actually supported by the chosen backend.
- Measure memory, latency, tokens/sec, energy and thermals on named devices.
- Keep Qwen3-Coder-480B-A35B-Instruct as the flagship research target; do not block a useful first APK on an unproven 480B mobile deployment.
- Evaluate AirLLM and other memory-efficient approaches against real Android compatibility, license, architecture and performance requirements.

**Exit criteria:** At least one explicitly named device/model configuration passes repeatable offline inference tests. Model storage and runtime support are documented separately.

## Phase 3 — Coding workspace and safe agent core

**Goal:** Turn chat into a controlled coding assistant.

- Implement agent task state machine: understand → inspect → plan → request permission → execute → verify → summarize.
- Add project/workspace abstraction and repository file indexing.
- Add read-only inspection before write-capable operations.
- Implement patch-based edits and reviewable diffs.
- Add isolated command/build/test execution with timeouts, resource limits and logs.
- Add cancellation, interruption recovery and task audit history.
- Require user approval before applying consequential changes.

**Exit criteria:** On a sample project, the agent can explain repository structure, propose a patch, apply an approved patch in a workspace, run a test command and report the actual result.

## Phase 4 — GitHub integration

**Goal:** Let users work with GitHub repositories through explicit authorization.

- Connect/disconnect GitHub with secure token handling and minimum required scopes.
- List and select repositories and branches.
- Inspect files, commits, issues and pull requests.
- Create a task workspace/branch for changes.
- Present diffs and test evidence before remote writes.
- Commit and open pull requests only after explicit confirmation.
- Make network use and remote actions visible in the conversation.

**Exit criteria:** A user can connect a repository, ask for a bounded change, review it, and explicitly authorize a branch/commit/PR workflow. No silent push, merge or credential exposure.

## Phase 5 — Extensible plugin platform

**Goal:** Add integrations without coupling them to the model or Android UI.

- Define plugin manifest, versioning, tool schemas, permission scopes and result format.
- Add plugin discovery, install/enable/disable, connection status and per-plugin permission review.
- Implement execution isolation, input validation, output limits, timeouts and audit events.
- Migrate GitHub to the same plugin contract.
- Add terminal/build tools and other integrations only when their threat model and UX are defined.

**Exit criteria:** A second independently implemented plugin can be added without modifying the agent's core orchestration or chat UI; permission tests pass.

## Phase 6 — Flagship-model research and optimization

**Goal:** Determine whether the 480B flagship can meet a useful mobile experience, or define an honest alternative deployment profile.

- Pin the exact Qwen3-Coder-480B-A35B-Instruct revision and audit tensors, shards, tokenizer, license and hashes.
- Validate candidate quantizations for coding quality, not just file size.
- Prove tensor reads, MoE routing, bounded-memory execution and multi-token generation in a host harness.
- Measure bytes read per token and cache behavior on the actual USB SSD and phone.
- Port only validated paths to Android; test sustained power and thermal behavior.
- Publish go/no-go results and supported-device matrix.
- Keep smaller local models and optional user-configured remote inference as separate, clearly labeled profiles if needed.

**Exit criteria:** A reproducible report establishes either a named supported device profile or a documented no-go/limitations decision. No unsupported claim of 480B on-device inference.

## Phase 7 — Reliability, privacy and release readiness

**Goal:** Make the APK safe and maintainable for daily use.

- Threat model, dependency review, secure storage and privacy review.
- Backup/export/delete controls for local conversations and project data.
- Permission and plugin audit screens.
- Crash, performance and battery testing across supported devices.
- Accessibility and localization pass.
- Release signing, versioning, changelog, upgrade and rollback strategy.
- Documentation for installation, model setup, storage, plugins and known limitations.

**Exit criteria:** Release checklist passes; support matrix and known limitations are public; APK can be installed, upgraded and recovered predictably.

## Cross-phase workstreams

- **Model research:** independent from UI progress; report reproducible evidence.
- **Security:** review every new permission, connector and execution surface before release.
- **Quality:** automated tests accompany each feature; manual device validation is required for hardware/storage behavior.
- **Documentation:** update architecture, ADRs, build rules and roadmap whenever a material decision changes.
- **Observability:** collect local diagnostics with user consent; never upload prompts, source code or credentials by default.

## Current priority

Start with Phase 0 and Phase 1: establish a reproducible Android project and a polished chat shell using a mock provider. In parallel, continue model/storage feasibility research as a separate workstream. This creates a usable product foundation without pretending the flagship model is already mobile-ready.
