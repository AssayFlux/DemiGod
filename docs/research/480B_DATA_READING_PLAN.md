# 480B Model Data-Reading Research Plan

**Status:** Proposed research and implementation sequence  
**Target:** Qwen3-Coder-480B-A35B-Instruct  
**Primary storage candidate:** USB-C external SSD  
**Secondary storage:** 128 GB microSD  
**Runtime target:** Offline Android, with host-side test harnesses allowed during development.

## 1. Research question

Can DemiGod read the complete 480B MoE checkpoint from removable storage, materialize the correct tensors and execute token generation with bounded memory and useful performance on a specified Android device?

Break this into independent questions:
1. Can we identify and validate every tensor and expert in the checkpoint?
2. Can we read required tensor ranges reliably from the selected USB storage provider?
3. Can we map router decisions to the exact expert tensors required for each layer?
4. Can the backend execute those tensors without requiring the entire checkpoint in RAM?
5. Can enough weights remain cached to avoid intolerable repeated SSD reads?
6. Can the phone sustain the resulting compute, memory and thermal load?

Do not conflate successful file reading with successful inference.

## 2. Model anatomy inventory

Before coding a scheduler, build a machine-readable model inventory from the pinned checkpoint:
- model config and architecture identifier;
- all tensor names, shapes, dtypes and byte ranges;
- shared attention, normalization and embedding tensors;
- router/gating tensors;
- each layer's expert tensor mapping;
- number and dimensions of experts per MoE layer;
- output head and any tied-weight relationships;
- tokenizer, special tokens and chat template;
- shard-to-tensor mapping and exact file hashes.

Cross-check the inventory against the official model configuration and a trusted reference implementation. Never infer tensor names or expert ordering from naming patterns alone.

Deliverable: model_inventory.json plus a validation report reconciling every tensor and shard.

## 3. Candidate read strategies

Evaluate the following independently; do not assume one is best before benchmarking.

### A. Whole-checkpoint load
Load all model weights into memory. This is a reference baseline only and is expected to exceed mobile resources. Use a capable host for correctness comparison if needed.

### B. Layer-wise streaming
Read a layer's required tensors into bounded buffers, execute that layer, then release/reuse buffers. Measure repeated reads across token steps. This controls peak memory but may cause large I/O per token.

### C. Expert-wise streaming
Keep shared layer tensors and selected expert tensors in a bounded cache. Fetch missing experts on demand. Record expert cache hit rate, misses, evictions and read bytes. The router's actual top-k output is authoritative.

### D. Hybrid layer + expert cache
Use a bounded layer working set, expert cache and prefetch queue. Tune cache size against available RAM/accelerator memory. Prevent prefetch from evicting tensors needed by active computation.

### E. Selective persistent cache
If the phone has sufficient memory, retain frequently reused shared tensors or experts across tokens. Cache decisions must be based on measured access frequency and memory pressure, not guesses.

For each strategy, measure peak memory, bytes read per token, random-read latency, time-to-first-token and sustained tokens/sec.

## 4. Read pipeline design

1. **Resolve volume:** identify SSD and persisted SAF permission; verify expected volume identity.
2. **Open package:** open shard handles through the storage adapter.
3. **Validate:** check manifest, shard size, hash, tensor index and bounds.
4. **Plan:** create an execution read plan from architecture and tensor inventory.
5. **Route:** execute router/gating operations and obtain exact expert IDs for the current token/layer.
6. **Schedule:** prioritize mandatory reads; prefetch only predicted data with spare budget.
7. **Read:** perform bounded positional reads; detect short reads and provider errors.
8. **Decode:** dequantize only required tensor blocks into aligned bounded buffers.
9. **Execute:** pass tensors to the supported backend and preserve required intermediate activations.
10. **Release/cache:** recycle buffers or retain them under the cache budget.
11. **Observe:** log bytes read, latency, queue depth, cache behavior and memory.
12. **Recover:** interrupt safely on disconnect; never continue with missing or stale tensor data.

The router must run before expert-specific fetches for that layer. Do not prefetch all experts as a fallback; that defeats sparse activation.

## 5. Storage and package compatibility

The first prototype should use an existing supported model representation if the selected backend can correctly represent this architecture and quantization. GGUF is a candidate only after verifying exact architecture/operator support and a valid conversion path for this model.

GGUF stores tensor names, dimensions, types and data offsets in its metadata/index structure; the data section is aligned. This makes indexed access conceptually possible, but the actual Android provider must support reliable seekable reads.

Source: https://github.com/ggml-org/ggml/blob/master/include/gguf.h

Do not convert the model to GGUF merely because the format is convenient. First verify:
- complete tensor coverage with no missing experts;
- correct MoE routing and expert ordering;
- numerical agreement with reference tensors;
- backend operator coverage;
- quantized output quality.

If no existing format/backend pair supports the model correctly, define a minimal experimental indexed container only after the tensor inventory and read benchmark exist.

## 6. Benchmark ladder

### R0 — File I/O only
Read known byte ranges from SSD, microSD and internal storage. Test sequential and random reads, cold/warm cache, block sizes, latency percentiles, short reads and disconnect.

### R1 — Tensor reconstruction
Read selected tensors and compare reconstructed values against trusted source within dtype/quantization tolerances.

### R2 — Single-layer execution
Execute one layer with known input activations and compare outputs to reference. Test shared tensors and MoE expert selection.

### R3 — Full forward pass
Run one complete forward pass on a host harness with bounded streaming. Verify logits against reference tolerances.

### R4 — Multi-token decode
Generate multiple tokens and record per-token bytes read, cache hit rate, p50/p95 latency and memory use.

### R5 — Android port
Repeat on target phone using the actual USB-C SSD, cable, enclosure and Android storage provider. Measure sustained performance, energy and thermals.

## 7. Metrics that decide success

Mandatory metrics:
- model package bytes and tensor count;
- storage bytes read per prompt and per generated token;
- sequential throughput and random IOPS;
- p50/p95/p99 read latency;
- short-read, timeout and disconnect rates;
- expert-cache hit/miss rate and evictions;
- prefetch accuracy and wasted bytes;
- peak managed/native/accelerator memory;
- time-to-first-token and tokens/sec;
- energy per generated token and thermal throttling;
- output correctness against reference;
- coding-task quality and quantization regression.

A benchmark reporting only model load time or average tokens/sec is insufficient.

## 8. Go/no-go rules

- No model is marked supported until every tensor and expert is accounted for.
- No storage provider is marked random-access capable until positional reads are tested under load.
- No quantization is accepted solely because it fits on disk.
- No streaming strategy is accepted without measuring bytes read per token.
- No Android feasibility claim is made without a named device and sustained thermal test.
- If storage I/O dominates token latency, prioritize cache/locality/quantization research before UI or agent feature work.

## 9. Immediate work sequence

1. Pin the official model revision and collect config/tokenizer/shard metadata.
2. Build the model inventory and shard/hash verifier.
3. Audit current conversion and inference backend support for this exact Qwen3 MoE architecture.
4. Build a host-side random-read/tensor-reconstruction harness.
5. Benchmark USB SSD and microSD on the target Android phone.
6. Implement one-layer reference execution and MoE expert selection.
7. Compare layer streaming, expert caching and hybrid scheduling.
8. Only then decide whether a custom indexed package or advanced compression is justified.

## 10. Unknowns

- Exact phone, SoC, RAM, Android version and accelerator APIs.
- SSD capacity, filesystem, bridge, cable and measured random-read performance.
- Exact quantized artifact and its accuracy.
- Backend/operator support for the precise model revision.
- Actual per-layer tensor sizes and expert layout.
- Sustainable memory budget after Android and app overhead.
- Minimum acceptable tokens/sec and power/thermal envelope.

These are inputs to the next detailed implementation plan, not assumptions to fill with invented values.
