#!/usr/bin/env python3
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OBF = os.path.join(HERE, "core")

if os.path.isdir(OBF):
    if OBF not in sys.path:
        sys.path.insert(0, OBF)

import json
import webbrowser
from core import Grok as WormAi, Log

PROMPT_FILE = "system-prompt.txt"
proxy = os.getenv("WORM_PROXY") or os.getenv("GROK_PROXY", "")

def get_system_prompt():
    try:
        if not os.path.exists(PROMPT_FILE):
            return ""
        return open(PROMPT_FILE, "r", encoding="utf-8").read().strip()
    except Exception as e:
        Log.Error(f"Failed to read system prompt: {e}")
        return ""

def send_message(client: WormAi, message: str, extra_data: dict | None):
    # Prepend system prompt to the first message if available
    actual_message = message
    if not extra_data:
        sp = get_system_prompt()
        if sp:
            actual_message = f"{sp}\n\nUser: {message}"
    try:
        res = client.start_convo(actual_message, extra_data=extra_data)
        if isinstance(res, dict):
            if "error" in res:
                return f"[Grok Error] {res.get('error', 'Unknown error')}", extra_data
            return res.get("response"), res.get("extra_data")
        return str(res), extra_data
    except Exception as e:
        Log.Error(f"Worm-Ai error: {e}")
        return f"[Worm-Ai Error] {e}", extra_data

def main():
    current_proxy = proxy
    client = WormAi(current_proxy)
    extra_data = None
    last_response = ""
    print("Worm-Ai CLI — type your message and press Enter. Commands: /exit /restart /web /proxy <url>")
    print("Made With <3 | t.me/xsocietyforums | github.com/kafyasfngl")
    while True:
        try:
            msg = input("> ").strip()
            if not msg:
                continue
            if msg == "/exit":
                return
            if msg == "/restart":
                extra_data = None
                print("Conversation restarted.")
                continue
            if msg.startswith("/proxy "):
                proxy_url = msg.split(maxsplit=1)[1]
                current_proxy = proxy_url
                client = WormAi(current_proxy)
                extra_data = None
                print(f"Proxy set to {proxy_url} and conversation restarted.")
                continue
            if msg == "/web":
                if not last_response:
                    print("No response yet to show in web view.")
                    continue
                path = os.path.join(os.getcwd(), "wormai_response.html")
                with open(path, "w", encoding="utf-8") as f:
                    f.write("<html><body><pre>" + last_response.replace("<", "&lt;").replace(">", "&gt;") + "</pre></body></html>")
                webbrowser.open("file://" + path)
                continue

            response, extra_data = send_message(client, msg, extra_data)
            last_response = response or ""
            print("\n" + last_response + "\n")
        except KeyboardInterrupt:
            print("\nInterrupted — exiting.")
            return

if __name__ == "__main__":
    main()
