# Qwen3-Coder-Next and AirLLM Research Plan

**Status:** Proposed research sequence  
**Target:** Qwen/Qwen3-Coder-Next  
**Backend tracks:** AirLLM/Transformers and GGUF/llama.cpp, tested separately

> Historical filename retained for link stability; this replaces the former 480B plan.

## 1. Research question
Can DemiGod run Qwen3-Coder-Next correctly and usefully through a memory-efficient backend, and what host/device profiles are required? Separate model correctness, backend compatibility, storage streaming and Android feasibility.

## 2. Facts to pin
Verify at exact revision: 80B total, approximately 3B active; 48 hybrid Gated DeltaNet/Gated Attention layers; 512 experts, 10 routed plus one shared; native 262,144 context; Apache-2.0 model-card license. Record config, tokenizer, chat template, generation defaults, shard inventory, sizes and SHA-256. Active parameter count is not storage size.

## 3. Track A — AirLLM / Transformers
AirLLM describes layer-wise model streaming and broad Qwen-family support. This is a host-side experiment, not proof of this exact model's compatibility.

1. Pin AirLLM, Transformers, PyTorch, Accelerate and compute stack.
2. Start from official Transformers checkpoint, not GGUF.
3. Verify model-class detection and layer offload behavior.
4. Validate DeltaNet recurrent/convolution state and Gated Attention state across prefill and at least 100 decode steps.
5. Ensure state is not reset between tokens or tool turns.
6. Compare logits/output with trusted non-streaming reference.
7. Validate tokenizer, template, tool calls, stop tokens and multi-turn behavior.
8. Measure disk/cache footprint, host RAM, accelerator memory, bytes read/token, TTFT and sustained tokens/sec.
9. Test multiple context sizes; 256K is a model ceiling, not a phone default.

Pass only with correct multi-token and multi-turn generation plus reproducible resource measurements.

## 4. Track B — GGUF / llama.cpp
Official Qwen GGUF repository documents Q5_K_M as a llama.cpp example.

1. Pin GGUF shards, quant metadata and hashes.
2. Pin llama.cpp commit, build flags and target ABI.
3. Verify hybrid architecture operators and recurrent-state behavior.
4. Test tokenizer/template and tool calls.
5. Compare coding quality against reference.
6. Measure RAM/accelerator allocation, file I/O, TTFT, tokens/sec, context and thermals.
7. After host correctness, build Android/JNI prototype and test SAF-backed storage.

Do not pass GGUF files to AirLLM. These are separate tracks.

## 5. Shared correctness suite
Code completion; multi-file patch; repository Q&A; schema-valid tool calls; multi-step tool loop; multi-turn state persistence; deterministic output/logit comparison where possible; context truncation; cancellation and cleanup. Score patch correctness, compile/test pass rate, tool validity and repository-task success.

## 6. Storage and memory experiments
Measure full checkpoint and converted artifact size, temporary AirLLM decomposition/cache, bytes read/token, cache hit/eviction, host RAM, accelerator memory, context/recurrent state, p50/p95/p99 read latency, TTFT, sustained speed, energy and thermals. Layer streaming may reduce accelerator residency while repeated reads dominate decode.

## 7. Android feasibility ladder
Host reference correctness; AirLLM host compatibility; GGUF host compatibility; Android runtime/operator support; SAF positional-read tests; small-context single-turn; multi-turn state; sustained speed/power/thermal on named phone; decision against published minimum useful speed. Reported phone is 11 GB RAM/256 GB storage; SoC and Android version unknown.

## 8. Go/no-go
No backend support from successful weight loading alone. No AirLLM-to-Android claim from Python support. No GGUF claim without operator/state validation. No 256K promise without state-memory tests. No quantization chosen only for disk fit. If 11 GB RAM cannot sustain it, keep flagship host/server-side and ship smaller verified Android model.

## 9. Immediate sequence
Pin official model/GGUF revisions; create host reference; test AirLLM/Transformers and recurrent state; test Q5_K_M GGUF with current llama.cpp; run shared correctness/tool suite; compare disk/RAM/accelerator/I/O/speed; then decide whether Android porting is justified.
