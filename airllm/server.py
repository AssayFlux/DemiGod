"""Experimental, opt-in AirLLM host bridge for DemiGod.

This service is deliberately bound to loopback by default. It is not an Android
runtime and it does not claim Qwen3-Coder-Next compatibility until a smoke test passes.
"""
from __future__ import annotations

import json
import os
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

MODEL_ID = os.getenv("DEMIGOD_MODEL_ID", "Qwen/Qwen3-Coder-Next")
MODEL_REVISION = os.getenv("DEMIGOD_MODEL_REVISION", "")
MODEL_CACHE = os.getenv("DEMIGOD_MODEL_CACHE", "./model-cache")
HOST = os.getenv("DEMIGOD_HOST", "127.0.0.1")
PORT = int(os.getenv("DEMIGOD_PORT", "8765"))
API_TOKEN = os.getenv("DEMIGOD_API_TOKEN", "")
MAX_NEW_TOKENS = int(os.getenv("DEMIGOD_MAX_NEW_TOKENS", "512"))
MAX_INPUT_CHARS = int(os.getenv("DEMIGOD_MAX_INPUT_CHARS", "24000"))

_model: Any = None
_load_error: str | None = None
_model_lock = threading.Lock()


def _load_model() -> Any:
    global _model, _load_error
    with _model_lock:
        if _model is not None:
            return _model
        if _load_error:
            raise RuntimeError(_load_error)
        try:
            import torch
            from airllm import AutoModel

            if not torch.cuda.is_available():
                raise RuntimeError(
                    "No CUDA device detected. This experimental harness currently "
                    "requires a CUDA host; it is not intended to run on the Android phone."
                )
            kwargs: dict[str, Any] = {"layer_shards_saving_path": MODEL_CACHE}
            if MODEL_REVISION:
                kwargs["revision"] = MODEL_REVISION
            _model = AutoModel.from_pretrained(MODEL_ID, **kwargs)
            return _model
        except Exception as exc:  # surfaced through /health and API errors
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
        truncation=True,
        max_length=8192,
        padding=False,
    )
    device = torch.device("cuda")
    input_ids = inputs["input_ids"].to(device)
    started = time.monotonic()
    with torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=max(1, min(max_tokens, MAX_NEW_TOKENS)),
            use_cache=True,
            return_dict_in_generate=True,
        )
    generated = output.sequences[0][input_ids.shape[-1]:]
    text = tokenizer.decode(generated, skip_special_tokens=True)
    if not text.strip():
        raise RuntimeError("Model returned an empty completion")
    return text


class Handler(BaseHTTPRequestHandler):
    server_version = "DemiGodAirLLM/0.1"

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self) -> bool:
        if not API_TOKEN:
            self._send(503, {"error": "Set DEMIGOD_API_TOKEN before starting the host bridge."})
            return False
        supplied = self.headers.get("Authorization", "")
        if supplied != f"Bearer {API_TOKEN}":
            self._send(401, {"error": "Unauthorized"})
            return False
        return True

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(200, {
                "status": "ready" if _model is not None else "model_not_loaded",
                "model": MODEL_ID,
                "model_revision_pinned": bool(MODEL_REVISION),
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
            messages = payload.get("messages")
            if not isinstance(messages, list) or not messages:
                raise ValueError("messages must be a non-empty array")
            normalized = []
            for item in messages:
                role = item.get("role")
                content = item.get("content")
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
        except ValueError as exc:
            self._send(400, {"error": str(exc)})
        except Exception as exc:
            self._send(503, {"error": f"Inference unavailable: {type(exc).__name__}: {exc}"})

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[demigod-airllm] {fmt % args}")


def main() -> None:
    if not API_TOKEN:
        raise SystemExit("Refusing to start without DEMIGOD_API_TOKEN.")
    if HOST not in {"127.0.0.1", "localhost"}:
        print("WARNING: non-loopback bind requested. Use a trusted private network and TLS tunnel.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"DemiGod AirLLM experiment listening on http://{HOST}:{PORT}")
    print(f"Model: {MODEL_ID}; pinned revision: {bool(MODEL_REVISION)}")
    server.serve_forever()


if __name__ == "__main__":
    main()
