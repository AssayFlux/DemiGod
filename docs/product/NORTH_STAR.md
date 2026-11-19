# DemiGod North Star

**Status:** Product direction / living document  
**Last updated:** 2026-11-19

## One-sentence vision

DemiGod is an offline-first Android AI coding assistant with the familiar, low-friction conversation experience of leading AI chat apps and the ability to understand, change, test and explain real software projects through permissioned tools and plugins.

## The user promise

A user can open the DemiGod APK, describe what they want in natural language, and work with one assistant across conversations, code, files and connected development services. The assistant should move beyond giving code snippets: when authorized, it should inspect a project, plan a change, edit files, run checks, explain the result and present a reviewable diff.

DemiGod must be useful as a conversational assistant even when no external account or plugin is connected. Network-dependent integrations are explicit opt-ins, not hidden requirements for the core offline experience.

## Product pillars

1. **Native-feeling Android chat.** A polished mobile-first interface inspired by the interaction patterns users know from ChatGPT and Claude, with original DemiGod branding. Conversations, streaming responses, markdown, readable code blocks, copy/share, attachments, chat history, model selection and accessible settings are core.
2. **Offline-first by default.** Core app navigation, local conversations, installed model management and supported local inference must work without a network connection. Clearly label features that need connectivity.
3. **A real coding agent.** Understand repository context, make a plan, inspect files, propose edits, apply authorized changes, run tests and show evidence. Distinguish suggestions from changes actually executed.
4. **Plugins and tools.** Extend the assistant through well-defined, permission-scoped integrations such as GitHub, local project access, terminal/build tools and future developer services. Users choose what to connect and what permissions to grant.
5. **Honest model engineering.** Qwen3-Coder-480B-A35B-Instruct is the current flagship research target. Its practical on-phone inference is unproven. AirLLM-style memory efficiency is research inspiration, not a claim that the library solves Android inference. Model providers and runtimes must remain replaceable.
6. **Trust and control.** Private data stays local unless the user explicitly invokes a network integration. Destructive actions, remote writes, pushes and merges require clear authorization and review.

## Experience principles

- Chat is the primary surface; coding tools should feel like capabilities of the assistant, not a cluttered IDE bolted onto the home screen.
- Keep the message composer reachable, responses readable and common actions obvious on a phone.
- Use progressive disclosure: advanced agent traces, tool calls, permissions, diffs and logs are available when useful without overwhelming ordinary chat.
- Show clear task states: planning, waiting for permission, running, testing, completed, failed or interrupted.
- Make code edits reviewable with file paths and diffs; never imply a file changed when it did not.
- Preserve conversation and task state across process death where feasible.
- Support accessibility, dark/light themes, dynamic text sizing and responsive layouts.

## What DemiGod is not

- Not a thin wrapper around a single hosted model API.
- Not an autonomous agent with unrestricted access to a user's phone, shell or GitHub account.
- Not a promise that a 480B model will run usefully on every Android device.
- Not a replacement for source control, tests or human review.
- Not a plugin marketplace before the permission and execution foundations are safe.

## Architecture north star

Keep these boundaries explicit:

- **Android client:** Kotlin + Jetpack Compose UI, navigation, local chat/task state, model/storage controls and permission UX.
- **Agent core:** provider-independent conversation orchestration, planning, tool selection, state machine, context assembly and audit trail.
- **Model runtime:** adapter interface for local runtimes and any explicitly configured remote provider. Qwen3-Coder is a model target, not a hard-coded dependency throughout the app.
- **Model/storage layer:** model catalog, import/integrity, removable-storage adapters, bounded memory and measured streaming.
- **Tool/plugin host:** typed tool contracts, manifests, scoped permissions, validation, timeouts and structured results.
- **Execution environment:** isolated workspace for repository edits, builds and tests; no implicit access to arbitrary device files.
- **Integrations:** GitHub and future services behind opt-in connectors with least-privilege credentials.

A backend or remote execution service may be introduced only as an explicit, separately permissioned capability. It must not silently become a runtime dependency for offline-first features.

## Definition of success

DemiGod succeeds when a user can reliably have a useful offline conversation, select a supported local model, connect a repository intentionally, ask for a bounded coding task, review the agent's plan and changes, run relevant checks, and understand exactly what happened. Performance and model support claims must be backed by reproducible device-level evidence.

## Decision rule

When trade-offs arise, prioritize in this order: user data safety and correctness; offline reliability; clear and reviewable behavior; mobile usability; measured performance; breadth of models and plugins.
