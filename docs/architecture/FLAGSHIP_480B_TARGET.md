# Flagship Model Target: Qwen3-Coder-Next

**Status:** Selected research target; runtime feasibility unproven  
**Decision:** [ADR-0003](../decisions/ADR-0003-qwen3-coder-next-flagship.md)

> Historical filename retained to avoid breaking existing links. The previous 480B target is superseded.

## 1. Selected model
- Model: [Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- Official GGUF: [Qwen/Qwen3-Coder-Next-GGUF](https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF)
- 80B total parameters; approximately 3B activated per token.
- 48 hybrid Gated DeltaNet/Gated Attention layers.
- 512 experts; 10 routed experts plus one shared expert.
- Native context: 262,144 tokens.
- Apache-2.0 license shown on the model card.

Verify against the exact pinned revision. These are model-card facts, not performance guarantees.

## 2. Total versus active parameters
Sparse activation may reduce per-token compute. It does not mean only 3B weights must exist. Full checkpoint and routed experts must be available. Storage is determined by the full artifact and quantization.

First-order decimal estimates for 80B parameters:
- BF16/FP16: approximately 160 GB.
- 8-bit: approximately 80 GB before metadata/overhead.
- 5-bit: approximately 50 GB before scales, block metadata, alignment and mixed tensor precision.
- 4-bit: approximately 40 GB before overhead.

These are arithmetic estimates, not downloadable file sizes. The official GGUF repository documents a Q5_K_M example; measure exact shard sizes and hashes before storage planning.

## 3. Separate backend tracks

### AirLLM / Transformers
AirLLM is Python/PyTorch layer-streaming inference. Its README describes broad Qwen-family support, but generic support is not proof of this exact model's compatibility.

Required proof: pin AirLLM/Transformers; load official Transformers checkpoint; verify hybrid DeltaNet recurrent state and attention state over prefill and multi-token decode; compare logits/output with trusted reference; test tokenizer/template/tool calls; measure host RAM, accelerator memory, disk staging, bytes read/token and speed.

Do not feed GGUF to AirLLM. This is host-side research, not Android-native inference.

### GGUF / llama.cpp
Official Qwen GGUF repository documents Q5_K_M and llama.cpp usage. Pin shards/hashes and llama.cpp revision; validate all hybrid operators, recurrent state, chat template, tool calls, context and multi-turn output. Measure memory, I/O, tokens/sec, power and thermals.

Host llama.cpp success does not prove Android/JNI/ABI/accelerator or SAF storage support.

## 4. Android reality
Reported phone: 11 GB RAM and 256 GB internal storage; exact phone model, SoC and external drive remain unknown. The full 80B checkpoint cannot be assumed to fit RAM. Low-GPU-memory AirLLM demonstrations do not imply low total host memory or Android compatibility. Disk does not replace memory bandwidth, compute, state cache or thermal headroom.

Policy: use a smaller verified model for daily Android; Qwen3-Coder-Next is a host/server experiment first. No promise of local 80B inference on the phone.

## 5. Feasibility gates
- F0: exact revision, license, tokenizer/template, config, shards and hashes.
- F1: AirLLM and GGUF/llama.cpp tested independently.
- F2: tensor/logit checks, recurrent state, multi-turn and tool-call correctness.
- F3: disk, host RAM, accelerator memory, context/state memory and I/O profile.
- F4: repository tasks, patch correctness, tests and tool reliability.
- F5: Android runtime, named phone, sustained speed, battery and thermals.

Record failed gates honestly. Never substitute another model/backend and call it Qwen3-Coder-Next support.
