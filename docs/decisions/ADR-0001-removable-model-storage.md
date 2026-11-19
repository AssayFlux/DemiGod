# ADR-0001: Removable Model Storage and Indexed Streaming

- **Status:** Accepted design direction; implementation details require device validation.
- **Date:** 2026-11-19
- **Context:** DemiGod is an offline-first Android coding assistant. Initial user storage target: 128 GB microSD plus USB-C external SSD.
- **Decision:** Separate model catalog, Android storage-provider adapter, model-format parser and inference backend. Use microSD as persistent secondary storage and USB SSD as preferred large-model storage. Use bounded indexed reads when the provider supports reliable random access. Treat USB media as removable and use Android SAF permissions.
- **Consequences:** Never assume a USB document URI is a normal path or always seekable. Do not require full-model extraction. If random reads are unsupported, use bounded staging or declare the provider unsupported for streamed inference. Validate file identity, lengths and hashes.
- **Rejected shortcut:** Treat ZIP or large external capacity as a substitute for RAM, memory bandwidth or compute. ZIP is not the default for quantized weights because compression benefit may not offset decompression cost.
- **Research track:** Indexed chunk packages and MoE-aware prefetch may be explored after the baseline format/backend has real-device benchmarks.
- **Validation:** Adapter conformance, random/sequential I/O, detach/reconnect, integrity, memory, thermal, energy and end-to-end inference tests on the target phone and drives.
