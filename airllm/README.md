# DemiGod AirLLM host experiment

This is a **host-side research adapter**, not an Android inference engine. It exposes a small OpenAI-compatible, non-streaming chat endpoint for a future Android opt-in host connection.

## Compatibility status

- Target under test: `Qwen/Qwen3-Coder-Next`.
- AirLLM's current generic path streams standard Transformers causal-LM layer modules; exact model compatibility still requires testing.
- AirLLM's generic Qwen-family support is not proof that this model's hybrid Gated DeltaNet/Gated Attention state is correct.
- The bridge currently requires a CUDA host by default. CPU execution is possible only when explicitly enabled and adequately provisioned; it may be impractically slow.
- The endpoint is non-streaming and is not connected to the Android app yet.
- A successful model load alone is not sufficient. Verify single-turn, multi-turn, recurrent-state preservation, tokenizer/template, tool calls and code-task correctness.

## Prepare a pinned local model snapshot

AirLLM's current `AutoModel` architecture detection does not reliably forward a revision parameter through every config-loading path. Therefore, download an exact Hugging Face commit into a local snapshot first; the service refuses to load a model without a local path and revision label.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r airllm/requirements.txt

export MODEL_REVISION=<EXACT_HUGGING_FACE_COMMIT_SHA>
hf download Qwen/Qwen3-Coder-Next \
  --revision "$MODEL_REVISION" \
  --local-dir /models/qwen3-coder-next
```

AirLLM decomposes the checkpoint into layer shards on disk. Check available storage before starting; original checkpoint files and decomposed cache may coexist and can require substantial additional disk space. Do not put model files in the Android APK or phone internal storage.

## Start the host bridge

```bash
export DEMIGOD_MODEL_ID=Qwen/Qwen3-Coder-Next
export DEMIGOD_MODEL_PATH=/models/qwen3-coder-next
export DEMIGOD_MODEL_REVISION="$MODEL_REVISION"
export DEMIGOD_MODEL_CACHE=/fast-local-ssd/demigod-airllm
export DEMIGOD_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python airllm/server.py
```

The server binds to `127.0.0.1:8765` by default. Do not expose it directly to the public internet. A future phone-to-host connection must be explicitly configured and protected (prefer a private VPN or authenticated TLS reverse proxy). The current app does not connect to this server.

## Smoke test

```bash
curl http://127.0.0.1:8765/health
curl -H "Authorization: Bearer $DEMIGOD_API_TOKEN" \
  http://127.0.0.1:8765/v1/models
curl -X POST http://127.0.0.1:8765/v1/chat/completions \
  -H "Authorization: Bearer $DEMIGOD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Return only: AIRLLM_SMOKE_OK"}],"max_tokens":32}'
```

Record AirLLM, Transformers, PyTorch, CUDA, model revision, config/tokenizer hashes, peak host RAM/VRAM, disk footprint, bytes read, TTFT and sustained tokens/sec. Test multi-turn state, tool-call format and recovery after cancellation before declaring support.

## Security

AirLLM's current `AutoModel` implementation resolves model architecture with `trust_remote_code=True`. Model loading can therefore execute Python code from the local snapshot. Use only a reviewed, pinned official snapshot and run it in an isolated environment without credentials or unrelated private files. The bridge requires a bearer token, refuses to start without a pinned revision label and binds to loopback by default.
