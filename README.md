# DemiGod

DemiGod is an offline-first Android AI coding assistant. Its goal is to provide local model inference and coding workflows on mobile devices, with optional GitHub connectivity when the user chooses to connect.

## Project principles

- Offline operation is the default; network access is optional, not a runtime dependency.
- Model storage, Android storage access, model parsing and inference are separate layers.
- AirLLM-style memory efficiency is a baseline inspiration, not a permanent dependency or a claim of equivalent implementation.
- Model support and performance must be proven on real devices.
- Total model parameters, active parameters, storage size, RAM use and compute cost are distinct quantities.

## Storage target

The initial storage design targets a **128 GB microSD card** and a **USB-C external SSD**:
- Internal app storage holds metadata, indexes, bounded caches and recovery state.
- microSD provides persistent secondary model storage.
- USB-C SSD is the preferred location for large model sets.
- The runtime uses indexed reads and bounded streaming where the Android storage provider supports reliable random access.
- Full-model extraction to internal storage is not a design requirement.

External storage does not replace RAM, memory bandwidth or compute. Very large models, including 480B-class MoE models, remain experimental research targets until actual phone benchmarks demonstrate feasibility.

## Documentation

- [Model storage and streaming architecture](docs/architecture/MODEL_STORAGE_AND_STREAMING.md)
- [ADR-0001: Removable model storage and indexed streaming](docs/decisions/ADR-0001-removable-model-storage.md)

## Current status

This repository contains the project foundation and architecture decisions. Runtime implementation, supported-device matrix and benchmark evidence must be added as milestones are completed. Design documents are not proof that a model already runs on a phone.
