# DemiGod Roadmap

**Status:** Directional roadmap; phase completion requires evidence  
**Last updated:** 2026-11-19

## Phase 0 — Documentation and engineering foundation
- Select Qwen3-Coder-Next as flagship research target.
- Preserve independent model/runtime/storage/agent interfaces.
- Audit repository, build system, CI, security and Astronaut patterns before implementation.
- Record exact target phone, SoC, Android version, RAM, external drive and filesystem.
- Establish reproducible build and automated checks.

**Exit:** buildable Android project, architecture contracts, model ADR and documented unknowns.

## Phase 1 — Android chat foundation
- Kotlin + Compose chat, history, streaming states, markdown/code, stop/regenerate and settings.
- Mock provider for deterministic UI tests.
- Model catalog distinguishes installed, compatible, unsupported and experimental models.

**Exit:** installable APK with offline UI and persistent conversations.

## Phase 2 — Verified small-model inference
- Add one local model/runtime supported on the actual phone.
- Measure memory, TTFT, tokens/sec, context, battery and sustained thermals.
- Implement import, hashes, resumability, SAF storage and bounded buffers.
- Do not block a useful APK on Qwen3-Coder-Next.

**Exit:** repeatable offline inference on named device with exact artifact/runtime record.

## Phase 3 — Coding-agent foundation
- Task lifecycle: understand → inspect → plan → permission → execute → verify → report.
- Project picker, repository tree, ignore rules, file search and bounded context.
- Patch edits, diff viewer, undo/recovery and checkpoints.
- Isolated terminal/build/test runner with timeouts, output limits and cancellation.

**Exit:** solve bounded task in sample repo, apply approved patch, run test and report actual result.

## Phase 4 — Repository intelligence
- Symbol/dependency indexing, language-aware retrieval, BM25 and optional embeddings.
- Incremental indexing, ignore/binary/secret handling.
- Context budget manager with file/line citations.
- Repository map and architecture summaries with freshness metadata.

**Exit:** retrieval benchmarks show relevant code is supplied without loading the whole repo indiscriminately.

## Phase 5 — GitHub and plugins
- Opt-in authentication, least-privilege scopes and secure credentials.
- Read repositories, issues, commits and PRs; review diffs before remote writes.
- Commit/push/PR operations require explicit approval.
- Typed plugin manifests, permissions, validation, timeouts, isolation and audit.

**Exit:** user-approved remote changes with auditable results.

## Phase 6 — Flagship Qwen3-Coder-Next research
- Pin official model revision, config, tokenizer/template, license and shard hashes.
- Test separate paths:
  - AirLLM/Transformers: original checkpoint, architecture compatibility, recurrent hybrid state, generation correctness and disk staging.
  - GGUF/llama.cpp: official Q5_K_M artifact, operator coverage, tool-call template, context and output correctness.
- Never assume AirLLM consumes GGUF or 3B active means 3B storage/RAM.
- Compare quantized outputs and coding-agent quality.
- Measure host RAM, accelerator memory, disk footprint, bytes read/token, TTFT, sustained tokens/sec, power and thermals.
- Investigate Android port only after correct host implementation and useful measured performance.

**Exit:** reproducible comparison and explicit go/no-go for each backend/device profile.

## Phase 7 — Reliability and release
- Threat model, dependency/license review, privacy controls, backup/export/delete.
- Offline, low-storage, process-death, cancellation, malformed-model and removable-drive recovery tests.
- Accessibility, localization, signing, upgrades and support matrix.

**Exit:** release checklist and public known limitations.

## Current priority
Complete model and architecture documentation first. Then audit Android project/build pipeline. In parallel benchmark a smaller local model for the 11 GB RAM phone and begin host-side Qwen3-Coder-Next compatibility experiments. No flagship support claims before evidence.
