# DemiGod North Star

**Status:** Product direction / living document  
**Last updated:** 2026-11-19

## Vision
DemiGod is an offline-first Android coding assistant combining a polished conversational experience with a real software-engineering agent: repository understanding, multi-file changes, execution, tests, debugging, review and explainable results.

## User promise
A user describes a task. DemiGod inspects the selected project, builds a grounded plan, requests necessary permissions, edits files through reviewable patches, runs checks, responds to failures and reports exactly what changed. It remains useful for ordinary chat and smaller local-model workflows when the flagship is unavailable.

## Product pillars
1. **Excellent coding workflow:** repository map, symbol/search retrieval, dependency awareness, context selection, planning, patch editing, diffs, terminal/build/test tools and debugging.
2. **Selected flagship:** Qwen3-Coder-Next (80B total, approximately 3B active per token), selected for coding-agent workflows. Research target, not proven Android deployment.
3. **Offline-first Android:** local conversations, installed supported models and core UI work without network. Network features are opt-in.
4. **Model/runtime independence:** adapters expose capabilities; agent orchestration does not hard-code Qwen, AirLLM, llama.cpp or a cloud vendor.
5. **Safe autonomy:** visible plan/execute/verify lifecycle, scoped tools, approvals for consequential operations, audit trail and reviewable diffs.
6. **Honest performance:** distinguish total parameters from active parameters, file size from memory, and successful loading from useful generation.

## Primary mobile target
- Confirmed handset: Motorola Moto G54 5G, 12 GB RAM, Android 15; 256 GB storage reported by the device owner.
- 12 GB is physical RAM, not an app memory budget. Runtime memory preflight and on-device PSS/RSS/thermal measurements are mandatory.
- Begin local model evaluation with compact quantized candidates (roughly 1B–3B class); this is a test range, not a promise that every model in it will fit or perform well.
- The UI and workspace must remain useful with no model installed. Qwen3-Coder-Next is not a local-phone target.

## Model strategy
- Flagship: Qwen/Qwen3-Coder-Next.
- Official model-card facts: 80B total, approximately 3B active, 48 hybrid Gated DeltaNet/Gated Attention layers, 512 experts with 10 routed plus a shared expert, native 262,144-token context, Apache-2.0 license. Re-verify against pinned revision.
- GGUF track: official Qwen/Qwen3-Coder-Next-GGUF with documented Q5_K_M example for llama.cpp. Measure exact artifact size and quality.
- AirLLM track: separate Transformers/PyTorch experiment using source checkpoint. Do not pass GGUF to AirLLM or assume generic Qwen-family support proves this exact hybrid model works.
- Android daily use: smaller model that passes device tests. 3B active does not mean the 80B weights disappear; 11 GB RAM is not proof of flagship feasibility.
- Remote inference/execution only with explicit user choice and privacy boundaries.

## Experience principles
- Chat is primary; coding workspace and agent traces appear progressively.
- Show plans, permissions, tool calls, diffs, commands, test evidence and task state.
- Never claim edits, commands or tests occurred unless they did.
- Recover safely from process death, cancellation and storage removal.
- Support accessibility, themes and responsive Android layouts.

## Architecture boundaries
- Android client: Kotlin/Compose UI, persistence and permission UX.
- Agent core: provider-independent planning, context assembly, tool routing, task state machine and audit.
- Model runtime: replaceable local and explicitly configured remote adapters.
- Model/storage: catalog, artifact verification, SAF adapters, bounded caches and measured streaming.
- Tool host: typed contracts, scopes, validation, timeouts and output limits.
- Workspace/execution: isolated project access, patch application, terminal, build and tests.
- Integrations: opt-in least-privilege connectors.

## Success
A user can work on a real project, ask for a bounded change, review a plan and patch, run tests, inspect failures and understand the outcome. Evaluate coding tasks and tool reliability, not parameter count alone. Device claims require reproducible evidence.

## Decision rule
Prioritize correctness and user-data safety, reliable coding-agent behavior, offline usability, review/verification, mobile performance and breadth of model support.
