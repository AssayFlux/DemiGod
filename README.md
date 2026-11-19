# DemiGod

DemiGod is an offline-first Android AI coding assistant. Its selected flagship coding-model target is **Qwen3-Coder-Next (80B total parameters, approximately 3B activated per token)**. The goal is a polished Android APK and a dependable coding-agent system that can inspect, edit, test and explain real projects.

## North Star
Build a coding assistant whose quality comes from the complete engineering system—not model size alone: repository understanding, planning, safe tool use, patch review, execution, testing, recovery and clear reporting.

## Selected model strategy
- **Flagship:** [Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next), 80B total / approximately 3B active, hybrid MoE coding-agent model with native 262,144-token context.
- **GGUF experiment:** [Official Qwen GGUF repository](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF). It documents a Q5_K_M example for llama.cpp; exact artifacts and compatibility must be validated.
- **AirLLM experiment:** separate Transformers/PyTorch host-side research. AirLLM is not Android-native and is not a GGUF loader.
- **Daily Android profile:** a smaller model proven on the actual phone. Flagship support remains experimental until benchmarks establish otherwise.
- Keep model providers and runtimes replaceable.

## Principles
- Offline operation is the default; network use is explicit and permissioned.
- Android APK is the primary deliverable; Kotlin + Jetpack Compose is the default direction.
- Total parameters, active parameters, weight storage, RAM/VRAM, context/state cache and compute are distinct.
- 3B active does not mean only 3B weights need storage or that an 11 GB phone can load the model.
- AirLLM reduces peak accelerator weight residency; it does not remove host RAM, I/O, state-cache, compute, thermal or bandwidth costs.
- No model/device combination is supported without repeatable tests.
- GitHub/plugins are opt-in and least-privilege.

## Documentation
- [North Star](docs/product/NORTH_STAR.md)
- [Roadmap](docs/product/ROADMAP.md)
- [Build Rules](docs/engineering/BUILD_RULES.md)
- [Flagship target](docs/architecture/FLAGSHIP_480B_TARGET.md) (historical filename retained)
- [Storage and streaming](docs/architecture/MODEL_STORAGE_AND_STREAMING.md)
- [Qwen3-Coder-Next research plan](docs/research/480B_DATA_READING_PLAN.md) (historical filename retained)
- [ADR-0001: Removable storage](docs/decisions/ADR-0001-removable-model-storage.md)
- [ADR-0002: Previous 480B target — superseded](docs/decisions/ADR-0002-480B-flagship-target.md)
- [ADR-0003: Qwen3-Coder-Next selection](docs/decisions/ADR-0003-qwen3-coder-next-flagship.md)

## Current status
This repository contains product, architecture and research documentation. It does not prove Qwen3-Coder-Next runs on Android or on the owner's phone. Audit model/runtime paths and benchmark a smaller local model while flagship feasibility research proceeds independently.
