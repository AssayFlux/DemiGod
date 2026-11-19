# ADR-0001: Removable Model Storage and Indexed Streaming

- **Status:** Accepted design direction; implementation details require device validation.
- **Date:** 2026-11-19
- **Context:** DemiGod is an offline-first Android coding assistant. The selected flagship research target is Qwen3-Coder-Next (80B total parameters, approximately 3B active). Initial user storage target discussed: 128 GB microSD plus USB-C external SSD.
- **Decision:** Separate model catalog, Android storage-provider adapter, model-format parser and inference backend. Use microSD as persistent secondary storage and USB SSD as candidate large-model storage. Use bounded indexed reads only when the provider supports reliable random access. Use Android SAF permissions and treat USB media as removable.
- **Backend distinction:** The official Qwen GGUF artifact is evaluated through a compatible GGUF runtime such as llama.cpp. AirLLM is a separate Transformers/PyTorch checkpoint experiment with its own decomposition/cache behavior. Do not feed GGUF files to AirLLM or assume AirLLM's host-side cache is a portable Android model package.
- **Consequences:** Never assume a USB document URI is a normal path or always seekable. Do not require full-model extraction as a universal strategy. If random reads are unsupported, use bounded staging or declare the provider unsupported for streamed inference. Validate file identity, lengths and hashes.
- **Rejected shortcut:** Treat ZIP or large external capacity as a substitute for RAM, memory bandwidth or compute. ZIP is not the default for quantized weights because compression benefit may not offset decompression cost.
- **Research track:** Indexed chunk packages and MoE-aware prefetch may be explored only after baseline Qwen3-Coder-Next format/backend paths have correctness and real-device benchmarks. Full model weights remain necessary despite sparse activation.
- **Validation:** Adapter conformance, random/sequential I/O, detach/reconnect, integrity, host/device memory, thermal, energy and end-to-end inference tests on the target phone and drives. No flagship Android support claim before evidence.
