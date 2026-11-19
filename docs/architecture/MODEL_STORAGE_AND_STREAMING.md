# DemiGod Model Storage & Streaming Architecture

**Status:** Proposed architecture; exact model/backend paths require validation  
**Selected flagship:** Qwen3-Coder-Next (80B total / approximately 3B active)

## 1. Goals
Support offline model libraries, removable storage, integrity checks, bounded reads, resumable imports and safe recovery. Storing a model does not prove useful inference. RAM, accelerator memory, context/state cache, bandwidth, compute, power and heat are independent limits.

## 2. Storage tiers
| Tier | Responsibility | Policy |
|---|---|---|
| Internal app-private | Catalog, metadata, indexes, bounded caches, journals | Keep lean; do not silently stage huge models |
| microSD | Persistent secondary library and smaller models | Measure free space and random reads |
| USB-C SSD | Candidate storage for large multi-shard artifacts | User-selected via SAF; removable; benchmark exact setup |

Phone internal storage is not a RAM substitute. SSD capacity/interface are not yet known.

## 3. Storage adapter
Keep Android URIs/paths out of inference code. Expose stat(identity,size), readAt(offset,length), openSequential, isAvailable and close. Use Android SAF for portable USB storage. Probe seekability and positional-read correctness; do not assume every provider supports random access. Validate offsets, lengths, short reads and volume identity. Handle detach and permission revocation.

## 4. Artifact catalog
Record model ID, source/revision, architecture, tokenizer/template, quantization, shard list, sizes, hashes, license, backend requirements and validation state.

Backend formats are separate:
- GGUF is consumed by a compatible GGUF runtime such as a validated llama.cpp build.
- AirLLM consumes a supported Transformers/PyTorch checkpoint and may decompose/cache layers on host storage.
- Never route GGUF into AirLLM or assume its Python cache is an Android model package.

Mark ready only after all shards and metadata are verified and the selected backend passes compatibility checks.

## 5. Streaming and cache
Resolve volume; validate manifest/shards/hashes; build tensor index; schedule bounded reads; validate byte counts; decode only needed blocks; dispatch tensors; recycle or cache under strict budget; record I/O and memory; cancel safely on drive removal.

Do not invent a custom package format until a real backend requires it and baseline measurements justify it.

## 6. MoE and hybrid state
All experts exist in the full artifact. The model card describes 10 routed experts plus a shared expert; confirm router semantics and tensor names from pinned config/code. Expert-aware prefetch is an optimization, never a replacement for actual router outputs.

Qwen3-Coder-Next also uses hybrid Gated DeltaNet/Gated Attention. Recurrent/convolution state and attention/KV state must persist correctly across tokens. A naive load-layer-then-discard approach may break decoding if required state is not retained. Validate backend state handling before Android streaming design.

## 7. Import and recovery
User selects source/destination; check free space; stage transactionally; resume or clean interrupted imports; verify lengths and hashes; validate tensor metadata and shard completeness; publish atomically where possible. On drive removal cancel reads, release handles, preserve completed output and mark generation interrupted. Resume only if backend state can be restored consistently.

## 8. Performance validation
Measure on exact phone, Android version, provider, SSD/enclosure/cable and runtime:
- sequential throughput and random-read IOPS/latency;
- p50/p95/p99 read latency and short-read/error rates;
- bytes read per token and cache hit/miss/eviction;
- host RAM, native memory, accelerator memory and context/state cache;
- TTFT and sustained tokens/sec;
- battery/energy and sustained thermals;
- detach/reconnect and process-death recovery.

## 9. Acceptance
Artifacts hash-verified and complete; random access tested; memory/cache budgets enforced; drive removal controlled; compatibility recorded per exact revision; offline inference proven for supported models. No Android support claim without real-device correctness and sustained performance.
