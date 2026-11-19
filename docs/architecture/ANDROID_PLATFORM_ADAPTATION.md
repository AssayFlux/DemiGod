# Android platform adaptation and first implementation

**Status:** Initial scaffold implemented; runtime and workspace integrations remain in progress.  
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

## AirLLM integration boundary

AirLLM lives in `airllm/` as a Python/PyTorch host experiment. It is not packaged in the APK and does not execute on the phone. The initial host bridge requires a locally downloaded, revision-pinned checkpoint, binds to loopback, requires a bearer token and exposes a non-streaming OpenAI-compatible chat endpoint. The Android app is not connected to it yet.

AirLLM's current AutoModel architecture detection uses `trust_remote_code=True`; loading a checkpoint can execute Python from the model snapshot. Use a reviewed official snapshot in an isolated host environment. Qwen3-Coder-Next support remains experimental until the exact pinned snapshot passes load, generation, multi-turn recurrent-state, tokenizer/template and tool-call checks.

## Execution safety

The terminal must be an isolated execution service, not unrestricted `Runtime.exec` from UI code. Before enabling it, implement workspace-scoped paths, command allow/deny policy, explicit approval, process timeouts, output caps, cancellation, environment isolation and audit records. Git writes, network access, destructive commands, push and merge require separate approvals.

## Next milestones

1. Obtain a green Android CI build and install the debug APK on the target phone.
2. Add Room persistence and conversation export/delete.
3. Add a typed inference contract, streaming event model and a deterministic mock provider.
4. Add a verified local runtime adapter selected by actual device benchmark.
5. Run the pinned AirLLM host smoke tests and compatibility suite.
6. Add SAF project browsing, bounded editor and reviewable patch application.
7. Add sandboxed command execution and diff/apply/recovery.
8. Connect the AirLLM host through explicit trusted-network setup only after compatibility tests pass.
