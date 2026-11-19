# DemiGod

DemiGod is an offline-first Android AI coding assistant. Its flagship research target is **Qwen3-Coder-480B-A35B-Instruct**. The goal is a polished, conversation-first Android APK with local model support and coding-agent workflows, plus optional GitHub and plugin connectivity when the user chooses to connect.

## North Star

DemiGod aims to combine the familiar, low-friction chat experience of leading AI assistants with the ability to inspect, edit, test and explain real software projects. The Android app is the primary product; the agent, model runtime, storage layer and plugins remain modular behind explicit interfaces.

## Project principles

- Offline operation is the default; network access is optional, visible and permissioned.
- The Android APK is the primary deliverable; Kotlin + Jetpack Compose is the default implementation direction.
- Chat is the primary user experience, with coding-agent capabilities available progressively when needed.
- The selected 480B checkpoint is the flagship research target; mobile feasibility must be proven, not assumed.
- 480B total parameters and 35B active parameters are different from model storage, RAM use and compute requirements.
- Model storage, Android storage access, model parsing and inference are separate layers.
- AirLLM-style memory efficiency is a baseline inspiration, not a permanent dependency or a claim of equivalent implementation.
- GitHub and other plugins are opt-in integrations with least-privilege permissions.
- Model output and tool output are untrusted; consequential actions require user control and review.
- Model support and performance must be proven on real devices.

## Storage target

The initial storage design targets a **128 GB microSD card** and a **USB-C external SSD**:
- Internal app storage holds metadata, indexes, bounded caches and recovery state.
- microSD provides persistent secondary model storage.
- USB-C SSD is the preferred location for the complete 480B model artifact.
- The runtime uses indexed reads and bounded streaming where the Android storage provider supports reliable random access.
- Full-model extraction to internal storage is not a design requirement.

The 128 GB microSD is not assumed to fit the complete 480B checkpoint. External storage does not replace RAM, memory bandwidth or compute. The 480B mobile target remains unproven until it passes tensor-read, inference, speed, power and thermal gates.

## Documentation

### Product and engineering direction
- [North Star](docs/product/NORTH_STAR.md)
- [Roadmap](docs/product/ROADMAP.md)
- [Build Rules](docs/engineering/BUILD_RULES.md)

### Model and storage architecture
- [480B flagship target and feasibility gates](docs/architecture/FLAGSHIP_480B_TARGET.md)
- [Model storage and streaming architecture](docs/architecture/MODEL_STORAGE_AND_STREAMING.md)
- [480B model data-reading research plan](docs/research/480B_DATA_READING_PLAN.md)
- [ADR-0001: Removable model storage and indexed streaming](docs/decisions/ADR-0001-removable-model-storage.md)
- [ADR-0002: 480B flagship model decision](docs/decisions/ADR-0002-480B-flagship-target.md)

## Current status

The repository contains architecture and research plans plus product direction. Runtime implementation, Android APK, supported-device matrix and benchmark evidence remain to be built. Design documents are not proof that the model already runs on a phone.

See the [Roadmap](docs/product/ROADMAP.md) for the staged build sequence and [Build Rules](docs/engineering/BUILD_RULES.md) for contribution and safety requirements.
