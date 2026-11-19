# DemiGod Build Rules

**Status:** Engineering rules; apply to all contributions  
**Last updated:** 2026-11-19

## 1. Product
- Primary deliverable: Android APK; Kotlin + Jetpack Compose by default.
- Offline-first core; network features explicit and permissioned.
- Chat-first UX with a complete coding workspace and agent.
- Keep UI, agent, runtime, storage, execution and plugins behind stable interfaces.

## 2. Selected model
- Flagship research target: **Qwen3-Coder-Next**, 80B total parameters and approximately 3B activated per token.
- Active parameters are not stored weights. Full model artifact remains necessary.
- GGUF track: Qwen/Qwen3-Coder-Next-GGUF; validate exact quantization, shards, hashes, tokenizer/template and llama.cpp revision.
- AirLLM track: separate Python/PyTorch Transformers experiment. Not Android-native and does not load GGUF.
- Generic AirLLM support for Qwen families does not prove exact Qwen3-Coder-Next hybrid-state compatibility.
- The 11 GB RAM phone uses a smaller model unless a specific configuration passes real-device tests.
- Keep Qwen-specific prompt/template behavior in model profiles/adapters.

## 3. Architecture and agent
- Agent calls typed provider/tool interfaces, not model-specific APIs directly.
- Adapters declare context, tool-use, structured-output and multimodal capabilities.
- Task lifecycle: understand, inspect, plan, permission, execute, verify, report.
- Treat repository/model/tool/plugin output as untrusted.
- Start read-only; request narrow permissions only when needed.
- Show paths, diffs, command intent, logs and actual test results.
- Approval required for destructive changes, broad writes, external publication, push, merge and risky commands.
- Never imply a command or test ran if it did not.

## 4. Inference honesty
- AirLLM layer streaming can reduce peak accelerator weight residency; it does not remove host RAM, I/O, context/state cache, compute, power or thermal costs.
- 256K context is a model limit, not a recommended phone setting.
- Record model revision, quantization, hashes, tokenizer/template, runtime version and hardware for every benchmark.
- Compare quantizations on code correctness, patch success, tool-call validity and repository tasks, not file size alone.
- No local/offline/speed claim without repeatable tests on a named device and artifact.
- Prefer a smaller verified model over an unverified flagship demo.

## 5. Storage
- Use Android SAF for user-selected USB storage; do not assume URIs are paths or support random reads.
- Verify manifests, shard lengths, hashes, tensor metadata and backend compatibility.
- Use bounded buffers, memory budgets, resumable imports and safe recovery.
- External SSD capacity does not replace RAM, bandwidth or compute.
- Keep credentials and private project data app-private.

## 6. Security and integrations
- GitHub is opt-in; explain scopes, least privilege and secure credential storage.
- Validate tool I/O; enforce timeouts, cancellation, resource limits and isolation.
- No unrestricted filesystem/shell access by default.
- Never silently transmit source, prompts, diagnostics or model files.
- No force-push or merge without explicit authorization.

## 7. Quality
- Unit-test state machines, parsers, permissions, context assembly and tool validation.
- Integration-test model/storage adapters and plugins.
- Real-device tests mandatory for USB, memory, thermals and inference.
- Test offline, process death, cancellation, low storage, malformed artifacts, revoked permissions and drive disconnect.
- Run formatting, lint, static analysis, unit tests and relevant builds.
- Never weaken/delete tests merely to pass CI without documented approval.

## 8. Git and docs
- All commits go directly to **Heaven only**. Do not create commits on other branches.
- Do not force-push, rewrite shared history or merge PRs without explicit authorization.
- Update README, North Star, roadmap, build rules, architecture docs and ADRs when model/runtime decisions change.
- Do not commit model binaries, generated outputs, credentials or user repository contents.
- Review licenses for code, dependencies and model artifacts.

## 9. Definition of done
- Behavior matches product direction with explicit permission/network states.
- Errors, cancellation and recovery are handled.
- Tests pass or exceptions are reported.
- Device/model/runtime assumptions are documented.
- Relevant docs and ADRs are updated.
- Final report states changes, verification and remaining unknowns.
