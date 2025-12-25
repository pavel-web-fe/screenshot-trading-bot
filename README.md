# 📸 Screenshot Trading Bot — OpenRouter Vision

Experimental AI-powered trading assistant that analyzes **chart screenshots**
and returns a short trading signal (`up / down / wait`) using **OpenRouter Vision models**.

The bot captures your screen via a hotkey, sends the image to an AI model,
and shows the result in a popup window.

---

## ⚠️ Disclaimer

> This project is for **educational and experimental purposes only**.  
> It is **NOT financial advice** and should **NOT** be used for real-money trading.

---

## 🚀 Features

- 📸 Full-screen screenshot capture
- 🧠 Chart analysis using Vision AI (OpenRouter)
- ⌨️ Hotkey-based workflow (`Alt + Q`)
- 🪟 Popup window with color-coded signal
- 💾 Screenshot & signal logging
- ⚡ Fast and minimal setup
- 🌐 Works with any browser or trading platform visible on screen

---

## 🖥 Supported Operating Systems

| OS | Status | Notes |
|----|-------|-------|
| Windows 10 / 11 | ✅ Fully supported | Recommended |
| Linux | ⚠️ Partial | Hotkeys may require root |
| macOS | ⚠️ Untested | Not officially supported |

---

## 🌐 Supported Browsers

The bot does **not** connect directly to browsers.  
It analyzes **what is visible on your screen**, so it works with **any browser**.

### Tested / Compatible:
- Google Chrome
- Microsoft Edge
- Brave
- Firefox
- Opera / Opera GX
- Vivaldi

Also works with:
- TradingView
- Pocket Option
- Deriv / Binary
- Any web-based or desktop chart platform

✅ If you can see the chart — the bot can analyze it.

---

## 🔧 Requirements

### Software
- Python **3.10+**
- Internet connection
- Administrator rights (for global hotkeys)

### Python Libraries
- `requests`
- `pyautogui`
- `keyboard`
- `pillow`

---

## 📦 Installation

### 1️⃣ Install Python
Download from:  
https://www.python.org/downloads/

During installation, make sure to enable:
