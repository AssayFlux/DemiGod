# Android platform adaptation and first implementation

**Status:** Initial scaffold implemented; Moto G54 5G / 12 GB / Android 15 is the primary target profile. Runtime and workspace integrations remain in progress.  
**Date:** 2026-11-19

## Product interface

DemiGod is chat-first, not terminal-first. The main surface is a conversational coding assistant with message history, a persistent composer, readable code output and copy affordances. Project files and terminal are dedicated workspace destinations. On mobile these are full-screen destinations rather than a cramped desktop split pane.

## Adapted from Astronaut

Reuse the engineering patterns, not the entire application:
- Kotlin + Jetpack Compose and a reproducible JDK 17 Android build.
- Replaceable runtime adapters and capability declarations.
- Android Storage Access Framework for user-selected project/model locations.
- Verified model manifests, SHA-256 validation, resumable downloads and immutable versions.
- Room + SQLCipher + Android Keystore for private conversation/project state when persistence is implemented.
- WorkManager for recoverable downloads/indexing, not foreground token generation.
- Real-device validation for memory pressure, USB storage, battery and thermals.

Do not inherit Astronaut's bounded editor as a general large-model random-access engine or its historical 15 GB model cap. Do not represent a GGUF catalog entry as a working llama.cpp runtime.

## Initial Android scaffold

The first Compose app provides:
- Chat-first navigation, a message composer and message bubbles.
- Fenced code-block presentation with a clipboard copy action.
- Chat, Files and Terminal workspace destinations.
- Explicit preview/model-not-connected status so no fake inference is presented as real.

Not implemented yet: persistent chat database, actual inference connection, streaming, full Markdown renderer, project SAF picker, file editor, terminal process runner, Git operations, model downloads, APK signing or release hardening.

## Primary phone profile: Moto G54 5G

The confirmed target configuration is Moto G54 5G, 12 GB RAM, Android 15 and 256 GB storage (capacity reported by the device owner). Treat 12 GB as physical-device RAM, not an app memory allowance: Android, vendor services, graphics and other apps consume a substantial share. The app must query runtime memory at launch and immediately before model load; never infer a safe model size from the RAM label alone.

Initial mobile policy:
- Keep the chat/workspace usable with no model installed and fully offline.
- Start local-model evaluation with compact quantized coding/instruct models in the roughly 1B–3B parameter class; this is a benchmark candidate range, not a compatibility guarantee.
- Benchmark multiple quantizations and context sizes. Measure peak PSS/RSS, native allocations, available memory, load time, TTFT, sustained tokens/sec, battery and thermal throttling on the actual handset.
- Use conservative context defaults and an explicit model-load preflight. Reject or warn on insufficient memory; unload on memory pressure and handle process death.
- Keep model files outside the APK. Support user-selected storage through SAF; test removable USB storage and seekability before claiming it works.
- Qwen3-Coder-Next (80B total) remains a research target and is not a Moto G54 local deployment target.

## AirLLM integration boundary

AirLLM lives in `airllm/` as a Python/PyTorch host experiment. It is not packaged in the APK and does not execute on the phone. The initial host bridge requires a locally downloaded, revision-pinned checkpoint, binds to loopback, requires a bearer token and exposes a non-streaming OpenAI-compatible chat endpoint. The Android app is not connected to it yet.

AirLLM's current AutoModel architecture detection uses `trust_remote_code=True`; loading a checkpoint can execute Python from the model snapshot. Use a reviewed official snapshot in an isolated host environment. Qwen3-Coder-Next support remains experimental until the exact pinned snapshot passes load, generation, multi-turn recurrent-state, tokenizer/template and tool-call checks.

## Execution safety

The terminal must be an isolated execution service, not unrestricted `Runtime.exec` from UI code. Before enabling it, implement workspace-scoped paths, command allow/deny policy, explicit approval, process timeouts, output caps, cancellation, environment isolation and audit records. Git writes, network access, destructive commands, push and merge require separate approvals.

## Next milestones

1. Build and install the debug APK on the Moto G54 5G (12 GB, Android 15); capture a baseline memory/thermal profile.
2. Add Room persistence and conversation export/delete.
3. Add a typed inference contract, streaming event model and a deterministic mock provider.
4. Benchmark compact quantized models on the Moto G54 and add only a verified local runtime adapter that passes memory, quality and thermal gates.
5. Run the pinned AirLLM host smoke tests and compatibility suite.
6. Add SAF project browsing, bounded editor and reviewable patch application.
7. Add sandboxed command execution and diff/apply/recovery.
8. Connect the AirLLM host through explicit trusted-network setup only after compatibility tests pass.
