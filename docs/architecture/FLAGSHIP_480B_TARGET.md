# 480B Flagship Target: Qwen3-Coder-480B-A35B-Instruct

**Status:** Selected flagship research target  
**Date:** 2026-11-19  
**Scope:** Product target and feasibility constraints, not a claim of successful Android deployment.

## 1. Selected model

DemiGod's flagship target is **Qwen/Qwen3-Coder-480B-A35B-Instruct**.

Official model-card facts:
- 480 billion total parameters.
- 35 billion active parameters per token.
- Mixture-of-Experts architecture.
- 160 experts, 8 activated experts.
- 62 layers.
- 96 query heads and 8 key/value heads.
- Native context length: 262,144 tokens.
- Non-thinking instruction model.

Source: https://huggingface.co/Qwen/Qwen3-Coder-480B-A35B-Instruct

Pin the exact checkpoint revision, tokenizer, chat template, license and source hashes before approving a model package.

## 2. Product decision

The 480B model is the flagship target. DemiGod's architecture, storage catalog, read scheduler, quantization evaluation and benchmark plan must account for the entire 480B checkpoint.

This decision does **not** mean:
- the full model fits on the 128 GB microSD;
- the model can run at useful speed on an arbitrary Android phone;
- 35B active parameters means only 35B need to be stored;
- external SSD storage substitutes for RAM or accelerator memory;
- a low-bit quantization is automatically accurate enough for coding.

The complete checkpoint contains all experts and shared weights. The runtime may access only selected experts for a token, but those expert weights still need to be stored and made available.

## 3. Theoretical weight-size arithmetic

First-order lower-bound estimate:

weight bytes = parameter count × bits per parameter / 8

Using 480,000,000,000 parameters and decimal GB:

| Nominal precision | Theoretical weight payload |
|---|---:|
| 16-bit | 960 GB |
| 8-bit | 480 GB |
| 4-bit | 240 GB |
| 3-bit | 180 GB |
| 2-bit | 120 GB |
| 1-bit | 60 GB |

These are arithmetic estimates, **not promised downloadable file sizes**. Real packages include quantization scales, block metadata, alignment, tensor-specific precision, tokenizer/configuration and possibly auxiliary tensors. Actual quantized file size must be measured from the exact checkpoint.

The official vLLM recipe describes server-scale deployments and lists approximately 1,152 GB for BF16, 576 GB for FP8 and 288 GB for NVFP4 in its deployment configurations. These are not Android requirements, but they demonstrate that ordinary supported deployments are currently server-class.

Source: https://github.com/vllm-project/recipes/blob/main/models/Qwen/Qwen3-Coder-480B-A35B-Instruct.yaml

## 4. Storage implications

Known user storage:
- 128 GB nominal microSD.
- USB-C external SSD, capacity not yet specified.
- Phone internal storage is not a model-capacity target.

Consequences:
- The 128 GB microSD cannot be assumed to hold a complete 480B package. Even the theoretical 2-bit payload is 120 GB before overhead and free-space reserve.
- The USB-C SSD is the required primary candidate for a complete 480B package.
- A 256 GB SSD may be sufficient for some 2-bit/3-bit artifacts, depending on actual file size and free-space reserve.
- A 512 GB SSD is a more sensible initial capacity target for experimenting with 4-bit artifacts and working room; it is not a performance guarantee.
- Do not split shards across microSD and SSD in the first prototype. Keep one complete model package on one volume unless multi-volume operation is deliberately implemented and tested.

Do not buy storage based only on theoretical bit-width arithmetic. First obtain exact quantized artifact sizes, confirm SSD capacity and filesystem, and reserve free space.

## 5. The critical I/O problem

The model has 35B active parameters per token. A rough active-weight traffic estimate, if those weights must be fetched from storage for every generated token, is:

| Active-weight precision | Approximate active payload per token |
|---|---:|
| 4-bit | 17.5 GB/token |
| 3-bit | 13.125 GB/token |
| 2-bit | 8.75 GB/token |
| 1-bit | 4.375 GB/token |

This simplified estimate derives from active parameter count. Actual traffic depends on tensor layout, quantization, cache reuse, shared weights, routing, read amplification and runtime implementation.

This table exposes the central problem: **storage capacity is not inference throughput**. Re-reading multi-gigabyte active weights for each token from a removable SSD is likely to be extremely slow. A layer-at-a-time design reduces peak RAM but does not automatically eliminate repeated I/O across token steps.

The research plan must therefore optimize:
1. Keep reusable weights in RAM/accelerator memory where possible.
2. Keep selected expert weights hot when routing locality makes reuse likely.
3. Load by layer and expert with bounded buffers, not the entire checkpoint.
4. Prefetch only when measured predictions reduce stalls.
5. Reduce bytes read through validated quantization and tensor layouts.
6. Measure actual bytes read per generated token, not only nominal model size.
7. Establish a minimum useful tokens/sec threshold before declaring a phone configuration supported.

Even a fast external SSD cannot make this problem disappear. Phone USB bandwidth, memory copies, compute speed, heat and battery are additional bottlenecks.

## 6. Accuracy is a hard constraint

Quantization must be evaluated on coding tasks, not selected by smallest file size. Compare candidate bit widths and formats against a trusted reference checkpoint using:
- code generation and patch correctness;
- repository-level edit tasks;
- compilation and test pass rates;
- tool-call and structured-output validity;
- long-context retrieval and instruction adherence;
- perplexity or log-likelihood where applicable;
- output stability across repeated runs.

A smaller artifact that breaks code correctness is not an acceptable optimization. Keep a documented quality/performance frontier and do not promote an experimental quantization as production-ready without evidence.

## 7. Feasibility gates

- **G0 — Artifact audit:** exact official checkpoint, file inventory, licensing, architecture, tokenizer and hash inventory.
- **G1 — Quantization audit:** reproducible quantized candidates; exact file sizes, format compatibility and coding-quality deltas.
- **G2 — Read-path proof:** indexed reads and correct tensor materialization from SSD on Android or a representative host harness.
- **G3 — Runtime proof:** validate router/expert dispatch, tensor correctness and one complete forward pass using bounded memory.
- **G4 — Token-generation proof:** produce correct multi-token output with measured storage traffic, latency, memory and thermal behavior.
- **G5 — Mobile usefulness:** meet a published minimum tokens/sec and sustained thermal/power envelope on a named phone model.

A failure at a gate is a result, not a reason to hide the limitation. Continue research or revise the supported-device claim; do not label the 480B mobile target complete prematurely.

## 8. Architecture consequence

DemiGod should be designed as a storage-backed inference research system with:
- model manifest and tensor/expert index;
- Android storage adapters for microSD and SAF-granted USB SSD;
- quantization-aware tensor readers;
- bounded RAM/accelerator cache;
- layer/expert read scheduler;
- I/O/compute telemetry;
- integrity and interruption recovery;
- pluggable execution backend.

The design must remain honest about the possibility that a phone can store the 480B model but cannot generate tokens from it at useful speed. The first engineering task is to prove the read path and establish a measured lower bound—not to promise a finished phone experience.
