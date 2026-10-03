"""Jarvis text agent: a local LLM (Ollama) that can run code and control this PC.

Safety default: every code block is shown to you and needs a y/n before it runs.
Use --auto only when you trust the task (hands-free mode).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SAFETY = """
You are Jarvis, a capable personal assistant running on the user's Windows laptop.
You can write and run Python and PowerShell to open apps, manage files, browse the web,
and build software projects. Work in the user's projects folder unless told otherwise.
Rules: never delete, overwrite, or move user files unless explicitly asked; prefer
reversible steps; before anything destructive, explain it in one line first; keep
answers short; if a task is large, make a plan, then do it step by step.
"""


def load_config():
    cfg = {"model": "qwen2.5:7b", "coder_model": "", "api_base": "http://localhost:11434"}
    p = ROOT / "config.json"
    if p.exists():
        cfg.update(json.loads(p.read_text(encoding="utf-8")))
    return cfg


def build_interpreter(model=None, api_base=None, api_key=None, auto=False, coder=False):
    from interpreter import interpreter  # open-interpreter

    cfg = load_config()
    name = model or (cfg["coder_model"] if coder and cfg.get("coder_model") else cfg["model"])
    base = api_base or cfg["api_base"]

    if api_base and "11434" not in api_base:
        # Any OpenAI-compatible endpoint (e.g. a free API gateway you already run)
        interpreter.llm.model = f"openai/{name}"
        interpreter.llm.api_base = api_base
        interpreter.llm.api_key = api_key or "none"
    else:
        interpreter.llm.model = f"ollama/{name}"
        interpreter.llm.api_base = base

    interpreter.llm.context_window = 8192
    interpreter.llm.max_tokens = 2048
    interpreter.llm.supports_vision = False
    interpreter.llm.supports_functions = False
    interpreter.offline = True
    interpreter.auto_run = auto
    interpreter.system_message += SAFETY
    return interpreter


def main():
    ap = argparse.ArgumentParser(description="Jarvis text agent")
    ap.add_argument("prompt", nargs="*", help="optional one-shot task")
    ap.add_argument("--model", help="override model name")
    ap.add_argument("--coder", action="store_true", help="use the coder model for building projects")
    ap.add_argument("--api-base", help="use an OpenAI-compatible endpoint instead of Ollama")
    ap.add_argument("--api-key")
    ap.add_argument("--auto", action="store_true", help="run code without asking (risky)")
    args = ap.parse_args()

    i = build_interpreter(args.model, args.api_base, args.api_key, args.auto, args.coder)
    if args.prompt:
        i.chat(" ".join(args.prompt))
    else:
        i.chat()


if __name__ == "__main__":
    sys.exit(main())
