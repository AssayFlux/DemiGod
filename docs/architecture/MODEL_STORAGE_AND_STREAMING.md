# DemiGod Model Storage & Streaming Architecture

**Status:** Proposed baseline architecture  
**Date:** 2026-11-19  
**Target:** Android offline model library using a 128 GB microSD card and a USB-C external SSD.

## 1. Goals and non-goals

DemiGod must operate offline after installation of the app and model assets. It must support removable storage, bounded memory use, integrity verification, resumable imports and safe recovery from drive disconnection. It must not require extracting every model into internal phone storage.

Storage capacity does not imply runtime feasibility. RAM, memory bandwidth, compute, accelerator support, context/KV-cache size, heat and battery consumption remain separate constraints. The selected flagship is Qwen3-Coder-480B-A35B-Instruct. Its complete checkpoint is the target for storage and streaming research, but practical phone inference is unproven. See [FLAGSHIP_480B_TARGET.md](FLAGSHIP_480B_TARGET.md) and [480B_DATA_READING_PLAN.md](../research/480B_DATA_READING_PLAN.md).

## 2. Three-tier storage design

| Tier | Responsibility | Policy |
|---|---|---|
| Internal app-private storage | Catalog database, manifests, indexes, small metadata, bounded cache, import journal and diagnostics | Keep lean; never silently copy huge models here |
| 128 GB microSD | Persistent secondary model library; small/medium quantized models and optional staging | Check real free space and reserve; treat as removable |
| USB-C external SSD | Preferred library for large models and multi-shard model sets | Treat as transient/removable; user grants access; handle detach/reconnect |

128 GB is nominal capacity, not usable free space. The external SSD capacity, filesystem, enclosure and sustained random-read performance are not yet known. Do not set a maximum supported model size until those are measured.

## 3. Android access model

### microSD
- Discover stable removable volumes using Android-supported storage APIs.
- Prefer app-specific directories where supported.
- Persist a volume identity and relative path, not an absolute mount path as the only locator.
- Re-resolve volume paths after remount and verify that the expected files are still present.
- Benchmark actual random and sequential reads on the target phone/card.

### USB-C SSD
- Use Android Storage Access Framework (SAF) document-tree selection and persisted URI permissions where available.
- Do not assume a USB document URI is a normal filesystem path.
- Access files through a storage-provider adapter using ContentResolver/document-provider APIs.
- Probe whether the provider returns a seekable file descriptor and supports reliable positional reads. Some providers may expose stream-like access only.
- If random access is unavailable or unreliable, use a bounded staging fallback or declare that provider unsupported for streamed inference. Never silently pretend that sequential access is random access.
- Handle detach, permission revocation, provider errors and device sleep as ordinary lifecycle events.

Android treats portable USB media differently from semi-permanent external volumes; SAF is the appropriate user-mediated access route for portable media. The implementation must be validated against the actual device and provider.

## 4. Storage adapter contract

Keep Android URIs and mount paths out of the inference engine. Define a platform-neutral adapter with these operations:

- stat: size, identity and available version metadata.
- readAt(offset, length): exact bounded positional read, or explicit unsupported/error.
- openSequential: sequential fallback for import and verification.
- isAvailable: current volume/provider availability.
- close: release descriptors and provider resources.

Validate all offsets and lengths before reads. A short read is an error. Native code receives only validated descriptors/handles through a narrow JNI boundary. Never pass arbitrary provider paths into native inference code.

## 5. Model library and format

Use a catalog independent of physical paths. Each model record should include:
- stable model ID, family, architecture and revision;
- tokenizer and chat-template identity;
- quantization type and measured bits-per-weight;
- shard/tensor inventory, expected lengths and cryptographic hashes;
- runtime/backend requirements;
- license and source provenance;
- storage volume identity and relative document/path identity;
- validation state and last integrity-check result.

Suggested logical layout:

    DemiGod/
      library/<model-id>/
        manifest.json
        model-00001-of-000NN.gguf
        model-00002-of-000NN.gguf
      imports/
      diagnostics/

Prefer supported quantized formats such as GGUF when the chosen backend supports the model architecture and operators. Parse metadata and tensor descriptors before bulk weight reads. Support multi-file models through a manifest and per-shard tensor index. Validate format versions, tensor bounds, alignment, dimensions and file sizes before native access.

Do not invent a new weight format for the first release. A future DemiGod indexed package may add independently addressable chunks, 64-bit offsets, per-chunk checksums, optional compression and bounded decompression. Ordinary ZIP compression is not the default: already-quantized weights may compress poorly, while decompression adds CPU cost and latency. Adopt compression only when end-to-end tests prove a net benefit.

## 6. Streaming pipeline

1. Discover model and storage volume.
2. Validate manifest, shard lengths, hashes and backend compatibility.
3. Build or load a tensor/layer read plan from the model index.
4. Schedule bounded reads ahead of compute.
5. Read aligned ranges through the storage adapter.
6. Verify chunk integrity when package metadata provides it.
7. Decode/dequantize only required blocks into bounded buffers.
8. Dispatch tensors to CPU/GPU/NPU memory where supported.
9. Recycle buffers as soon as dependencies complete.
10. On storage loss, cancel reads, invalidate affected cache entries and interrupt generation safely.

Use double/triple buffering only when measurements show useful overlap between storage I/O and compute. Adapt queue depth, prefetch window and cache budget to measured latency and available memory. Never let prefetch consume memory required by Android or the active runtime.

### Cache policy
- Strict byte-budgeted LRU or workload-aware cache.
- Pin only tensors needed for the current execution window.
- Separate metadata/index cache from weight-block cache.
- Avoid duplicate copies between managed and native layers.
- Record cache hits, misses, evictions and bytes read.
- Invalidate cache when volume identity, file size, manifest version or hash changes.

## 7. MoE-specific considerations

For a Mixture-of-Experts model, all expert weights still need to exist on storage even if only a subset is activated per token. Active parameter count is not total storage size.

A future scheduler may use router outputs to prioritize expert reads, prefetch likely experts and cache recently used experts under a strict memory budget. It must measure prediction accuracy and wasted I/O and fall back to demand reads. Expert prediction does not remove the cost of accessing expert weights. External storage alone does not make a 480B model practical on a phone.

## 8. Import, integrity and recovery

Imports are transactional:
1. User selects source and destination volume.
2. Check free space plus configured reserve.
3. Copy/import into a temporary staging location.
4. Verify byte lengths and cryptographic hashes.
5. Validate model metadata and tensor ranges.
6. Publish the completed model atomically where supported; otherwise use a commit marker and recovery journal.
7. Resume or clean incomplete imports after process death.

A multi-shard model is ready only when every required shard is present and validated. Downloads, when explicitly initiated online, must support pause/resume and hash verification. Offline imports from files already on the device must remain supported.

If the SSD disconnects during inference:
- stop issuing reads and cancel outstanding operations;
- release descriptors and affected buffers;
- preserve the prompt, conversation and output already committed;
- mark generation interrupted, never successful;
- let the user reconnect/reselect the volume and verify identity;
- resume only if the backend can restore a consistent execution state; otherwise restart the current generation safely.

## 9. Capacity and safety policy

- Display actual free bytes, not nominal card capacity.
- Initial proposed free-space reserve: 10% of volume capacity or 8 GiB, whichever is larger. Validate this default through usability testing.
- Do not silently use internal storage as overflow.
- Do not split a model across microSD and SSD in the first release unless every shard is explicitly mapped and missing-volume behavior is tested. Prefer one complete model set on one volume.
- Treat all model files/manifests as untrusted input.
- Check integer overflow, offset/length bounds, alignment, tensor dimensions and decompression limits.
- Never store GitHub credentials or private repository data in shared external storage.
- Keep sensitive app state in app-private storage and Android Keystore-backed mechanisms.
- Never auto-execute files from model storage.

## 10. Performance validation

Do not make universal speed claims for microSD or USB SSD. Test the exact phone, Android version, card, SSD, enclosure, cable and filesystem.

Required measurements:
- sequential throughput and random-read IOPS;
- random read latency at 4 KiB, 64 KiB, 256 KiB and 1 MiB;
- p50/p95/p99 latency, short-read rate and error rate;
- cold/warm cache behavior;
- time-to-first-token and end-to-end tokens/sec;
- peak app/native memory and accelerator allocation;
- battery/energy use and thermal throttling over sustained inference;
- detach/reconnect, screen-off and process-death recovery.

Run internal, microSD and USB SSD tests separately. Advertised interface speed is not a substitute for real phone measurements.

## 11. Milestones

### S0 — Storage discovery and benchmark harness
Discover internal, microSD and SAF-granted USB storage; implement adapter conformance tests; measure real device I/O and detach behavior.

### S1 — Reliable model library
Import/copy/verify supported quantized model files; persist catalog and volume identity; recover interrupted imports; run a small supported model from internal and microSD storage.

### S2 — USB SSD streaming prototype
Implement SAF adapter and seekability probe; bounded positional reads and cache; run a supported model from SSD without full internal extraction; pass detach/reconnect and integrity tests.

### S3 — Performance scheduling
Add adaptive prefetch, bounded cache and I/O/compute overlap; measure latency, tokens/sec, memory, power and thermals.

### S4 — Advanced formats and MoE research
Prototype indexed chunk packaging only if baseline tests justify it; test block-level compression, quantization-aware layouts and expert-aware prefetch with accuracy/wasted-I/O reporting.

## 12. Acceptance criteria

The subsystem is not complete until:
- microSD and user-granted USB SSD can be discovered and identified where supported;
- model import is hash-verified and does not require a full-model internal copy;
- random-access capability is detected, with a documented fallback for unsupported providers;
- cache and memory budgets are enforced;
- SSD removal during a read causes controlled interruption, not crash or silent corruption;
- interrupted imports recover without marking incomplete models ready;
- tensor offsets and lengths are validated before native access;
- benchmarks report real-device latency, throughput, memory, tokens/sec, power and thermal behavior;
- offline inference works with networking disabled once a model is installed.

## 13. Open decisions

- Exact phone model, RAM, SoC and Android version.
- SSD capacity, filesystem, enclosure and USB bridge.
- First-release model family and quantization formats.
- Whether the selected backend can consume seekable descriptors or requires a local file path.
- Minimum Android API level.

Resolve these through device tests rather than assumptions based on storage capacity.
