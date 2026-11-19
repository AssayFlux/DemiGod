"""Experimental, opt-in AirLLM host bridge for DemiGod.

Host-only research adapter. It is not an Android runtime. It loads only a local,
revision-pinned snapshot; model loading may execute model-side Python code through
the current AirLLM/Transformers stack, so use an isolated environment.
"""
from __future__ import annotations

import hmac
import json
import os
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

MODEL_ID = os.getenv("DEMIGOD_MODEL_ID", "Qwen/Qwen3-Coder-Next")
MODEL_PATH_VALUE = os.getenv("DEMIGOD_MODEL_PATH", "").strip()
MODEL_PATH = Path(MODEL_PATH_VALUE).expanduser()
MODEL_REVISION = os.getenv("DEMIGOD_MODEL_REVISION", "")
MODEL_CACHE = os.getenv("DEMIGOD_MODEL_CACHE", "./model-cache")
HOST = os.getenv("DEMIGOD_HOST", "127.0.0.1")
PORT = int(os.getenv("DEMIGOD_PORT", "8765"))
API_TOKEN = os.getenv("DEMIGOD_API_TOKEN", "")
MAX_NEW_TOKENS = int(os.getenv("DEMIGOD_MAX_NEW_TOKENS", "512"))
MAX_CONTEXT_TOKENS = int(os.getenv("DEMIGOD_MAX_CONTEXT_TOKENS", "4096"))
MAX_INPUT_CHARS = int(os.getenv("DEMIGOD_MAX_INPUT_CHARS", "24000"))
ALLOW_CPU = os.getenv("DEMIGOD_ALLOW_CPU", "0") == "1"

_model: Any = None
_model_lock = threading.Lock()
_generation_lock = threading.Lock()
_model_architecture = "unknown"
_load_error: str | None = None


def _load_model() -> Any:
    global _model, _model_architecture, _load_error
    with _model_lock:
        if _model is not None:
            return _model
        if _load_error:
            raise RuntimeError(_load_error)
        try:
            if not MODEL_REVISION:
                raise RuntimeError("Set DEMIGOD_MODEL_REVISION to the exact Hugging Face commit SHA.")
            if not MODEL_PATH.is_dir() or not (MODEL_PATH / "config.json").is_file():
                raise RuntimeError(
                    "DEMIGOD_MODEL_PATH must point to a locally downloaded model snapshot containing config.json."
                )

            config = json.loads((MODEL_PATH / "config.json").read_text(encoding="utf-8"))
            architectures = config.get("architectures") or []
            _model_architecture = architectures[0] if architectures else str(config.get("model_type", "unknown"))

            import torch
            from airllm import AutoModel

            if not torch.cuda.is_available() and not ALLOW_CPU:
                raise RuntimeError(
                    "No CUDA device detected. Set DEMIGOD_ALLOW_CPU=1 only if the host has "
                    "enough system RAM; CPU inference for this model may be impractically slow."
                )

            # AirLLM's AutoModel currently resolves its model config independently of the
            # revision argument. Passing a pre-downloaded local snapshot avoids an unpinned
            # remote fetch during initialization.
            _model = AutoModel.from_pretrained(
                str(MODEL_PATH),
                layer_shards_saving_path=MODEL_CACHE,
                max_seq_len=MAX_CONTEXT_TOKENS,
            )
            print(f"[demigod-airllm] loaded architecture={_model_architecture} device={_model.device}")
            return _model
        except Exception as exc:
            _load_error = f"{type(exc).__name__}: {exc}"
            raise RuntimeError(_load_error) from exc


def _complete(messages: list[dict[str, str]], max_tokens: int) -> str:
    import torch

    model = _load_model()
    tokenizer = model.tokenizer
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    if len(prompt) > MAX_INPUT_CHARS:
        raise ValueError(f"Prompt exceeds configured limit ({MAX_INPUT_CHARS} characters)")

    inputs = tokenizer(
        [prompt],
        return_tensors="pt",
        return_attention_mask=False,
        truncation=True,
        max_length=MAX_CONTEXT_TOKENS,
        padding=False,
    )
    input_ids = inputs["input_ids"].to(model.device)
    with _generation_lock, torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=max(1, min(max_tokens, MAX_NEW_TOKENS)),
            use_cache=True,
            return_dict_in_generate=True,
        )
    generated = output.sequences[0][input_ids.shape[-1]:]
    answer = tokenizer.decode(generated, skip_special_tokens=True)
    if not answer.strip():
        raise RuntimeError("Model returned an empty completion")
    return answer


class Handler(BaseHTTPRequestHandler):
    server_version = "DemiGodAirLLM/0.2"

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        supplied = self.headers.get("Authorization", "")
        expected = f"Bearer {API_TOKEN}"
        if not API_TOKEN or not hmac.compare_digest(supplied, expected):
            self._send(401, {"error": "Unauthorized or host API token is not configured."})
            return False
        return True

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(200, {
                "status": "ready" if _model is not None else "model_not_loaded",
                "model": MODEL_ID,
                "architecture": _model_architecture,
                "local_snapshot_configured": bool(MODEL_PATH_VALUE),
                "revision_label_configured": bool(MODEL_REVISION),
                "load_error": _load_error,
                "android_runtime": False,
            })
            return
        if not self._authorized():
            return
        if self.path == "/v1/models":
            self._send(200, {"object": "list", "data": [{
                "id": MODEL_ID, "object": "model", "owned_by": "local-host-experiment"
            }]})
            return
        self._send(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if not self._authorized():
            return
        if self.path != "/v1/chat/completions":
            self._send(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("Invalid request body size")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object")
            if payload.get("stream", False):
                raise ValueError("Streaming is not implemented by this first host bridge.")
            messages = payload.get("messages")
            if not isinstance(messages, list) or not messages:
                raise ValueError("messages must be a non-empty array")

            normalized = []
            for item in messages:
                if not isinstance(item, dict):
                    raise ValueError("Each message must be an object")
                role, content = item.get("role"), item.get("content")
                if role not in {"system", "user", "assistant"} or not isinstance(content, str):
                    raise ValueError("Only text system/user/assistant messages are supported")
                normalized.append({"role": role, "content": content})

            answer = _complete(normalized, int(payload.get("max_tokens", 256)))
            self._send(200, {
                "id": f"chatcmpl-{uuid.uuid4().hex}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": MODEL_ID,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": answer},
                    "finish_reason": "stop",
                }],
            })
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})
        except Exception as exc:
            print(f"[demigod-airllm] inference error: {type(exc).__name__}: {exc}")
            self._send(503, {"error": "Inference unavailable; inspect the host log for details."})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[demigod-airllm] {fmt % args}")


def main() -> None:
    if not API_TOKEN:
        raise SystemExit("Refusing to start without DEMIGOD_API_TOKEN.")
    if not MODEL_REVISION:
        raise SystemExit("Refusing to start without a pinned DEMIGOD_MODEL_REVISION.")
    if not MODEL_PATH_VALUE:
        raise SystemExit("Set DEMIGOD_MODEL_PATH to a local, pinned model snapshot.")
    if HOST not in {"127.0.0.1", "localhost"}:
        print("WARNING: non-loopback bind requested. Use a trusted private network and TLS tunnel.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"DemiGod AirLLM experiment listening on http://{HOST}:{PORT}")
    print(f"Model: {MODEL_ID}; revision label: {MODEL_REVISION}; snapshot: {MODEL_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()
