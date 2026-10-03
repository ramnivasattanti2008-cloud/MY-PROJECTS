# Jarvis (local, free)

Local LLM via Ollama + Open Interpreter for controlling this PC + offline voice + optional Open WebUI.

## Install
Double-click `Setup-Jarvis.bat`. It detects RAM/GPU, picks a model, installs everything. Re-run any time.
Options: `Setup-Jarvis.bat -WithCoder`, `-SkipWebUI`, `-Model qwen2.5:14b`.

## Use
- `Jarvis.bat` – text agent. Asks y/n before running each code block.
  - `Jarvis.bat --coder "build a flask todo app in ~/projects/todo"` (needs `-WithCoder`)
  - `Jarvis.bat --auto` – no confirmations (risky)
- `Jarvis-Voice.bat` – say "Jarvis, open Notepad". Flags: `--no-wake`, `--whisper small.en`, `--threshold 0.01`.
- `Jarvis-UI.bat` – ChatGPT-style UI at http://localhost:8080 (chat only, no PC control).

## Use a stronger free cloud model for hard tasks
Point at any OpenAI-compatible endpoint you already run:
`Jarvis.bat --api-base http://localhost:PORT/v1 --model MODELNAME`

## Notes
- Quality and speed depend on your hardware. Bigger models = smarter but slower.
- Everything runs locally; nothing is sent anywhere.
- Delete `.venv`, `.venv-webui` and `config.json` to reset.
