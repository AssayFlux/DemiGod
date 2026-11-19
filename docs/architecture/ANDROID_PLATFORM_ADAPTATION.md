# Android platform adaptation and first implementation

**Status:** Initial scaffold implemented; execution, persistence and inference adapters remain in progress.  
**Date:** 2026-11-19

## Product interface

DemiGod is chat-first, not terminal-first. The main surface is a conversational coding assistant with message history, a persistent composer, readable code output and copy affordances. Project files and terminal are dedicated workspace destinations. The phone layout uses full-screen destinations rather than a cramped desktop split pane.

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
- Chat-first navigation and a message composer.
- User/assistant message presentation and selectable text.
- A terminal destination that clearly reports execution is not connected.
- A project-files destination reserved for SAF integration.
- Explicit preview/model-not-connected status so no fake inference is presented as real.

Not implemented in this milestone: persistent chat database, actual inference connection, streaming, markdown parser, project SAF picker, file editor, terminal process runner, Git operations, model downloads or APK signing.

## AirLLM integration boundary

AirLLM lives in `airllm/` as a Python/PyTorch host experiment. It is not packaged in the APK and does not execute on the phone. The initial host bridge binds to loopback, requires a bearer token and exposes a non-streaming OpenAI-compatible chat endpoint. A phone connection is a separate opt-in integration and must use a private authenticated transport.

Qwen3-Coder-Next support is experimental until the exact pinned model revision passes load, generation, multi-turn recurrent-state, tokenizer/template and tool-call checks. The official model card describes an 80B-total hybrid Gated DeltaNet/Gated Attention model with approximately 3B active parameters; active parameters do not imply a 3B artifact or 11 GB phone compatibility.

## Execution safety

The terminal must be an isolated execution service, not unrestricted `Runtime.exec` from UI code. Before enabling it, implement workspace-scoped paths, command allow/deny policy, explicit approval, process timeouts, output caps, cancellation, environment isolation and audit records. Git writes, network access, destructive commands, push and merge require separate approvals.

## Next milestones

1. Add Compose UI tests and run the first Android CI build.
2. Add Room persistence and conversation export/delete.
3. Add a typed inference contract, streaming event model and a deterministic mock provider.
4. Add a verified local runtime adapter selected by actual device benchmark.
5. Add SAF project browsing and bounded editor.
6. Add sandboxed command execution and diff/apply/recovery.
7. Connect the AirLLM host through an explicit trusted-network setup only after its compatibility smoke tests pass.
