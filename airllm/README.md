# DemiGod AirLLM host experiment

This is a **host-side research adapter**, not an Android inference engine. It exposes a small OpenAI-compatible, non-streaming chat endpoint so the Android client can later connect through an explicitly configured and secured host connection.

## Current support status

- Target under test: `Qwen/Qwen3-Coder-Next`.
- AirLLM's documented API uses `from airllm import AutoModel` and `AutoModel.from_pretrained(...)`.
- The fact that AirLLM supports other Qwen models does **not** prove this exact Qwen3-Coder-Next revision works.
- The model's hybrid Gated DeltaNet/Gated Attention state, tokenizer template, multi-turn behavior and tool-call output must pass the smoke tests before compatibility is declared.
- This initial bridge requires a CUDA host. It does not run on the owner's 11 GB Android phone.
- The server does not stream tokens yet; the endpoint is intentionally a first integration milestone.

## Install

Use a dedicated Python 3.11 environment on a CUDA-capable Linux host with a compatible PyTorch/CUDA installation. Install PyTorch for the host first, then:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r airllm/requirements.txt
```

AirLLM may require a newer Transformers build for newer model architectures. Do not blindly upgrade Transformers in a production environment: record the exact AirLLM, Transformers, PyTorch, CUDA and model revisions for each successful run.

## Start

Use a pinned Hugging Face commit SHA for reproducible testing:

```bash
export DEMIGOD_MODEL_ID=Qwen/Qwen3-Coder-Next
export DEMIGOD_MODEL_REVISION=<PINNED_HUGGING_FACE_COMMIT_SHA>
export DEMIGOD_MODEL_CACHE=/fast-local-ssd/demigod-airllm
export DEMIGOD_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python airllm/server.py
```

The server binds to `127.0.0.1:8765` by default. Do not expose it directly to the public internet. A phone-to-host connection must be explicitly configured and protected (prefer a private VPN or authenticated TLS reverse proxy). Keep source code and model prompts on the host unless the user opts in.

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

A successful health endpoint is not proof of model compatibility. Compatibility requires successful load, one-token generation, multi-turn generation with preserved recurrent state, tokenizer/chat-template checks, cancellation/recovery tests and coding-agent tool-call validation. Record peak host RAM/VRAM, disk footprint, bytes read, time-to-first-token, tokens/sec and thermal/power behavior.

## Security notes

AirLLM's model-loading path and Transformers may import model implementation code depending on the selected model and installed versions. Use only the official model repository, pin its revision, inspect any remote code before execution, and run experiments in an isolated environment without secrets. The bridge requires a bearer token and refuses to start without one. Loopback binding is the default.
