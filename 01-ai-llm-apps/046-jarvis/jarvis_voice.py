"""Jarvis voice mode: say "Jarvis, <command>". Fully offline (faster-whisper + Windows speech).

Code the agent wants to run is shown in this window and needs y/n unless you pass --auto.
"""
import argparse
import queue
import subprocess
import sys
import time

import numpy as np
import sounddevice as sd

from jarvis import build_interpreter

RATE = 16000
BLOCK = 480  # 30 ms


def speak(text: str):
    text = text.replace("'", " ").replace('"', " ").replace("\n", " ")[:600]
    ps = (
        "Add-Type -AssemblyName System.Speech;"
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        f"$s.Speak('{text}')"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)


def listen(q, threshold, silence_s=0.9, max_s=20):
    """Block until one spoken phrase is captured; return float32 audio or None."""
    frames, started, quiet, t0 = [], False, 0.0, time.time()
    while time.time() - t0 < 3600:
        block = q.get()
        level = float(np.sqrt(np.mean(block**2)))
        if level > threshold:
            started, quiet = True, 0.0
        elif started:
            quiet += BLOCK / RATE
        if started:
            frames.append(block)
            if quiet >= silence_s or len(frames) * BLOCK / RATE > max_s:
                return np.concatenate(frames)
        elif len(frames) == 0:
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true", help="run code without asking (risky)")
    ap.add_argument("--no-wake", action="store_true", help="respond to everything, not just 'Jarvis ...'")
    ap.add_argument("--whisper", default="base.en", help="tiny.en / base.en / small.en / medium.en")
    ap.add_argument("--threshold", type=float, default=0.015, help="mic sensitivity (lower = more sensitive)")
    ap.add_argument("--model")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    print("Loading speech model...")
    stt = WhisperModel(args.whisper, device="cpu", compute_type="int8")
    agent = build_interpreter(model=args.model, auto=args.auto)

    q: "queue.Queue[np.ndarray]" = queue.Queue()

    def cb(indata, frames, t, status):
        q.put(indata[:, 0].copy())

    print('Listening. Say "Jarvis, ..." (Ctrl+C to quit)')
    speak("Jarvis online.")
    with sd.InputStream(samplerate=RATE, channels=1, dtype="float32", blocksize=BLOCK, callback=cb):
        while True:
            audio = listen(q, args.threshold)
            if audio is None or len(audio) < RATE * 0.4:
                continue
            segs, _ = stt.transcribe(audio, language="en", vad_filter=True)
            heard = " ".join(s.text for s in segs).strip()
            if not heard:
                continue
            low = heard.lower()
            if not args.no_wake:
                if "jarvis" not in low:
                    continue
                heard = heard[low.index("jarvis") + len("jarvis"):].strip(" ,.!?")
            if not heard:
                speak("Yes?")
                continue
            print(f"\n> {heard}")
            if heard.lower().strip(" .!") in {"stop", "quit", "exit", "goodbye"}:
                speak("Goodbye.")
                return
            try:
                agent.chat(heard)
                last = [m for m in agent.messages if m.get("role") == "assistant" and m.get("type") == "message"]
                if last:
                    speak(last[-1]["content"])
            except KeyboardInterrupt:
                raise
            except Exception as e:  # keep the loop alive
                print("Error:", e)
                speak("Sorry, something went wrong.")
            q.queue.clear()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
