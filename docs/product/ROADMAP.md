# DemiGod Roadmap

**Status:** Implementation has started; phase completion requires evidence  
**Last updated:** 2026-11-19

## Phase 0 — Documentation and engineering foundation
- [x] Select Qwen3-Coder-Next as flagship research target.
- [x] Preserve independent model/runtime/storage/agent interfaces.
- [x] Audit Astronaut patterns and record Android adaptation.
- [x] Create initial Kotlin + Compose Android application scaffold.
- [x] Add Android CI build, unit-test and lint workflow.
- [x] Add experimental AirLLM host bridge with explicit security boundary.
- [ ] Confirm exact target phone model, SoC, Android version and external-drive/filesystem details.
- [ ] Obtain a green CI build and install the debug APK on the target phone.

**Exit:** reproducible build, architecture contracts, model ADR and documented device assumptions.

## Phase 1 — Android chat foundation
- [x] Chat-first Compose shell, persistent composer layout, message bubbles and Chat/Files/Terminal destinations.
- [x] Basic fenced-code block presentation with copy action.
- [x] Explicit preview status; no fake inference or command execution.
- [ ] Conversation persistence, streaming, stop/regenerate, settings and real model selector.
- [ ] UI/instrumentation tests and accessibility review.

**Exit:** installable APK with offline UI and persistent conversations.

## Phase 2 — Verified local inference
- [ ] Add one local model/runtime supported on the actual phone.
- [ ] Measure memory, TTFT, tokens/sec, context, battery and sustained thermals.
- [ ] Implement import, hashes, resumability, SAF storage and bounded buffers.
- [ ] Do not block a useful APK on Qwen3-Coder-Next.

**Exit:** repeatable offline inference on named device with exact artifact/runtime record.

## Phase 3 — Coding-agent foundation
- [ ] Typed provider and tool contracts; task lifecycle: understand → inspect → plan → permission → execute → verify → report.
- [ ] Project picker, repository tree, ignore rules, file search and bounded context.
- [ ] Patch edits, diff viewer, undo/recovery and checkpoints.
- [ ] Isolated terminal/build/test runner with timeouts, output limits and cancellation.

**Exit:** solve bounded task in sample repo, apply approved patch, run test and report actual result.

## Phase 4 — Repository intelligence
- [ ] Symbol/dependency indexing, language-aware retrieval, BM25 and optional embeddings.
- [ ] Incremental indexing, ignore/binary/secret handling.
- [ ] Context budget manager with file/line citations.
- [ ] Repository map and architecture summaries with freshness metadata.

**Exit:** retrieval benchmarks show relevant code is supplied without loading the whole repo indiscriminately.

## Phase 5 — GitHub and plugins
- [ ] Opt-in authentication, least-privilege scopes and secure credentials.
- [ ] Read repositories, issues, commits and PRs; review diffs before remote writes.
- [ ] Commit/push/PR operations require explicit approval.
- [ ] Typed plugin manifests, permissions, validation, timeouts, isolation and audit.

**Exit:** user-approved remote changes with auditable results.

## Phase 6 — Flagship Qwen3-Coder-Next research
- [ ] Pin official model revision, config, tokenizer/template, license and shard hashes.
- [ ] AirLLM/Transformers: prove architecture compatibility, recurrent hybrid state, generation correctness and disk staging.
- [ ] GGUF/llama.cpp: validate official artifact, operator coverage, tool-call template, context and output correctness.
- [ ] Compare quantizations and coding-agent quality; measure host RAM, accelerator memory, disk footprint, bytes read/token, TTFT, tokens/sec, power and thermals.
- [ ] Investigate Android port only after correct host implementation and useful measured performance.

**Exit:** reproducible comparison and explicit go/no-go for each backend/device profile.

## Phase 7 — Reliability and release
- [ ] Threat model, dependency/license review, privacy controls, backup/export/delete.
- [ ] Offline, low-storage, process-death, cancellation, malformed-model and removable-drive recovery tests.
- [ ] Accessibility, localization, signing, upgrades and support matrix.

**Exit:** release checklist and public known limitations.

## Current priority
Get the Android CI build green, install the first APK on the target phone, and validate the AirLLM host bridge on a CUDA host. In parallel, start conversation persistence and the typed inference interface. No Qwen3-Coder-Next or phone compatibility claims before measured evidence.
