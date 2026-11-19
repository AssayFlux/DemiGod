# DemiGod

DemiGod is an offline-first Android AI coding assistant: a ChatGPT-style coding chat with code generation/copy, project files, an integrated terminal and a permissioned coding agent.

## Current build status

The first Kotlin + Jetpack Compose Android scaffold is now on `Heaven`. It includes:
- Chat-first navigation, a message composer and selectable message text.
- Fenced code blocks with a copy action.
- Chat, Files and Terminal workspace destinations.
- Explicit preview state: model inference, project access and command execution are not connected yet.
- GitHub Actions build, unit-test and lint workflow.

The next milestone is to get CI green and install the debug APK on the target Android phone. The current UI is a foundation, not a finished coding assistant.

## Primary mobile target

The confirmed target is **Moto G54 5G, 12 GB RAM, Android 15** (256 GB storage reported). The 12 GB figure is physical device RAM, not memory available to the app. Local inference will start with compact quantized model candidates and must pass real-device memory, speed, battery and thermal benchmarks. The app remains useful without a model installed. Qwen3-Coder-Next is a separate research target, not a promised Moto G54 workload.

## Model strategy

- **Flagship research target:** [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next), 80B total parameters / approximately 3B activated per token.
- **AirLLM experiment:** a separate Python/PyTorch host bridge in [airllm/](airllm/README.md). It is not packaged in the APK and is not an Android runtime.
- **GGUF experiment:** [official Qwen GGUF repository](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF), to be tested separately with a compatible llama.cpp build.
- **Phone profile:** select a smaller local model only after real-device memory, speed, battery and thermal tests.

AirLLM compatibility with the exact Qwen3-Coder-Next revision remains unverified. Its host bridge is loopback-bound by default, requires a bearer token, and currently offers non-streaming chat completions only.

## Principles

- Offline operation is the default; network use is explicit and permissioned.
- Keep UI, agent, runtime, storage, execution and plugins behind replaceable interfaces.
- Active parameters are not stored weights. 3B active does not mean a 3B artifact or 11 GB phone compatibility.
- No fake model responses, command execution or test results.
- No model/device support claim without repeatable evidence.
- All commits go directly to **Heaven only**. No force-push or PR merge without explicit approval.

## Documentation

- [North Star](docs/product/NORTH_STAR.md)
- [Roadmap](docs/product/ROADMAP.md)
- [Build Rules](docs/engineering/BUILD_RULES.md)
- [Android platform adaptation](docs/architecture/ANDROID_PLATFORM_ADAPTATION.md)
- [Storage and streaming](docs/architecture/MODEL_STORAGE_AND_STREAMING.md)
- [Flagship target](docs/architecture/FLAGSHIP_480B_TARGET.md) (historical filename retained)
- [Qwen3-Coder-Next research plan](docs/research/480B_DATA_READING_PLAN.md) (historical filename retained)
- [AirLLM host experiment](airllm/README.md)
- [ADR-0001: Removable storage](docs/decisions/ADR-0001-removable-model-storage.md)
- [ADR-0002: Previous 480B target — superseded](docs/decisions/ADR-0002-480B-flagship-target.md)
- [ADR-0003: Qwen3-Coder-Next selection](docs/decisions/ADR-0003-qwen3-coder-next-flagship.md)
