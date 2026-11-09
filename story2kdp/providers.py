"""Explicitly opt-in provider adapters. Never retry a billed request automatically."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import requests

class ProviderError(RuntimeError): pass

MODELS = {"openai":"gpt-4.1-mini", "anthropic":"claude-sonnet-4-5", "gemini":"gemini-2.5-flash"}

def text_task(provider: str, prompt: str, cache_dir: str | Path, *, model: str | None = None,
              max_output_tokens: int = 1000, approve_paid_request: bool = False) -> str:
    """Only call when the operator explicitly approves usage. Cache identical requests."""
    if not approve_paid_request:
        raise ProviderError("Paid provider calls require explicit approval")
    if provider not in MODELS:
        raise ProviderError("Supported text providers: openai, anthropic, gemini")
    selected=model or MODELS[provider]
    key=hashlib.sha256(json.dumps([provider,selected,prompt,max_output_tokens]).encode()).hexdigest()
    cache=Path(cache_dir);cache.mkdir(parents=True,exist_ok=True)
    file=cache / (key+".json")
    if file.exists():return json.loads(file.read_text())["text"]
    secrets={"openai":"OPENAI_API_KEY", "anthropic":"ANTHROPIC_API_KEY", "gemini":"GEMINI_API_KEY"}
    api_key=os.getenv(secrets[provider])
    if not api_key:raise ProviderError("Missing environment variable "+secrets[provider])
    if provider=="openai":
        url="https://api.openai.com/v1/chat/completions"
        headers={"Authorization":"Bearer "+api_key}
        payload={"model":selected,"messages":[{"role":"user","content":prompt}],"max_tokens":max_output_tokens}
    elif provider=="anthropic":
        url="https://api.anthropic.com/v1/messages"
        headers={"x-api-key":api_key,"anthropic-version":"2023-06-01"}
        payload={"model":selected,"max_tokens":max_output_tokens,"messages":[{"role":"user","content":prompt}]}
    else:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{selected}:generateContent"
        headers={"x-goog-api-key":api_key}
        payload={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":max_output_tokens}}
    try:
        resp=requests.post(url,json=payload,headers=headers,timeout=120)
        resp.raise_for_status();data=resp.json()
        if provider=="openai": result=data["choices"][0]["message"]["content"]
        elif provider=="anthropic":result="\n".join(p["text"] for p in data["content"] if p.get("type")=="text")
        else:result="\n".join(p["text"] for p in data["candidates"][0]["content"]["parts"] if "text" in p)
        file.write_text(json.dumps({"text":result,"provider":provider,"model":selected,"usage":data.get("usage") or data.get("usageMetadata")},indent=2))
        return result
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise ProviderError(f"Provider request failed (no automatic retry): {exc}") from exc
