# ADR-0002: Select Qwen3-Coder-480B-A35B-Instruct as DemiGod Flagship

- **Status:** Accepted target; feasibility unproven.
- **Date:** 2026-11-19
- **Decision:** DemiGod's flagship research target is Qwen3-Coder-480B-A35B-Instruct (480B total, 35B active, MoE).
- **Reason:** The project owner explicitly selected the 480B-parameter coding model. Storage, quantization, indexing, expert scheduling and benchmark work must be designed around the complete checkpoint.
- **Constraints:** 35B active does not mean 35B total storage. All model weights must be available. A 128 GB microSD is not a safe complete-model target. The USB-C SSD is the primary candidate, but capacity is unknown. External storage does not replace RAM, bandwidth or compute.
- **Feasibility caveat:** Practical on-phone token generation is not established. The project must pass artifact, quantization, read-path, runtime, generation and sustained mobile-use gates before claiming support.
- **Validation:** Use exact model revision, tensor inventory, hashes, reference tensor/logit comparisons, coding benchmarks, bytes-read-per-token, latency, memory, energy and thermal measurements.
- **Sources:** Official model card https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct ; vLLM deployment recipe https://github.com/vllm-project/recipes/blob/main/models/Qwen/Qwen3-Coder-480B-A35B-Instruct.yaml
