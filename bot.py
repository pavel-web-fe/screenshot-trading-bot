import base64
import io
import json
import os
import re
import threading
from datetime import datetime

import requests
import pyautogui
import keyboard
import tkinter as tk
from PIL import Image


# ==================== CONFIG ====================
OPENROUTER_API_KEY = "" # API Key OpenRouter
MODEL = "qwen/qwen3-vl-32b-instruct" # AI Model OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"

OUTPUT_DIR = "screenshots_log"
LOG_FILE = "signals.log"

os.makedirs(OUTPUT_DIR, exist_ok=True)
# ================================================


def check_connection() -> bool:
    """Check OpenRouter API availability"""
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            timeout=10
        )
        return r.status_code == 200
    except Exception:
        return False


def generate_filename(prefix="screenshot", ext="png") -> str:
    """Generate timestamp-based filename"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"{prefix}_{ts}.{ext}")


def take_screenshot() -> Image.Image:
    """Capture full screen screenshot"""
    return pyautogui.screenshot()


def send_to_openrouter(image_b64: str) -> str:
    """Send screenshot to OpenRouter Vision model and get trading signal"""
    prompt = (
        "You are a professional trader. "
        "Analyze the chart screenshot and return ONLY one signal: "
        "'up', 'down', or 'wait', optionally with duration 1–5 minutes.\n"
        "Examples: 'up 2 min', 'down 1 min', 'wait'."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai",
        "X-Title": "Screenshot Trading Bot",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise trading assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def parse_signal(text: str):
    """Extract signal and duration from AI response"""
    t = text.lower()

    if re.search(r"(up|long)", t):
        signal = "up"
    elif re.search(r"(down|short)", t):
        signal = "down"
    elif re.search(r"(wait|hold)", t):
        signal = "wait"
    else:
        signal = "unknown"

    m = re.search(r"([1-5])\s*(min|m)", t)
    minutes = int(m.group(1)) if m else None

    return signal, minutes


def show_popup(signal: str, minutes: int | None):
    """Display signal popup window"""
    root = tk.Tk()
    root.title("AI Signal")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    colors = {
        "up": "#2ecc71",
        "down": "#e74c3c",
        "wait": "#f1c40f"
    }
    bg = colors.get(signal, "#bdc3c7")

    label_text = signal.upper()
    if minutes:
        label_text += f" — {minutes} min"

    frame = tk.Frame(root, bg=bg)
    frame.pack(expand=True, fill="both")

    tk.Label(
        frame,
        text=label_text,
        bg=bg,
        font=("Arial", 16, "bold")
    ).pack(expand=True)

    root.after(4000, root.destroy)
    root.mainloop()


def log_signal(image_path, ai_text, signal, minutes):
    """Save signal to log file"""
    entry = {
        "time": datetime.now().isoformat(),
        "image": image_path,
        "signal": signal,
        "minutes": minutes,
        "raw_ai_response": ai_text
    }

    with open(os.path.join(OUTPUT_DIR, LOG_FILE), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def process_screenshot():
    """Main workflow: screenshot → AI → popup → log"""
    img = take_screenshot()
    path = generate_filename()
    img.save(path)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    ai_response = send_to_openrouter(img_b64)
    signal, minutes = parse_signal(ai_response)

    show_popup(signal, minutes)
    log_signal(path, ai_response, signal, minutes)


def on_hotkey():
    threading.Thread(target=process_screenshot, daemon=True).start()


def main():
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY is not set")
        return

    if not check_connection():
        print("ERROR: Cannot connect to OpenRouter")
        return

    print("Running... Press ALT + Q to analyze screen")
    keyboard.add_hotkey("alt+q", on_hotkey)
    keyboard.wait()


if __name__ == "__main__":
    main()
