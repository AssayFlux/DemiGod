# ADR-0003: Select Qwen3-Coder-Next as DemiGod Flagship

- **Status:** Accepted target; backend and Android feasibility unproven.
- **Date:** 2026-11-19
- **Decision:** Select **Qwen/Qwen3-Coder-Next** as DemiGod's flagship coding-model research target.
- **Facts:** Official model card identifies 80B total, approximately 3B active, 48 hybrid Gated DeltaNet/Gated Attention layers, 512 experts with 10 routed plus one shared, 262,144 native context and Apache-2.0 license. Re-verify pinned revision.
- **Reason:** Designed for coding agents and long-horizon tool-oriented development. DemiGod prioritizes coding-agent workflow quality rather than parameter count alone.
- **GGUF:** Use official Qwen/Qwen3-Coder-Next-GGUF as llama.cpp experiment baseline; model card documents Q5_K_M example. Exact size, hashes, operator support and coding quality must be measured.
- **AirLLM:** Evaluate separately as Transformers/PyTorch host-side experiment. Generic Qwen-family support does not prove exact hybrid-state compatibility. Do not feed GGUF into AirLLM.
- **Android:** Reported phone has 11 GB RAM and 256 GB internal storage. Active parameters do not eliminate the complete 80B weight set. No Android support claim until correctness, memory, I/O, speed, power and thermal gates pass on named device.
- **Architecture:** Keep agent provider-independent; implement distinct runtime adapters/model profiles. A smaller verified local model remains daily Android profile while flagship is evaluated.
- **Validation:** Pin revisions; validate tokenizer/template, recurrent state, multi-token/multi-turn correctness, tool use, hashes, memory, bytes read/token, TTFT, tokens/sec and coding outcomes.
- **Sources:**
  - https://huggingface.co/Qwen/Qwen3-Coder-Next
  - https://huggingface.co/Qwen/Qwen3-Coder-Next-GGUF
  - https://github.com/lyogavin/airllm
