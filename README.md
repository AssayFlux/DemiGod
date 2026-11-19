# DemiGod

DemiGod is an offline-first Android AI coding assistant. Its flagship research target is **Qwen3-Coder-480B-A35B-Instruct**. The goal is local model inference and coding workflows on mobile devices, with optional GitHub connectivity when the user chooses to connect.

## Project principles

- Offline operation is the default; network access is optional, not a runtime dependency.
- The selected 480B checkpoint is the flagship target; mobile feasibility must be proven, not assumed.
- 480B total parameters and 35B active parameters are different from model storage, RAM use and compute requirements.
- Model storage, Android storage access, model parsing and inference are separate layers.
- AirLLM-style memory efficiency is a baseline inspiration, not a permanent dependency or a claim of equivalent implementation.
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

- [480B flagship target and feasibility gates](docs/architecture/FLAGSHIP_480B_TARGET.md)
- [Model storage and streaming architecture](docs/architecture/MODEL_STORAGE_AND_STREAMING.md)
- [480B model data-reading research plan](docs/research/480B_DATA_READING_PLAN.md)
- [ADR-0001: Removable model storage and indexed streaming](docs/decisions/ADR-0001-removable-model-storage.md)
- [ADR-0002: 480B flagship model decision](docs/decisions/ADR-0002-480B-flagship-target.md)

## Current status

The repository contains architecture and research plans. Runtime implementation, supported-device matrix and benchmark evidence remain to be built. Design documents are not proof that the model already runs on a phone.
